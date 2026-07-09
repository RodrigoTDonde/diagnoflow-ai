from __future__ import annotations

from .. import models
from .schemas import CriticalitySignal, HistoricalSignal, IncidentContext


def consultar_historico_maquina(
    equipment: models.Equipment,
    current_incident: IncidentContext,
) -> HistoricalSignal:
    recent_count = len(equipment.incidents)
    repeated_patterns: list[str] = []

    if any(incident.vibration for incident in equipment.incidents):
        repeated_patterns.append("Ocorrências anteriores com vibração registrada")
    if any(incident.overheating for incident in equipment.incidents):
        repeated_patterns.append("Histórico de aquecimento acima do padrão")
    if any(incident.electrical_failure for incident in equipment.incidents):
        repeated_patterns.append("Há eventos anteriores ligados a falha elétrica")

    if not repeated_patterns:
        repeated_patterns.append("Sem padrão recorrente relevante no histórico local")

    summary = (
        f"Equipamento {equipment.name} possui {recent_count} ocorrência(s) registrada(s) "
        f"antes da análise atual."
    )
    return HistoricalSignal(
        summary=summary,
        recent_incident_count=max(recent_count - (1 if current_incident.id else 0), 0),
        repeated_symptom_patterns=repeated_patterns,
    )


def calcular_criticidade_ocorrencia(
    equipment: models.Equipment,
    current_incident: IncidentContext,
) -> CriticalitySignal:
    active_symptoms = sum(1 for active in current_incident.symptoms.values() if active)
    priority: CriticalitySignal.__annotations__["priority"] = "medium"
    risk: CriticalitySignal.__annotations__["operational_risk"] = "moderate"
    justification = "Criticidade inicial calculada por regras locais de suporte ao agente."

    if current_incident.symptoms.get("total_stop"):
        priority = "critical"
        risk = "critical"
        justification = "Parada total implica indisponibilidade imediata do ativo."
    elif current_incident.symptoms.get("electrical_failure"):
        priority = "high"
        risk = "high"
        justification = "Falha elétrica exige resposta rápida por risco operacional."
    elif current_incident.symptoms.get("overheating") and current_incident.symptoms.get("vibration"):
        priority = "high"
        risk = "high"
        justification = "Aquecimento combinado com vibração indica degradação acelerada."
    elif equipment.criticality.lower() == "alta" and active_symptoms >= 2:
        priority = "high"
        risk = "high"
        justification = "Ativo crítico com múltiplos sintomas ativos exige escalonamento."

    if current_incident.perceived_urgency.lower() == "alta" and priority == "medium":
        priority = "high"
        risk = "high"
        justification = "Urgência percebida alta elevou a criticidade operacional."

    return CriticalitySignal(priority=priority, operational_risk=risk, justification=justification)
