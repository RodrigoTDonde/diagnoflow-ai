from app.llm_orchestrator.guardrails import validate_structured_diagnostic
from app.llm_orchestrator.diagnostic_service import _append_runtime_metadata
from app.llm_orchestrator import graph as graph_module
from app.llm_orchestrator.provider import (
    LLMInvocationContext,
    MockDiagnosticLLMProvider,
    build_provider,
    inspect_provider_readiness,
)
from app.llm_orchestrator.schemas import StructuredDiagnosticDraft
from app.config import LLMRuntimeSettings


def _sample_draft() -> StructuredDiagnosticDraft:
    return StructuredDiagnosticDraft(
        probable_cause="Rolamento em degradação",
        confidence_level=0.78,
        priority="high",
        operational_risk="high",
        recommended_actions=["Coletar vibração", "Inspecionar lubrificação"],
        involved_parts=["rolamentos", "mancais"],
        inspection_checklist=["Bloquear equipamento", "Verificar temperatura"],
        evidence_summary=["Há vibração crescente", "Há aquecimento acima do padrão"],
        missing_information=["Sem laudo instrumental anexado"],
        observations="Saída estruturada para validação da fase 2.",
        technical_report="Relatório técnico preliminar gerado por fluxo estruturado.",
        requires_human_validation=True,
    )


def test_guardrail_accepts_valid_structured_diagnostic():
    draft = _sample_draft()
    validated = validate_structured_diagnostic(draft)
    assert validated == draft


def test_guardrail_rejects_empty_evidence_summary():
    draft = _sample_draft().model_copy(update={"evidence_summary": []})

    try:
        validate_structured_diagnostic(draft)
    except ValueError as exc:
        assert "evidence item" in str(exc)
    else:
        raise AssertionError("Guardrail should reject diagnostics without evidence summary.")


def test_build_provider_returns_mock_provider_for_unconfigured_runtime():
    settings = LLMRuntimeSettings(
        provider="not-configured",
        model="diagnoflow-mock-agent",
        temperature=0.2,
        top_p=0.9,
        agent_strategy="single-agent",
        use_langgraph=True,
        require_human_validation_for_high_risk=True,
        ollama_base_url="http://127.0.0.1:11434",
    )

    provider = build_provider(settings)
    assert isinstance(provider, MockDiagnosticLLMProvider)


def test_mock_provider_keeps_fallback_path_active():
    settings = LLMRuntimeSettings(
        provider="not-configured",
        model="diagnoflow-mock-agent",
        temperature=0.2,
        top_p=0.9,
        agent_strategy="single-agent",
        use_langgraph=True,
        require_human_validation_for_high_risk=True,
        ollama_base_url="http://127.0.0.1:11434",
    )
    provider = MockDiagnosticLLMProvider()
    context = LLMInvocationContext(
        system_prompt="Prompt técnico",
        user_prompt="Descreva um diagnóstico estruturado",
        settings=settings,
    )

    assert provider.generate_structured_diagnostic(context) is None


def test_provider_readiness_reports_fallback_when_unconfigured():
    settings = LLMRuntimeSettings(
        provider="not-configured",
        model="diagnoflow-mock-agent",
        temperature=0.2,
        top_p=0.9,
        agent_strategy="single-agent",
        use_langgraph=True,
        require_human_validation_for_high_risk=True,
        ollama_base_url="http://127.0.0.1:11434",
    )

    readiness = inspect_provider_readiness(settings)
    assert readiness.status == "fallback-active"
    assert readiness.ready is False
    assert "DIAGNOFLOW_LLM_PROVIDER=ollama" in readiness.activation_hint
    assert "qwen3:0.6b" in readiness.activation_hint


def test_provider_readiness_reports_unreachable_ollama(monkeypatch):
    settings = LLMRuntimeSettings(
        provider="ollama",
        model="qwen3:0.6b",
        temperature=0.2,
        top_p=0.9,
        agent_strategy="single-agent",
        use_langgraph=True,
        require_human_validation_for_high_risk=True,
        ollama_base_url="http://127.0.0.1:11434",
    )

    class BrokenClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            raise RuntimeError("offline")

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr("app.llm_orchestrator.provider.httpx.Client", BrokenClient)

    readiness = inspect_provider_readiness(settings)
    assert readiness.status == "unreachable"
    assert readiness.ready is False
    assert "ollama serve" in readiness.activation_hint


def test_get_agent_runtime_label_reports_langgraph_when_available(monkeypatch):
    monkeypatch.setattr(graph_module, "StateGraph", object)
    monkeypatch.setenv("DIAGNOFLOW_USE_LANGGRAPH", "true")
    monkeypatch.setenv("DIAGNOFLOW_LLM_PROVIDER", "not-configured")

    assert graph_module.get_agent_runtime_label() == "langgraph"


def test_append_runtime_metadata_avoids_duplicate_runtime_suffix():
    original = "Diagnóstico estruturado. Runtime atual: langgraph | provider=ollama | model=qwen3:0.6b | mode=local-free."
    updated = _append_runtime_metadata(original, "langgraph", "ollama", "qwen3:0.6b", "local-free")

    assert updated == original
