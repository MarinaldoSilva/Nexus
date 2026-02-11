import requests

# Debug: verificar opções disponíveis
print("Verificando métodos permitidos...")
r = requests.options("http://localhost:8000/api/files/folders/")
print(f"Status: {r.status_code}")
print(f"Allow header: {r.headers.get('Allow', 'N/A')}")
print(f"Content-Type: {r.headers.get('Content-Type', 'N/A')}")

# Debug: tentar GET
print("\nTestando GET...")
r2 = requests.get("http://localhost:8000/api/files/folders/")
print(f"Status: {r2.status_code}")
print(f"Response: {r2.text[:200]}")
