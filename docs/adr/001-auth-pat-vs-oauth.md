# ADR-001: Autenticação via PAT em vez de OAuth (nesta fase)

## Status
Proposto — validar após Teste 1 do `testing-checklist.md`.

## Contexto
O servidor precisa autenticar contra a REST API do Databricks para chamar Unity Catalog e SQL Warehouse. Databricks suporta tanto Personal Access Tokens (PAT) quanto OAuth (recomendado oficialmente para produção).

## Decisão
Usar PAT escopado (`unity-catalog`, `sql`) nesta fase de MVP local.

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| PAT escopado | Simples de gerar e usar, suficiente para uso local single-user | Não é a recomendação oficial de produção; requer rotação manual |
| OAuth (service principal) | Recomendado pela Databricks para produção, mais seguro | Setup mais complexo; houve relato de falha de OAuth especificamente na Free Edition em contexto de CLI/DABs — risco a validar antes de adotar |

## Consequências
- Documentar claramente que esta escolha é adequada para o escopo atual (PoC local, single-user) e não deve ser replicada sem revisão em um cenário multi-usuário ou produção.
- Reavaliar para OAuth se o projeto evoluir para transporte HTTP remoto ou uso por múltiplos usuários.

## Nota de verificação
Se o Teste 1 do checklist falhar com PAT, este ADR precisa ser revisitado antes de prosseguir — não assumir que OAuth resolveria sem testar, dado o relato de instabilidade de OAuth já observado na Free Edition em outro contexto (Databricks Asset Bundles via CLI).
