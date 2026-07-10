# Future LLM Integration

## Objetivo da segunda fase

Substituir ou complementar o mecanismo determinístico atual por um orquestrador com LLM capaz de produzir triagem técnica mais rica, mantendo validação humana.

## Abordagem recomendada

A recomendação para a entrega final é começar com um agente único e controlado, com tools delimitadas, structured output e guardrails, em vez de iniciar por multiagente. Essa estratégia reduz risco, facilita demonstração e conversa melhor com o escopo da avaliação final.

## Arquitetura escolhida

Para iniciar a fase 2, a direção escolhida é:

- FastAPI como backend principal;
- LangGraph como orquestrador do agente;
- tools locais implementadas no backend;
- output estruturado validado por schema;
- validação humana para recomendações críticas.

## Fluxo previsto

1. Coletar ocorrência, contexto do equipamento e histórico.
2. Consultar tools internas para enriquecer o contexto.
3. Invocar o modelo com system prompt técnico e parâmetros controlados.
4. Validar saída estruturada antes de exibir ao usuário.
5. Exigir confirmação humana para recomendações críticas.

## Tools planejadas

- consultar histórico da máquina;
- consultar base de falhas conhecidas;
- calcular criticidade;
- gerar checklist técnico;
- gerar relatório estruturado.

## Ordem sugerida de implementação

1. definir modelo e framework;
2. criar schema do diagnóstico estruturado;
3. implementar o novo serviço de diagnóstico no backend;
4. conectar 2 ou 3 tools principais;
5. validar saída, risco e necessidade de revisão humana;
6. só depois avaliar MCP, RAG ou multiagente.

## Ativação local com Ollama

Na branch `fase-2`, a aplicação já expõe um painel técnico em `Futura integração com IA` e um endpoint `GET /agent/runtime` para mostrar:

- provider configurado;
- status de prontidão;
- motivo do fallback ou da disponibilidade;
- dica de ativação local.

Fluxo recomendado para ativação:

1. instalar o Ollama no sistema operacional;
2. iniciar o servidor local com `ollama serve`;
3. baixar um modelo compatível, por exemplo `ollama pull qwen3:0.6b`;
4. configurar no backend:
   - `DIAGNOFLOW_LLM_PROVIDER=ollama`
   - `DIAGNOFLOW_LLM_MODEL=qwen3:0.6b`
   - `DIAGNOFLOW_OLLAMA_BASE_URL=http://127.0.0.1:11434`
5. iniciar o backend e verificar `GET /agent/runtime`;
6. confirmar na interface se o provider aparece como `reachable`.

Enquanto o Ollama não estiver instalado ou acessível, o DiagnoFlow AI permanece em fallback estruturado local, sem quebrar a aplicação.

## Smoke test validado na branch `fase-2`

- instalação do `Ollama` concluída com sucesso no Windows;
- servidor local respondendo em `127.0.0.1:11434`;
- modelo `qwen3:0.6b` baixado;
- endpoint `GET /agent/runtime` retornando `provider=ollama`, `provider_status=reachable` e `provider_ready=true`;
- `POST /incidents` retornando `201` com `runtime_provider=ollama`.

## Riscos e mitigação

- Alucinação: exigir referências de evidência e revisão humana.
- Excesso de confiança: exibir nível de confiança e incertezas.
- Segurança: limitar acesso a dados operacionais sensíveis.
- Padronização: validar structured outputs com schema rígido.
