from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

print("Verificando SQL Warehouses...")
for warehouse in w.warehouses.list():
    print(f"Nome: {warehouse.name} | Estado: {warehouse.state} | ID: {warehouse.id}")