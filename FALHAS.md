# Falhas corrigidas

| data | o que quebrou | menor correção | prompt / infra |
| --- | --- | --- | --- |
| 2026-09-22 | Script reaproveitado tentou registrar duas respostas de tradução em pasta evidence ausente | Unificar caminhos em verificacao/i18n e salvar resposta antes do log; custo dessas duas chamadas sem medição recuperável | infra |
| 2026-09-21 | Âmbar claro com baixo contraste e rótulos SVG reduzidos no celular | Usar primary-ink no texto e preservar 14px com largura mínima 720px; permitir rolagem local | prompt |
| 2026-09-21 | Retomada dependia de checkpoint manual e preferências de leitura eram sobrescritas no CSS | Salvar tópico no scrollspy e herdar medida/entrelinha na prosa | infra |
| 2026-09-21 | Extração do anti-FOUC capturou tag mencionada no comentário e gerou erro de sintaxe | Remover comentários HTML antes de extrair o script; testar ausência de erros no navegador | prompt |
| 2026-09-21 | Camada v2 escutava botões só no main, retomava scroll local e perdia campos extras no export | Delegar eventos no body, resolver âncoras pelo manifesto e validar/preservar JSON em namespace próprio | infra |

| 2026-09-22 | gen:data executado no diretório do curso e seleção de testes não encontrou casos | executar no portal e apontar test/*.test.mjs | prompt |

| 2026-09-22 | Um lote ES retornou JSON truncado | reduzir lotes e dividir resposta inválida recursivamente com cache e teto | infra |
