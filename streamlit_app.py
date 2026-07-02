from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

import streamlit as st


APP_NOTICE = "Diagnóstico simulado - nenhum LLM foi integrado nesta fase."
SYMPTOM_FIELDS = [
    ("abnormal_noise", "Ruído anormal"),
    ("vibration", "Vibração"),
    ("overheating", "Superaquecimento"),
    ("leakage", "Vazamento"),
    ("electrical_failure", "Falha elétrica"),
    ("total_stop", "Parada total"),
    ("performance_loss", "Perda de desempenho"),
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def seed_equipment() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "Bomba P-101",
            "type": "Bomba centrifuga",
            "sector": "Utilidades",
            "manufacturer": "WEG",
            "model": "CPX-400",
            "criticality": "alta",
            "status": "operando com restricao",
            "created_at": now_iso(),
        },
        {
            "id": 2,
            "name": "Motor M-204",
            "type": "Motor eletrico",
            "sector": "Mistura",
            "manufacturer": "Siemens",
            "model": "HT-315",
            "criticality": "media",
            "status": "operacional",
            "created_at": now_iso(),
        },
        {
            "id": 3,
            "name": "Compressor C-88",
            "type": "Compressor rotativo",
            "sector": "Ar comprimido",
            "manufacturer": "Atlas Copco",
            "model": "GA-75",
            "criticality": "alta",
            "status": "em observacao",
            "created_at": now_iso(),
        },
    ]


def blank_symptoms() -> dict[str, bool]:
    return {key: False for key, _ in SYMPTOM_FIELDS}


def score_symptoms(symptoms: dict[str, bool]) -> int:
    return sum(1 for active in symptoms.values() if active)


def build_mock_diagnostic(incident: dict[str, Any], equipment: dict[str, Any]) -> dict[str, Any]:
    symptoms = incident["symptoms"]
    symptom_score = score_symptoms(symptoms)

    probable_cause = "Desalinhamento mecanico e desgaste progressivo"
    involved_parts = ["acoplamento", "rolamentos", "base de fixacao"]
    recommended_actions = [
        "Inspecionar alinhamento a laser e reaperto da base",
        "Verificar condicao dos rolamentos e lubrificacao",
        "Registrar tendencia de vibracao para comparacao na proxima rodada",
    ]
    priority = "medium"
    operational_risk = "moderate"

    if symptoms["electrical_failure"] or "eletr" in incident["main_symptom"].lower():
        probable_cause = "Intermitencia eletrica no conjunto de acionamento"
        involved_parts = ["painel de comando", "inversor de frequencia", "cabos de potencia"]
        recommended_actions = [
            "Bloquear equipamento e medir continuidade dos circuitos",
            "Inspecionar bornes, contatores e aquecimento no painel",
            "Validar parametros do inversor antes do retorno operacional",
        ]
        priority = "high"
        operational_risk = "high"
    elif symptoms["overheating"] and symptoms["vibration"]:
        probable_cause = "Rolamento em degradacao com geracao de calor e vibracao"
        involved_parts = ["rolamentos", "mancais", "sistema de lubrificacao"]
        recommended_actions = [
            "Executar inspecao termografica e coleta de vibracao",
            "Planejar troca de rolamentos no menor intervalo possivel",
            "Verificar contaminacao ou falta de lubrificante",
        ]
        priority = "high"
        operational_risk = "high"
    elif symptoms["leakage"]:
        probable_cause = "Falha de vedacao ou desgaste em retentor"
        involved_parts = ["selos", "retentores", "tubulacoes de vedacao"]
        recommended_actions = [
            "Identificar ponto exato do vazamento",
            "Verificar integridade de selos, juntas e conexoes",
            "Avaliar impacto do vazamento sobre seguranca e processo",
        ]
    elif symptoms["total_stop"]:
        probable_cause = "Parada total associada a protecao operacional ou falha critica"
        involved_parts = ["sistema de protecao", "motor", "acoplamento"]
        recommended_actions = [
            "Manter equipamento indisponivel ate liberacao tecnica",
            "Executar checklist de retorno com foco em protecao e acionamento",
            "Documentar causa raiz preliminar antes da retomada",
        ]
        priority = "critical"
        operational_risk = "critical"

    if incident["perceived_urgency"] == "alta" and priority == "medium":
        priority = "high"
        operational_risk = "high"

    confidence = min(0.52 + (symptom_score * 0.06), 0.93)
    observations = (
        f"Diagnostico simulado para {equipment['name']} ({equipment['type']}). "
        "A inferencia foi baseada em regras estaticas de sintomas, sem uso de LLM."
    )
    technical_report = (
        "Relatorio tecnico preliminar\n\n"
        f"Equipamento: {equipment['name']}\n"
        f"Tipo: {equipment['type']}\n"
        f"Sintoma principal: {incident['main_symptom']}\n"
        f"Descricao operacional: {incident['description']}\n"
        f"Turno informado: {incident['shift']}\n"
        f"Urgencia percebida: {incident['perceived_urgency']}\n\n"
        f"Causa provavel: {probable_cause}\n"
        f"Prioridade: {priority}\n"
        f"Risco operacional: {operational_risk}\n"
        f"Pecas potencialmente envolvidas: {', '.join(involved_parts)}\n"
        f"Acoes recomendadas: {'; '.join(recommended_actions)}\n\n"
        "Observacao: diagnostico simulado, sem integracao com modelo de IA nesta fase."
    )

    return {
        "id": len(st.session_state.get("diagnostics", [])) + 1,
        "incident_id": incident["id"],
        "probable_cause": probable_cause,
        "confidence_level": round(confidence, 2),
        "priority": priority,
        "operational_risk": operational_risk,
        "recommended_actions": recommended_actions,
        "involved_parts": involved_parts,
        "observations": observations,
        "technical_report": technical_report,
        "created_at": now_iso(),
    }


