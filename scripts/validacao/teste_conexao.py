from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

print("Conectando ao Databricks...")
for catalog in w.catalogs.list():
    print(f"Catálogo encontrado: {catalog.name}")
