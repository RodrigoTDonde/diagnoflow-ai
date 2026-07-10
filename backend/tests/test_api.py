from fastapi.testclient import TestClient

from app.main import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "DiagnoFlow AI" in response.text


def test_dashboard():
    with TestClient(app) as client:
        response = client.get("/dashboard")
        assert response.status_code == 200
        payload = response.json()
        assert "summary" in payload
        assert "latest_incidents" in payload
        assert payload["latest_incidents"]

        diagnostic = payload["latest_incidents"][0]["diagnostic"]
        assert diagnostic["runtime_label"] in {"fallback-local", "langgraph"}
        assert diagnostic["runtime_mode"] == "fallback-local"
        assert diagnostic["runtime_provider"] == "not-configured"
        assert diagnostic["inspection_checklist"]
        assert diagnostic["evidence_summary"]
        assert isinstance(diagnostic["requires_human_validation"], bool)


def test_spa_fallback():
    with TestClient(app) as client:
        response = client.get("/historico")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "DiagnoFlow AI" in response.text


def test_agent_runtime_endpoint():
    with TestClient(app) as client:
        response = client.get("/agent/runtime")

    assert response.status_code == 200
    payload = response.json()
    assert payload["runtime_label"] in {"fallback-local", "langgraph"}
    assert payload["runtime_mode"] == "fallback-local"
    assert payload["provider"] == "not-configured"
    assert payload["provider_status"] == "fallback-active"
    assert payload["provider_ready"] is False
    assert "fallback local" in payload["provider_reason"].lower()
    assert isinstance(payload["provider_cli_available"], bool)
    assert "DIAGNOFLOW_LLM_PROVIDER=ollama" in payload["activation_hint"]
    assert "qwen3:0.6b" in payload["activation_hint"]
    assert payload["model"] == "diagnoflow-mock-agent"
    assert payload["use_langgraph"] is True
    assert payload["require_human_validation_for_high_risk"] is True
    assert "triagem técnica" in payload["system_prompt"].lower()
    assert len(payload["tools"]) >= 5


def test_create_incident_returns_structured_diagnostic():
    payload = {
        "equipment_id": 1,
        "main_symptom": "Falha elétrica com parada total",
        "description": "Equipamento desligou após alarme e não retomou operação.",
        "shift": "noite",
        "perceived_urgency": "alta",
        "symptoms": {
            "electrical_failure": True,
            "total_stop": True,
        },
    }

    with TestClient(app) as client:
        response = client.post("/incidents", json=payload)

    assert response.status_code == 201
    body = response.json()
    diagnostic = body["diagnostic"]

    assert diagnostic["priority"] == "critical"
    assert diagnostic["operational_risk"] == "critical"
    assert diagnostic["requires_human_validation"] is True
    assert diagnostic["inspection_checklist"]
    assert diagnostic["technical_report"]
    assert diagnostic["evidence_summary"]
    assert diagnostic["missing_information"]
    assert diagnostic["runtime_label"] in {"fallback-local", "langgraph"}
    assert diagnostic["runtime_provider"] == "not-configured"
    assert diagnostic["runtime_model"] == "diagnoflow-mock-agent"
    assert "Runtime atual:" in diagnostic["observations"]


def test_get_diagnostic_exposes_phase_two_fields():
    with TestClient(app) as client:
        dashboard = client.get("/dashboard")
        incident_id = dashboard.json()["latest_incidents"][0]["incident"]["id"]

        response = client.get(f"/diagnostics/{incident_id}")

    assert response.status_code == 200
    diagnostic = response.json()
    assert diagnostic["inspection_checklist"]
    assert diagnostic["evidence_summary"]
    assert diagnostic["missing_information"]
    assert "Runtime atual:" in diagnostic["observations"]
