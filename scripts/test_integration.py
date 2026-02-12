import os
import random
import time

import requests

BASE_URL = "http://127.0.0.1:8000"

# Lista de dados para simular aleatoriedade "realista"
NOMES = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira"]
EMPRESAS = ["TechCorp", "NexusLtda", "InovaSys", "AlphaBeta"]


class NexusTester:
    def __init__(self):
        self.session = requests.Session()
        self.user_data = self._generate_user_data()
        self.token = None
        self.file_id = None

    def _generate_user_data(self):
        """Gera dados de usuário semi-aleatórios e realistas"""
        nome = random.choice(NOMES)
        sobrenome = random.choice(SOBRENOMES)
        empresa = random.choice(EMPRESAS)

        # Adiciona timestamp para garantir unicidade
        ts = int(time.time())
        username = f"{nome.lower()}.{sobrenome.lower()}.{ts}"
        email = f"{nome.lower()}.{sobrenome.lower()}@{empresa.lower()}.com.br"  # Email corporativo fake

        return {
            "username": username,
            "email": email,
            "password1": "SenhaSegura@2026",
            "password2": "SenhaSegura@2026",
        }

    def log(self, step, msg, status="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}
        print(f"{icons.get(status, '')} [{step}] {msg}")

    def register(self):
        url = f"{BASE_URL}/api/auth/register/"
        self.log("AUTH", f"Tentando registrar usuário: {self.user_data['email']}")

        try:
            r = self.session.post(url, json=self.user_data)
            if r.status_code == 201:
                self.log("AUTH", "Registro realizado com sucesso.", "SUCCESS")
                return True
            else:
                self.log(
                    "AUTH", f"Falha no registro: {r.status_code} - {r.text}", "ERROR"
                )
                return False
        except Exception as e:
            self.log("AUTH", f"Erro de conexão: {e}", "ERROR")
            return False

    def login(self):
        url = f"{BASE_URL}/api/auth/login/"
        # Tenta logar apenas com email
        payload = {
            "email": self.user_data["email"],
            "password": self.user_data["password1"],
        }
        self.log(
            "AUTH", f"Tentando realizar login com email: {self.user_data['email']}"
        )

        r = self.session.post(url, json=payload)

        if r.status_code == 200:
            data = r.json()
            # Tenta pegar key (TokenAuth) ou access (JWT) ou cookie
            if "key" in data:
                self.token = data["key"]
            elif "access" in data:
                self.token = data["access"]
            elif "user" in data:
                # Cookies session based - verifica cookie
                if self.session.cookies.get("sessionid"):
                    self.log("AUTH", "Login via Session Cookie sucesso.", "SUCCESS")
                    return True

            if self.token:
                self.session.headers.update(
                    {"Authorization": f"Bearer {self.token}"}
                )  # Adjust prefix if needed
                self.log(
                    "AUTH",
                    f"Login sucesso. Token obtido: {self.token[:10]}...",
                    "SUCCESS",
                )
            return True
        else:
            self.log("AUTH", f"Falha no Login: {r.status_code} - {r.text}", "ERROR")
            return False

    def upload_file(self):
        url = f"{BASE_URL}/files/criar/"
        filename = f"relatorio_{self.user_data['username']}.txt"
        content = f"Relatório Confidential de {self.user_data['email']}\nGerado em {time.ctime()}"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        self.log("VAULT", f"Enviando arquivo: {filename}")

        # Abrir arquivo para upload
        files = {"file": (filename, open(filename, "rb"))}  # Tupla (nome, arquivo)

        r = self.session.post(url, files=files)

        # Cleanup local file
        files["file"][1].close()
        os.remove(filename)

        if r.status_code == 201:
            data = r.json()
            # Ajuste conforme estrutura de resposta do serializer
            # Pode vir dentro de 'results' ou raiz
            result_data = data.get("results", data)
            self.file_id = result_data.get("id")
            self.log("VAULT", f"Upload sucesso. ID: {self.file_id}", "SUCCESS")
            return True
        else:
            self.log("VAULT", f"Falha no Upload: {r.status_code} - {r.text}", "ERROR")
            return False

    def list_files(self):
        url = f"{BASE_URL}/files/listar/"
        self.log("VAULT", "Listando arquivos...")
        r = self.session.get(url)

        if r.status_code == 200:
            data = r.json()
            items = data.get("result", [])
            self.log(
                "VAULT", f"Listagem sucesso. Total de arquivos: {len(items)}", "SUCCESS"
            )

            # Valida se o arquivo criado está na lista
            found = any(f["id"] == self.file_id for f in items)
            if found:
                self.log(
                    "VAULT", "Arquivo recém-criado foi encontrado na lista.", "SUCCESS"
                )
            else:
                self.log(
                    "VAULT", "ALERTA: Arquivo criado não encontrado na lista!", "WARN"
                )
            return True
        else:
            self.log("VAULT", f"Falha na Listagem: {r.status_code} - {r.text}", "ERROR")
            return False

    def update_file(self):
        if not self.file_id:
            return False

        url = f"{BASE_URL}/files/atualizar/{self.file_id}/"
        new_name = f"updated_project_{int(time.time())}.txt"
        payload = {"name": new_name}

        self.log("VAULT", f"Atualizando nome para: {new_name}")
        r = self.session.patch(url, json=payload)

        if r.status_code == 200:
            self.log("VAULT", "Update realizado com sucesso.", "SUCCESS")
            return True
        else:
            self.log("VAULT", f"Falha no Update: {r.status_code} - {r.text}", "ERROR")
            return False

    def delete_file(self):
        if not self.file_id:
            return False

        url = f"{BASE_URL}/files/deletar/{self.file_id}/"
        self.log("VAULT", f"Deletando arquivo ID: {self.file_id}")
        r = self.session.delete(url)

        if r.status_code == 204:
            self.log("VAULT", "Arquivo deletado com sucesso.", "SUCCESS")
            return True
        else:
            self.log("VAULT", f"Falha no Delete: {r.status_code} - {r.text}", "ERROR")
            return False

    def logout(self):
        url = f"{BASE_URL}/api/auth/logout/"
        self.log("AUTH", "Realizando Logout...")
        r = self.session.post(url)
        if r.status_code == 200:
            self.log("AUTH", "Logout sucesso.", "SUCCESS")
        else:
            self.log("AUTH", f"Logout status: {r.status_code}", "WARN")

    def run(self):
        print("=== 🚀 INICIANDO TESTE DE INTEGRAÇÃO NEXUS ===")
        if not self.register():
            return
        if not self.login():
            return

        if self.upload_file():
            self.list_files()
            self.update_file()
            self.delete_file()

        self.logout()
        print("\n=== ✅ TESTE FINALIZADO ===")


if __name__ == "__main__":
    tester = NexusTester()
    tester.run()
