# DiagnoFlow AI

DiagnoFlow AI é uma aplicação full stack para triagem técnica de máquinas rotativas industriais. Na entrega intermediária, a proposta foi demonstrar uma jornada funcional de registro de sintomas, organização de ocorrências e geração de diagnóstico técnico mockado, sem integrar nenhum LLM real ao produto publicado.

## Situação das entregas no repositório

- `main`: versão estável da entrega intermediária, sem LLM real integrado.
- `fase-2`: evolução da entrega final, com arquitetura de agente, runtime configurável, smoke test real com `Ollama` e trilha de auditoria humana.

## Acesso rápido

- Endpoint público da entrega intermediária:
  `https://diagnoflow-ai-ty4bspr76dgyzc8bsgpzje.streamlit.app/`
- Repositório GitHub:
  `https://github.com/rodrigodondesenai/diagnoflow-ai`

Observação: por estar publicada no plano gratuito do Streamlit Community Cloud, a aplicação pode entrar em modo de inatividade após um período sem uso. Nesse caso, basta clicar em `Yes, get this app back up!` para reativá-la.

## Problema e solução

Em rotinas de manutenção industrial, técnicos precisam registrar sinais iniciais de falha com rapidez, manter histórico organizado e produzir um parecer preliminar antes de uma análise aprofundada. O problema escolhido tem complexidade suficiente porque envolve contexto operacional, criticidade do ativo, múltiplos sintomas concorrentes e necessidade de priorização.

A solução entregue foi uma aplicação com:

- cadastro de equipamentos;
- abertura de ocorrência com sintomas operacionais;
- diagnóstico simulado baseado em regras;
- histórico filtrável;
- relatório técnico textual;
- documentação da futura integração com IA generativa.

## O que a entrega intermediária oferece

- endpoint funcional em FastAPI;
- frontend React com múltiplas telas navegáveis;
- dados simulados persistidos em SQLite;
- interações de cadastro, listagem, histórico e geração de diagnóstico mockado;
- avisos explícitos na interface e na API de que não há LLM integrado nesta etapa;
- suporte para publicação em endpoint único, com FastAPI servindo o build do frontend;
- versão paralela em Streamlit para entrega online simplificada.

## O que não existe na entrega intermediária publicada

- nenhuma chamada para OpenAI, Anthropic, Gemini, Ollama, LangChain ou outro provedor;
- nenhuma inferência real com modelo generativo;
- nenhuma autenticação;
- nenhum deploy com Docker.

## Versões disponíveis

O repositório possui duas formas de entrega da mesma proposta:

1. **Full stack FastAPI + React + SQLite**
   - versão principal e mais completa;
   - inclui API, frontend separado, testes e preparo para deploy público.

2. **Streamlit para entrega online simplificada**
   - versão paralela em `streamlit_app.py`;
   - usa `st.session_state` e dados mockados iniciais;
   - reduz o risco de deploy para um endpoint público único na primeira entrega.

## Por que Streamlit foi adicionado

A versão Streamlit foi criada para reduzir risco operacional na publicação online da primeira entrega. Em vez de depender da combinação entre build React, API FastAPI e configuração de deploy em produção, a banca pode acessar uma versão única e simples com:

- dashboard;
- cadastro de equipamentos;
- registro de ocorrências;
- diagnóstico simulado;
- histórico;
- relatório técnico;
- página de futura integração com IA.

Essa decisão atende ao objetivo de colocar a entrega em um endpoint público rapidamente, sem mudar o escopo funcional e sem integrar LLM real.

## Arquitetura

```text
frontend (React + Vite + TypeScript)
        |
        v
build estático do frontend
        |
        v
backend (FastAPI + SQLAlchemy)
        |
        v
SQLite local
```

### Estrutura do repositório

```text
diagnoflow-ai/
|- backend/
|  |- app/
|  |  |- main.py
|  |  |- database.py
|  |  |- models.py
|  |  |- schemas.py
|  |  |- seed.py
|  |  |- routes/
|  |  `- services/
|  `- tests/
|- frontend/
|  |- build em `dist/` (gerado, não versionado)
|  `- src/
|- docs/
|- prompts/
|- .streamlit/
|- requirements-streamlit.txt
|- streamlit_app.py
|- README.md
`- .gitignore
```

## Escolhas de design

- FastAPI foi escolhida para entregar API REST clara, documentação automática em `/docs` e validação simples com Pydantic.
- SQLite foi usado para reduzir complexidade de setup na avaliação intermediária.
- React com TypeScript foi adotado para permitir interface navegável, componentes reutilizáveis e tipagem explícita de `Equipment`, `Incident` e `Diagnostic`.
- O diagnóstico mockado foi isolado em `backend/app/services/mock_diagnostic_service.py`, facilitando a troca futura por uma integração real com LLM.
- Em produção, o FastAPI serve o build do frontend e faz fallback de rotas da SPA para `index.html`, preservando `/docs` e as rotas da API.
- A versão Streamlit foi mantida em um único arquivo `streamlit_app.py` de forma intencional, porque esta fase exige um protótipo simples, demonstrável e rápido de publicar. A modularização de estado, regras e views fica planejada para a fase 2.

