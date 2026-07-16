param(
    [int]$Port = 8000,
    [string]$Model = "qwen3:0.6b",
    [string]$OllamaBaseUrl = "http://127.0.0.1:11434",
    [switch]$SkipModelPull,
    [switch]$PreflightOnly
)

$ErrorActionPreference = "Stop"

function Get-OllamaCommand {
    $command = Get-Command ollama -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $fallbackPath = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
    if (Test-Path $fallbackPath) {
        return $fallbackPath
    }

    throw "Ollama nao encontrado. Instale o Ollama antes de rodar a demo da fase 2."
}

function Test-OllamaServer {
    param([string]$BaseUrl)

    try {
        Invoke-RestMethod -Uri "$BaseUrl/api/tags" -Method Get -TimeoutSec 2 | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Ensure-OllamaServer {
    param(
        [string]$CommandPath,
        [string]$BaseUrl
    )

    if (Test-OllamaServer -BaseUrl $BaseUrl) {
        Write-Host "Ollama ja esta ativo em $BaseUrl"
        return
    }

    Write-Host "Iniciando servidor Ollama..."
    Start-Process -FilePath $CommandPath -ArgumentList "serve" -WindowStyle Hidden | Out-Null

    for ($attempt = 1; $attempt -le 15; $attempt++) {
        Start-Sleep -Seconds 1
        if (Test-OllamaServer -BaseUrl $BaseUrl) {
            Write-Host "Ollama respondeu apos $attempt segundo(s)."
            return
        }
    }

    throw "O servidor Ollama nao respondeu em $BaseUrl."
}

function Ensure-OllamaModel {
    param(
        [string]$CommandPath,
        [string]$ExpectedModel,
        [switch]$AllowPull
    )

    $listOutput = & $CommandPath list
    if ($listOutput -match [regex]::Escape($ExpectedModel)) {
        Write-Host "Modelo $ExpectedModel ja disponivel."
        return
    }

    if (-not $AllowPull) {
        throw "Modelo $ExpectedModel nao encontrado e o pull automatico foi desabilitado."
    }

    Write-Host "Baixando modelo $ExpectedModel..."
    & $CommandPath pull $ExpectedModel
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendPath = Join-Path $repoRoot "backend"
$backendPython = Join-Path $backendPath ".venv\Scripts\python.exe"

if (-not (Test-Path $backendPython)) {
    throw "Python da venv nao encontrado em $backendPython"
}

$ollamaCommand = Get-OllamaCommand
Ensure-OllamaServer -CommandPath $ollamaCommand -BaseUrl $OllamaBaseUrl
Ensure-OllamaModel -CommandPath $ollamaCommand -ExpectedModel $Model -AllowPull:(-not $SkipModelPull)

$env:DIAGNOFLOW_LLM_PROVIDER = "ollama"
$env:DIAGNOFLOW_LLM_MODEL = $Model
$env:DIAGNOFLOW_OLLAMA_BASE_URL = $OllamaBaseUrl
$env:DIAGNOFLOW_USE_LANGGRAPH = "true"
$env:DIAGNOFLOW_AGENT_STRATEGY = "single-agent"
$env:DIAGNOFLOW_REQUIRE_HUMAN_VALIDATION_FOR_HIGH_RISK = "true"

Write-Host "Runtime configurado: provider=ollama, model=$Model, langgraph=true"

if ($PreflightOnly) {
    Write-Host "Preflight concluido com sucesso."
    exit 0
}

Push-Location $backendPath
try {
    Write-Host "Iniciando backend da fase 2 em http://127.0.0.1:$Port ..."
    & $backendPython -m uvicorn app.main:app --host 0.0.0.0 --port $Port
} finally {
    Pop-Location
}
