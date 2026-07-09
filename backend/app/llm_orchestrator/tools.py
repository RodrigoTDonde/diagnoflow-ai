from __future__ import annotations

from .. import models
from .schemas import (
    CriticalitySignal,
    HistoricalSignal,
    IncidentContext,
    InspectionChecklistSignal,
    KnownFailureSignal,
    TechnicalReportSignal,
)


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


def consultar_base_falhas(
    current_incident: IncidentContext,
) -> KnownFailureSignal:
    symptoms = current_incident.symptoms

    if symptoms.get("electrical_failure") or "elétr" in current_incident.main_symptom.lower():
        return KnownFailureSignal(
            probable_cause_hint="Intermitência elétrica no conjunto de acionamento",
            evidence=[
                "Base local associa falha elétrica a painéis, inversores ou conexões aquecidas.",
                "Sintoma principal ou flags indicam falha elétrica.",
            ],
            recommended_actions=[
                "Bloquear equipamento e medir continuidade dos circuitos",
                "Inspecionar bornes, contatores e aquecimento no painel",
                "Validar parâmetros do inversor antes do retorno operacional",
            ],
            involved_parts=["painel de comando", "inversor de frequência", "cabos de potência"],
        )

    if symptoms.get("overheating") and symptoms.get("vibration"):
        return KnownFailureSignal(
            probable_cause_hint="Rolamento em degradação com geração de calor e vibração",
            evidence=[
                "Combinação de aquecimento e vibração é recorrente em degradação de rolamentos.",
                "Base local de falhas indica risco de dano progressivo quando ambos sintomas coexistem.",
            ],
            recommended_actions=[
                "Executar inspeção termográfica e coleta de vibração",
                "Planejar troca de rolamentos no menor intervalo possível",
                "Verificar contaminação ou falta de lubrificante",
            ],
            involved_parts=["rolamentos", "mancais", "sistema de lubrificação"],
        )

    if symptoms.get("leakage"):
        return KnownFailureSignal(
            probable_cause_hint="Falha de vedação ou desgaste em retentor",
            evidence=[
                "Vazamento em ativo rotativo costuma indicar desgaste de selagem ou retentores.",
                "Base local sugere inspecionar ponto de vedação antes de ampliar a intervenção.",
            ],
            recommended_actions=[
                "Identificar ponto exato do vazamento",
                "Verificar integridade de selos, juntas e conexões",
                "Avaliar impacto do vazamento sobre segurança e processo",
            ],
            involved_parts=["selos", "retentores", "tubulações de vedação"],
        )

    if symptoms.get("total_stop"):
        return KnownFailureSignal(
            probable_cause_hint="Parada total associada a proteção operacional ou falha crítica",
            evidence=[
                "Parada total costuma envolver lógica de proteção, acionamento ou falha mecânica severa.",
                "Base local sugere retenção do ativo até confirmação técnica.",
            ],
            recommended_actions=[
                "Manter equipamento indisponível até liberação técnica",
                "Executar checklist de retorno com foco em proteção e acionamento",
                "Documentar causa raiz preliminar antes da retomada",
            ],
            involved_parts=["sistema de proteção", "motor", "acoplamento"],
        )

    return KnownFailureSignal(
        probable_cause_hint="Desalinhamento mecânico e desgaste progressivo",
        evidence=[
            "Sem combinação crítica específica na base local; hipótese padrão recai sobre desalinhamento e desgaste.",
            "Sinais operacionais indicam necessidade de inspeção mecânica inicial.",
        ],
        recommended_actions=[
            "Inspecionar alinhamento a laser e reaperto da base",
            "Verificar condição dos rolamentos e lubrificação",
            "Registrar tendência de vibração para comparação na próxima rodada",
        ],
        involved_parts=["acoplamento", "rolamentos", "base de fixação"],
    )


