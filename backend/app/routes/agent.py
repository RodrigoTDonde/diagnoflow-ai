from fastapi import APIRouter

from ..config import get_llm_runtime_settings
from ..llm_orchestrator.graph import get_agent_runtime_label, get_system_prompt
from ..llm_orchestrator.provider import inspect_provider_readiness
from ..llm_orchestrator.tools import describe_available_tools
from ..schemas import AgentRuntimeRead

router = APIRouter(prefix="/agent", tags=["agent"])


@router.get("/runtime", response_model=AgentRuntimeRead)
def get_agent_runtime():
    settings = get_llm_runtime_settings()
    readiness = inspect_provider_readiness(settings)
    return {
        "runtime_label": get_agent_runtime_label(),
        "runtime_mode": settings.runtime_mode,
        "provider": settings.provider,
        "provider_status": readiness.status,
        "provider_ready": readiness.ready,
        "provider_reason": readiness.reason,
        "model": settings.model,
        "temperature": settings.temperature,
        "top_p": settings.top_p,
        "agent_strategy": settings.agent_strategy,
        "use_langgraph": settings.use_langgraph,
        "require_human_validation_for_high_risk": settings.require_human_validation_for_high_risk,
        "system_prompt": get_system_prompt(),
        "tools": describe_available_tools(),
    }
