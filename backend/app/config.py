from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMRuntimeSettings:
    provider: str
    model: str
    temperature: float
    top_p: float
    agent_strategy: str
    use_langgraph: bool
    require_human_validation_for_high_risk: bool
    ollama_base_url: str

    @property
    def runtime_mode(self) -> str:
        if self.provider.lower() == "ollama":
            return "local-free"
        if self.provider.lower() == "openai":
            return "cloud-api"
        return "fallback-local"


DEVELOPMENT_RUNTIME_PRESET = {
    "provider": "not-configured",
    "model": "diagnoflow-mock-agent",
    "notes": "Modo padrão de desenvolvimento sem custo, usando fallback local.",
}

LOCAL_DEMO_RUNTIME_PRESET = {
    "provider": "ollama",
    "model": "qwen3:0.6b",
    "notes": "Modo recomendado para demonstração local gratuita, usando Ollama.",
}

API_DEMO_RUNTIME_PRESET = {
    "provider": "openai",
    "model": "gpt-5-mini",
    "notes": "Modo opcional para demonstração com API paga e maior previsibilidade.",
}


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_float(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def get_llm_runtime_settings() -> LLMRuntimeSettings:
    return LLMRuntimeSettings(
        provider=os.getenv("DIAGNOFLOW_LLM_PROVIDER", "not-configured"),
        model=os.getenv("DIAGNOFLOW_LLM_MODEL", "diagnoflow-mock-agent"),
        temperature=_parse_float(os.getenv("DIAGNOFLOW_LLM_TEMPERATURE"), 0.2),
        top_p=_parse_float(os.getenv("DIAGNOFLOW_LLM_TOP_P"), 0.9),
        agent_strategy=os.getenv("DIAGNOFLOW_AGENT_STRATEGY", "single-agent"),
        use_langgraph=_parse_bool(os.getenv("DIAGNOFLOW_USE_LANGGRAPH"), True),
        require_human_validation_for_high_risk=_parse_bool(
            os.getenv("DIAGNOFLOW_REQUIRE_HUMAN_VALIDATION_FOR_HIGH_RISK"),
            True,
        ),
        ollama_base_url=os.getenv("DIAGNOFLOW_OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
    )