def create_seed_incident(equipment: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    incident = {
        "id": 1,
        "equipment_id": equipment["id"],
        "equipment_name": equipment["name"],
        "equipment_criticality": equipment["criticality"],
        "main_symptom": "Vibracao crescente com aquecimento",
        "description": "Operador relatou aumento de vibracao nas ultimas 6 horas e temperatura acima do padrao.",
        "shift": "manha",
        "perceived_urgency": "alta",
        "status": "open",
        "symptoms": {
            "abnormal_noise": False,
            "vibration": True,
            "overheating": True,
            "leakage": False,
            "electrical_failure": False,
            "total_stop": False,
            "performance_loss": True,
        },
        "created_at": now_iso(),
    }
    diagnostic = build_mock_diagnostic(incident, equipment)
    return incident, diagnostic


def init_state() -> None:
    st.session_state.setdefault("equipment", seed_equipment())
    st.session_state.setdefault("incidents", [])
    st.session_state.setdefault("diagnostics", [])
    st.session_state.setdefault("latest_diagnostic", None)
    st.session_state.setdefault("selected_incident_id", None)

    if not st.session_state.incidents:
        incident, diagnostic = create_seed_incident(st.session_state.equipment[0])
        st.session_state.incidents = [incident]
        st.session_state.diagnostics = [diagnostic]
        st.session_state.latest_diagnostic = {
            "incident": deepcopy(incident),
            "diagnostic": deepcopy(diagnostic),
        }
        st.session_state.selected_incident_id = incident["id"]


def find_equipment(equipment_id: int) -> dict[str, Any]:
    for item in st.session_state.equipment:
        if item["id"] == equipment_id:
            return item
    raise ValueError("Equipamento nao encontrado.")


def latest_incident_rows(limit: int = 5) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for incident in reversed(st.session_state.incidents[-limit:]):
        diagnostic = next((item for item in st.session_state.diagnostics if item["incident_id"] == incident["id"]), None)
        if diagnostic:
            rows.append({"incident": incident, "diagnostic": diagnostic})
    return rows


def history_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for incident in st.session_state.incidents:
        diagnostic = next((item for item in st.session_state.diagnostics if item["incident_id"] == incident["id"]), None)
        if not diagnostic:
            continue
        rows.append(
            {
                "Equipamento": incident["equipment_name"],
                "Sintoma": incident["main_symptom"],
                "Criticidade": incident["equipment_criticality"],
                "Status": incident["status"],
                "Prioridade": diagnostic["priority"],
                "Risco": diagnostic["operational_risk"],
                "Data": incident["created_at"].replace("T", " "),
            }
        )
    return list(reversed(rows))


def render_notice() -> None:
    st.warning(APP_NOTICE, icon=":material/warning:")


def render_dashboard() -> None:
    st.title("DiagnoFlow AI")
    st.caption("Dashboard operacional simplificado para publicacao online da primeira entrega.")
    render_notice()

    total_equipment = len(st.session_state.equipment)
    open_incidents = sum(1 for item in st.session_state.incidents if item["status"] == "open")
    critical_alerts = sum(1 for item in st.session_state.diagnostics if item["priority"] == "critical")
    simulated_diagnostics = len(st.session_state.diagnostics)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Equipamentos cadastrados", total_equipment, border=True)
    with col2:
        st.metric("Ocorrencias abertas", open_incidents, border=True)
    with col3:
        st.metric("Alertas criticos", critical_alerts, border=True)
    with col4:
        st.metric("Diagnosticos simulados", simulated_diagnostics, border=True)

    with st.container(border=True):
        st.subheader("Ultimas ocorrencias")
        for row in latest_incident_rows():
            incident = row["incident"]
            diagnostic = row["diagnostic"]
            st.markdown(f"**{incident['equipment_name']}**")
            st.write(f"{incident['main_symptom']} | prioridade {diagnostic['priority']} | risco {diagnostic['operational_risk']}")
            st.caption(diagnostic["probable_cause"])


def render_equipment() -> None:
    st.title("Equipamentos")
    render_notice()

    left, right = st.columns([1.4, 1], gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Ativos cadastrados")
            st.dataframe(
                [
                    {
                        "Nome": item["name"],
                        "Tipo": item["type"],
                        "Setor": item["sector"],
                        "Criticidade": item["criticality"],
                        "Status": item["status"],
                    }
                    for item in st.session_state.equipment
                ],
                use_container_width=True,
                hide_index=True,
            )
    with right:
        with st.form("equipment_form", border=True):
            st.subheader("Novo equipamento")
            name = st.text_input("Nome do equipamento")
            equipment_type = st.text_input("Tipo")
            sector = st.text_input("Setor")
            manufacturer = st.text_input("Fabricante")
            model = st.text_input("Modelo")
            criticality = st.selectbox("Criticidade", ["baixa", "media", "alta"])
            status = st.selectbox("Status", ["operacional", "em observacao", "operando com restricao", "parado"])
            submitted = st.form_submit_button("Cadastrar equipamento", use_container_width=True)
            if submitted:
                new_equipment = {
                    "id": len(st.session_state.equipment) + 1,
                    "name": name,
                    "type": equipment_type,
                    "sector": sector,
                    "manufacturer": manufacturer,
                    "model": model,
                    "criticality": criticality,
                    "status": status,
                    "created_at": now_iso(),
                }
                st.session_state.equipment.append(new_equipment)
                st.success("Equipamento cadastrado com sucesso.", icon=":material/check_circle:")


def render_new_incident() -> None:
    st.title("Nova ocorrencia")
    render_notice()

    left, right = st.columns([1.25, 1], gap="large")
    with left:
        with st.form("incident_form", border=True):
            st.subheader("Registrar ocorrencia")
            equipment_options = {item["name"]: item["id"] for item in st.session_state.equipment}
            selected_equipment_name = st.selectbox("Equipamento", list(equipment_options.keys()))
            main_symptom = st.text_input("Sintoma principal")
            description = st.text_area("Descricao operacional", height=140)
            shift = st.selectbox("Turno", ["manha", "tarde", "noite"])
            urgency = st.selectbox("Urgencia percebida", ["baixa", "media", "alta"])
            status = st.selectbox("Status da ocorrencia", ["open", "closed"])

            st.markdown("**Sintomas observados**")
            symptom_values: dict[str, bool] = {}
            cols = st.columns(2)
            for index, (key, label) in enumerate(SYMPTOM_FIELDS):
                with cols[index % 2]:
                    symptom_values[key] = st.checkbox(label, key=f"symptom_{key}")

            submitted = st.form_submit_button("Gerar diagnostico simulado", use_container_width=True)
            if submitted:
                equipment = find_equipment(equipment_options[selected_equipment_name])
                incident = {
                    "id": len(st.session_state.incidents) + 1,
                    "equipment_id": equipment["id"],
                    "equipment_name": equipment["name"],
                    "equipment_criticality": equipment["criticality"],
                    "main_symptom": main_symptom,
                    "description": description,
                    "shift": shift,
                    "perceived_urgency": urgency,
                    "status": status,
                    "symptoms": symptom_values,
                    "created_at": now_iso(),
                }
                diagnostic = build_mock_diagnostic(incident, equipment)
                st.session_state.incidents.append(incident)
                st.session_state.diagnostics.append(diagnostic)
                st.session_state.latest_diagnostic = {"incident": incident, "diagnostic": diagnostic}
                st.success("Ocorrencia registrada e diagnostico simulado gerado.", icon=":material/analytics:")

    with right:
        with st.container(border=True):
            st.subheader("Diagnostico simulado")
            current = st.session_state.get("latest_diagnostic")
            if not current:
                st.caption("Registre uma ocorrencia para ver o resultado.")
                return

            incident = current["incident"]
            diagnostic = current["diagnostic"]
            st.badge("Sem LLM nesta fase", icon=":material/warning:", color="orange")
            st.write(f"**Equipamento:** {incident['equipment_name']}")
            st.write(f"**Causa provavel:** {diagnostic['probable_cause']}")
            st.write(f"**Confianca simulada:** {int(diagnostic['confidence_level'] * 100)}%")
            st.write(f"**Prioridade:** {diagnostic['priority']}")
            st.write(f"**Risco operacional:** {diagnostic['operational_risk']}")
            st.write(f"**Observacoes:** {diagnostic['observations']}")
            st.write("**Acoes recomendadas**")
            for action in diagnostic["recommended_actions"]:
                st.markdown(f"- {action}")
            st.write("**Pecas possivelmente envolvidas**")
            st.caption(", ".join(diagnostic["involved_parts"]))


def render_history() -> None:
    st.title("Historico")
    render_notice()

    equipment_filter = st.selectbox("Filtro por equipamento", ["Todos"] + [item["name"] for item in st.session_state.equipment])
    criticality_filter = st.selectbox("Filtro por criticidade", ["Todas", "baixa", "media", "alta"])
    status_filter = st.selectbox("Filtro por status", ["Todos", "open", "closed"])

    filtered = []
    for row in history_rows():
        if equipment_filter != "Todos" and row["Equipamento"] != equipment_filter:
            continue
        if criticality_filter != "Todas" and row["Criticidade"] != criticality_filter:
            continue
        if status_filter != "Todos" and row["Status"] != status_filter:
            continue
        filtered.append(row)

    with st.container(border=True):
        st.subheader("Ocorrencias registradas")
        st.dataframe(filtered, use_container_width=True, hide_index=True)


def render_technical_report() -> None:
    st.title("Relatorio tecnico")
    render_notice()

    if not st.session_state.diagnostics:
        st.info("Nenhum relatorio disponivel ainda.", icon=":material/info:")
        return

    options = []
    for incident in st.session_state.incidents:
        options.append(f"#{incident['id']} - {incident['equipment_name']} - {incident['main_symptom']}")

    default_index = 0
    if st.session_state.selected_incident_id is not None:
        for index, incident in enumerate(st.session_state.incidents):
            if incident["id"] == st.session_state.selected_incident_id:
                default_index = index
                break

    selected = st.selectbox("Selecione um registro", options, index=default_index)
    selected_id = int(selected.split(" - ")[0].replace("#", ""))
    st.session_state.selected_incident_id = selected_id
    incident = next(item for item in st.session_state.incidents if item["id"] == selected_id)
    diagnostic = next(item for item in st.session_state.diagnostics if item["incident_id"] == selected_id)

    with st.container(border=True):
        st.subheader("Relatorio textual")
        st.text_area("Conteudo", diagnostic["technical_report"], height=320)
        st.download_button(
            "Baixar relatorio .txt",
            data=diagnostic["technical_report"],
            file_name=f"diagnoflow-relatorio-{selected_id}.txt",
            mime="text/plain",
            use_container_width=True,
        )


def render_future_ai() -> None:
    st.title("Futura integracao com IA")
    render_notice()

    with st.container(border=True):
        st.subheader("Evolucao prevista para a segunda entrega")
        st.markdown(
            """
            - substituir o motor de regras por uma orquestracao com LLM;
            - consultar historico da maquina;
            - consultar base de falhas conhecidas;
            - calcular criticidade;
            - gerar checklist tecnico;
            - gerar relatorio estruturado.
            """
        )
        st.write(
            "A fase atual continua 100% mockada. Na segunda entrega, a integracao devera incluir system prompt, tools, validacao humana e structured outputs."
        )
        st.write(
            "Riscos previstos: alucinacao, excesso de confianca e necessidade de trilha de auditoria para recomendacoes tecnicas."
        )


def main() -> None:
    st.set_page_config(
        page_title="DiagnoFlow AI Streamlit",
        page_icon=":material/precision_manufacturing:",
        layout="wide",
    )
    init_state()

    with st.sidebar:
        st.title("DiagnoFlow AI")
        page = st.radio(
            "Navegacao",
            [
                "Dashboard",
                "Equipamentos",
                "Nova Ocorrencia",
                "Historico",
                "Relatorio Tecnico",
                "Futura Integracao com IA",
            ],
        )
        st.caption("Versao Streamlit para entrega online simplificada.")

    if page == "Dashboard":
        render_dashboard()
    elif page == "Equipamentos":
        render_equipment()
    elif page == "Nova Ocorrencia":
        render_new_incident()
    elif page == "Historico":
        render_history()
    elif page == "Relatorio Tecnico":
        render_technical_report()
    else:
        render_future_ai()


if __name__ == "__main__":
    main()
