# Plano de Implementação da Entrega Final

Este documento transforma o escopo da avaliação final e os conceitos da aula sobre agentes, tools, MCP e guardrails em um plano prático para evoluir o DiagnoFlow AI.

## Objetivo da fase 2

Evoluir a aplicação da entrega intermediária para uma solução com IA generativa integrada de verdade, demonstrando domínio sobre:

- escolha de modelo;
- escolha de framework;
- system prompt;
- parâmetros do modelo;
- tools disponibilizadas ao LLM;
- saída estruturada;
- guardrails;
- justificativa técnica das decisões.

## O que será reaproveitado da fase 1

- problema escolhido: triagem técnica de máquinas rotativas industriais;
- fluxo principal: equipamentos, ocorrência, diagnóstico, histórico e relatório;
- base full stack com FastAPI, React e SQLite;
- dados e entidades já existentes no backend;
- telas já prontas para operação;
- documentação do domínio e da futura integração.

## Direção recomendada

Com base no escopo da avaliação final e na aula sobre agentes, a melhor evolução para este projeto é:

1. começar com um agente único bem controlado;
2. integrar tools delimitadas e previsíveis;
3. exigir structured outputs;
4. adicionar validação humana antes de recomendações críticas;
5. considerar multiagente apenas se a complexidade justificar.

## O que não fazer logo de início

- não começar por multiagente;
- não misturar muitas bibliotecas de agentes ao mesmo tempo;
- não deixar o modelo responder em texto livre sem schema;
- não permitir ações destrutivas ou automáticas sem confirmação;
- não expandir o escopo com RAG antes de o fluxo básico com tools estar estável.

## Arquitetura recomendada para a fase 2

```text
Frontend React
    |
    v
Backend FastAPI
    |
    +--> Orquestrador de diagnóstico com LLM
    |       |
    |       +--> system prompt
    |       +--> tools internas
    |       +--> validação de output
    |       `--> guardrails
    |
    +--> Banco SQLite
    |
    `--> Histórico, equipamentos, ocorrências e base de falhas
```

## Estratégia de implementação recomendada

### Etapa 1 - Manter a interface e trocar apenas o motor do diagnóstico

Substituir o serviço mockado atual por uma camada de orquestração no backend, sem desmontar o frontend.

Resultado esperado:

- o usuário continua usando o mesmo fluxo;
- o backend deixa de responder com regra fixa;
- o diagnóstico passa a ser gerado por LLM com contexto e tools.

### Etapa 2 - Implementar agente único com tools

Começar com um agente único de triagem técnica.

Tools recomendadas:

- `consultar_historico_maquina`
- `consultar_base_falhas`
- `calcular_criticidade_ocorrencia`
- `gerar_checklist_inspecao`
- `gerar_relatorio_tecnico`

Essas tools devem ter:

- nome claro;
- docstring útil para o modelo;
- parâmetros tipados;
- retorno previsível;
- escopo curto, uma função por tool.

### Etapa 3 - Structured output obrigatório

O diagnóstico não deve sair em texto solto. A recomendação é exigir um schema com campos como:

- `probable_cause`
- `confidence_level`
- `priority`
- `operational_risk`
- `recommended_actions`
- `involved_parts`
- `evidence_summary`
- `missing_information`
- `requires_human_validation`

Isso ajuda em:

- previsibilidade da interface;
- validação técnica;
- apresentação para a banca;
- redução de alucinação operacional.

### Etapa 4 - Guardrails

Adicionar pelo menos três camadas:

1. guardrail de input
   - bloquear tentativa de prompt injection óbvia;
   - limitar entradas malformadas;
   - tratar contexto de usuário como dado, não como instrução.

2. guardrail de ação
   - impedir qualquer ação crítica automática;
   - exigir confirmação humana para recomendações sensíveis;
   - limitar tools ao escopo técnico permitido.

3. guardrail de output
   - validar o schema;
   - rejeitar campos vazios ou inconsistentes;
   - destacar incerteza, evidência e necessidade de validação humana.

### Etapa 5 - Evolução opcional

Só depois de o fluxo acima estar estável considerar:

