# ADR 0002: Sistema de Auditoria via Middleware e Django Signals

## Status
Aprovado

## Contexto
Toda modificação de arquivos ou pastas (criação, edição, exclusão) e ações críticas (downloads) precisam de logs de auditoria imutáveis. O sistema de log deve interferir o mínimo possível no fluxo principal das Views de negócios, sendo transparente e desacoplado.

## Decisões & Justificativas
1. **Django Signals (`post_save`, `post_delete`)**:
   * **Por quê?** Permite centralizar a criação dos registros de auditoria sempre que um arquivo ou pasta for modificado, independentemente se a modificação partiu da API REST, do Admin do Django, ou do console de gerenciamento.
2. **AuditMiddleware e Thread Local**:
   * **Por quê?** Os Signals do Django não têm acesso nativo ao objeto `request` (que contém o usuário autenticado e o IP da requisição). O middleware armazena temporariamente o contexto da requisição na thread de execução atual, permitindo que a função `save_log()` capture essas informações.
3. **Generic Foreign Keys (GFK)**:
   * **Por quê?** A auditoria deve registrar o evento de qualquer tipo de objeto (arquivos, pastas, links compartilhados) sem duplicar colunas FK específicas.

## Consequências
* **Positivas**: Altíssimo desacoplamento e garantia de log mesmo se o objeto for editado via Django Admin.
* **Negativas**: Operações em lote (bulk updates ou bulk deletes) não disparam signals nativos do Django, exigindo atenção especial de desenvolvimento para evitar desvios de auditoria.
