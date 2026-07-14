# Nexus - Documentação do Sistema

Bem-vindo à documentação oficial do **Nexus**, um sistema corporativo robusto para gerenciamento de arquivos, pastas e compartilhamentos desenvolvido sobre a plataforma Django.

## Estrutura da Documentação

A documentação está dividida de forma modular e estruturada:

* **[Arquitetura do Sistema](../docs/architecture.md)**: Visão geral da arquitetura, fluxo de dados e padrões de projeto adotados.
* **[Registro de Decisões de Arquitetura (ADR)](../docs/adr/README.md)**: Histórico e justificativa das decisões técnicas cruciais tomadas no projeto.
* **Documentação dos Módulos (Apps)**:
  * **[Core](../docs/core/README.md)**: Usuários, permissões e autenticação.
  * **[Vault (Cofre)](../docs/vault/README.md)**: Upload de arquivos, organização de pastas e compressão.
  * **[Share (Compartilhamento)](../docs/share/README.md)**: Geração de links e downloads temporários seguros.
  * **[Audit (Auditoria)](../docs/audit/README.md)**: Monitoramento e registro de eventos e acessos no sistema.

## Glossário do Sistema

* **Vault (Cofre)**: O espaço lógico privado de armazenamento pertencente a um usuário onde ele guarda seus arquivos e pastas.
* **Audit (Auditoria)**: O registro imutável (ou com exclusão restrita a administradores com privilégios específicos) de qualquer ação significativa no sistema (ex: Criação, Edição, Deleção e Download).
* **Shared Link (Link Compartilhado)**: Um link público ou privado gerado temporariamente contendo um UUID único, mapeado para um arquivo ou pasta, com data de expiração.
