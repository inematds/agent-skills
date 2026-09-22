# Verificação trilíngue — 2026-09-22

- Versão 1.1.0, PT/EN/ES: 39 páginas, 48 tópicos e 53 diagramas por idioma.
- 1.656 unidades de tradução em inglês e espanhol; dicionários completos e placeholders validados.
- 39 páginas abertas em Chromium; 1.182 referências locais verificadas; sem overflow horizontal mobile, sem texto SVG fora do viewBox, sem exceções JavaScript.
- Testados seletor preservando aula/âncora, progresso isolado, notas persistentes e rejeição de importação de outro curso.
- 38 verificações da experiência original passaram; 13 testes do laboratório passaram. Scripts Python e dados CSV têm bytes idênticos nos três idiomas.
- Inspeção visual amostral das capturas em inglês e espanhol; não constitui revisão humana integral das traduções.
- Portal: 9 testes passaram e build Next.js com Webpack concluído. Content-base: 41 testes passaram.
- Preferências visuais compartilhadas; notas e progresso separados por idioma. Trocar idioma não migra anotações.

## Tradução e custo

Modelo: `openai/gpt-5.4-nano` via OpenRouter, preço conferido em 22/09/2026. Chave carregada em runtime. Cache de respostas e dicionários evita repetir trechos.

41 chamadas com uso registrado: US$ 0.17124384. Este é um subtotal medido: duas chamadas iniciais não tiveram uso recuperável após falha de gravação, portanto não é o custo total. Não inclui consumo do agente para autoria, implementação e revisão.

Um lote ES truncado foi substituído por lotes menores. Teto do script: US$ 1,00 sobre chamadas registradas.
