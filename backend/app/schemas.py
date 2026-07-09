from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EquipmentBase(BaseModel):
    name: str
    type: str
    sector: str
    manufacturer: str
    model: str
    criticality: str
    status: str


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SymptomFlags(BaseModel):
    abnormal_noise: bool = False
    vibration: bool = False
    overheating: bool = False
    leakage: bool = False
    electrical_failure: bool = False
    total_stop: bool = False
    performance_loss: bool = False


class IncidentCreate(BaseModel):
    equipment_id: int
    main_symptom: str
    description: str
    shift: str
    perceived_urgency: str
    status: str = "open"
    symptoms: SymptomFlags = Field(default_factory=SymptomFlags)


class IncidentRead(BaseModel):
    id: int
    equipment_id: int
    main_symptom: str
    description: str
    shift: str
    perceived_urgency: str
    status: str
    abnormal_noise: bool
    vibration: bool
    overheating: bool
    leakage: bool
    electrical_failure: bool
    total_stop: bool
    performance_loss: bool
    created_at: datetime
    equipment: EquipmentRead

    model_config = ConfigDict(from_attributes=True)


class DiagnosticRead(BaseModel):
    id: int
    incident_id: int
    probable_cause: str
    confidence_level: float
    priority: str
    operational_risk: str
    recommended_actions: List[str]
    involved_parts: List[str]
    observations: str
    technical_report: str
    evidence_summary: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    requires_human_validation: bool = True
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentWithDiagnostic(BaseModel):
    incident: IncidentRead
    diagnostic: DiagnosticRead


class DashboardSummary(BaseModel):
    total_equipment: int
    open_incidents: int
    critical_alerts: int
    simulated_diagnostics: int


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    latest_incidents: List[IncidentWithDiagnostic]


class HistoryFilters(BaseModel):
    equipment_id: Optional[int] = None
    criticality: Optional[str] = None
    status: Optional[str] = None
