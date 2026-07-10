from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas
from ..database import get_db
from ..llm_orchestrator import generate_diagnostic_payload, serialize_diagnostic_record

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[schemas.IncidentWithDiagnostic])
def list_incidents(
    equipment_id: int | None = Query(default=None),
    criticality: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(models.Incident)
        .options(
            joinedload(models.Incident.equipment),
            joinedload(models.Incident.diagnostic).joinedload(models.Diagnostic.reviews),
        )
        .join(models.Equipment)
        .order_by(models.Incident.created_at.desc())
    )

    if equipment_id:
        query = query.filter(models.Incident.equipment_id == equipment_id)
    if criticality:
        query = query.filter(func.lower(models.Equipment.criticality) == criticality.lower())
    if status_filter:
        query = query.filter(func.lower(models.Incident.status) == status_filter.lower())

    incidents = query.all()
    return [
        {
            "incident": incident,
            "diagnostic": serialize_diagnostic_record(incident.equipment, incident, incident.diagnostic),
        }
        for incident in incidents
        if incident.diagnostic
    ]


@router.post("", response_model=schemas.IncidentWithDiagnostic, status_code=status.HTTP_201_CREATED)
def create_incident(payload: schemas.IncidentCreate, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(models.Equipment.id == payload.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found.")

    incident_data = payload.model_dump(exclude={"symptoms"})
    incident_data.update({key: int(value) for key, value in payload.symptoms.model_dump().items()})
    incident = models.Incident(**incident_data)
    db.add(incident)
    db.flush()

    diagnostic_data = generate_diagnostic_payload(equipment, payload)
    diagnostic = models.Diagnostic(incident_id=incident.id, **diagnostic_data)
    db.add(diagnostic)
    db.commit()
    db.refresh(incident)
    db.refresh(diagnostic)

    incident = (
        db.query(models.Incident)
        .options(
            joinedload(models.Incident.equipment),
            joinedload(models.Incident.diagnostic).joinedload(models.Diagnostic.reviews),
        )
        .filter(models.Incident.id == incident.id)
        .first()
    )
    return {
        "incident": incident,
        "diagnostic": serialize_diagnostic_record(incident.equipment, incident, incident.diagnostic),
    }