- MCP para expor tools de forma padronizada;
- LangGraph para fluxo mais explícito de estado e transições;
- RAG com documentos técnicos e manuais;
- multiagente com supervisor e especialistas.

## Escolha técnica sugerida para começar

### Opção mais segura

- backend atual em FastAPI;
- chamadas diretas ao provedor ou SDK simples;
- tools internas implementadas no próprio backend;
- structured output com schema Python;
- frontend React reaproveitado sem refatoração grande.

### Opção com melhor narrativa acadêmica

- FastAPI no backend;
- LangGraph como orquestrador do agente;
- tools locais bem definidas;
- structured output validado;
- guardrails explícitos;
- MCP documentado como evolução seguinte ou prova de extensibilidade.

## Arquitetura escolhida para iniciar a fase 2

A arquitetura escolhida para começar a entrega final será:

- `FastAPI + LangGraph + tools locais + structured output + guardrails`

Essa escolha foi feita porque oferece o melhor equilíbrio entre:

- reaproveitamento da base atual;
- clareza arquitetural para apresentação;
- controle explícito do fluxo do agente;
- facilidade para demonstrar tools e validação humana;
- alinhamento com os conceitos cobrados em aula.

## Por que não começar pela opção mais simples

A opção com chamadas diretas ao provedor seria válida e mais rápida, mas perderíamos parte da narrativa técnica que a avaliação final tende a valorizar, especialmente:

- estado explícito do fluxo;
- separação clara entre raciocínio, tools e validação;
- possibilidade de mostrar guardrails e evolução para supervisor ou MCP;
- aderência mais visível ao conteúdo de agentes discutido em aula.

## Como essa arquitetura fica no projeto

```text
frontend/react
    |
    v
backend/fastapi
    |
    +--> llm_orchestrator/
    |       +--> graph.py
    |       +--> prompt.py
    |       +--> schemas.py
    |       +--> guardrails.py
    |       `--> tools/
    |
    +--> services/
    |       `--> diagnostic_service.py
    |
    `--> persistence/sqlite
```

## Primeiro ciclo de implementação

O primeiro ciclo da fase 2 deve ser pequeno e demonstrável:

1. criar o schema estruturado do diagnóstico;
2. criar 2 tools iniciais:
   - `consultar_historico_maquina`
   - `calcular_criticidade_ocorrencia`
3. criar o system prompt técnico inicial;
4. criar o grafo do agente com LangGraph;
5. integrar esse agente ao backend atual sem quebrar o frontend;
6. marcar saídas críticas como dependentes de validação humana.

Status atual deste repositório:

- schema estruturado iniciado;
- tools iniciais implementadas;
- grafo-base do agente criado com fallback local;
- configuração de provider/modelo preparada por ambiente.
- adapter do provider criado para futura integração real com LLM.
- primeiro adapter concreto preparado para OpenAI Responses API em modo opcional.
- adapter adicional preparado para Ollama local, com foco em custo zero.

## Primeiro provider escolhido para a fase 2

O primeiro provider escolhido para iniciar a integração real será a OpenAI Responses API, pelos seguintes motivos:

- boa aderência a structured outputs com JSON Schema;
- documentação e ecossistema maduros para demonstração acadêmica;
- boa narrativa para explicar modelo, parâmetros, tools e output estruturado;
- facilidade de manter fallback local enquanto a integração real não estiver ativa.

## Opção gratuita priorizada

Como alternativa prática para evitar custo por API, a arquitetura também foi preparada para Ollama local.

Essa opção é interessante quando:

- o objetivo é manter custo de inferência em zero;
- a máquina disponível suporta o modelo local;
- a qualidade do modelo aberto for suficiente para a demonstração;
- a banca valorizar a justificativa técnica de uso local e controle de dados.

Se a qualidade do modelo local não for suficiente, a arquitetura continua pronta para ativar OpenAI depois com mínimo retrabalho.

## Estratégia recomendada de ativação

### 1. Desenvolvimento diário

Usar fallback local:

- `DIAGNOFLOW_LLM_PROVIDER=not-configured`
- `DIAGNOFLOW_LLM_MODEL=diagnoflow-mock-agent`

Motivo:

- custo zero;
- estabilidade;
- foco em arquitetura, tools e guardrails antes da inferência real.

### 2. Demonstração local gratuita

Usar Ollama:

- `DIAGNOFLOW_LLM_PROVIDER=ollama`
- `DIAGNOFLOW_LLM_MODEL=qwen3:0.6b`
- `DIAGNOFLOW_OLLAMA_BASE_URL=http://127.0.0.1:11434`

