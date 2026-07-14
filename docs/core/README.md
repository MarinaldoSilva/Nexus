# App Core

O app `core` é responsável pela autenticação do usuário, gerenciamento de perfil e modelos base de auditoria temporal.

## Estrutura do App

* **[abstract_models.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/core/abstract_models.py)**: Define o `TimestampedModel` contendo campos utilitários de rastreabilidade temporal (`created_at`, `updated_at`).
* **[models.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/core/models.py)**: Define o modelo `User` estendendo `AbstractUser`, implementando controle de tipos de usuários (Admin e Default) e definindo o campo `email` como identificador único de login.
* **[serializers.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/core/serializers.py)**: Serializador do usuário utilizado para leitura e atualização parcial.
* **[views.py](file:///c:/Users/Ativos/Documents/nexus/Nexus/core/views.py)**: ViewSets e Views de leitura de dados de perfil (`UserListAPIView`), atualização (`UserUpdateAPIView`) e controle de fallback para contas inativas (`AccountInactiveView`).

## Detalhes de Implementação

O `core` substitui a autenticação padrão do Django por um fluxo baseado em e-mail, suportando integração total com o `dj-rest-auth` e o fluxo de registro via `django-allauth`.

### Padrão de Projeto Aplicado
* **Inheritance Mapping**: O modelo `User` herda de `AbstractUser` e `TimestampedModel` para estender o comportamento do ORM padrão sem perder a compatibilidade com a infraestrutura de autenticação embutida do Django.
