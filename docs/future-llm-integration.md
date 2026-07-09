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

## Riscos e mitigação

- Alucinação: exigir referências de evidência e revisão humana.
- Excesso de confiança: exibir nível de confiança e incertezas.
- Segurança: limitar acesso a dados operacionais sensíveis.
- Padronização: validar structured outputs com schema rígido.
