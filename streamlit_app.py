from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

import streamlit as st


APP_NOTICE = "Diagnóstico simulado - nenhum LLM foi integrado nesta fase."
APP_SUBTITLE = "Protótipo de triagem técnica com diagnóstico simulado"
SYMPTOM_FIELDS = [
    ("abnormal_noise", "Ruído anormal"),
    ("vibration", "Vibração"),
    ("overheating", "Superaquecimento"),
    ("leakage", "Vazamento"),
    ("electrical_failure", "Falha elétrica"),
    ("total_stop", "Parada total"),
    ("performance_loss", "Perda de desempenho"),
]


def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
            [data-testid="stAppViewBlockContainer"] {
                padding-top: 1.8rem;
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #112b33 0%, #163843 100%);
            }
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.9rem;
            }
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] label p,
            [data-testid="stSidebar"] [role="radiogroup"] p {
                color: #e7f0f2 !important;
            }
            .sidebar-shell {
                margin-bottom: 0.9rem;
            }
            .sidebar-shell h2 {
                margin: 0;
                color: #f6fbfc;
                font-size: 2rem;
                line-height: 1.1;
            }
            .sidebar-shell p {
                margin: 0.65rem 0 0 0;
                color: #c9d8dd;
                font-size: 1rem;
            }
            .sidebar-nav-label {
                color: #f3fafc;
                font-weight: 700;
                margin: 0.4rem 0 0.35rem 0;
                font-size: 1rem;
            }
            .status-box {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 14px;
                padding: 0.9rem 1rem;
                margin-top: 0.45rem;
            }
            .status-box h4 {
                margin: 0 0 0.45rem 0;
                color: #f3fafc;
                font-size: 0.95rem;
            }
            .status-box ul {
                margin: 0;
                padding-left: 1rem;
                color: #deebef;
            }
            .status-box li {
                margin: 0.18rem 0;
            }
            .flow-box {
                background: #ffffff;
                border: 1px solid #d7e1e5;
                border-radius: 14px;
                padding: 0.95rem 1rem;
                margin-top: 0.75rem;
                color: #17323a;
            }
            .flow-box strong {
                color: #12313a;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def seed_equipment() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "Bomba P-101",
            "type": "Bomba centrífuga",
            "sector": "Utilidades",
            "manufacturer": "WEG",
            "model": "CPX-400",
            "criticality": "alta",
            "status": "operando com restrição",
            "created_at": now_iso(),
        },
        {
            "id": 2,
            "name": "Motor M-204",
            "type": "Motor elétrico",
            "sector": "Mistura",
            "manufacturer": "Siemens",
            "model": "HT-315",
            "criticality": "média",
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
            "status": "em observação",
            "created_at": now_iso(),
        },
    ]


def score_symptoms(symptoms: dict[str, bool]) -> int:
    return sum(1 for active in symptoms.values() if active)


def format_priority(priority: str) -> str:
    labels = {
        "critical": "Crítica",
        "high": "Alta",
        "medium": "Média",
        "low": "Baixa",
    }
    return labels.get(priority, priority.title())


def format_risk(risk: str) -> str:
    labels = {
        "critical": "Crítico",
        "high": "Alto",
        "moderate": "Moderado",
        "low": "Baixo",
    }
    return labels.get(risk, risk.title())


def format_status(status: str) -> str:
    labels = {
        "open": "Aberta",
        "closed": "Encerrada",
    }
    return labels.get(status, status.title())


