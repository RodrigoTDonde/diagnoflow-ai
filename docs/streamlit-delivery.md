# Streamlit Delivery

Esta versao paralela em Streamlit foi criada para reduzir o risco de deploy da primeira entrega e facilitar a publicacao em um endpoint publico unico.

## Motivacao

- evitar dependencia de deploy separado para frontend e backend;
- manter a narrativa do projeto DiagnoFlow AI;
- reaproveitar regras mockadas de diagnostico ja definidas;
- simplificar a demonstracao online para a disciplina.

## O que foi reaproveitado

- tema e objetivo do produto;
- entidades principais: equipamentos, ocorrencias e diagnosticos;
- sintomas tecnicos;
- regras de diagnostico simulado;
- pagina de futura integracao com IA;
- aviso explicito de que nao ha LLM integrado nesta fase.

## Como rodar

```powershell
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

## Como publicar rapidamente

### Streamlit Community Cloud

1. Enviar o estado final do projeto para o GitHub.
2. Criar uma nova app no Streamlit Community Cloud.
3. Apontar para este repositorio.
4. Definir `streamlit_app.py` como arquivo principal.
5. Usar `requirements-streamlit.txt` para as dependencias.
6. Publicar e validar o link em janela anonima.

## Checklist de validacao do endpoint

- abrir a aplicacao sem erro;
- navegar por todas as telas;
- cadastrar um equipamento;
- registrar uma ocorrencia;
- confirmar o diagnostico simulado;
- abrir historico e relatorio tecnico;
- confirmar o aviso explicito de que nao ha LLM nesta fase.

## Limites desta versao

- dados ficam em `st.session_state`, sem persistencia de banco;
- foco em simplicidade para avaliacao online;
- nenhuma integracao real com OpenAI, Anthropic, Gemini, Ollama, LangChain ou qualquer LLM.
