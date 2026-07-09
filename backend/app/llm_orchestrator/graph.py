from __future__ import annotations

from typing import Any, TypedDict

from .. import models
from ..config import get_llm_runtime_settings
from ..schemas import IncidentCreate
from .guardrails import validate_structured_diagnostic
from .prompt import SYSTEM_PROMPT_TEMPLATE
from .provider import LLMInvocationContext, build_provider
from .schemas import (
    CriticalitySignal,
    EquipmentContext,
    HistoricalSignal,
    IncidentContext,
    InspectionChecklistSignal,
    KnownFailureSignal,
    StructuredDiagnosticDraft,
    TechnicalReportSignal,
)
from .tools import (
    calcular_criticidade_ocorrencia,
    consultar_base_falhas,
    consultar_historico_maquina,
    gerar_checklist_inspecao,
    gerar_relatorio_tecnico,
)

try:
    from langgraph.graph import END, START, StateGraph  # type: ignore
except ImportError:  # pragma: no cover - dependency will be optional during this step
    END = "END"
    START = "START"
    StateGraph = None


class DiagnosticAgentState(TypedDict, total=False):
    equipment: EquipmentContext
    incident: IncidentContext
    historical_signal: HistoricalSignal
    criticality_signal: CriticalitySignal
    known_failure_signal: KnownFailureSignal
    inspection_checklist_signal: InspectionChecklistSignal
    technical_report_signal: TechnicalReportSignal
    evidence_summary: list[str]
    missing_information: list[str]
    draft: StructuredDiagnosticDraft


def _build_incident_context(incident: IncidentCreate) -> IncidentContext:
    return IncidentContext(
        equipment_id=incident.equipment_id,
        main_symptom=incident.main_symptom,
        description=incident.description,
        shift=incident.shift,
        perceived_urgency=incident.perceived_urgency,
        symptoms=incident.symptoms.model_dump(),
    )


def _build_equipment_context(equipment: models.Equipment) -> EquipmentContext:
    return EquipmentContext.model_validate(equipment, from_attributes=True)


def collect_context_node(state: DiagnosticAgentState) -> DiagnosticAgentState:
    equipment = state["equipment"]
    incident = state["incident"]
    return {
        **state,
        "evidence_summary": [f"Sintoma principal informado: {incident.main_symptom}"],
        "missing_information": [
            "Não há leitura instrumental anexada para vibração, temperatura ou corrente.",
            "A confirmação final depende de inspeção técnica presencial.",
        ],
    }


def historical_tool_node(state: DiagnosticAgentState, equipment_model: models.Equipment) -> DiagnosticAgentState:
    signal = consultar_historico_maquina(equipment_model, state["incident"])
    evidence = list(state.get("evidence_summary", []))
    evidence.append(signal.summary)
    return {**state, "historical_signal": signal, "evidence_summary": evidence}


def criticality_tool_node(state: DiagnosticAgentState, equipment_model: models.Equipment) -> DiagnosticAgentState:
    signal = calcular_criticidade_ocorrencia(equipment_model, state["incident"])
    evidence = list(state.get("evidence_summary", []))
    evidence.append(signal.justification)
    return {**state, "criticality_signal": signal, "evidence_summary": evidence}


def failure_knowledge_tool_node(state: DiagnosticAgentState) -> DiagnosticAgentState:
    signal = consultar_base_falhas(state["incident"])
    evidence = list(state.get("evidence_summary", []))
    evidence.extend(signal.evidence)
    return {**state, "known_failure_signal": signal, "evidence_summary": evidence}


def inspection_checklist_tool_node(state: DiagnosticAgentState) -> DiagnosticAgentState:
    signal = gerar_checklist_inspecao(state["incident"], state["known_failure_signal"])
    evidence = list(state.get("evidence_summary", []))
    evidence.append(signal.rationale)
    return {**state, "inspection_checklist_signal": signal, "evidence_summary": evidence}


def technical_report_tool_node(state: DiagnosticAgentState, equipment_model: models.Equipment) -> DiagnosticAgentState:
    signal = gerar_relatorio_tecnico(
        equipment_model,
        state["incident"],
        state["criticality_signal"],
        state["known_failure_signal"],
        state["inspection_checklist_signal"],
    )
    evidence = list(state.get("evidence_summary", []))
    evidence.append(signal.summary)
    return {**state, "technical_report_signal": signal, "evidence_summary": evidence}


