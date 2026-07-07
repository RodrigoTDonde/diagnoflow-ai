# Checklist de Fechamento da Entrega Intermediária

Este documento transforma os critérios da primeira avaliação em um plano objetivo de execução para o projeto DiagnoFlow AI.

## Status geral

- `Pronto`: item validado tecnicamente ou documentado com clareza.
- `Em andamento`: item com base pronta, mas ainda exige confirmação final.
- `Pendente`: item que ainda depende de ação antes da entrega.

## 1. Endpoint público

- `Pendente` Definir o endpoint oficial da entrega.
- `Recomendado` Usar a versão Streamlit como endpoint público principal.
- `Pronto` Instruções de publicação rápida documentadas em `README.md` e `docs/streamlit-delivery.md`.
- `Pendente` Publicar o link e validar abertura em janela anônima.
- `Pendente` Testar acesso em outra rede ou dispositivo.

## 2. Fluxo funcional da aplicação

- `Pronto` Dashboard implementado.
- `Pronto` Equipamentos implementado com cadastro.
- `Pronto` Nova ocorrência implementada com sintomas e diagnóstico simulado.
- `Pronto` Histórico implementado.
- `Pronto` Relatório técnico implementado.
- `Pronto` Página de futura integração com IA implementada.
- `Em andamento` Validação manual completa do fluxo na versão que será publicada.

## 3. Validação visual

- `Em andamento` Melhorias de contraste e tema da versão Streamlit aplicadas.
- `Pendente` Confirmar visual final em todas as telas no navegador.
- `Pendente` Confirmar leitura adequada em largura menor de tela.
- `Pronto` Aviso explícito de diagnóstico simulado presente na interface.

## 4. Restrições da primeira fase

- `Pronto` Nenhuma integração real com OpenAI, Anthropic, Gemini, Ollama ou LangChain em código ativo.
- `Pronto` Diagnóstico mantido como mockado ou simulado.
- `Pronto` Documentação deixa claro que não há LLM nesta fase.

## 5. Repositório e organização

- `Pronto` Estrutura do repositório organizada.
- `Pronto` README presente.
- `Pronto` Documentação de prompts do agente presente.
- `Pronto` Documentação de decisões de design presente.
- `Pronto` Documentação da futura integração com IA presente.
- `Pronto` Rascunho do futuro system prompt presente.
- `Pronto` Arquivo de suporte para deploy presente.
- `Em andamento` Fechar com `git status` limpo antes da submissão.

## 6. README

- `Pronto` Descrição do problema e da solução.
- `Pronto` Explicação da futura integração com IA.
- `Pronto` Escolhas de design e arquitetura.
- `Pronto` Instruções para rodar backend, frontend e Streamlit.
- `Pronto` Comandos de validação.
- `Pronto` Relato do que funcionou com o agente.
- `Pronto` Relato do que não funcionou e exigiu correção.
- `Pronto` Limitações da primeira fase.

## 7. Evidência de uso do agente

- `Pronto` Prompt inicial documentado.
- `Pronto` Iterações documentadas.
- `Pronto` Erros encontrados documentados.
- `Pronto` Correções feitas documentadas.
- `Pronto` Comandos executados documentados.
- `Pronto` Decisão de criar versão Streamlit documentada.

## 8. Validações técnicas

- `Pronto` `python -m py_compile streamlit_app.py`
- `Pronto` `cd backend && .\\.venv\\Scripts\\python -m pytest`
- `Pronto` `cd frontend && npm run build`
- `Pronto` `git grep -n "\\u00" -- README.md docs prompts streamlit_app.py frontend/src backend/app`
- `Em andamento` Rodar `git status --short` novamente após o fechamento final.

## 9. Fechamento para entrega

- `Pendente` Escolher e publicar o endpoint oficial.
- `Pendente` Fazer a rodada final de validação manual como avaliador.
- `Pendente` Revisar se os links finais do GitHub e do endpoint estão prontos para envio.
- `Pendente` Criar o commit final da entrega quando tudo estiver estabilizado.

## Próximas ações prioritárias

1. Publicar a versão Streamlit em um endpoint público.
2. Validar manualmente todas as telas da versão publicada.
3. Revisar o README apenas se a publicação exigir ajuste de link ou instruções.
4. Criar o commit final com o tema do Streamlit estabilizado.
5. Confirmar `git status` limpo e preparar os links para submissão.

## Roteiro de validação em 1 minuto

1. Abrir o endpoint em janela anônima.
2. Confirmar que a tela inicial carrega sem erro.
3. Navegar por Dashboard, Equipamentos e Nova Ocorrência.
4. Registrar uma ocorrência de teste e confirmar o diagnóstico simulado.
5. Abrir Histórico e Relatório Técnico.
6. Confirmar que o aviso de que não há LLM nesta fase está visível.
