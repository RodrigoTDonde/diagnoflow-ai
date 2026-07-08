# Streamlit Delivery

Esta versão paralela em Streamlit foi criada para reduzir o risco operacional da primeira entrega e facilitar a publicação em um endpoint público único.

## Motivação

- evitar dependência de publicação separada para frontend e backend;
- manter a narrativa do projeto DiagnoFlow AI;
- reaproveitar regras mockadas de diagnóstico já definidas;
- simplificar a demonstração online para a disciplina.

## O que foi reaproveitado

- tema e objetivo do produto;
- entidades principais: equipamentos, ocorrências e diagnósticos;
- sintomas técnicos;
- regras de diagnóstico simulado;
- página de futura integração com IA;
- aviso explícito de que não há LLM integrado nesta fase.

## Como rodar

```powershell
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

## Como publicar rapidamente

### Streamlit Community Cloud

1. Enviar o estado final do projeto para o GitHub.
2. Criar uma nova app no Streamlit Community Cloud.
3. Apontar para este repositório.
4. Definir `streamlit_app.py` como arquivo principal.
5. Usar `requirements-streamlit.txt` para as dependências.
6. Publicar e validar o link em janela anônima.

## Checklist de validação do endpoint

- abrir a aplicação sem erro;
- navegar por todas as telas;
- cadastrar um equipamento;
- registrar uma ocorrência;
- confirmar o diagnóstico simulado;
- abrir histórico e relatório técnico;
- confirmar o aviso explícito de que não há LLM nesta fase.

## Limites desta versão

- dados ficam em `st.session_state`, sem persistência de banco;
- foco em simplicidade para avaliação online;
- nenhuma integração real com OpenAI, Anthropic, Gemini, Ollama, LangChain ou qualquer LLM.
