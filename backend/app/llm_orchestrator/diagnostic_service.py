from __future__ import annotations

from .. import models
from ..schemas import IncidentCreate
from ..services.mock_diagnostic_service import build_mock_diagnostic
from .guardrails import validate_structured_diagnostic
from .schemas import EquipmentContext, IncidentContext, StructuredDiagnosticDraft
from .tools import calcular_criticidade_ocorrencia, consultar_historico_maquina


def _build_context(equipment: models.Equipment, incident: IncidentCreate) -> IncidentContext:
    return IncidentContext(
        equipment_id=incident.equipment_id,
        main_symptom=incident.main_symptom,
        description=incident.description,
        shift=incident.shift,
        perceived_urgency=incident.perceived_urgency,
        symptoms=incident.symptoms.model_dump(),
    )


def _build_model_context(equipment: models.Equipment, incident: models.Incident) -> IncidentContext:
    return IncidentContext(
        id=incident.id,
        equipment_id=incident.equipment_id,
        main_symptom=incident.main_symptom,
        description=incident.description,
        shift=incident.shift,
        perceived_urgency=incident.perceived_urgency,
        symptoms={
            "abnormal_noise": bool(incident.abnormal_noise),
            "vibration": bool(incident.vibration),
            "overheating": bool(incident.overheating),
            "leakage": bool(incident.leakage),
            "electrical_failure": bool(incident.electrical_failure),
            "total_stop": bool(incident.total_stop),
            "performance_loss": bool(incident.performance_loss),
        },
    )


def build_structured_mock_diagnostic(
    equipment: models.Equipment,
    incident: IncidentCreate,
) -> StructuredDiagnosticDraft:
    incident_context = _build_context(equipment, incident)
    equipment_context = EquipmentContext.model_validate(equipment, from_attributes=True)
    historical_signal = consultar_historico_maquina(equipment, incident_context)
    criticality_signal = calcular_criticidade_ocorrencia(equipment, incident_context)
    legacy_payload = build_mock_diagnostic(incident, equipment_context.name, equipment_context.type)

    evidence_summary = [
        f"Sintoma principal informado: {incident_context.main_symptom}",
        historical_signal.summary,
        criticality_signal.justification,
    ]
    missing_information = [
        "Não há leitura instrumental anexada para vibração, temperatura ou corrente.",
        "A confirmação final depende de inspeção técnica presencial.",
    ]

    draft = StructuredDiagnosticDraft(
        probable_cause=legacy_payload["probable_cause"],
        confidence_level=legacy_payload["confidence_level"],
        priority=criticality_signal.priority,
        operational_risk=criticality_signal.operational_risk,
        recommended_actions=legacy_payload["recommended_actions"],
        involved_parts=legacy_payload["involved_parts"],
        evidence_summary=evidence_summary,
        missing_information=missing_information,
        observations=legacy_payload["observations"],
        technical_report=legacy_payload["technical_report"],
        requires_human_validation=criticality_signal.priority in {"high", "critical"},
    )
    return validate_structured_diagnostic(draft)


def build_structured_mock_diagnostic_from_models(
    equipment: models.Equipment,
    incident: models.Incident,
    diagnostic: models.Diagnostic,
) -> StructuredDiagnosticDraft:
    incident_context = _build_model_context(equipment, incident)
    historical_signal = consultar_historico_maquina(equipment, incident_context)
    criticality_signal = calcular_criticidade_ocorrencia(equipment, incident_context)

    evidence_summary = [
        f"Sintoma principal informado: {incident_context.main_symptom}",
        historical_signal.summary,
        criticality_signal.justification,
    ]
    missing_information = [
        "Não há leitura instrumental anexada para vibração, temperatura ou corrente.",
        "A confirmação final depende de inspeção técnica presencial.",
    ]

    draft = StructuredDiagnosticDraft(
        probable_cause=diagnostic.probable_cause,
        confidence_level=diagnostic.confidence_level,
        priority=criticality_signal.priority,
        operational_risk=criticality_signal.operational_risk,
        recommended_actions=list(diagnostic.recommended_actions),
        involved_parts=list(diagnostic.involved_parts),
        evidence_summary=evidence_summary,
        missing_information=missing_information,
        observations=diagnostic.observations,
        technical_report=diagnostic.technical_report,
        requires_human_validation=criticality_signal.priority in {"high", "critical"},
    )
    return validate_structured_diagnostic(draft)


def generate_diagnostic_payload(equipment: models.Equipment, incident: IncidentCreate) -> dict:
    draft = build_structured_mock_diagnostic(equipment, incident)
    return {
        "probable_cause": draft.probable_cause,
        "confidence_level": draft.confidence_level,
        "priority": draft.priority,
        "operational_risk": draft.operational_risk,
        "recommended_actions": draft.recommended_actions,
        "involved_parts": draft.involved_parts,
        "observations": draft.observations,
        "technical_report": draft.technical_report,
    }


def serialize_diagnostic_record(
    equipment: models.Equipment,
    incident: models.Incident,
    diagnostic: models.Diagnostic,
) -> dict:
    draft = build_structured_mock_diagnostic_from_models(equipment, incident, diagnostic)
    return {
        "id": diagnostic.id,
        "incident_id": diagnostic.incident_id,
        "probable_cause": diagnostic.probable_cause,
        "confidence_level": diagnostic.confidence_level,
        "priority": diagnostic.priority,
        "operational_risk": diagnostic.operational_risk,
        "recommended_actions": diagnostic.recommended_actions,
        "involved_parts": diagnostic.involved_parts,
        "observations": diagnostic.observations,
        "technical_report": diagnostic.technical_report,
        "evidence_summary": draft.evidence_summary,
        "missing_information": draft.missing_information,
        "requires_human_validation": draft.requires_human_validation,
        "created_at": diagnostic.created_at,
    }
