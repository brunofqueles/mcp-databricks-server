"""
Cliente Databricks — conexao centralizada e reutilizavel.

Todas as tools (list_tables, describe_table, run_query_readonly, etc.)
devem obter sua conexao atraves deste modulo, em vez de instanciar o
WorkspaceClient diretamente. Isso garante um unico ponto de mudanca
caso a estrategia de autenticacao evolua (ver docs/adr/001-auth-pat-vs-oauth.md).
"""

import logging
from pathlib import Path

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

# Carrega as variaveis do arquivo .env (na raiz do projeto) para o
# ambiente do processo, antes de qualquer tentativa de autenticacao.
# parents[2] sobe de src/client/ ate a raiz do projeto.
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

logger = logging.getLogger("mcp-databricks-server")

_client: WorkspaceClient | None = None


def get_workspace_client() -> WorkspaceClient:
    """
    Retorna uma instancia autenticada do WorkspaceClient.

    A autenticacao usa as variaveis DATABRICKS_HOST e DATABRICKS_TOKEN,
    carregadas do arquivo .env na raiz do projeto — nunca credenciais
    hardcoded no codigo.

    Reutiliza a mesma instancia entre chamadas (padrao singleton simples),
    evitando reconectar a cada chamada de tool.
    """
    global _client

    if _client is None:
        logger.info("Criando conexao com o Databricks workspace")
        _client = WorkspaceClient()

    return _client