# App Audit

O app `audit` implementa a rastreabilidade detalhada de todas as mutações e acessos de recursos no sistema Nexus.

## Estrutura do App

* **[models.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/audit/models.py)**: Define o modelo `Audit` contendo o tipo de ação (`CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `LOGOUT`, `DOWNLOAD`), chave primária genérica vinculada a qualquer tabela do banco de dados, dados em JSON de cache de mutação (`cache_data`), IP e Timestamp.
* **[middleware.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/audit/middleware.py)**: `AuditMiddleware` intercepta cada requisição HTTP e guarda uma referência temporária da requisição na thread ativa.
* **[signals.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/audit/signals.py)**: Observadores do Django configurados para capturar a criação/edição/deleção nos modelos de arquivos e pastas e chamar o utilitário de persistência de log.

## Funcionamento Técnico

1. O middleware guarda a requisição atual em uma variável local à thread de execução usando `threading.local()`.
2. Quando o ORM executa uma gravação, o Django dispara o signal associado.
3. O receptor (`receiver`) no arquivo `signals.py` busca a request atual do middleware.
4. Se houver um usuário autenticado e a request for válida, um registro de auditoria é gerado contendo o estado anterior do objeto (através de `model_to_dict`).
5. As exclusões de log são bloqueadas por padrão no método `delete()` do modelo `Audit` para manter a integridade jurídica da rastreabilidade.
