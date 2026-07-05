# Design Decisions

## Arquitetura

- Backend em FastAPI com SQLAlchemy e SQLite para simplicidade local.
- Frontend em React + Vite + TypeScript para navegação fluida e tipagem explícita.
- Serviço de diagnóstico isolado em `mock_diagnostic_service.py` para facilitar substituição futura por LLM.
- Versão Streamlit mantida em `streamlit_app.py` como arquivo único nesta fase para reduzir complexidade, acelerar deploy e manter a revisão mais direta para a entrega intermediária.

## Produto

- Dashboard com indicadores rápidos e ocorrências recentes.
- Fluxo principal centrado em cadastrar ativos, abrir ocorrência e analisar histórico.
- Relatório textual copiado para a área de transferência na versão React e baixado em `.txt` na versão Streamlit.

## UX

- Interface com visual técnico e responsivo.
- Navegação lateral fixa em desktop e empilhada em mobile.
- Mensagem explícita informando ausência de IA real nesta fase.

## Evolução planejada

- Na segunda fase, a tendência é separar estado, regras mockadas e renderização da versão Streamlit em módulos menores, caso a integração com LLM e tools aumente a complexidade do fluxo.