## Tecnologias e IA utilizadas na entrega intermediária

- FastAPI: backend e API REST com documentação automática.
- React + Vite + TypeScript: interface navegável, componentização e tipagem explícita.
- SQLite: persistência local simples para a entrega intermediária.
- Streamlit: versão paralela para publicação pública simplificada.
- Codex: agente de codificação usado para acelerar implementação, revisão e documentação.

Importante:

- nenhum modelo de IA generativa foi integrado à aplicação nesta fase;
- não houve uso de OpenAI, Anthropic, Gemini, Ollama, LangChain ou outro provedor dentro do produto entregue;
- o uso de IA nesta etapa ocorreu apenas como suporte ao desenvolvimento, por meio do agente de codificação.

## Como a IA será integrada futuramente

Na segunda fase, a regra determinística atual poderá ser substituída por um fluxo de orquestração com:

1. coleta da ocorrência e do contexto do equipamento;
2. consulta a tools internas;
3. chamada a um LLM com prompt técnico controlado;
4. validação de saída estruturada;
5. revisão humana antes de decisões críticas.

Direção escolhida para iniciar a fase 2:

- FastAPI + LangGraph + tools locais + output estruturado + validação humana.

Estratégia recomendada:

- desenvolvimento com fallback local;
- demonstração gratuita com Ollama, se a máquina suportar;
- uso de API paga apenas se for necessário aumentar previsibilidade da demo final.

As tools planejadas estão documentadas em [docs/future-llm-integration.md](docs/future-llm-integration.md) e incluem:

- consultar histórico da máquina;
- consultar base de falhas conhecidas;
- calcular criticidade;
- gerar checklist técnico;
- gerar relatório estruturado.

Para a consolidação técnica da fase 2, consulte também:

- [docs/final-delivery-technical-brief.md](docs/final-delivery-technical-brief.md)

## Estado atual da entrega final na branch `fase-2`

Na branch `fase-2`, o projeto já demonstra os principais elementos esperados para a entrega final:

- runtime do agente exposto em `GET /agent/runtime`, já validado com `runtime_label=langgraph`;
- tools locais explícitas e documentadas;
- output estruturado validado;
- guardrails de saída e de revisão humana;
- smoke test real com `Ollama + qwen3:0.6b`;
- trilha de auditoria com revisão humana persistida no backend;
- frontend refletindo runtime, evidências, lacunas e histórico de revisão.

## Funcionalidades implementadas

- dashboard com totais operacionais e últimas ocorrências;
- cadastro de equipamentos com criticidade e status;
- registro de nova ocorrência com múltiplos sintomas;
- diagnóstico simulado com causa provável, confiança, prioridade, risco, ações, peças e observações;
- histórico com filtros por equipamento, criticidade e status;
- relatório técnico textual com botão de cópia na versão React e download de arquivo `.txt` na versão Streamlit;
- página explicando a futura integração com IA.

## Como rodar o backend em desenvolvimento

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger/OpenAPI:

- `http://127.0.0.1:8000/docs`

## Como rodar o frontend em desenvolvimento

```powershell
cd frontend
npm install
npm run dev
```

## Como rodar a versão Streamlit

```powershell
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

Essa versão não substitui a full stack. Ela existe apenas como alternativa de publicação online simplificada para a avaliação intermediária.

## Publicação recomendada para a entrega intermediária

Para reduzir risco na avaliação, a recomendação é publicar a versão `Streamlit` como endpoint oficial da primeira entrega.

### Opção recomendada: Streamlit Community Cloud

1. Garanta que o repositório no GitHub esteja atualizado.
2. Acesse o painel do Streamlit Community Cloud.
3. Escolha `New app`.
4. Selecione este repositório.
5. Configure:
   - `Main file path`: `streamlit_app.py`
   - `Python requirements`: `requirements-streamlit.txt`
6. Publique a aplicação.
7. Abra o link gerado em janela anônima.
8. Valide rapidamente as telas:
   - Dashboard
   - Equipamentos
   - Nova Ocorrência
   - Histórico
   - Relatório Técnico
   - Futura Integração com IA

### O que conferir antes de enviar o link

- a aplicação abre sem erro;
- o aviso de diagnóstico simulado aparece com clareza;
- o cadastro de equipamento funciona;
- o registro de ocorrência gera diagnóstico simulado;
- o histórico mostra os registros;
- o relatório técnico está acessível;
- o visual está legível em todas as telas.

## Como rodar a versão full stack localmente

1. Gere o build do frontend:

```powershell
cd frontend
npm install
npm run build
```

2. Inicie o backend servindo a SPA:

```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. Acesse:

