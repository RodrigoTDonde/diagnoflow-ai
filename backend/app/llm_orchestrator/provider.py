from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import shutil
from typing import Any
from typing import Protocol

import httpx

from ..config import LLMRuntimeSettings
from .schemas import StructuredDiagnosticDraft


@dataclass(frozen=True)
class LLMInvocationContext:
    system_prompt: str
    user_prompt: str
    settings: LLMRuntimeSettings


@dataclass(frozen=True)
class ProviderReadiness:
    status: str
    ready: bool
    reason: str
    cli_available: bool
    activation_hint: str


class DiagnosticLLMProvider(Protocol):
    def generate_structured_diagnostic(
        self,
        context: LLMInvocationContext,
    ) -> StructuredDiagnosticDraft | None:
        ...


class MockDiagnosticLLMProvider:
    """Provider placeholder for phase 2.

    Returns ``None`` on purpose so the orchestrator can keep using the
    deterministic local fallback until a real provider is connected.
    """

    def generate_structured_diagnostic(
        self,
        context: LLMInvocationContext,
    ) -> StructuredDiagnosticDraft | None:
        _ = context
        return None


class OpenAIDiagnosticLLMProvider:
    """Optional OpenAI provider for the phase 2 architecture.

    It is intentionally defensive:
    - if the SDK is not installed, returns ``None``;
    - if the runtime is not configured for OpenAI, returns ``None``;
    - if the model call fails, returns ``None`` so the fallback path stays active.
    """

    def __init__(self, settings: LLMRuntimeSettings):
        self.settings = settings

    def _build_response_format(self) -> dict[str, Any]:
        schema = StructuredDiagnosticDraft.model_json_schema()
        return {
            "format": {
                "type": "json_schema",
                "name": "diagnoflow_structured_diagnostic",
                "schema": schema,
                "strict": True,
            }
        }

    def generate_structured_diagnostic(
        self,
        context: LLMInvocationContext,
    ) -> StructuredDiagnosticDraft | None:
        if self.settings.provider.lower() != "openai":
            return None

        try:
            from openai import OpenAI
        except ImportError:
            return None

        try:
            client = OpenAI()
            response = client.responses.create(
                model=self.settings.model,
                input=[
                    {"role": "system", "content": context.system_prompt},
                    {"role": "user", "content": context.user_prompt},
                ],
                temperature=self.settings.temperature,
                top_p=self.settings.top_p,
                text=self._build_response_format(),
            )
            output_text = getattr(response, "output_text", None)
            if not output_text:
                return None
            return StructuredDiagnosticDraft.model_validate_json(output_text)
        except Exception:
            return None


class OllamaDiagnosticLLMProvider:
    """Optional local Ollama provider.

    Inference from Ollama docs/common usage:
    - local server usually listens on port 11434
    - `/api/chat` accepts model, messages and format parameters
    - failures should fall back to the deterministic local path
    """

    def __init__(self, settings: LLMRuntimeSettings):
        self.settings = settings

    def _build_payload(self, context: LLMInvocationContext) -> dict[str, Any]:
        schema = StructuredDiagnosticDraft.model_json_schema()
        return {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": context.system_prompt},
                {"role": "user", "content": context.user_prompt},
            ],
            "stream": False,
            "options": {
                "temperature": self.settings.temperature,
                "top_p": self.settings.top_p,
            },
            "format": schema,
        }

    def generate_structured_diagnostic(
        self,
        context: LLMInvocationContext,
    ) -> StructuredDiagnosticDraft | None:
        if self.settings.provider.lower() != "ollama":
            return None

        try:
            with httpx.Client(base_url=self.settings.ollama_base_url, timeout=60.0) as client:
                response = client.post("/api/chat", json=self._build_payload(context))
                response.raise_for_status()
                data = response.json()
        except Exception:
            return None

        message = data.get("message", {})
        content = message.get("content")
        if not content:
            return None

        try:
            return StructuredDiagnosticDraft.model_validate_json(content)
        except Exception:
            return None


def build_provider(settings: LLMRuntimeSettings) -> DiagnosticLLMProvider:
    if settings.provider.lower() == "ollama":
        return OllamaDiagnosticLLMProvider(settings)
    if settings.provider.lower() == "openai":
        return OpenAIDiagnosticLLMProvider(settings)
    return MockDiagnosticLLMProvider()


def inspect_provider_readiness(settings: LLMRuntimeSettings) -> ProviderReadiness:
    provider_name = settings.provider.lower()

    if provider_name == "not-configured":
        return ProviderReadiness(
            status="fallback-active",
            ready=False,
            reason="Nenhum provider real foi configurado; o fallback local estruturado permanece ativo.",
            cli_available=bool(shutil.which("ollama")),
            activation_hint="Defina DIAGNOFLOW_LLM_PROVIDER=ollama e DIAGNOFLOW_LLM_MODEL=qwen3:8b quando quiser testar o modo local gratuito.",
        )

    if provider_name == "openai":
        if importlib.util.find_spec("openai") is None:
            return ProviderReadiness(
                status="sdk-missing",
                ready=False,
                reason="O runtime está apontado para OpenAI, mas o pacote `openai` não está instalado neste ambiente.",
                cli_available=False,
                activation_hint="Instale o pacote openai no backend e configure as credenciais antes de ativar esse provider.",
            )
        return ProviderReadiness(
            status="sdk-available",
            ready=True,
            reason="SDK da OpenAI encontrado; a integração depende apenas das credenciais e da chamada do provider.",
            cli_available=False,
            activation_hint="Configure a credencial do provider e mantenha o schema estruturado ativo para preservar o controle do output.",
        )

    if provider_name == "ollama":
        cli_available = bool(shutil.which("ollama"))
        try:
            with httpx.Client(base_url=settings.ollama_base_url, timeout=2.0) as client:
                response = client.get("/api/tags")
                response.raise_for_status()
            return ProviderReadiness(
                status="reachable",
                ready=True,
                reason="Servidor Ollama local acessível e pronto para receber chamadas.",
                cli_available=cli_available,
                activation_hint="Mantenha o servidor Ollama ativo e confirme que o modelo configurado já foi baixado antes da demonstração.",
            )
        except Exception:
            return ProviderReadiness(
                status="unreachable",
                ready=False,
                reason="O runtime está configurado para Ollama, mas o servidor local não respondeu no endpoint esperado.",
                cli_available=cli_available,
                activation_hint="Instale o Ollama, execute `ollama serve` e baixe o modelo configurado, por exemplo `ollama pull qwen3:8b`.",
            )

    return ProviderReadiness(
        status="unknown-provider",
        ready=False,
        reason="O provider configurado não corresponde aos modos suportados pelo DiagnoFlow AI nesta fase.",
        cli_available=False,
        activation_hint="Use apenas os providers suportados nesta fase: not-configured, ollama ou openai.",
    )
