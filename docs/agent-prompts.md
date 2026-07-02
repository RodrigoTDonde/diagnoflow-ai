# Agent Prompts

Este documento registra evidencias do uso do agente de codificacao na construcao e revisao da entrega intermediaria do projeto DiagnoFlow AI.

## Prompt inicial usado

O agente recebeu como tarefa principal a criacao completa da aplicacao dentro do repositorio local, com os seguintes requisitos centrais:

- backend em Python com FastAPI;
- frontend em React com Vite e TypeScript;
- banco local SQLite;
- multiplas telas navegaveis;
- historico, formularios e visualizacoes;
- endpoint funcional;
- documentacao e README detalhados;
- nenhum LLM real nesta primeira fase;
- diagnosticos exclusivamente simulados/mockados.

## Estrategia adotada pelo agente

O trabalho foi dividido em etapas:

1. leitura do enunciado anexado;
2. criacao da estrutura base do backend;
3. criacao da interface React com navegacao;
4. adicao de documentacao da futura integracao com IA;
5. validacoes locais;
6. revisao final voltada para os criterios da disciplina.

## Iteracoes realizadas

### Iteracao 1 - Estrutura inicial

- criacao de `backend/app`, `backend/tests`, `frontend/src`, `docs` e `prompts`;
- implementacao da API FastAPI com rotas de equipamentos, ocorrencias e diagnosticos;
- criacao do servico `mock_diagnostic_service.py`;
- criacao do frontend com dashboard, equipamentos, nova ocorrencia, historico e futura IA.

### Iteracao 2 - Validacao tecnica

- compilacao do backend com `python -m compileall`;
- instalacao de dependencias do frontend;
- instalacao de dependencias do backend;
- execucao de `pytest`;
- execucao de `npm run build`;
- smoke tests de endpoints com `TestClient`.

### Iteracao 3 - Correcao apos validacao

- adicao de `frontend/src/vite-env.d.ts` para corrigir `import.meta.env`;
- ajuste dos testes do backend para usar `with TestClient(app)`;
- troca de `datetime.utcnow()` por funcao auxiliar com `timezone.utc`;
- limpeza de artefatos de build e atualizacao do `.gitignore`.

### Iteracao 4 - Revisao para a banca

- ampliacao do `README.md`;
- reforco das evidencias de uso do agente;
- revisao visual da interface com banners de mock;
- checagem explicita de ausencia de integracao real com LLM.

### Iteracao 5 - Versao Streamlit paralela

- decisao de criar uma segunda interface sem substituir FastAPI + React;
- reaproveitamento do conceito de equipamentos, ocorrencias, diagnosticos e relatorio tecnico;
- implementacao de `streamlit_app.py` com `st.session_state` e dados mockados iniciais;
- manutencao explicita da restricao: nenhum LLM real integrado nesta fase;
- preparacao de documentacao especifica para entrega online simplificada.

## Prompt atual para esta etapa

O agente recebeu uma nova orientacao para criar uma versao Streamlit paralela do projeto, com as seguintes exigencias:

- nao apagar, renomear ou substituir a versao full stack existente;
- usar apenas diagnostico simulado/mockado;
- criar `streamlit_app.py`;
- criar `requirements-streamlit.txt`;
- criar documentacao de apoio para a entrega online;
- atualizar `README.md` e este arquivo com a justificativa da nova versao;
- validar a app Streamlit e garantir ausencia de integracao com LLM real.

## Erros encontrados

- `npm install` falhou inicialmente por indisponibilidade de cache/rede no ambiente restrito.
- `python -m venv .venv` falhou inicialmente durante `ensurepip`.
- `npm run build` falhou com o erro `Property 'env' does not exist on type 'ImportMeta'`.
- `pytest` falhou porque o banco nao era inicializado quando o `lifespan` da app nao era acionado no teste.
- O build do frontend gerou arquivos derivados que nao deveriam permanecer versionados.

## Nova decisao de arquitetura

Foi adicionada uma versao Streamlit paralela para reduzir o risco de deploy da primeira entrega. A decisao nao substitui a arquitetura principal; ela cria uma trilha de entrega online mais simples, adequada ao prazo e ao criterio de endpoint publico.

## Correcao feita

- repeticao de comandos com permissao ampliada quando o bloqueio era do ambiente;
- criacao do arquivo `frontend/src/vite-env.d.ts`;
- atualizacao dos testes para contexto correto do `TestClient`;
- limpeza de artefatos gerados e reforco do `.gitignore`;
- reforco textual da interface para deixar claro que o diagnostico e simulado.

## Comandos executados

### Inspecao e estrutura

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

O agente foi util para:

- acelerar a construcao do projeto end-to-end;
- manter consistencia entre frontend e backend;
- criar uma segunda interface mais simples sem desmontar a versao principal;
- documentar a futura integracao com IA sem ferir a restricao de nao usar LLM nesta fase;
- identificar e corrigir problemas de validacao antes da entrega.

## Limite observado

Parte dos erros iniciais nao estava no codigo do projeto, mas no ambiente de execucao restrito. Isso exigiu repeticao de alguns comandos com permissoes ampliadas e revisao manual dos resultados antes de seguir.