Motivo:

- custo zero por inferência;
- boa narrativa para uso local;
- permite provar integração real sem depender de API paga.

Status atualizado:

- smoke test local já validado com `Ollama + qwen3:0.6b`;
- runtime detectado como `reachable`;
- fluxo de criação de ocorrência preservado com resposta `201`.

### 3. Demonstração final com maior previsibilidade

Usar OpenAI apenas se necessário:

- `DIAGNOFLOW_LLM_PROVIDER=openai`
- `DIAGNOFLOW_LLM_MODEL=gpt-5-mini`

Motivo:

- maior robustez para structured outputs;
- melhor consistência para demo curta;
- custo controlável se usado só na reta final.

### Recomendação geral

O caminho mais econômico e seguro é:

1. desenvolver com fallback local;
2. testar integração real com Ollama;
3. ativar OpenAI apenas se o modelo local não atingir a qualidade esperada para a apresentação.

## O que fica para o segundo ciclo

- adicionar `consultar_base_falhas`;
- adicionar `gerar_checklist_inspecao`;
- adicionar `gerar_relatorio_tecnico`;
- enriquecer a UI com evidências, incertezas e revisão humana;
- avaliar MCP como camada de extensibilidade;
- considerar RAG ou multiagente apenas se houver ganho real.

## Recomendação de ordem real de execução

1. definir o modelo e a estratégia de integração;
2. criar schema do diagnóstico final;
3. criar o novo serviço de diagnóstico com interface compatível com o backend atual;
4. implementar 2 ou 3 tools primeiro;
5. integrar system prompt técnico;
6. validar saída estruturada;
7. exibir evidência, incerteza e necessidade de revisão humana na UI;
8. documentar decisões de engenharia no README;
9. só depois pensar em MCP, RAG ou multiagente.

## Mapeamento dos conceitos da aula para o projeto

### Agente

No DiagnoFlow AI, o agente deve ser responsável por:

- interpretar a ocorrência;
- decidir quais tools consultar;
- consolidar o diagnóstico;
- devolver resposta estruturada.

### Tools

As tools devem acessar:

- histórico do equipamento;
- regras de criticidade;
- base de falhas frequentes;
- contexto operacional armazenado;
- geração de checklist e relatório.

### Human-in-the-loop

A aplicação deve deixar claro que:

- o diagnóstico é assistido por IA;
- recomendações críticas exigem validação humana;
- o sistema apoia a decisão, mas não substitui o técnico responsável.

### Multiagente

Só faz sentido se houver ganho real, por exemplo:

- pesquisador técnico;
- sintetizador do diagnóstico;
- revisor de segurança.

Para esta entrega, isso é opcional e não deve vir antes do agente único.

## O que provavelmente mais conta para a nota final

- a aplicação realmente usa IA generativa;
- as decisões de engenharia estão justificadas;
- o fluxo mostra tools e controle, não apenas chat;
- há clareza sobre prompt, modelo e parâmetros;
- existe proteção contra respostas ruins ou perigosas;
- a apresentação consegue explicar por que a arquitetura escolhida faz sentido.

## Riscos principais da fase 2

- integrar o modelo sem schema e perder controle da saída;
- escolher arquitetura complexa demais cedo demais;
- usar tools amplas e perigosas;
- não separar dado do usuário de instrução do sistema;
- não documentar o raciocínio de engenharia no README.

## Próximo passo recomendado

Começar pela implementação de um novo serviço de diagnóstico no backend, com esta meta mínima:

- 1 agente;
- 2 ou 3 tools;
- 1 system prompt técnico;
- 1 schema estruturado;
- 1 validação humana obrigatória para casos críticos.
