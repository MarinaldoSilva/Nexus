# App Vault

O app `vault` gerencia a estrutura de diretórios e arquivos armazenados de cada usuário.

## Estrutura do App

* **[models.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/vault/models.py)**:
  * `Folder`: Modelo auto-referenciável representando pastas hierárquicas.
  * `File`: Modelo mapeando os metadados do arquivo e vinculando-o ao armazenamento físico.
* **[services.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/vault/services.py)**: Contém o serviço de negócios focado na compressão de arquivos binários em formato ZIP.
* **[permissions.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/vault/permissions.py)**: Define a política de restrição de acesso que garante que apenas administradores possam realizar exclusões ou modificações críticas.
* **[views.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/vault/views.py)**:
  * `FolderViewSet`: CRUD completo de pastas.
  * `FileViewSet`: CRUD de arquivos e endpoint customizado de compressão rápida (`comprimir`).

## Lógica de Armazenamento e Compressão

O upload do arquivo passa pela função `upload_path()`, que renomeia o arquivo original com um identificador UUID para garantir unicidade e isolamento em diretórios por ID do dono do arquivo.

### Padrão de Projeto Aplicado
* **Service Layer**: Toda lógica de compressão com `zipfile` está encapsulada em `vault/services.py` para não inflar as views.
* **Hierarchical Tree (Adjacency List)**: O modelo `Folder` usa um relacionamento `parent = models.ForeignKey("self")` para construir uma árvore infinita de subpastas de forma relacional padrão.
