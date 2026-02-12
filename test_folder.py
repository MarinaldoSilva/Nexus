import time

import requests

# Criar usuário
print("Criando usuário...")
username = f"testfolder{int(time.time())}"
reg = requests.post(
    "http://localhost:8000/api/auth/register/",
    json={
        "username": username,
        "email": f"{username}@test.com",
        "password1": "test123!",
        "password2": "test123!",
    },
)

if reg.status_code != 201:
    print(f"❌ Erro registro: {reg.status_code} - {reg.text}")
    exit(1)

token = reg.json()["access"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Usuário {username} criado")

# Teste 1: Criar pasta raiz
print("\n1. Criando pasta raiz 'Documentos'...")
r1 = requests.post(
    "http://localhost:8000/api/files/folders/",
    headers=headers,
    json={"name": "Documentos"},
)
print(f"Status: {r1.status_code}")
if r1.status_code == 201:
    folder1 = r1.json()
    print(f"✅ Pasta criada: {folder1.get('name')} (ID: {folder1.get('id')})")
else:
    print(f"❌ Erro: {r1.text}")
    exit(1)

# Teste 2: Criar subpasta
print("\n2. Criando subpasta 'Trabalho' dentro de 'Documentos'...")
r2 = requests.post(
    "http://localhost:8000/api/files/folders/",
    headers=headers,
    json={"name": "Trabalho", "parent": folder1["id"]},
)
print(f"Status: {r2.status_code}")
if r2.status_code == 201:
    folder2 = r2.json()
    print(
        f"✅ Subpasta criada: {folder2.get('name')} (parent: {folder2.get('parent')})"
    )
else:
    print(f"❌ Erro: {r2.text}")

# Teste 3: Listar pastas
print("\n3. Listando todas as pastas...")
r3 = requests.get("http://localhost:8000/api/files/folders/", headers=headers)
print(f"Status: {r3.status_code}")
if r3.status_code == 200:
    folders = r3.json()
    print(f"✅ Total de pastas: {len(folders)}")
    for f in folders:
        print(f"   - {f['name']} (ID: {f['id']}, parent: {f.get('parent')})")
else:
    print(f"❌ Erro: {r3.text}")

print("\n✅ TESTES CONCLUÍDOS!")
