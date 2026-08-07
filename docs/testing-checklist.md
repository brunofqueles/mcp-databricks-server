# Checklist de validação de ambiente

Este checklist deve ser executado e marcado **antes** de qualquer lógica de tool ser implementada. O objetivo é eliminar risco técnico desconhecido cedo, não descobrir problemas de autenticação/permissão no meio da implementação de uma feature.

## Pré-requisito

- [ ] PAT gerado no Databricks (Settings → Developer → Access tokens), com escopo `unity-catalog` + `sql` se a opção de escopo estiver disponível na UI
- [ ] Variáveis de ambiente configuradas localmente (nunca commitadas — ver `.env.example`)

## Teste 1 — REST API crua responde

```bash
curl -X GET "$DATABRICKS_HOST/api/2.1/unity-catalog/catalogs" \
  -H "Authorization: Bearer $DATABRICKS_TOKEN"
```

- [ ] Retornou JSON com lista de catálogos (não 401/403)

**Se falhar:** problema de token/permissão. Resolver aqui antes de avançar — não adianta seguir para o SDK se a API crua já falha.

## Teste 2 — SDK Python autentica

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient(host=DATABRICKS_HOST, token=DATABRICKS_TOKEN)
for catalog in w.catalogs.list():
    print(catalog.name)
```

- [ ] Lista de catálogos impressa sem exceção

## Teste 3 — SQL Warehouse disponível

```python
warehouses = list(w.warehouses.list())
print(warehouses)
```

- [ ] Pelo menos 1 warehouse listado
- [ ] Warehouse está em estado `RUNNING` (ou foi iniciado manualmente na UI antes do teste)

## Teste 4 — Execução de query real

```python
result = w.statement_execution.execute_statement(
    warehouse_id="<ID_DO_WAREHOUSE>",
    statement="SELECT 1"
)
print(result)
```

- [ ] Retornou resultado sem erro — valida a peça que RF3 (`run_query_readonly`) vai usar

## Teste 5 — Handshake MCP básico (sem tools reais)

- [ ] Server MCP mínimo (`initialize` + `tools/list` vazio) registrado em `claude_desktop_config.json`
- [ ] Claude Desktop reiniciado e handshake confirmado nos logs locais do MCP (Claude Desktop expõe logs de conexão de servidores MCP — consultar documentação atual se o caminho do log mudou)

## Resultado

Só avançar para a Semana 2 do cronograma (implementação de `list_tables`) depois que **todos** os itens acima estiverem marcados. Qualquer teste que falhar deve virar uma nota em `docs/adr/` se a causa raiz for uma limitação de plataforma (ex: Free Edition), não só um bug pontual.
