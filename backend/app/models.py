from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    type = Column(String(80), nullable=False)
    sector = Column(String(80), nullable=False)
    manufacturer = Column(String(80), nullable=False)
    model = Column(String(80), nullable=False)
    criticality = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    incidents = relationship("Incident", back_populates="equipment", cascade="all, delete-orphan")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    main_symptom = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    shift = Column(String(30), nullable=False)
    perceived_urgency = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False, default="open")
    abnormal_noise = Column(Integer, nullable=False, default=0)
    vibration = Column(Integer, nullable=False, default=0)
    overheating = Column(Integer, nullable=False, default=0)
    leakage = Column(Integer, nullable=False, default=0)
    electrical_failure = Column(Integer, nullable=False, default=0)
    total_stop = Column(Integer, nullable=False, default=0)
    performance_loss = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    equipment = relationship("Equipment", back_populates="incidents")
    diagnostic = relationship("Diagnostic", back_populates="incident", uselist=False, cascade="all, delete-orphan")


class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False, unique=True)
    probable_cause = Column(String(160), nullable=False)
    confidence_level = Column(Float, nullable=False)
    priority = Column(String(30), nullable=False)
    operational_risk = Column(String(30), nullable=False)
    recommended_actions = Column(JSON, nullable=False)
    involved_parts = Column(JSON, nullable=False)
    observations = Column(Text, nullable=False)
    technical_report = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    incident = relationship("Incident", back_populates="diagnostic")
    reviews = relationship("HumanValidationReview", back_populates="diagnostic", cascade="all, delete-orphan")


class HumanValidationReview(Base):
    __tablename__ = "human_validation_reviews"

    id = Column(Integer, primary_key=True, index=True)
    diagnostic_id = Column(Integer, ForeignKey("diagnostics.id"), nullable=False)
    reviewer_name = Column(String(120), nullable=False)
    decision = Column(String(30), nullable=False)
    notes = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    diagnostic = relationship("Diagnostic", back_populates="reviews")
