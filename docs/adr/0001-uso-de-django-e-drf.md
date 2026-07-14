# ADR 0001: Escolha do Django, DRF e Autenticação JWT

## Status
Aprovado

## Contexto
O Nexus necessita de um backend robusto, escalável, seguro e de rápido desenvolvimento para atuar como o núcleo do sistema de gerenciamento de arquivos. Era necessário escolher a tecnologia principal e definir uma estratégia de autenticação segura para comunicações Stateless via API REST.

## Decisões & Justificativas
1. **Django & Django REST Framework (DRF)**:
   * **Por quê?** O ecossistema do Django oferece o padrão ORM maduro, migrações automatizadas eficientes, segurança nativa contra vulnerabilidades clássicas e excelente integração com PostgreSQL. O DRF simplifica a criação de serializadores complexos e ViewSets.
2. **Autenticação Stateless com JWT (JSON Web Tokens)**:
   * Utilização do `djangorestframework-simplejwt` aliado ao `dj-rest-auth`.
   * **Por quê?** O JWT elimina a necessidade de persistência de sessões no servidor (Scale-out amigável) e, quando armazenado em cookies HTTP-Only e Secure, previne ataques de roubo de sessão via Cross-Site Scripting (XSS).

## Consequências
* **Positivas**: Estruturação limpa do código, validação de tokens performática e facilidade para plugar frontends web e mobile no futuro.
* **Negativas**: A revogação de tokens antes da expiração exige estratégias adicionais (como blacklists em cache Redis).
