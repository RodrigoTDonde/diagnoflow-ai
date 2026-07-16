param(
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$runtimeUrl = "http://127.0.0.1:$Port/agent/runtime"

try {
    $response = Invoke-RestMethod -Uri $runtimeUrl -Method Get -TimeoutSec 5
} catch {
    throw "Nao foi possivel acessar $runtimeUrl"
}

Write-Host "runtime_label=$($response.runtime_label)"
Write-Host "provider=$($response.provider)"
Write-Host "provider_status=$($response.provider_status)"
Write-Host "provider_ready=$($response.provider_ready)"
Write-Host "model=$($response.model)"
Write-Host "use_langgraph=$($response.use_langgraph)"

if ($response.runtime_label -ne "langgraph") {
    throw "Runtime invalido: esperado langgraph."
}

if ($response.provider -ne "ollama") {
    throw "Provider invalido: esperado ollama."
}

if (-not $response.provider_ready) {
    throw "Provider ainda nao esta pronto para a demo."
}

if (-not $response.use_langgraph) {
    throw "LangGraph nao esta ativo."
}

Write-Host "Checagem da fase 2 concluida com sucesso."