def build_mock_diagnostic(incident: dict[str, Any], equipment: dict[str, Any]) -> dict[str, Any]:
    symptoms = incident["symptoms"]
    symptom_score = score_symptoms(symptoms)

    probable_cause = "Desalinhamento mecânico e desgaste progressivo"
    involved_parts = ["acoplamento", "rolamentos", "base de fixação"]
    recommended_actions = [
        "Inspecionar alinhamento a laser e reaperto da base",
        "Verificar condição dos rolamentos e lubrificação",
        "Registrar tendência de vibração para comparação na próxima rodada",
    ]
    priority = "medium"
    operational_risk = "moderate"

    if symptoms["electrical_failure"] or "elétr" in incident["main_symptom"].lower() or "eletr" in incident["main_symptom"].lower():
        probable_cause = "Intermitência elétrica no conjunto de acionamento"
        involved_parts = ["painel de comando", "inversor de frequência", "cabos de potência"]
        recommended_actions = [
            "Bloquear equipamento e medir continuidade dos circuitos",
            "Inspecionar bornes, contatores e aquecimento no painel",
            "Validar parâmetros do inversor antes do retorno operacional",
        ]
        priority = "high"
        operational_risk = "high"
    elif symptoms["overheating"] and symptoms["vibration"]:
        probable_cause = "Rolamento em degradação com geração de calor e vibração"
        involved_parts = ["rolamentos", "mancais", "sistema de lubrificação"]
        recommended_actions = [
            "Executar inspeção termográfica e coleta de vibração",
            "Planejar troca de rolamentos no menor intervalo possível",
            "Verificar contaminação ou falta de lubrificante",
        ]
        priority = "high"
        operational_risk = "high"
    elif symptoms["leakage"]:
        probable_cause = "Falha de vedação ou desgaste em retentor"
        involved_parts = ["selos", "retentores", "tubulações de vedação"]
        recommended_actions = [
            "Identificar ponto exato do vazamento",
            "Verificar integridade de selos, juntas e conexões",
            "Avaliar impacto do vazamento sobre segurança e processo",
        ]
    elif symptoms["total_stop"]:
        probable_cause = "Parada total associada a proteção operacional ou falha crítica"
        involved_parts = ["sistema de proteção", "motor", "acoplamento"]
        recommended_actions = [
            "Manter equipamento indisponível até liberação técnica",
            "Executar checklist de retorno com foco em proteção e acionamento",
            "Documentar causa raiz preliminar antes da retomada",
        ]
        priority = "critical"
        operational_risk = "critical"

    if incident["perceived_urgency"] == "alta" and priority == "medium":
        priority = "high"
        operational_risk = "high"

    confidence = min(0.52 + (symptom_score * 0.06), 0.93)
    observations = (
        f"Diagnóstico simulado para {equipment['name']} ({equipment['type']}). "
        "A inferência foi baseada em regras estáticas de sintomas, sem uso de LLM."
    )
    technical_report = (
        "Relatório técnico preliminar\n\n"
        f"Equipamento: {equipment['name']}\n"
        f"Tipo: {equipment['type']}\n"
        f"Sintoma principal: {incident['main_symptom']}\n"
        f"Descrição operacional: {incident['description']}\n"
        f"Turno informado: {incident['shift']}\n"
        f"Urgência percebida: {incident['perceived_urgency']}\n\n"
        f"Causa provável: {probable_cause}\n"
        f"Prioridade: {format_priority(priority)}\n"
        f"Risco operacional: {format_risk(operational_risk)}\n"
        f"Peças potencialmente envolvidas: {', '.join(involved_parts)}\n"
        f"Ações recomendadas: {'; '.join(recommended_actions)}\n\n"
        "Observação: diagnóstico simulado, sem integração com modelo de IA nesta fase."
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
        "main_symptom": "Vibração crescente com aquecimento",
        "description": "Operador relatou aumento de vibração nas últimas 6 horas e temperatura acima do padrão.",
        "shift": "manhã",
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
    raise ValueError("Equipamento não encontrado.")


def next_equipment_id() -> int:
    if not st.session_state.equipment:
        return 1
    return max(item["id"] for item in st.session_state.equipment) + 1


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
                "Criticidade": incident["equipment_criticality"].title(),
                "Status": format_status(incident["status"]),
                "Prioridade": format_priority(diagnostic["priority"]),
                "Data": incident["created_at"].replace("T", " "),
            }
        )
    return list(reversed(rows))


def render_hero() -> None:
    st.title("DiagnoFlow AI")
    st.caption(APP_SUBTITLE)
    st.info(APP_NOTICE, icon=":material/warning:")


