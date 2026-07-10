from __future__ import annotations

from .. import models
from ..config import get_llm_runtime_settings
from ..schemas import IncidentCreate
from .guardrails import validate_structured_diagnostic
from .graph import get_agent_runtime_label, run_diagnostic_agent
from .schemas import EquipmentContext, IncidentContext, StructuredDiagnosticDraft
from .tools import (
    calcular_criticidade_ocorrencia,
    consultar_base_falhas,
    consultar_historico_maquina,
    gerar_checklist_inspecao,
    gerar_relatorio_tecnico,
)


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
    draft = run_diagnostic_agent(equipment, incident)
    return validate_structured_diagnostic(draft)


def build_structured_mock_diagnostic_from_models(
    equipment: models.Equipment,
    incident: models.Incident,
    diagnostic: models.Diagnostic,
) -> StructuredDiagnosticDraft:
    incident_context = _build_model_context(equipment, incident)
    historical_signal = consultar_historico_maquina(equipment, incident_context)
    criticality_signal = calcular_criticidade_ocorrencia(equipment, incident_context)
    known_failure_signal = consultar_base_falhas(incident_context)
    inspection_checklist_signal = gerar_checklist_inspecao(incident_context, known_failure_signal)
    technical_report_signal = gerar_relatorio_tecnico(
        equipment,
        incident_context,
        criticality_signal,
        known_failure_signal,
        inspection_checklist_signal,
    )

    evidence_summary = [
        f"Sintoma principal informado: {incident_context.main_symptom}",
        historical_signal.summary,
        criticality_signal.justification,
        *known_failure_signal.evidence,
        inspection_checklist_signal.rationale,
        technical_report_signal.summary,
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
        inspection_checklist=inspection_checklist_signal.checklist_items,
        evidence_summary=evidence_summary,
        missing_information=missing_information,
        observations=diagnostic.observations,
        technical_report=diagnostic.technical_report,
        requires_human_validation=criticality_signal.priority in {"high", "critical"},
    )
    return validate_structured_diagnostic(draft)


def generate_diagnostic_payload(equipment: models.Equipment, incident: IncidentCreate) -> dict:
    draft = build_structured_mock_diagnostic(equipment, incident)
    settings = get_llm_runtime_settings()
    observations = (
        f"{draft.observations} Runtime atual: {get_agent_runtime_label()} | "
        f"provider={settings.provider} | model={settings.model} | mode={settings.runtime_mode}."
    )
    return {
        "probable_cause": draft.probable_cause,
        "confidence_level": draft.confidence_level,
        "priority": draft.priority,
        "operational_risk": draft.operational_risk,
        "recommended_actions": draft.recommended_actions,
        "involved_parts": draft.involved_parts,
        "observations": observations,
        "technical_report": draft.technical_report,
    }


def serialize_diagnostic_record(
    equipment: models.Equipment,
    incident: models.Incident,
    diagnostic: models.Diagnostic,
) -> dict:
    draft = build_structured_mock_diagnostic_from_models(equipment, incident, diagnostic)
    settings = get_llm_runtime_settings()
    ordered_reviews = sorted(diagnostic.reviews, key=lambda review: review.created_at, reverse=True)
    latest_review = ordered_reviews[0] if ordered_reviews else None
    return {
        "id": diagnostic.id,
        "incident_id": diagnostic.incident_id,
        "probable_cause": diagnostic.probable_cause,
        "confidence_level": diagnostic.confidence_level,
        "priority": diagnostic.priority,
        "operational_risk": diagnostic.operational_risk,
        "recommended_actions": diagnostic.recommended_actions,
        "involved_parts": diagnostic.involved_parts,
        "inspection_checklist": draft.inspection_checklist,
        "observations": (
            f"{diagnostic.observations} Runtime atual: {get_agent_runtime_label()} | "
            f"provider={settings.provider} | model={settings.model} | mode={settings.runtime_mode}."
        ),
        "technical_report": diagnostic.technical_report,
        "evidence_summary": draft.evidence_summary,
        "missing_information": draft.missing_information,
        "requires_human_validation": draft.requires_human_validation,
        "runtime_label": get_agent_runtime_label(),
        "runtime_provider": settings.provider,
        "runtime_model": settings.model,
        "runtime_mode": settings.runtime_mode,
        "latest_review_status": latest_review.decision if latest_review else None,
        "latest_reviewed_by": latest_review.reviewer_name if latest_review else None,
        "review_count": len(ordered_reviews),
        "human_reviews": ordered_reviews,
        "created_at": diagnostic.created_at,
    }
