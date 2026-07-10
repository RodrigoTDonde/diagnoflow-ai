# Agent Prompts

Este documento registra evidências do uso do agente de codificação na construção e revisão da entrega intermediária do projeto DiagnoFlow AI.

## Prompt inicial usado

O agente recebeu como tarefa principal a criação completa da aplicação dentro do repositório local, com os seguintes requisitos centrais:

- backend em Python com FastAPI;
- frontend em React com Vite e TypeScript;
- banco local SQLite;
- múltiplas telas navegáveis;
- histórico, formulários e visualizações;
- endpoint funcional;
- documentação e README detalhados;
- nenhum LLM real nesta primeira fase;
- diagnósticos exclusivamente simulados/mockados.

## Estratégia adotada pelo agente

O trabalho foi dividido em etapas:

1. leitura do enunciado anexado;
2. criação da estrutura base do backend;
3. criação da interface React com navegação;
4. adição de documentação da futura integração com IA;
5. validações locais;
6. revisão final voltada para os critérios da disciplina.

## Iterações realizadas

### Iteração 1 - Estrutura inicial

- criação de `backend/app`, `backend/tests`, `frontend/src`, `docs` e `prompts`;
- implementação da API FastAPI com rotas de equipamentos, ocorrências e diagnósticos;
- criação do serviço `mock_diagnostic_service.py`;
- criação do frontend com dashboard, equipamentos, nova ocorrência, histórico e futura IA.

### Iteração 2 - Validação técnica

- compilação do backend com `python -m compileall`;
- instalação de dependências do frontend;
- instalação de dependências do backend;
- execução de `pytest`;
- execução de `npm run build`;
- smoke tests de endpoints com `TestClient`.

### Iteração 3 - Correção após validação

- adição de `frontend/src/vite-env.d.ts` para corrigir `import.meta.env`;
- ajuste dos testes do backend para usar `with TestClient(app)`;
- troca de `datetime.utcnow()` por função auxiliar com `timezone.utc`;
- limpeza de artefatos de build e atualização do `.gitignore`.

### Iteração 4 - Revisão para a banca

- ampliação do `README.md`;
- reforço das evidências de uso do agente;
- revisão visual da interface com banners de mock;
- checagem explícita de ausência de integração real com LLM.

### Iteração 5 - Versão Streamlit paralela

- decisão de criar uma segunda interface sem substituir FastAPI + React;
- reaproveitamento do conceito de equipamentos, ocorrências, diagnósticos e relatório técnico;
- implementação de `streamlit_app.py` com `st.session_state` e dados mockados iniciais;
- manutenção explícita da restrição: nenhum LLM real integrado nesta fase;
- preparação de documentação específica para entrega online simplificada.

## Prompt atual para esta etapa

O agente recebeu uma nova orientação para criar uma versão Streamlit paralela do projeto, com as seguintes exigências:

- não apagar, renomear ou substituir a versão full stack existente;
- usar apenas diagnóstico simulado/mockado;
- criar `streamlit_app.py`;
- criar `requirements-streamlit.txt`;
- criar documentação de apoio para a entrega online;
- atualizar `README.md` e este arquivo com a justificativa da nova versão;
- validar a app Streamlit e garantir ausência de integração com LLM real.

## Erros encontrados

- `npm install` falhou inicialmente por indisponibilidade de cache/rede no ambiente restrito.
- `python -m venv .venv` falhou inicialmente durante `ensurepip`.
- `npm run build` falhou com o erro `Property 'env' does not exist on type 'ImportMeta'`.
- `pytest` falhou porque o banco não era inicializado quando o `lifespan` da app não era acionado no teste.
- O build do frontend gerou arquivos derivados que não deveriam permanecer versionados.

## Nova decisão de arquitetura

Foi adicionada uma versão Streamlit paralela para reduzir o risco de deploy da primeira entrega. A decisão não substitui a arquitetura principal; ela cria uma trilha de entrega online mais simples, adequada ao prazo e ao critério de endpoint público.

## Correção feita

- repetição de comandos com permissão ampliada quando o bloqueio era do ambiente;
- criação do arquivo `frontend/src/vite-env.d.ts`;
- atualização dos testes para contexto correto do `TestClient`;
- limpeza de artefatos gerados e reforço do `.gitignore`;
- reforço textual da interface para deixar claro que o diagnóstico é simulado.

## Comandos executados

### Inspeção e estrutura

```powershell
Get-Content -Raw <arquivo>
Get-ChildItem -Force
rg --files
git status --short
```

### Backend

```powershell
python -m compileall backend\app backend\tests
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -c "..."
```

### Frontend

```powershell
npm install
npm run build
```

### Streamlit

```powershell
python -m py_compile streamlit_app.py
pip install -r requirements-streamlit.txt
git grep -n "<unicode-escapes>" -- README.md docs prompts streamlit_app.py frontend/src backend/app
```

### Git

```powershell
git add backend .gitignore
git commit -m "feat(backend): implementa api e diagnostico mockado"
git add frontend
git commit -m "feat(frontend): cria interface multipagina do diagnoflow"
git add README.md docs prompts .gitignore
git commit -m "docs: documenta arquitetura e limpa artefatos de build"
```

## Resultado do uso do agente

O agente foi útil para:

- acelerar a construção do projeto end-to-end;
- manter consistência entre frontend e backend;
- criar uma segunda interface mais simples sem desmontar a versão principal;
- documentar a futura integração com IA sem ferir a restrição de não usar LLM nesta fase;
- identificar e corrigir problemas de validação antes da entrega.

## Limite observado

Parte dos erros iniciais não estava no código do projeto, mas no ambiente de execução restrito. Isso exigiu repetição de alguns comandos com permissões ampliadas e revisão manual dos resultados antes de seguir.

## Extensão para a fase 2

Na evolução da entrega final, o agente passou a receber orientações adicionais para:

- preparar uma arquitetura real com `FastAPI + LangGraph + tools locais + output estruturado + guardrails`;
- expor configuração do runtime do agente;
- integrar provider local com `Ollama`;
- validar smoke test real com modelo local;
- adicionar trilha de auditoria de validação humana.

### Iterações relevantes da fase 2

- criação da pasta `backend/app/llm_orchestrator` com grafo, prompt, tools, guardrails e provider;
- ampliação do frontend para expor runtime, evidências, lacunas e revisão humana;
- criação do endpoint `GET /agent/runtime`;
- instalação local do `Ollama` e teste real com `qwen3:0.6b`;
- criação da tabela e do fluxo de `human_validation_reviews`.

### Evidências adicionais de uso do agente

- modelagem incremental com commits pequenos na branch `fase-2`;
- validação repetida com `pytest` e `npm run build`;
- ajustes de documentação após teste real com `Ollama`;
- inclusão do fluxo human-in-the-loop com auditoria persistida.

### Comandos relevantes da fase 2

```powershell
.\.venv\Scripts\python -m pytest
npm run build
winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements
Start-Process -FilePath "C:\Users\rodrigo.donde\AppData\Local\Programs\Ollama\ollama.exe" -ArgumentList "serve" -WindowStyle Hidden
& "C:\Users\rodrigo.donde\AppData\Local\Programs\Ollama\ollama.exe" pull qwen3:0.6b
.\.venv\Scripts\python -c "..."
git log --oneline
```
