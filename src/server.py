"""
MCP Databricks Server — entrypoint.

Servidor MCP que expõe operações sobre o Unity Catalog do Databricks.
Handshake validado; primeira tool real (list_tables) registrada.
"""

import asyncio
import logging

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from tools.list_tables import TOOL_DEFINITION as LIST_TABLES_DEFINITION
from tools.list_tables import handle_list_tables

# Logging vai para stderr (nunca para stdout) — stdout e reservado
# exclusivamente para as mensagens do protocolo MCP.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-databricks-server")

server = Server("databricks-mcp-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Responde a mensagem 'tools/list' do protocolo.

    Retorna a lista de tools disponiveis. Cada tool nova implementada
    deve ser adicionada aqui.
    """
    logger.info("Recebida chamada tools/list")
    return [LIST_TABLES_DEFINITION]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """
    Responde a mensagem 'tools/call' do protocolo.

    Roteia a chamada para o handler correto, de acordo com o nome
    da tool solicitada pelo cliente MCP.
    """
    logger.info(f"Recebida chamada tools/call — tool={name}, args={arguments}")

    if name == "list_tables":
        return await handle_list_tables(arguments)

    raise ValueError(f"Tool desconhecida: {name}")


async def main():
    """
    Inicializa o transporte stdio e coloca o servidor para rodar,
    aguardando mensagens do cliente MCP (Claude Code) via stdin/stdout.
    """
    logger.info("Iniciando MCP Databricks Server")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="databricks-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())