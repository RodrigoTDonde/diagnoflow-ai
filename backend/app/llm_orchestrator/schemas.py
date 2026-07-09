from typing import Literal

from pydantic import BaseModel, Field


PriorityLevel = Literal["low", "medium", "high", "critical"]
RiskLevel = Literal["low", "moderate", "high", "critical"]


class EquipmentContext(BaseModel):
    id: int
    name: str
    type: str
    sector: str
    manufacturer: str
    model: str
    criticality: str
    status: str


class IncidentContext(BaseModel):
    id: int | None = None
    equipment_id: int
    main_symptom: str
    description: str
    shift: str
    perceived_urgency: str
    symptoms: dict[str, bool]


class HistoricalSignal(BaseModel):
    summary: str
    recent_incident_count: int = 0
    repeated_symptom_patterns: list[str] = Field(default_factory=list)


class CriticalitySignal(BaseModel):
    priority: PriorityLevel
    operational_risk: RiskLevel
    justification: str


class KnownFailureSignal(BaseModel):
    probable_cause_hint: str
    evidence: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    involved_parts: list[str] = Field(default_factory=list)


class StructuredDiagnosticDraft(BaseModel):
    probable_cause: str
    confidence_level: float = Field(ge=0.0, le=1.0)
    priority: PriorityLevel
    operational_risk: RiskLevel
    recommended_actions: list[str] = Field(default_factory=list)
    involved_parts: list[str] = Field(default_factory=list)
    evidence_summary: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    observations: str
    technical_report: str
    requires_human_validation: bool = True