def gerar_checklist_inspecao(
    current_incident: IncidentContext,
    known_failure: KnownFailureSignal,
) -> InspectionChecklistSignal:
    checklist_items = [
        "Confirmar bloqueio e liberação segura do equipamento antes da inspeção.",
        "Registrar condição visual inicial do ativo e da área ao redor.",
    ]

    if current_incident.symptoms.get("electrical_failure"):
        checklist_items.extend(
            [
                "Medir continuidade elétrica e reaperto de bornes no painel.",
                "Verificar aquecimento anormal em contatores, inversor e cabos de potência.",
            ]
        )
    elif current_incident.symptoms.get("overheating") and current_incident.symptoms.get("vibration"):
        checklist_items.extend(
            [
                "Coletar vibração e temperatura em mancais e rolamentos.",
                "Verificar lubrificação, folga e ruído em rolamentos.",
            ]
        )
    elif current_incident.symptoms.get("leakage"):
        checklist_items.extend(
            [
                "Identificar ponto exato do vazamento e documentar evidência fotográfica.",
                "Inspecionar vedação, selos, juntas e conexões próximas.",
            ]
        )
    elif current_incident.symptoms.get("total_stop"):
        checklist_items.extend(
            [
                "Validar atuação de proteções, intertravamentos e alarmes de parada.",
                "Executar checklist de retorno somente após liberação técnica formal.",
            ]
        )
    else:
        checklist_items.extend(
            [
                "Verificar alinhamento, fixação de base e condição geral do acoplamento.",
                "Comparar ruído, vibração e temperatura com histórico operacional.",
            ]
        )

    checklist_items.append(f"Conferir componentes associados: {', '.join(known_failure.involved_parts)}.")
    return InspectionChecklistSignal(
        checklist_items=checklist_items,
        rationale="Checklist inicial gerado com base nos sintomas atuais e na hipótese principal da base local de falhas.",
    )


def gerar_relatorio_tecnico(
    equipment: models.Equipment,
    current_incident: IncidentContext,
    criticality: CriticalitySignal,
    known_failure: KnownFailureSignal,
    checklist: InspectionChecklistSignal,
) -> TechnicalReportSignal:
    report = (
        "Relatório técnico preliminar\n\n"
        f"Equipamento: {equipment.name}\n"
        f"Tipo: {equipment.type}\n"
        f"Setor: {equipment.sector}\n"
        f"Sintoma principal: {current_incident.main_symptom}\n"
        f"Descrição operacional: {current_incident.description}\n"
        f"Turno informado: {current_incident.shift}\n"
        f"Urgência percebida: {current_incident.perceived_urgency}\n\n"
        f"Causa provável: {known_failure.probable_cause_hint}\n"
        f"Prioridade: {criticality.priority}\n"
        f"Risco operacional: {criticality.operational_risk}\n"
        f"Peças potencialmente envolvidas: {', '.join(known_failure.involved_parts)}\n"
        f"Ações recomendadas: {'; '.join(known_failure.recommended_actions)}\n"
        f"Checklist inicial: {'; '.join(checklist.checklist_items)}\n\n"
        "Observação: fluxo preparado para fase 2, ainda sem chamada real para LLM."
    )
    return TechnicalReportSignal(
        technical_report=report,
        summary="Relatório técnico montado a partir das tools de criticidade, falhas conhecidas e checklist.",
    )


def describe_available_tools() -> list[dict[str, str]]:
    return [
        {
            "name": "consultar_historico_maquina",
            "purpose": "Busca contexto de ocorrências anteriores do equipamento para apoiar a análise atual.",
        },
        {
            "name": "calcular_criticidade_ocorrencia",
            "purpose": "Classifica prioridade e risco operacional com base nos sintomas e na criticidade do ativo.",
        },
        {
            "name": "consultar_base_falhas",
            "purpose": "Sugere hipóteses, evidências e ações com base em falhas frequentes conhecidas.",
        },
        {
            "name": "gerar_checklist_inspecao",
            "purpose": "Monta um checklist inicial de inspeção coerente com a hipótese principal.",
        },
        {
            "name": "gerar_relatorio_tecnico",
            "purpose": "Consolida um relatório técnico textual com contexto, prioridade e recomendações.",
        },
    ]
