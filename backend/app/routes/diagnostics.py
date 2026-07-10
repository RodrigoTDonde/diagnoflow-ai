from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas
from ..database import get_db
from ..llm_orchestrator import serialize_diagnostic_record

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])


@router.get("/{incident_id}", response_model=schemas.DiagnosticRead)
def get_diagnostic(incident_id: int, db: Session = Depends(get_db)):
    diagnostic = (
        db.query(models.Diagnostic)
        .options(joinedload(models.Diagnostic.reviews))
        .filter(models.Diagnostic.incident_id == incident_id)
        .first()
    )
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    incident = db.query(models.Incident).filter(models.Incident.id == diagnostic.incident_id).first()
    equipment = db.query(models.Equipment).filter(models.Equipment.id == incident.equipment_id).first()
    return serialize_diagnostic_record(equipment, incident, diagnostic)


@router.post("/{incident_id}/review", response_model=schemas.DiagnosticRead, status_code=status.HTTP_201_CREATED)
def create_human_review(
    incident_id: int,
    payload: schemas.HumanValidationReviewCreate,
    db: Session = Depends(get_db),
):
    diagnostic = (
        db.query(models.Diagnostic)
        .options(joinedload(models.Diagnostic.reviews))
        .filter(models.Diagnostic.incident_id == incident_id)
        .first()
    )
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")

    review = models.HumanValidationReview(
        diagnostic_id=diagnostic.id,
        reviewer_name=payload.reviewer_name,
        decision=payload.decision,
        notes=payload.notes,
    )
    db.add(review)
    db.commit()

    diagnostic = (
        db.query(models.Diagnostic)
        .options(joinedload(models.Diagnostic.reviews))
        .filter(models.Diagnostic.id == diagnostic.id)
        .first()
    )
    incident = db.query(models.Incident).filter(models.Incident.id == diagnostic.incident_id).first()
    equipment = db.query(models.Equipment).filter(models.Equipment.id == incident.equipment_id).first()
    return serialize_diagnostic_record(equipment, incident, diagnostic)
