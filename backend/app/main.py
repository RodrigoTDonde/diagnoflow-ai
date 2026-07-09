from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload

from . import models, schemas
from .database import Base, SessionLocal, engine, get_db
from .llm_orchestrator import serialize_diagnostic_record
from .routes import diagnostics, equipment, incidents
from .seed import seed_data


REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST_DIR = REPO_ROOT / "frontend" / "dist"
FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / "assets"
SPA_EXCLUDED_PREFIXES = (
    "/equipment",
    "/incidents",
    "/diagnostics",
    "/dashboard",
    "/docs",
    "/openapi.json",
    "/redoc",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="DiagnoFlow AI API",
    version="0.1.0",
    description="API para triagem técnica simulada de máquinas rotativas industriais.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(equipment.router)
app.include_router(incidents.router)
app.include_router(diagnostics.router)

if FRONTEND_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS_DIR), name="frontend-assets")


def serve_spa() -> FileResponse:
    index_file = FRONTEND_DIST_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(
            status_code=503,
            detail="Frontend build não encontrado. Execute `cd frontend && npm run build` antes de iniciar o modo de produção.",
        )
    return FileResponse(index_file)


@app.get("/", include_in_schema=False)
def root():
    return serve_spa()


@app.get("/dashboard", response_model=schemas.DashboardResponse)
def dashboard(db: Session = Depends(get_db)):
    latest = (
        db.query(models.Incident)
        .options(joinedload(models.Incident.equipment), joinedload(models.Incident.diagnostic))
        .order_by(models.Incident.created_at.desc())
        .limit(5)
        .all()
    )
    summary = schemas.DashboardSummary(
        total_equipment=db.query(models.Equipment).count(),
        open_incidents=db.query(models.Incident).filter(models.Incident.status == "open").count(),
        critical_alerts=db.query(models.Diagnostic).filter(models.Diagnostic.priority == "critical").count(),
        simulated_diagnostics=db.query(models.Diagnostic).count(),
    )
    return {
        "summary": summary,
        "latest_incidents": [
            {
                "incident": incident,
                "diagnostic": serialize_diagnostic_record(incident.equipment, incident, incident.diagnostic),
            }
            for incident in latest
            if incident.diagnostic
        ],
    }


@app.get("/{full_path:path}", include_in_schema=False)
def spa_fallback(full_path: str):
    normalized_path = f"/{full_path}".rstrip("/")
    if not normalized_path:
        normalized_path = "/"

    if normalized_path.startswith(SPA_EXCLUDED_PREFIXES):
        raise HTTPException(status_code=404, detail="Route not found.")

    candidate = FRONTEND_DIST_DIR / full_path
    if candidate.is_file():
        return FileResponse(candidate)

    return serve_spa()
