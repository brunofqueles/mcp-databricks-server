"""
Tool: list_tables

Lista as tabelas de um catalogo/schema do Unity Catalog.
Corresponde ao requisito funcional RF1.
"""

import logging

import mcp.types as types

from client.databricks_client import get_workspace_client

logger = logging.getLogger("mcp-databricks-server")

# Schema da tool — descreve ao cliente MCP (Claude Code) o nome,
# a descricao e os parametros que essa tool aceita. E essa descricao
# que o modelo le para decidir quando chamar esta tool.
TOOL_DEFINITION = types.Tool(
    name="list_tables",
    description=(
        "Lista as tabelas existentes em um catalogo e schema especificos "
        "do Unity Catalog no Databricks."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "catalog": {
                "type": "string",
                "description": "Nome do catalogo do Unity Catalog (ex: 'b2b').",
            },
            "schema": {
                "type": "string",
                "description": "Nome do schema dentro do catalogo (ex: 'default').",
            },
        },
        "required": ["catalog", "schema"],
    },
)


async def handle_list_tables(arguments: dict) -> list[types.TextContent]:
    """
    Executa a tool list_tables: consulta o Unity Catalog e retorna
    o nome das tabelas encontradas, formatado como texto.

    RF4: erros sao capturados e retornados de forma compreensivel,
    nunca como excecao crua propagada ao cliente MCP.
    """
    catalog = arguments.get("catalog")
    schema = arguments.get("schema")

    logger.info(f"Executando list_tables — catalog={catalog}, schema={schema}")

    try:
        client = get_workspace_client()
        tables = list(client.tables.list(catalog_name=catalog, schema_name=schema))

        if not tables:
            return [
                types.TextContent(
                    type="text",
                    text=f"Nenhuma tabela encontrada em {catalog}.{schema}.",
                )
            ]

        nomes = "\n".join(f"- {t.name}" for t in tables)
        resultado = f"Tabelas em {catalog}.{schema}:\n{nomes}"

        return [types.TextContent(type="text", text=resultado)]

    except Exception as e:
        logger.error(f"Erro ao executar list_tables: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Erro ao listar tabelas de {catalog}.{schema}: {str(e)}",
            )
        ]