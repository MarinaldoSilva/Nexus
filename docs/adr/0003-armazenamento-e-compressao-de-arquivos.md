# ADR 0003: Armazenamento Seguro de Arquivos e Processamento de Compressão

## Status
Aprovado

## Contexto
O gerenciamento físico e lógico de uploads de arquivos exige segurança quanto a vazamento de nomes sensíveis de arquivos e conflito de duplicidade de nomes. Além disso, operações de compressão de arquivos devem ser performáticas e não sobrecarregar o storage principal.

## Decisões & Justificativas
1. **Ofuscação de Nome e Organização de Pasta por ID de Usuário (UUID)**:
   * **Por quê?** Mapear o caminho de upload alterando o nome original do arquivo para um `uuid4` único previne ataques de Directory Traversal e evita conflito de nomes. Salvar sob o diretório do ID do usuário garante isolamento físico inicial.
2. **Compressão On-the-Fly em Memória (`io.BytesIO`)**:
   * **Por quê?** Compactar arquivos diretamente no buffer de memória (`BytesIO`) evita a gravação e limpeza de arquivos temporários em disco no servidor web, aumentando a segurança e a velocidade de resposta de APIs de compressão avulsa.

## Consequências
* **Positivas**: Proteção contra vazamento de metadados via nomes de arquivos no servidor e uso eficiente de recursos de E/S de disco.
* **Negativas**: Arquivos excessivamente grandes podem esgotar a memória RAM do servidor web durante a compressão. Se o volume de uploads gigantes crescer, será necessário migrar para um processamento assíncrono em fila (Celery).
