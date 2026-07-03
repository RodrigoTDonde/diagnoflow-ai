# Checklist de Fechamento da Entrega Intermediaria

Este documento transforma os criterios da primeira avaliacao em um plano objetivo de execucao para o projeto DiagnoFlow AI.

## Status Geral

- `Pronto`: item validado tecnicamente ou documentado com clareza.
- `Em andamento`: item com base pronta, mas ainda exige confirmacao final.
- `Pendente`: item que ainda depende de acao antes da entrega.

## 1. Endpoint Publico

- `Pendente` Definir o endpoint oficial da entrega.
- `Recomendado` Usar a versao Streamlit como endpoint publico principal.
- `Pronto` Instrucoes de publicacao rapida documentadas em `README.md` e `docs/streamlit-delivery.md`.
- `Pendente` Publicar o link e validar abertura em janela anonima.
- `Pendente` Testar acesso em outra rede ou dispositivo.

## 2. Fluxo Funcional da Aplicacao

- `Pronto` Dashboard implementado.
- `Pronto` Equipamentos implementado com cadastro.
- `Pronto` Nova ocorrencia implementada com sintomas e diagnostico simulado.
- `Pronto` Historico implementado.
- `Pronto` Relatorio tecnico implementado.
- `Pronto` Pagina de futura integracao com IA implementada.
- `Em andamento` Validacao manual completa do fluxo na versao que sera publicada.

## 3. Validacao Visual

- `Em andamento` Melhorias de contraste e tema da versao Streamlit aplicadas.
- `Pendente` Confirmar visual final em todas as telas no navegador.
- `Pendente` Confirmar leitura adequada em largura menor de tela.
- `Pronto` Aviso explicito de diagnostico simulado presente na interface.

## 4. Restricoes da Primeira Fase

- `Pronto` Nenhuma integracao real com OpenAI, Anthropic, Gemini, Ollama ou LangChain em codigo ativo.
- `Pronto` Diagnostico mantido como mockado ou simulado.
- `Pronto` Documentacao deixa claro que nao ha LLM nesta fase.

## 5. Repositorio e Organizacao

- `Pronto` Estrutura do repositorio organizada.
- `Pronto` README presente.
- `Pronto` Documentacao de prompts do agente presente.
- `Pronto` Documentacao de decisoes de design presente.
- `Pronto` Documentacao da futura integracao com IA presente.
- `Pronto` Rascunho do futuro system prompt presente.
- `Pronto` Arquivo de suporte para deploy presente.
- `Em andamento` Fechar com `git status` limpo antes da submissao.

## 6. README

- `Pronto` Descricao do problema e da solucao.
- `Pronto` Explicacao da futura integracao com IA.
- `Pronto` Escolhas de design e arquitetura.
- `Pronto` Instrucoes para rodar backend, frontend e Streamlit.
- `Pronto` Comandos de validacao.
- `Pronto` Relato do que funcionou com o agente.
- `Pronto` Relato do que nao funcionou e exigiu correcao.
- `Pronto` Limitacoes da primeira fase.

## 7. Evidencia de Uso do Agente

- `Pronto` Prompt inicial documentado.
- `Pronto` Iteracoes documentadas.
- `Pronto` Erros encontrados documentados.
- `Pronto` Correcoes feitas documentadas.
- `Pronto` Comandos executados documentados.
- `Pronto` Decisao de criar versao Streamlit documentada.

## 8. Validacoes Tecnicas

- `Pronto` `python -m py_compile streamlit_app.py`
- `Pronto` `cd backend && .\\.venv\\Scripts\\python -m pytest`
- `Pronto` `cd frontend && npm run build`
- `Pronto` `git grep -n "\\u00" -- README.md docs prompts streamlit_app.py frontend/src backend/app`
- `Em andamento` Rodar `git status --short` novamente apos o fechamento final.

## 9. Fechamento para Entrega

- `Pendente` Escolher e publicar o endpoint oficial.
- `Pendente` Fazer a rodada final de validacao manual como avaliador.
- `Pendente` Revisar se os links finais do GitHub e do endpoint estao prontos para envio.
- `Pendente` Criar o commit final da entrega quando tudo estiver estabilizado.

## Proximas Acoes Prioritarias

1. Publicar a versao Streamlit em um endpoint publico.
2. Validar manualmente todas as telas da versao publicada.
3. Revisar o README apenas se a publicacao exigir ajuste de link ou instrucoes.
4. Criar o commit final com o tema do Streamlit estabilizado.
5. Confirmar `git status` limpo e preparar os links para submissao.

## Roteiro de Validacao em 1 Minuto

1. Abrir o endpoint em janela anonima.
2. Confirmar que a tela inicial carrega sem erro.
3. Navegar por Dashboard, Equipamentos e Nova Ocorrencia.
4. Registrar uma ocorrencia de teste e confirmar o diagnostico simulado.
5. Abrir Historico e Relatorio Tecnico.
6. Confirmar que o aviso de que nao ha LLM nesta fase esta visivel.
