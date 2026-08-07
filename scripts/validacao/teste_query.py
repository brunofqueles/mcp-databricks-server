from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

warehouse_id = "34b1a397b50ec474"

print("Executando query de teste...")
result = w.statement_execution.execute_statement(
    warehouse_id=warehouse_id,
    statement="SELECT 1 AS teste"
)
print(f"Status: {result.status.state}")
print(f"Resultado: {result.result.data_array}")