# Arquitetura — MCP Databricks Server

## 1. Visão geral

```
┌─────────────────┐         stdio (JSON-RPC 2.0)          ┌────────────────────────┐
│  Claude Desktop  │ ◄────────────────────────────────────► │   MCP Server (Python)  │
│  (Host + Client) │   initialize / tools/list / tools/call  │                        │
└─────────────────┘                                         │  Tool Handlers          │
                                                              │  - list_tables          │
                                                              │  - describe_table       │
                                                              │  - run_query_readonly   │
                                                              │           │             │
                                                              │  Guard (bloqueio DDL/DML)│
                                                              │           │             │
                                                              │  Databricks Client (SDK) │
                                                              └───────────┼─────────────┘
                                                                          │ HTTPS REST
                                                              ┌───────────▼─────────────┐
                                                              │  Databricks Workspace    │
                                                              │  (Unity Catalog + SQL    │
                                                              │   Warehouse)             │
                                                              └──────────────────────────┘
```

## 2. Fluxo de mensagens do protocolo MCP

> Seção a detalhar após a Semana 1 (validação de handshake). Deve cobrir, no mínimo:
> - Mensagem `initialize` — o que host e server trocam no aperto de mão inicial
> - `tools/list` — como o server descreve suas capacidades (schema JSON de cada tool)
> - `tools/call` — o ciclo de chamada e retorno de uma tool específica
> - Códigos de erro JSON-RPC utilizados e por quê
> - Por que stdio foi escolhido nesta fase (vs. HTTP+SSE) e o trade-off disso

## 3. Componentes e justificativa

| Componente | Escolha | Por quê |
|---|---|---|
| Protocolo | MCP Python SDK oficial | Padrão mantido pela Anthropic |
| Integração Databricks | `databricks-sdk` | SDK oficial, tipado |
| Transporte | stdio | Suficiente para uso local via Claude Desktop nesta fase |
| Autenticação | PAT escopado | Ver ADR-001 |
| Validação de query | Guard próprio (bloqueio DDL/DML) | Segurança desde o início, não como afterthought |

## 4. Limitações conhecidas

> Preencher conforme os testes do `testing-checklist.md` revelarem limitações reais da Free Edition (não suposições).

## 5. Evolução futura

- Transporte HTTP+SSE para uso remoto (fora do escopo do MVP)
- Reuso deste server como camada de acesso a dados por outros agentes (ex: diagnóstico de falhas de pipeline)
