"""
MCP Databricks Server — entrypoint.

Esqueleto minimo do servidor MCP, sem tools reais ainda.
Objetivo: validar que o handshake do protocolo (initialize -> tools/list)
funciona corretamente com um cliente MCP (Claude Code), antes de
implementar qualquer logica de negocio.

Proxima etapa: registrar as tools reais importando de src/tools/.
"""

import asyncio
import logging

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Logging vai para stderr (nunca para stdout) — stdout e reservado
# exclusivamente para as mensagens do protocolo MCP.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-databricks-server")

# Cria a instancia do servidor MCP. O nome "databricks-mcp-server"
# e o identificador que aparece para o cliente (Claude Code) durante
# o handshake inicial.
server = Server("databricks-mcp-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Responde a mensagem 'tools/list' do protocolo.

    Retorna uma lista vazia de proposito — ainda nao implementamos
    nenhuma tool real. O objetivo aqui e confirmar que o servidor
    responde corretamente a essa etapa do handshake.
    """
    logger.info("Recebida chamada tools/list — retornando lista vazia (esqueleto)")
    return []


async def main():
    """
    Inicializa o transporte stdio e coloca o servidor para rodar,
    aguardando mensagens do cliente MCP (Claude Code) via stdin/stdout.
    """
    logger.info("Iniciando MCP Databricks Server (modo esqueleto, sem tools)")

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