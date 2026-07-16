from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("", response_model=list[schemas.EquipmentRead])
def list_equipment(db: Session = Depends(get_db)):
    return (
        db.query(models.Equipment)
        .filter(
            models.Equipment.name != "",
            models.Equipment.type != "",
            models.Equipment.sector != "",
            models.Equipment.manufacturer != "",
            models.Equipment.model != "",
        )
        .order_by(models.Equipment.created_at.desc())
        .all()
    )


@router.post("", response_model=schemas.EquipmentRead, status_code=status.HTTP_201_CREATED)
def create_equipment(payload: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Equipment).filter(models.Equipment.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Equipment with this name already exists.")

    equipment = models.Equipment(**payload.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment
