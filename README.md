# Agent Skills · Codex — INEMA v2

Curso completo em português, inglês e espanhol baseado nos seis passos da transcrição fornecida de [Como Desenvolver Habilidades em Codex Melhor que 99% das Pessoas](https://www.youtube.com/watch?v=9KOtMsZ9I28).

Abra **index.html** no navegador. O curso usa arquivos locais e funciona sem backend, build ou conexão de rede. Links externos são apenas referências. O kit de laboratório fica em `materiais/kit-agent-skills.zip`.

## Conteúdo
- 4 trilhas, 8 módulos e 48 tópicos aprofundados.
- 53 diagramas SVG, 48 exercícios com respostas comentadas e 8 checagens de conhecimento.
- Exemplos copiáveis, comparações fazer/evitar, linhas de processo e simulador de custo por entrega aceita.
- Projeto completo: CSV → relatório semanal, com script Python, skill de exemplo, dados sintéticos e 13 testes.
- Estudo de caso complementar: vídeo → artigo, incluindo seleção, recorte e posicionamento de imagens.
- Aproximadamente 10 mil palavras de conteúdo autoral nos tópicos. Estimativa de estudo: 7–9 horas com prática.

## Aprendizagem v2
Progresso explícito por tópico, módulo, trilha e curso; marcação de dúvidas; grifos e notas por seleção de texto; Minha jornada; retomada por âncora; export/import JSON; temas escuro, claro, sépia, foco e alto contraste; tamanho, fonte, largura e entrelinha.

Os dados ficam no navegador. Em `file://`, políticas de armazenamento variam entre navegadores; exporte suas notas. Se armazenamento for bloqueado, a leitura funciona e o estado fica em memória durante a página. Um servidor HTTP local oferece uma origem estável entre todas as páginas:

```bash
python3 -m http.server 8080
```

Abra `http://localhost:8080`. Não há login nem sincronização em nuvem.

## Estrutura
- `index.html`: apresentação e acesso às trilhas.
- `curso/trilha1` a `curso/trilha4`: índices e módulos completos.
- `assets`: CSS, camada de aprendizagem, interações e manifesto.
- `materiais`: downloads e laboratório educativo.
- `scripts/content.py`: conteúdo autoral editável.
- `scripts/build_course.py`: gera as 13 páginas usando somente Python padrão.
- `verificacao`: evidências de testes e capturas de desktop/celular.

## Manutenção

```bash
python3 scripts/build_course.py
python3 scripts/build_locales.py
python3 scripts/package_course.py
python3 materiais/laboratorio/scripts/testar_relatorio.py
npm ci
npm test
node scripts/verify_locales.mjs
```

O navegador de teste pode ser indicado por `CHROMIUM_PATH`. Sem override, o teste usa a instalação local conhecida quando presente, ou o Chromium gerenciado pelo Playwright. Em outra máquina, instale o navegador de teste com `npx playwright install chromium` se necessário. O navegador de teste não é dependência para estudar.

## Verificação
38 checagens de navegador passaram, 394 referências locais conferidas no PT e 13 testes do laboratório passaram. Inclui abertura `file://`, leitura sem JS, storage bloqueado, responsive desktop/mobile, notas persistentes, temas, quiz, retomada por navegação real e validação de importação. Evidências em `verificacao/RELATORIO.md`. A revisão trilíngue conferiu as 39 páginas e 1.182 referências locais; veja `verificacao/i18n/RELATORIO.md`.

O código Python foi executado; o acionamento da skill didática numa sessão separada de Codex é uma atividade do aluno e não foi medido nesta criação. A revisão não é uma certificação completa WCAG. Publicação: GitHub Pages em https://inematds.github.io/agent-skills/. Inglês em `en/`, espanhol em `es/`. O seletor preserva a aula e a âncora; progresso e notas são separados por idioma, preferências visuais são compartilhadas.

## Fontes e versão
Metodologia: transcrição enviada pelo usuário; o vídeo não foi baixado ou assistido por frames nesta tarefa. Fatos de formato e ativação conferidos em [Build skills](https://learn.chatgpt.com/docs/build-skills) e [Customization](https://learn.chatgpt.com/docs/customization/overview), em 21/09/2026. A promessa “99%” é o título da fonte, não um benchmark do curso. Exemplos de custo são sintéticos.

Versão **1.1.0**. Formato e assets de base: skill `formato-curso-v2`, com correções locais de integração registradas em `FALHAS.md`. Conteúdo, imagens vetoriais e exercícios desenvolvidos para este projeto.

A geração dos idiomas usa BeautifulSoup (`pip install beautifulsoup4`) e dicionários versionados, sem API. `scripts/acquire_locales.py` é uma ferramenta opcional de manutenção com chamadas pagas via OpenRouter e chave carregada em runtime; não é necessário executá-la para estudar ou reconstruir esta versão.

<!-- inema-backlink:v1 -->
## Mais no INEMA.CLUB

- [Ficha completa deste curso](https://www.inema.club/cursos/281-agent-skills-crie-skills-verificaveis-no-codex/)
- [Guia: como aprender inteligência artificial](https://www.inema.club/aprender-inteligencia-artificial/)
- [Todos os cursos](https://www.inema.club/cursos/)
<!-- /inema-backlink:v1 -->