- `http://127.0.0.1:8000/` para a interface React;
- `http://127.0.0.1:8000/docs` para a documentação da API;
- `http://127.0.0.1:8000/dashboard` para uma rota principal da API.

## Como ativar a arquitetura da fase 2 localmente

Na branch `fase-2`, o backend já possui a estrutura do orquestrador com:

- tools locais;
- output estruturado;
- guardrails;
- fallback determinístico;
- adapters opcionais para Ollama e OpenAI.

Use o arquivo `backend/.env.example` como referência para as variáveis de ambiente.

Modo padrão de desenvolvimento:

```powershell
$env:DIAGNOFLOW_LLM_PROVIDER="not-configured"
$env:DIAGNOFLOW_LLM_MODEL="diagnoflow-mock-agent"
```

Modo de demonstração local gratuita com Ollama:

```powershell
$env:DIAGNOFLOW_LLM_PROVIDER="ollama"
$env:DIAGNOFLOW_LLM_MODEL="qwen3:0.6b"
$env:DIAGNOFLOW_OLLAMA_BASE_URL="http://127.0.0.1:11434"
```

Smoke test já validado nesta branch:

- `Ollama` instalado localmente;
- servidor respondendo em `http://127.0.0.1:11434`;
- modelo `qwen3:0.6b` baixado com sucesso;
- criação de ocorrência funcionando com `runtime_provider=ollama`.

Modo opcional com API:

```powershell
$env:DIAGNOFLOW_LLM_PROVIDER="openai"
$env:DIAGNOFLOW_LLM_MODEL="gpt-5-mini"
```

Se nenhuma integração real estiver configurada, o sistema continua operando com fallback local estruturado, sem quebrar o fluxo da aplicação.

## Endpoints principais

- `GET /`
- `GET /dashboard`
- `GET /equipment`
- `POST /equipment`
- `GET /incidents`
- `POST /incidents`
- `GET /diagnostics/{incident_id}`
- `GET /docs`

## Dados iniciais

Ao iniciar a API, o banco local é criado automaticamente e um seed adiciona:

- equipamentos de exemplo;
- uma ocorrência inicial;
- um diagnóstico simulado já associado ao histórico.

## Comandos de validação

Backend:

```powershell
cd backend
.\.venv\Scripts\python -m pytest
```

Frontend:

```powershell
cd frontend
npm run build
```

Streamlit:

```powershell
python -m py_compile streamlit_app.py
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

Repositório:

```powershell
git status --short
```

## Evidência de uso do Codex

O uso do agente de codificação está documentado em [docs/agent-prompts.md](docs/agent-prompts.md), incluindo:

- prompt inicial da tarefa;
- iterações de implementação;
- erros encontrados na validação;
- correções aplicadas;
- comandos executados;
- decisões tomadas para estabilizar a entrega.

## O que funcionou bem com o Codex

- geração rápida da estrutura completa de backend, frontend e documentação;
- criação coerente de contratos entre API e interface;
- organização do repositório em commits separados por backend, frontend e documentação;
- execução iterativa de validação local para encontrar e corrigir falhas antes da revisão final.

## O que não funcionou de primeira e precisou de correção

- `npm install` falhou inicialmente por restrição de rede/cache do ambiente;
- a criação da `venv` falhou no `ensurepip` e precisou ser refeita com permissão ampliada;
- o build do frontend falhou por ausência da tipagem de `import.meta.env`;
- os testes do backend falharam inicialmente porque o `TestClient` não estava disparando o `lifespan` da aplicação fora de contexto;
- a adaptação para SPA exigiu revisar a rota `/` e incluir fallback para rotas internas do React.

## Limitações da primeira fase

- diagnóstico inteiramente mockado por regras simples;
- sem consumo de APIs externas;
- sem autenticação e sem controle de perfis;
- sem auditoria avançada das ações do usuário;
- sem observabilidade de produção;
- sem integração real com modelo generativo nesta etapa.

## Estado atual para a avaliação intermediária

- aplicação funcional localmente;
- backend validado com `pytest`;
- frontend validado com `npm run build`;
- versão Streamlit criada para publicação online simplificada;
- repositório organizado e documentado;
- mensagem explícita de que não há LLM nesta fase;
- endpoint único pronto para demonstração pública.

## Documentação complementar

- [docs/agent-prompts.md](docs/agent-prompts.md)
- [docs/design-decisions.md](docs/design-decisions.md)
- [docs/final-delivery-implementation-plan.md](docs/final-delivery-implementation-plan.md)
- [docs/final-delivery-technical-brief.md](docs/final-delivery-technical-brief.md)
- [docs/future-llm-integration.md](docs/future-llm-integration.md)
- [prompts/future-system-prompt.txt](prompts/future-system-prompt.txt)
