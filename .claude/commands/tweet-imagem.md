---
name: tweet-imagem
description: Gera imagem PNG estilo print de tweet/X via render HTML para Playwright screenshot. Use quando precisar criar slide individual de carrossel Instagram com texto + autor + foto + numero (1/5, 2/5...). Output PNG 1080x1350 em squad/output/imagens/. NAO usa IA (Gemini/Flux) usa template HTML estatico.
model: claude-sonnet-4-5
---

# /tweet-imagem — render HTML → PNG estilo tweet/X

Gera **um slide PNG 1080x1350** com aparência de print de tweet/X. Usado por `/criar-carrossel` pra renderizar cada slide do carrossel quando o estilo escolhido é "tweet card".

**Não usa IA generativa.** Usa template HTML estático + Playwright headless screenshot. Determinístico, rápido (<3s/slide), gratuito.

## Quando usar

- Slide de carrossel Instagram em formato print de tweet (texto + autor + foto + handle)
- Citação/quote com autoria do Gui (ou outro autor)
- Slide de abertura de carrossel com pergunta/afirmação curta no estilo X

**Não usar para:** ilustrações, ícones, fotos compostas, antes/depois, story telling visual. Pra esses, esperar `/gerar-imagem` (Gemini/Flux via OpenRouter — ainda não disponível).

## Inputs

| Flag | Obrigatório | Default | Descrição |
|---|---|---|---|
| `--texto` | sim | — | Texto principal do tweet. Suporta `**bold**` e `\n`. |
| `--autor` | não | `{{NOME_OPERADOR}}` | Nome em bold no header |
| `--handle` | não | `@{{HANDLE_OPERADOR}}` | Handle abaixo do nome |
| `--foto` | não | fallback "G" | Path local OU URL da foto de perfil |
| `--numero` | não | (oculto) | Pill canto superior direito (`1/5`, `2/5`...) |
| `--data` | não | hoje pt-BR | Data exibida no footer |
| `--output` | sim | — | Path final do PNG |
| `--template` | não | `default.html` | Path do template HTML alternativo |

## Pipeline

1. Carrega template HTML em `Páginas Astro {{NOME_OPERADOR}}/scripts/tweet-templates/default.html`
2. Substitui placeholders: `{{TEXTO}}`, `{{AUTOR}}`, `{{HANDLE}}`, `{{FOTO_HTML}}`, `{{NUMERO}}`, `{{DATA}}`
3. Lança Playwright headless Chromium em viewport 1080x1350
4. `page.setContent(html)` + espera imagens carregarem
5. Screenshot com clip exato 1080x1350
6. Salva em path indicado (cria diretório se não existe)

## Como rodar

Sempre dentro de `Páginas Astro {{NOME_OPERADOR}}/` (onde Playwright está instalado):

```bash
cd "Páginas Astro {{NOME_OPERADOR}}"
node scripts/tweet-imagem.mjs \
  --texto "A maioria dos negócios digitais morrem porque o dono virou o gargalo" \
  --autor "{{NOME_OPERADOR}}" \
  --handle "@{{HANDLE_OPERADOR}}" \
  --foto /caminho/foto-gui.jpg \
  --numero "1/5" \
  --output "../Squad Empresa {{NOME_OPERADOR}}/squad/output/imagens/2026-05-07/teste/slide-1.png"
```

## Convenção de output

Sempre em `squad/output/imagens/YYYY-MM-DD/{slug}/slide-N.png`.

- `YYYY-MM-DD` = data do carrossel
- `{slug}` = 2-4 palavras do tema em kebab-case (mesmo slug usado em `/criar-carrossel`)
- `slide-N.png` = N começando em 1, com zero-padding opcional (`slide-01.png` se ≥10 slides)

## Restrições

- Web fonts: usar **system fonts** (já configurado no template). Inter via CDN não é garantido em headless offline — então o template usa `-apple-system, "Segoe UI", "Helvetica Neue"...` por padrão. Se precisar Inter, embutir como `@font-face` com base64.
- **Não chamar OpenRouter** — esta skill é local-only.
- **Não confundir com `/gerar-imagem`** — aquela vai usar IA (Gemini/Flux) quando OpenRouter API key chegar. Esta é determinística.

## Fluxo

```
[ Skill chamada com flags --texto --autor ... --output ]
        ↓
[ 1. Carrega scripts/tweet-templates/default.html ] → tweet-imagem.mjs
        ↓
[ 2. Substitui placeholders {{TEXTO}}, {{AUTOR}}... ] → tweet-imagem.mjs
        ↓
[ 3. Resolve foto: path local → file://, url → manter, vazio → inicial ] → tweet-imagem.mjs
        ↓
[ 4. Playwright launch chromium 1080x1350 ] → tweet-imagem.mjs
        ↓
[ 5. page.setContent(html) + wait images ] → tweet-imagem.mjs
        ↓
[ 6. screenshot clip 1080x1350 → arquivo PNG ] → tweet-imagem.mjs
        ↓
[ 7. Caller (geralmente /criar-carrossel) recebe path do PNG ]
        ↓
   ⟶ FIM
```

## Integração com /criar-carrossel

`/criar-carrossel` chama `/tweet-imagem` 1x por slide (loop sequencial). Cada slide vira um PNG numerado na pasta do carrossel. Depois `@revisor-visual` audita e `@bug-hunter` valida arquivos antes de mandar pro Gimmick via `criar_conteudo`.

## Aprendizados

Registrar em `squads/dev/agentes/paginas-dev/aprendizados.md` qualquer ajuste de template/script (novo placeholder, fix de fonte, novo formato de output).
