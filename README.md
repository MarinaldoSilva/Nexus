<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Projeto Nexus</title>
</head>
<body>

<h1>Projeto Nexus</h1>

<p>O Nexus é um sistema para gerenciar arquivos e pastas usando Django REST Framework. Ele permite fazer upload, organizar arquivos e registrar ações no sistema. A autenticação usa JWT em cookies.</p>

<h2>Tecnologias usadas</h2>
<ul>
    <li>Python 3.12+</li>
    <li>Django e Django REST Framework</li>
    <li>PostgreSQL</li>
    <li>UV</li>
    <li>Docker</li>
</ul>

<h2>Como rodar o projeto</h2>

<h3>Instalar o UV</h3>
<p><strong>Windows:</strong></p>
<pre><code>powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
</code></pre>

<p><strong>Linux/Mac:</strong></p>
<pre><code>curl -LsSf https://astral.sh/uv/install.sh | sh
</code></pre>

<h3>Baixar o projeto e instalar dependências</h3>
<pre><code>git clone &lt;url-do-seu-repo&gt;
cd nexus_system
uv sync
</code></pre>

<h3>Ativar o ambiente virtual</h3>
<p><strong>Windows:</strong></p>
<pre><code>.\.venv\Scripts\activate
</code></pre>

<p><strong>Linux/Mac:</strong></p>
<pre><code>source .venv/bin/activate
</code></pre>

<h3>Configurar o banco de dados</h3>
<p>Com Docker:</p>
<pre><code>docker-compose up -d db
</code></pre>

<p>Ou crie um arquivo <code>.env</code> com as credenciais do PostgreSQL.</p>

<h3>Criar tabelas e usuário admin</h3>
<pre><code>uv run python manage.py migrate
uv run python manage.py createsuperuser
</code></pre>

<h3>Rodar o servidor</h3>
<pre><code>uv run python manage.py runserver
</code></pre>

<p>API: <a href="http://localhost:8000/api/">http://localhost:8000/api/</a><br>
Admin: <a href="http://localhost:8000/admin/">http://localhost:8000/admin/</a></p>

<h2>O que já funciona</h2>
<ul>
    <li>Cadastro e login com JWT</li>
    <li>Upload, listagem e exclusão de arquivos</li>
    <li>Criação e navegação de pastas</li>
    <li>Compressão de arquivos</li>
    <li>Logs de auditoria</li>
</ul>

<h2>Comandos úteis</h2>

<p>Verificar lint:</p>
<pre><code>uv run ruff check .
</code></pre>

<p>Corrigir:</p>
<pre><code>uv run ruff check --fix .
</code></pre>

<p>Formatar:</p>
<pre><code>uv run ruff format .
</code></pre>

</body>
</html>
