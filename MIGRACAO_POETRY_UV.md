# 🚀 Guia Completo: Migração Poetry → UV

Este guia ensina como migrar um projeto Python de **Poetry** para **UV** e como configurar um projeto do zero com as melhores práticas.

---

## 📑 Índice

1. [O que é UV e por que migrar?](#1-o-que-é-uv-e-por-que-migrar)
2. [Instalando UV](#2-instalando-uv)
3. [Migração: Poetry → UV](#3-migração-poetry--uv)
4. [Configuração Inicial de Projeto](#4-configuração-inicial-de-projeto)
5. [Docker com UV](#5-docker-com-uv)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. O que é UV e por que migrar?

### **O que é UV?**

[UV](https://github.com/astral-sh/uv) é um **gerenciador de pacotes Python ultrarrápido** criado pela Astral (mesma empresa do Ruff), escrito em **Rust**.

### **Comparação:**

| Recurso               | Poetry                  | UV                               |
| --------------------- | ----------------------- | -------------------------------- |
| **Velocidade**        | ~10s para instalar deps | ~0.5s (20x mais rápido!)         |
| **Linguagem**         | Python                  | Rust                             |
| **Compatibilidade**   | pyproject.toml          | pyproject.toml (100% compatível) |
| **Lock file**         | poetry.lock             | uv.lock                          |
| **Resolução de deps** | Lenta                   | Instantânea                      |

### **Por que migrar?**

- ✅ **20-100x mais rápido** que Poetry/pip
- ✅ **Menos bugs** de resolução de dependências
- ✅ **Sintaxe simples** (similar ao npm/cargo)
- ✅ **Totalmente compatível** com pyproject.toml

---

## 2. Instalando UV

### **Windows**

#### **Método 1: PowerShell (Recomendado)**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### **Método 2: winget**

```powershell
winget install --id=astral-sh.uv -e
```

#### **Método 3: scoop**

```powershell
scoop install uv
```

---

### **macOS/Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### **Verificar instalação**

```bash
uv --version
# Saída esperada: uv 0.X.X
```

---

## 3. Migração: Poetry → UV

### **Passo 1: Backup do projeto**

```bash
# Copie o projeto antes de migrar
cp -r meu-projeto meu-projeto-backup
cd meu-projeto
```

---

### **Passo 2: Converter pyproject.toml**

**ANTES (Poetry):**

```toml
[tool.poetry]
name = "nexus-system"
version = "0.1.0"
description = "Sistema de arquivos"
authors = ["Você <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"
django = "^6.0.1"
djangorestframework = "^3.16.1"

[tool.poetry.group.dev.dependencies]
ruff = "^0.14.14"
pre-commit = "^4.5.1"
```

**DEPOIS (UV):**

```toml
[project]
name = "nexus-system"
version = "0.1.0"
description = "Sistema de arquivos"
requires-python = ">=3.12"
dependencies = [
    "django>=6.0.1",
    "djangorestframework>=3.16.1",
]

[dependency-groups]
dev = [
    "ruff>=0.14.14",
    "pre-commit>=4.5.1",
]
```

---

### **Passo 3: Conversão Automática**

Use o script Python abaixo para converter automaticamente:

```python
# convert_poetry_to_uv.py
import tomli
import tomli_w

with open("pyproject.toml", "rb") as f:
    data = tomli.load(f)

poetry = data.get("tool", {}).get("poetry", {})

# Criar estrutura UV
uv_config = {
    "project": {
        "name": poetry.get("name", "my-project"),
        "version": poetry.get("version", "0.1.0"),
        "description": poetry.get("description", ""),
        "requires-python": f">={poetry['dependencies']['python'].strip('^')}",
        "dependencies": [
            f"{pkg}>={ver.strip('^')}"
            for pkg, ver in poetry.get("dependencies", {}).items()
            if pkg != "python"
        ],
    },
    "dependency-groups": {
        "dev": [
            f"{pkg}>={ver.strip('^')}"
            for pkg, ver in poetry.get("group", {}).get("dev", {}).get("dependencies", {}).items()
        ]
    }
}

# Mesclar com configurações existentes (Ruff, etc)
data.pop("tool", None).pop("poetry", None)
data.update(uv_config)

with open("pyproject.toml", "wb") as f:
    tomli_w.dump(data, f)

print("✅ Conversão concluída!")
```

**Executar:**

```bash
uv pip install tomli tomli-w
python convert_poetry_to_uv.py
```

---

### **Passo 4: Remover Poetry**

```bash
# Deletar arquivos do Poetry
rm poetry.lock
rm -rf .venv  # Se quiser recriá-lo

# Opcional: desinstalar Poetry
pip uninstall poetry
```

---

### **Passo 5: Instalar dependências com UV**

```bash
# Criar ambiente virtual e instalar deps
uv sync

# Ativar ambiente
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

**Pronto!** Agora você tem `uv.lock` em vez de `poetry.lock`.

---

## 4. Configuração Inicial de Projeto

### **4.1. Estrutura de Projeto Django**

```
meu-projeto/
├── .venv/                 # Ambiente virtual (criado pelo UV)
├── .vscode/
│   └── settings.json      # Configurações do VSCode
├── .git/
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml         # Configuração central
├── uv.lock                # Lock file do UV
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app1/
├── app2/
└── README.md
```

---

### **4.2. pyproject.toml Completo**

```toml
[project]
name = "nexus-system"
version = "0.1.0"
description = "Enterprise File & Data Management System"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "django>=6.0.1",
    "djangorestframework>=3.16.1",
    "psycopg2>=2.9.11",
    "python-dotenv>=1.2.1",
]

[dependency-groups]
dev = [
    "ruff>=0.14.14",
    "pre-commit>=4.5.1",
]

# === RUFF: Linter + Formatter ===
[tool.ruff]
line-length = 88
target-version = "py312"

# Ignorar migrations e arquivos gerados
exclude = [
    "*/migrations/*",
    ".venv",
    ".git",
]

[tool.ruff.lint]
# E=Erros, F=Pyflakes, I=Isort, B=Bugbear, UP=Pyupgrade
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

---

### **4.3. Pre-commit Setup**

**.pre-commit-config.yaml:**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

**Instalar hooks:**

```bash
uv run pre-commit install
```

---

### **4.4. .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
.venv/
venv/
ENV/

# UV
uv.lock

# Django
*.log
db.sqlite3
media/
staticfiles/

# IDEs
.vscode/
.idea/
*.swp

# Env
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

---

### **4.5. .vscode/settings.json**

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.enable": true,
  "ruff.lint.enable": true,
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

---

## 5. Docker com UV

### **5.1. Dockerfile**

```dockerfile
# === STAGE 1: Builder ===
FROM python:3.12-slim AS builder

# Instalar UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Configurar diretório
WORKDIR /app

# Copiar apenas arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências
RUN uv sync --frozen --no-dev

# === STAGE 2: Runner ===
FROM python:3.12-slim

WORKDIR /app

# Copiar venv do builder
COPY --from=builder /app/.venv /app/.venv

# Copiar código
COPY . .

# Configurar PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expor porta
EXPOSE 8000

# Comando
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

### **5.2. docker-compose.yml**

```yaml
version: "3.8"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: nexus
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: uv run python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/nexus

volumes:
  postgres_data:
```

---

### **5.3. Comandos Docker + UV**

```bash
# Build
docker-compose build

# Rodar servidor
docker-compose up

# Executar comandos dentro do container
docker-compose exec web uv run python manage.py migrate
docker-compose exec web uv run python manage.py createsuperuser

# Adicionar nova dependência
docker-compose exec web uv add django-cors-headers
docker-compose restart web
```

---

## 6. Troubleshooting

### **Problema 1: "uv: command not found"**

```bash
# Adicionar UV ao PATH (Windows PowerShell)
$env:Path += ";$env:USERPROFILE\.cargo\bin"

# Linux/macOS
export PATH="$HOME/.cargo/bin:$PATH"

# Ou reinstalar
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### **Problema 2: Conflito de dependências**

```bash
# Forçar reinstalação
uv sync --reinstall

# Limpar cache
uv cache clean
```

---

### **Problema 3: "No module named 'X'"**

```bash
# Garantir que está no ambiente certo
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows

# Reinstalar
uv sync
```

---

## 📊 Comparação de Comandos

| Tarefa         | Poetry                 | UV                          |
| -------------- | ---------------------- | --------------------------- |
| Criar projeto  | `poetry new`           | `uv init`                   |
| Adicionar dep  | `poetry add django`    | `uv add django`             |
| Remover dep    | `poetry remove django` | `uv remove django`          |
| Instalar deps  | `poetry install`       | `uv sync`                   |
| Rodar script   | `poetry run python`    | `uv run python`             |
| Ativar venv    | `poetry shell`         | `source .venv/bin/activate` |
| Atualizar deps | `poetry update`        | `uv lock --upgrade`         |

---

## 🎯 Checklist de Migração

- [ ] Backup do projeto original
- [ ] UV instalado (`uv --version`)
- [ ] `pyproject.toml` convertido
- [ ] `poetry.lock` removido
- [ ] `uv sync` executado com sucesso
- [ ] `.gitignore` atualizado
- [ ] Pre-commit instalado (`uv run pre-commit install`)
- [ ] Ruff configurado (`.vscode/settings.json`)
- [ ] Docker atualizado (se usar)
- [ ] Testes rodando (`uv run pytest`)

---

## 🚀 Próximos Passos

Após migrar:

1. **Commit inicial:**

   ```bash
   git add .
   git commit -m "chore: migra Poetry para UV"
   ```

2. **Atualizar CI/CD** (GitHub Actions exemplo):

   ```yaml
   - name: Install UV
     run: curl -LsSf https://astral.sh/uv/install.sh | sh

   - name: Install dependencies
     run: uv sync

   - name: Run tests
     run: uv run pytest
   ```

3. **Documentar no README:**

   ```markdown
   ## Setup

   1. Instalar UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   2. Instalar deps: `uv sync`
   3. Rodar servidor: `uv run python manage.py runserver`
   ```

---

## 📚 Recursos Adicionais

- [Documentação UV](https://docs.astral.sh/uv/)
- [Guia de Migração Oficial](https://docs.astral.sh/uv/guides/projects/)
- [Comparação com Poetry](https://github.com/astral-sh/uv#comparison)
- [Exemplos de Projetos](https://github.com/astral-sh/uv/tree/main/examples)

---

**Pronto para migrar!** 🎉
