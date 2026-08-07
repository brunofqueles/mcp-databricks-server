# MCP Databricks Server

Servidor MCP (Model Context Protocol) construído do zero para expor operações do Unity Catalog do Databricks — listagem de tabelas, descrição de schema e execução de queries somente-leitura — a qualquer cliente MCP (Claude Desktop, Claude Code).

## O que é este projeto

Prova de conceito técnica com foco em profundidade de protocolo: o objetivo não é apenas "usar" o MCP SDK, mas demonstrar entendimento do ciclo de mensagens JSON-RPC 2.0 por trás dele (`initialize` → `tools/list` → `tools/call`), aplicado a um caso de uso real de Engenharia de Dados — trazer acesso a metadados de catálogo para dentro do fluxo de trabalho de IA, sem sair do editor/terminal.

## Status

🚧 Em desenvolvimento — fase de validação de ambiente.

## Requisitos funcionais

| ID | Descrição |
|---|---|
| RF1 | Listar tabelas de um catálogo/schema do Unity Catalog |
| RF2 | Descrever estrutura de uma tabela (colunas, tipos, comentários) |
| RF3 | Executar query SQL somente-leitura e retornar resultado formatado |
| RF4 | Retornar erro compreensível em caso de falha |

## Requisitos não funcionais

| ID | Descrição |
|---|---|
| RNF1 | Autenticação via PAT com escopo mínimo (`unity-catalog`, `sql`) |
| RNF2 | Bloqueio ativo de comandos DDL/DML na execução de query |
| RNF3 | Logging de cada chamada de tool |
| RNF4 | Transporte via stdio (uso local) |
| RNF5 | Documentação do fluxo de protocolo |

## Arquitetura

Ver [docs/architecture.md](docs/architecture.md) para o diagrama completo e o detalhamento do fluxo de mensagens do protocolo MCP.

## Decisões técnicas (ADRs)

| ADR | Tema | Status |
|---|---|---|
| [001](docs/adr/001-auth-pat-vs-oauth.md) | Autenticação: PAT vs OAuth | Proposto |

## Stack

- Python 3.11+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (oficial)
- `databricks-sdk`
- `pytest`

## Setup local

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # preencher DATABRICKS_HOST e DATABRICKS_TOKEN
```

## Como testar a conexão antes de rodar o server

Ver [docs/testing-checklist.md](docs/testing-checklist.md) — checklist de validação de ambiente (PAT, SDK, SQL Warehouse) que deve passar antes de qualquer lógica de tool ser implementada.

## Como rodar

```bash
python src/server.py
```

Registrar no `claude_desktop_config.json` (ver `claude_desktop_config.example.json` neste repositório).

## Licença

MIT
