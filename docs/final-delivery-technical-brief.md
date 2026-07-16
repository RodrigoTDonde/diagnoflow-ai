# Resumo Técnico da Entrega Final

Este documento consolida a configuração técnica da fase 2 do DiagnoFlow AI para apresentação acadêmica.

## Objetivo

Evoluir o protótipo de triagem técnica industrial da primeira entrega para uma aplicação com integração real de IA generativa, mantendo:

- fluxo funcional de equipamentos, ocorrências, diagnóstico e histórico;
- output estruturado;
- guardrails explícitos;
- validação humana para casos críticos;
- justificativa técnica das decisões.

## Arquitetura adotada

- `FastAPI` como backend principal;
- `React + Vite + TypeScript` como interface;
- `SQLite` para persistência local;
- `LangGraph` como orquestrador preparado para o fluxo do agente;
- `LangGraph` instalado no ambiente do backend e validado no runtime da fase 2;
- tools locais implementadas no backend;
- output estruturado validado por schema;
- trilha de auditoria de validação humana.

## Modelo e estratégia de integração

### Modo padrão de desenvolvimento

- provider: `not-configured`
- model: `diagnoflow-mock-agent`
- objetivo: manter custo zero e permitir evolução da arquitetura sem depender de inferência real o tempo todo.

### Modo local gratuito validado

- provider: `ollama`
- model: `qwen3:0.6b`
- endpoint local: `http://127.0.0.1:11434`
- objetivo: demonstrar integração real com custo zero e controle local.

### Modo opcional de maior previsibilidade

- provider: `openai`
- model sugerido: `gpt-5-mini`
- objetivo: usar apenas se a demo final exigir maior robustez de output estruturado.

## Parâmetros do modelo

Os parâmetros expostos no runtime atual são:

- `temperature=0.2`
- `top_p=0.9`
- `agent_strategy=single-agent`
- `use_langgraph=true`
- `require_human_validation_for_high_risk=true`

Justificativa:

- temperatura baixa reduz variação desnecessária;
- `top_p` moderado mantém diversidade controlada;
- agente único simplifica a narrativa arquitetural;
- validação humana obrigatória reduz risco operacional.

## System prompt

O prompt técnico atual orienta o agente a:

- analisar sintomas operacionais;
- considerar histórico;
- priorizar segurança;
- produzir saída estruturada;
- destacar hipóteses, evidências e lacunas;
- marcar recomendações críticas para revisão humana.

Referências:

- [prompts/future-system-prompt.txt](prompts/future-system-prompt.txt)
- [backend/app/llm_orchestrator/prompt.py](../backend/app/llm_orchestrator/prompt.py)

## Tools disponibilizadas ao agente

- `consultar_historico_maquina`
  Busca contexto de ocorrências anteriores do equipamento.
- `calcular_criticidade_ocorrencia`
  Classifica prioridade e risco operacional.
- `consultar_base_falhas`
  Sugere hipótese técnica, evidências e ações iniciais.
- `gerar_checklist_inspecao`
  Monta checklist coerente com a hipótese principal.
- `gerar_relatorio_tecnico`
  Consolida um relatório textual estruturado.

## Output estruturado

O diagnóstico foi modelado para retornar, entre outros:

- causa provável;
- confiança;
- prioridade;
- risco operacional;
- ações recomendadas;
- peças envolvidas;
- checklist de inspeção;
- evidências consideradas;
- lacunas de contexto;
- sinalização de validação humana.

Isso garante:

- previsibilidade da interface;
- menor risco de texto solto inconsistente;
- melhor explicação para a banca.

## Guardrails aplicados

### Guardrail de output

- valida presença de causa provável;
- valida presença de ações recomendadas;
- valida presença de evidências mínimas.

### Guardrail operacional

- casos de maior risco seguem com `requires_human_validation=true`;
- o frontend exibe alerta visual para revisão antes de decisão crítica.

### Guardrail de runtime

- o endpoint `GET /agent/runtime` expõe:
  - provider;
  - modelo;
  - status de prontidão;
  - motivo do fallback;
  - dica de ativação local;
  - tools disponíveis.

## Human-in-the-loop

Foi adicionada uma trilha de auditoria humana com:

- tabela `human_validation_reviews`;
- endpoint `POST /diagnostics/{incident_id}/review`;
- armazenamento de:
  - responsável técnico;
  - decisão;
  - observações;
  - data/hora;
- exibição no frontend:
  - última revisão;
  - responsável;
  - quantidade de revisões;
  - trilha de auditoria.

## Evidência de teste real com Ollama

O smoke test local da fase 2 já foi validado nesta branch:

- `Ollama` instalado com sucesso no Windows via `winget`;
- servidor local respondendo em `127.0.0.1:11434`;
- modelo `qwen3:0.6b` baixado;
- `GET /agent/runtime` retornando:
  - `provider=ollama`
  - `provider_status=reachable`
  - `provider_ready=true`
- `POST /incidents` retornando `201` com:
  - `runtime_provider=ollama`
  - `runtime_model=qwen3:0.6b`

## O que a aplicação já demonstra na fase 2

- integração real opcional com provider local;
- configuração visível de runtime;
- tools explícitas;
- output estruturado;
- revisão humana registrada;
- histórico com auditoria.

## Próximo passo recomendado

Para fechar a entrega final com mais força acadêmica, o próximo passo recomendado é:

- consolidar a apresentação final destacando fluxo, modelo, prompt, tools, guardrails e auditoria humana em uma demo curta e objetiva.
