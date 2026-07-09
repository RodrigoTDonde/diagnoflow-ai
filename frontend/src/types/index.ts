export type Equipment = {
  id: number;
  name: string;
  type: string;
  sector: string;
  manufacturer: string;
  model: string;
  criticality: string;
  status: string;
  created_at: string;
};

export type SymptomFlags = {
  abnormal_noise: boolean;
  vibration: boolean;
  overheating: boolean;
  leakage: boolean;
  electrical_failure: boolean;
  total_stop: boolean;
  performance_loss: boolean;
};

export type Incident = {
  id: number;
  equipment_id: number;
  main_symptom: string;
  description: string;
  shift: string;
  perceived_urgency: string;
  status: string;
  abnormal_noise: boolean;
  vibration: boolean;
  overheating: boolean;
  leakage: boolean;
  electrical_failure: boolean;
  total_stop: boolean;
  performance_loss: boolean;
  created_at: string;
  equipment: Equipment;
};

export type Diagnostic = {
  id: number;
  incident_id: number;
  probable_cause: string;
  confidence_level: number;
  priority: string;
  operational_risk: string;
  recommended_actions: string[];
  involved_parts: string[];
  inspection_checklist?: string[];
  observations: string;
  technical_report: string;
  evidence_summary?: string[];
  missing_information?: string[];
  requires_human_validation?: boolean;
  runtime_label?: string;
  runtime_provider?: string;
  runtime_model?: string;
  runtime_mode?: string;
  created_at: string;
};

export type IncidentWithDiagnostic = {
  incident: Incident;
  diagnostic: Diagnostic;
};

export type DashboardResponse = {
  summary: {
    total_equipment: number;
    open_incidents: number;
    critical_alerts: number;
    simulated_diagnostics: number;
  };
  latest_incidents: IncidentWithDiagnostic[];
};
