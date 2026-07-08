# Checklist de Fechamento da Entrega Intermediária

Este documento transforma os critérios da primeira avaliação em um plano objetivo de execução para o projeto DiagnoFlow AI.

## Status geral

- `Pronto`: item validado tecnicamente ou documentado com clareza.
- `Observação`: item que merece acompanhamento, mas não bloqueia a entrega.

## 1. Endpoint público

- `Pronto` Endpoint oficial definido na versão Streamlit publicada.
- `Pronto` Instruções de publicação rápida documentadas em `README.md` e `docs/streamlit-delivery.md`.
- `Pronto` Link público publicado e validado.
- `Observação` Revalidar abertura rapidamente antes da apresentação final.

## 2. Fluxo funcional da aplicação

- `Pronto` Dashboard implementado.
- `Pronto` Equipamentos implementado com cadastro.
- `Pronto` Nova ocorrência implementada com sintomas e diagnóstico simulado.
- `Pronto` Histórico implementado.
- `Pronto` Relatório técnico implementado.
- `Pronto` Página de futura integração com IA implementada.
- `Pronto` Fluxo principal validado na versão publicada.

## 3. Validação visual

- `Pronto` Melhorias de contraste e tema da versão Streamlit aplicadas.
- `Pronto` Visual final conferido nas telas principais.
- `Observação` Em telas muito estreitas, vale sempre uma checagem rápida antes da demonstração.
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
- `Pronto` Documentação de publicação em Streamlit presente.
- `Pronto` Repositório finalizado com `git status` limpo.

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
- `Pronto` `git status --short` conferido no fechamento final.

## 9. Fechamento para entrega

- `Pronto` Endpoint oficial definido e publicado.
- `Pronto` Rodada final de validação manual concluída.
- `Pronto` Links finais do GitHub e do endpoint preparados.
- `Pronto` Commits finais realizados com repositório limpo.

## Próximas ações prioritárias

1. Reabrir o link publicado pouco antes da apresentação para evitar tela de inatividade.
2. Validar rapidamente Dashboard, Equipamentos e Nova Ocorrência.
3. Confirmar que o aviso de diagnóstico simulado continua visível.
4. Ter em mãos o link do GitHub e o link da aplicação.
5. Não fazer novas mudanças estruturais sem necessidade.

## Roteiro de validação em 1 minuto

1. Abrir o endpoint em janela anônima.
2. Confirmar que a tela inicial carrega sem erro.
3. Navegar por Dashboard, Equipamentos e Nova Ocorrência.
4. Registrar uma ocorrência de teste e confirmar o diagnóstico simulado.
5. Abrir Histórico e Relatório Técnico.
6. Confirmar que o aviso de que não há LLM nesta fase está visível.