def render_sidebar_status() -> None:
    st.markdown(
        """
        <div class="status-box">
            <h4>Status do protótipo</h4>
            <ul>
                <li>Diagnóstico simulado</li>
                <li>Sem LLM integrado nesta fase</li>
                <li>Dados mockados para demonstração</li>
                <li>Arquitetura preparada para evolução futura</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_intro() -> None:
    st.markdown(
        """
        <div class="sidebar-shell">
            <h2>DiagnoFlow AI</h2>
            <p>Protótipo de triagem técnica com diagnóstico simulado</p>
        </div>
        <div class="sidebar-nav-label">Navegação</div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    render_hero()
    st.caption("Visão geral da demonstração funcional da triagem técnica industrial.")

    total_equipment = len(st.session_state.equipment)
    open_incidents = sum(1 for item in st.session_state.incidents if item["status"] == "open")
    simulated_diagnostics = len(st.session_state.diagnostics)
    high_criticality = sum(1 for item in st.session_state.equipment if item["criticality"] == "alta")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Equipamentos", total_equipment, border=True)
    with col2:
        st.metric("Ocorrências abertas", open_incidents, border=True)
    with col3:
        st.metric("Diagnósticos", simulated_diagnostics, border=True)
    with col4:
        st.metric("Ativos críticos", high_criticality, border=True)

    st.markdown(
        """
        <div class="flow-box">
            <strong>Fluxo principal</strong><br>
            Registrar sintomas → gerar diagnóstico simulado → emitir relatório técnico.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.subheader("Últimas ocorrências")
        for row in latest_incident_rows():
            incident = row["incident"]
            diagnostic = row["diagnostic"]
            st.markdown(f"**{incident['equipment_name']}**")
            st.write(
                f"{incident['main_symptom']} | prioridade {format_priority(diagnostic['priority'])} | risco {format_risk(diagnostic['operational_risk'])}"
            )
            st.caption(diagnostic["probable_cause"])


def render_equipment() -> None:
    render_hero()
    st.subheader("Equipamentos")

    left, right = st.columns([1.4, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**Ativos cadastrados**")
            st.dataframe(
                [
                    {
                        "Nome": item["name"],
                        "Tipo": item["type"],
                        "Setor": item["sector"],
                        "Criticidade": item["criticality"].title(),
                        "Status": item["status"].title(),
                    }
                    for item in st.session_state.equipment
                ],
                use_container_width=True,
                hide_index=True,
            )
    with right:
        with st.form("equipment_form", border=True):
            st.markdown("**Novo equipamento**")
            name = st.text_input("Nome do equipamento")
            equipment_type = st.text_input("Tipo")
            sector = st.text_input("Setor")
            manufacturer = st.text_input("Fabricante")
            model = st.text_input("Modelo")
            criticality = st.selectbox("Criticidade", ["baixa", "média", "alta"])
            status = st.selectbox("Status", ["operacional", "em observação", "operando com restrição", "parado"])
            submitted = st.form_submit_button("Cadastrar equipamento", use_container_width=True)
            if submitted:
                if not all([name.strip(), equipment_type.strip(), sector.strip(), manufacturer.strip(), model.strip()]):
                    st.error("Preencha todos os campos do equipamento antes de cadastrar.", icon=":material/error:")
                    return

                new_equipment = {
                    "id": next_equipment_id(),
                    "name": name.strip(),
                    "type": equipment_type.strip(),
                    "sector": sector.strip(),
                    "manufacturer": manufacturer.strip(),
                    "model": model.strip(),
                    "criticality": criticality,
                    "status": status,
                    "created_at": now_iso(),
                }
                st.session_state.equipment = [*st.session_state.equipment, new_equipment]
                st.success("Equipamento cadastrado com sucesso.", icon=":material/check_circle:")
                st.rerun()


def render_new_incident() -> None:
    render_hero()
    st.subheader("Nova ocorrência")

    left, right = st.columns([1.2, 1], gap="large")
    with left:
        with st.form("incident_form", border=True):
            st.markdown("**Registrar ocorrência**")
            equipment_options = {item["name"]: item["id"] for item in st.session_state.equipment}
            selected_equipment_name = st.selectbox("Equipamento", list(equipment_options.keys()))
            main_symptom = st.text_input("Sintoma principal")
            description = st.text_area("Descrição operacional", height=140)
            shift = st.selectbox("Turno", ["manhã", "tarde", "noite"])
            urgency = st.selectbox("Urgência percebida", ["baixa", "média", "alta"])
            status = st.selectbox("Status da ocorrência", ["open", "closed"])

            st.markdown("**Sintomas observados**")
            symptom_values: dict[str, bool] = {}
            cols = st.columns(2)
            for index, (key, label) in enumerate(SYMPTOM_FIELDS):
                with cols[index % 2]:
                    symptom_values[key] = st.checkbox(label, key=f"symptom_{key}")

            submitted = st.form_submit_button("Gerar diagnóstico simulado", use_container_width=True)
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
                st.session_state.selected_incident_id = incident["id"]
                st.success("Ocorrência registrada e diagnóstico simulado gerado.", icon=":material/analytics:")

    with right:
        with st.container(border=True):
            st.markdown("**Diagnóstico simulado**")
            current = st.session_state.get("latest_diagnostic")
            if not current:
                st.caption("Registre uma ocorrência para ver o resultado.")
                return

            incident = current["incident"]
            diagnostic = current["diagnostic"]

            st.write(f"**Equipamento:** {incident['equipment_name']}")
            stat1, stat2 = st.columns(2)
            with stat1:
                st.metric("Prioridade", format_priority(diagnostic["priority"]), border=True)
            with stat2:
                st.metric("Risco", format_risk(diagnostic["operational_risk"]), border=True)

            st.markdown(f"**Causa provável:** {diagnostic['probable_cause']}")
            st.write("**Confiança simulada**")
            st.progress(diagnostic["confidence_level"])
            st.caption(f"{int(diagnostic['confidence_level'] * 100)}%")

            with st.expander("Ações recomendadas", expanded=True):
                for action in diagnostic["recommended_actions"]:
                    st.markdown(f"- {action}")

            with st.expander("Peças possivelmente envolvidas"):
                st.write(", ".join(diagnostic["involved_parts"]))

            with st.expander("Observações"):
                st.write(diagnostic["observations"])


def render_history() -> None:
    render_hero()
    st.subheader("Histórico")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        equipment_filter = st.selectbox("Equipamento", ["Todos"] + [item["name"] for item in st.session_state.equipment])
    with filter_col2:
        criticality_filter = st.selectbox("Criticidade", ["Todas", "baixa", "média", "alta"])
    with filter_col3:
        status_filter = st.selectbox("Status", ["Todos", "open", "closed"])

    filtered = []
    for row in history_rows():
        if equipment_filter != "Todos" and row["Equipamento"] != equipment_filter:
            continue
        if criticality_filter != "Todas" and row["Criticidade"].lower() != criticality_filter:
            continue
        if status_filter != "Todos" and row["Status"] != format_status(status_filter):
            continue
        filtered.append(row)

    with st.container(border=True):
        st.markdown("**Ocorrências registradas**")
        st.dataframe(filtered, use_container_width=True, hide_index=True)


def render_technical_report() -> None:
    render_hero()
    st.subheader("Relatório técnico")

    if not st.session_state.diagnostics:
        st.info("Nenhum relatório disponível ainda.", icon=":material/info:")
        return

    options = [f"#{incident['id']} - {incident['equipment_name']} - {incident['main_symptom']}" for incident in st.session_state.incidents]

    default_index = 0
    if st.session_state.selected_incident_id is not None:
        for index, incident in enumerate(st.session_state.incidents):
            if incident["id"] == st.session_state.selected_incident_id:
                default_index = index
                break

    selected = st.selectbox("Selecione um registro", options, index=default_index)
    selected_id = int(selected.split(" - ")[0].replace("#", ""))
    st.session_state.selected_incident_id = selected_id
    diagnostic = next(item for item in st.session_state.diagnostics if item["incident_id"] == selected_id)

    with st.container(border=True):
        st.markdown("**Relatório textual**")
        st.text_area("Conteúdo", diagnostic["technical_report"], height=320)
        st.download_button(
            "Baixar relatório .txt",
            data=diagnostic["technical_report"],
            file_name=f"diagnoflow-relatorio-{selected_id}.txt",
            mime="text/plain",
            use_container_width=True,
        )


def render_future_ai() -> None:
    render_hero()
    st.subheader("Futura integração com IA")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.container(border=True):
            st.markdown("**Futuro system prompt**")
            st.write(
                "A segunda fase deverá incluir um system prompt técnico para orientar o modelo com foco em segurança operacional, limites de confiança e formato padronizado de resposta."
            )

        with st.container(border=True):
            st.markdown("**Futuras tools**")
            st.markdown(
                """
                - consultar histórico da máquina;
                - consultar base de falhas conhecidas;
                - calcular criticidade;
                - gerar checklist técnico;
                - gerar relatório estruturado.
                """
            )

        with st.container(border=True):
            st.markdown("**Structured outputs**")
            st.write(
                "A saída futura deverá seguir schemas rígidos para causa provável, prioridade, risco, recomendações, checklist e relatório técnico."
            )

    with col2:
        with st.container(border=True):
            st.markdown("**Validação humana**")
            st.write(
                "Mesmo com LLM na segunda entrega, qualquer recomendação crítica deverá passar por validação humana antes de orientar manutenção real."
            )

        with st.container(border=True):
            st.markdown("**Riscos de alucinação**")
            st.write(
                "Os riscos principais são excesso de confiança, recomendações sem evidência e omissão de contexto operacional. Por isso, a integração futura precisará de rastreabilidade e revisão."
            )


def main() -> None:
    st.set_page_config(
        page_title="DiagnoFlow AI Streamlit",
        page_icon=":material/precision_manufacturing:",
        layout="wide",
    )
    apply_custom_css()
    init_state()

    with st.sidebar:
        render_sidebar_intro()
        page = st.radio(
            "Navegação",
            [
                "Dashboard",
                "Equipamentos",
                "Nova Ocorrência",
                "Histórico",
                "Relatório Técnico",
                "Futura Integração com IA",
            ],
            label_visibility="collapsed",
        )
        render_sidebar_status()

    if page == "Dashboard":
        render_dashboard()
    elif page == "Equipamentos":
        render_equipment()
    elif page == "Nova Ocorrência":
        render_new_incident()
    elif page == "Histórico":
        render_history()
    elif page == "Relatório Técnico":
        render_technical_report()
    else:
        render_future_ai()


if __name__ == "__main__":
    main()
