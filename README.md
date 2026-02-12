# 🗂️ NEXUS - Enterprise File & Data Management System

Sistema de gerenciamento de arquivos com auditoria completa, construído com Django REST Framework e autenticação JWT.

---

## 🚀 Quick Start

### **1. Pré-requisitos**

- Python 3.12+
- PostgreSQL 15+
- UV (gerenciador de pacotes)

---

### **2. Instalar UV**

**Windows:**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verifique: `uv --version`

---

### **3. Clonar e Configurar**

```bash
# Clone o repositório
git clone <seu-repo-url>
cd nexus_system

# Instale todas as dependências
uv sync

# Ative o ambiente virtual
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

---

### **4. Configurar Banco de Dados**

#### **Opção A: Docker (Recomendado)**

```bash
# Iniciar PostgreSQL
docker-compose up -d db

# Aguardar 5 segundos para o DB ficar pronto
# Rodar migrations
uv run python manage.py migrate

# Criar superusuário
uv run python manage.py createsuperuser
```

#### **Opção B: PostgreSQL Local**

1. Crie um arquivo `.env` na raiz:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

DB_NAME=nexus_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

2. Execute as migrations:

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

---

### **5. Rodar o Servidor**

```bash
uv run python manage.py runserver
```

Acesse:

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

---

## 📦 Estrutura do Projeto

```
nexus_system/
├── config/          # Configurações Django
├── core/            # App de usuários customizados
├── vault/           # Gerenciamento de arquivos/pastas
├── audit/           # Sistema de auditoria
├── .vscode/         # Configurações VSCode + Ruff
├── pyproject.toml   # Dependências + configuração Ruff
├── uv.lock          # Lock file do UV
└── docker-compose.yml
```

---

## 🔐 Autenticação

O projeto usa **JWT via cookies**:

### **Registro:**

```bash
POST /api/auth/register/
{
  "username": "usuario",
  "email": "email@example.com",
  "password1": "senha123",
  "password2": "senha123"
}
```

### **Login:**

```bash
POST /api/auth/login/
{
  "email": "email@example.com",
  "password": "senha123"
}
```

Retorna cookies:

- `nexus-auth` (access token)
- `nexus-refresh-token` (refresh token)

---

## 📁 Endpoints Principais

### **Arquivos:**

- `GET /api/files/` - Listar arquivos do usuário
- `POST /api/files/` - Upload de arquivo
- `POST /api/files/comprimir/` - Comprimir arquivo (público)
- `DELETE /api/files/{id}/` - Deletar (admin only)

### **Pastas:**

- `GET /api/files/folders/` - Listar pastas
- `POST /api/files/folders/` - Criar pasta

---

## 🛠️ Desenvolvimento

### **Adicionar Dependência**

```bash
# Produção
uv add django-cors-headers

# Dev
uv add --dev pytest
```

### **Rodar Linter**

```bash
# Verificar erros
uv run ruff check .

# Corrigir automaticamente
uv run ruff check --fix .

# Formatar código
uv run ruff format .
```

### **Pre-commit**

```bash
# Instalar hooks
uv run pre-commit install

# Testar manualmente
uv run pre-commit run --all-files
```

---

## 🐳 Docker

### **Desenvolvimento:**

```bash
# Iniciar tudo (DB + Adminer)
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### **Acessar Adminer (GUI do DB):**

- URL: http://localhost:8080
- Sistema: PostgreSQL
- Servidor: db
- Usuário: `postgres`
- Senha: `postgres`
- Base: `nexus_db`

---

## 📊 Recursos do Projeto

### ✅ **Implementado:**

- [x] Autenticação JWT com cookies
- [x] Upload/download de arquivos
- [x] Sistema hierárquico de pastas
- [x] Compressão de arquivos (3 níveis)
- [x] Auditoria completa (logs de ações)
- [x] Admin customizado com Unfold
- [x] Linting automatizado (Ruff)
- [x] Pre-commit hooks

### 🚧 **Roadmap:**

- [ ] Testes unitários (coverage > 70%)
- [ ] Documentação Swagger/OpenAPI
- [ ] Upload em massa
- [ ] Versionamento de arquivos
- [ ] Compartilhamento de arquivos
- [ ] CI/CD pipeline

---

## 🧪 Testes

```bash
# Rodar testes (quando implementados)
uv run pytest

# Com coverage
uv run pytest --cov=.
```

---

## 🔍 Troubleshooting

### **Erro: "No module named 'X'"**

```bash
uv sync --reinstall
```

### **Erro: "connection refused" (PostgreSQL)**

```bash
# Verificar se o Docker está rodando
docker-compose ps

# Reiniciar DB
docker-compose restart db
```

### **Erro: "uv: command not found"**

```bash
# Reinstalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 📚 Documentação Adicional

- [Guia de Migração Poetry → UV](./docs/guia_migracao_poetry_uv.md)
- [Configuração Ruff + VSCode](./docs/guia_ruff_vscode.md)

---

## 👤 Autores

- **Seu Nome** - Desenvolvimento inicial

---

## 📄 Licença

Este projeto é privado/proprietário.

---

**Pronto para começar!** 🎉
