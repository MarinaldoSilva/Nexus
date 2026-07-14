# App Share

O app `share` fornece capacidades de compartilhamento de arquivos e pastas através de links únicos temporários.

## Estrutura do App

* **[models.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/share/models.py)**: Define o modelo `SharedLink` que mapeia um UUID único como chave primária, vincula a um arquivo ou pasta, possui data de expiração (`expired`) e sinalizadores de controle de estado (`is_active`).
* **[serializers.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/share/serializers.py)**: Valida dados de expiração e mapeamentos de arquivos/pastas.
* **[views.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/share/views.py)**: `SharedLinkViewSet` oferece CRUD de links e o endpoint público `/download/` para realizar o download direto e emitir registro na auditoria.

## Fluxo de Download Seguro

Quando um link é acessado pelo endpoint de download:
1. Valida se o link existe, está ativo e não ultrapassou a data de expiração.
2. Registra o evento de download na auditoria (`Audit.objects.create(...)`), mapeando o IP de origem do usuário e o seu User Agent.
3. Se for um arquivo, redireciona o cliente para a URL do arquivo no storage. Se for pasta, emite retorno indicando que o recurso está em desenvolvimento.