def compose_draft_node(state: DiagnosticAgentState) -> DiagnosticAgentState:
    incident = state["incident"]
    equipment = state["equipment"]
    criticality = state["criticality_signal"]
    known_failure = state["known_failure_signal"]
    checklist = state["inspection_checklist_signal"]
    report_signal = state["technical_report_signal"]

    probable_cause = known_failure.probable_cause_hint
    involved_parts = known_failure.involved_parts
    recommended_actions = known_failure.recommended_actions

    confidence_level = min(0.52 + (sum(1 for active in incident.symptoms.values() if active) * 0.06), 0.93)
    observations = (
        f"Diagnóstico estruturado para {equipment.name} ({equipment.type}) com fluxo preparado para agente. "
        "Nesta etapa, a composição usa histórico, criticidade e base local de falhas conhecidas."
    )
    draft = StructuredDiagnosticDraft(
        probable_cause=probable_cause,
        confidence_level=round(confidence_level, 2),
        priority=criticality.priority,
        operational_risk=criticality.operational_risk,
        recommended_actions=recommended_actions,
        involved_parts=involved_parts,
        inspection_checklist=checklist.checklist_items,
        evidence_summary=state["evidence_summary"],
        missing_information=state["missing_information"],
        observations=observations,
        technical_report=report_signal.technical_report,
        requires_human_validation=criticality.priority in {"high", "critical"},
    )
    return {**state, "draft": draft}


def guardrail_node(state: DiagnosticAgentState) -> DiagnosticAgentState:
    draft = validate_structured_diagnostic(state["draft"])
    return {**state, "draft": draft}


def llm_provider_node(state: DiagnosticAgentState) -> DiagnosticAgentState:
    settings = get_llm_runtime_settings()
    provider = build_provider(settings)
    incident = state["incident"]
    equipment = state["equipment"]

    context = LLMInvocationContext(
        system_prompt=SYSTEM_PROMPT_TEMPLATE,
        user_prompt=(
            f"Equipamento: {equipment.name} ({equipment.type})\n"
            f"Sintoma principal: {incident.main_symptom}\n"
            f"Descrição: {incident.description}\n"
            f"Turno: {incident.shift}\n"
            f"Urgência: {incident.perceived_urgency}\n"
            f"Evidências: {' | '.join(state.get('evidence_summary', []))}\n"
            f"Lacunas: {' | '.join(state.get('missing_information', []))}"
        ),
        settings=settings,
    )
    provider_draft = provider.generate_structured_diagnostic(context)
    if provider_draft is None:
        return state
    return {**state, "draft": provider_draft}


def _run_fallback_agent(equipment_model: models.Equipment, incident_payload: IncidentCreate) -> StructuredDiagnosticDraft:
    state: DiagnosticAgentState = {
        "equipment": _build_equipment_context(equipment_model),
        "incident": _build_incident_context(incident_payload),
    }
    state = collect_context_node(state)
    state = historical_tool_node(state, equipment_model)
    state = criticality_tool_node(state, equipment_model)
    state = failure_knowledge_tool_node(state)
    state = inspection_checklist_tool_node(state)
    state = technical_report_tool_node(state, equipment_model)
    state = compose_draft_node(state)
    state = llm_provider_node(state)
    state = guardrail_node(state)
    return state["draft"]


def _build_langgraph_app(equipment_model: models.Equipment):
    settings = get_llm_runtime_settings()
    if StateGraph is None or not settings.use_langgraph:
        return None

    graph = StateGraph(DiagnosticAgentState)
    graph.add_node("collect_context", collect_context_node)
    graph.add_node("historical_tool", lambda state: historical_tool_node(state, equipment_model))
    graph.add_node("criticality_tool", lambda state: criticality_tool_node(state, equipment_model))
    graph.add_node("failure_knowledge_tool", failure_knowledge_tool_node)
    graph.add_node("inspection_checklist_tool", inspection_checklist_tool_node)
    graph.add_node("technical_report_tool", lambda state: technical_report_tool_node(state, equipment_model))
    graph.add_node("compose_draft", compose_draft_node)
    graph.add_node("llm_provider", llm_provider_node)
    graph.add_node("guardrail", guardrail_node)

    graph.add_edge(START, "collect_context")
    graph.add_edge("collect_context", "historical_tool")
    graph.add_edge("historical_tool", "criticality_tool")
    graph.add_edge("criticality_tool", "failure_knowledge_tool")
    graph.add_edge("failure_knowledge_tool", "inspection_checklist_tool")
    graph.add_edge("inspection_checklist_tool", "technical_report_tool")
    graph.add_edge("technical_report_tool", "compose_draft")
    graph.add_edge("compose_draft", "llm_provider")
    graph.add_edge("llm_provider", "guardrail")
    graph.add_edge("guardrail", END)
    return graph.compile()


def run_diagnostic_agent(equipment_model: models.Equipment, incident_payload: IncidentCreate) -> StructuredDiagnosticDraft:
    app = _build_langgraph_app(equipment_model)
    if app is None:
        return _run_fallback_agent(equipment_model, incident_payload)

    initial_state: DiagnosticAgentState = {
        "equipment": _build_equipment_context(equipment_model),
        "incident": _build_incident_context(incident_payload),
    }
    result: dict[str, Any] = app.invoke(initial_state)
    draft = result.get("draft")
    if not isinstance(draft, StructuredDiagnosticDraft):
        raise ValueError("Diagnostic agent did not produce a structured draft.")
    return draft


def get_agent_runtime_label() -> str:
    settings = get_llm_runtime_settings()
    if StateGraph is not None and settings.use_langgraph:
        return "langgraph"
    return "fallback-local"


def get_system_prompt() -> str:
    return SYSTEM_PROMPT_TEMPLATE
