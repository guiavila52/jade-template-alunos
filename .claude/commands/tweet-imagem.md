---
name: tweet-imagem
description: Gera imagem PNG 1080x1350 via render HTML para Playwright screenshot. 5 templates: tweet/X (default), quote-autoral, lista, antes-depois, story-sequencial. Use quando precisar criar slide individual de carrossel Instagram. Output PNG em workspace/output/imagens/. NAO usa IA — template HTML estatico, deterministico, gratuito.
model: claude-sonnet-4-5
---

# /tweet-imagem — render HTML → PNG (5 templates de slide)

Gera **um slide PNG 1080x1350** a partir de um template HTML estático + Playwright headless screenshot. Usado por `/criar-carrossel` pra renderizar cada slide do carrossel.

**Não usa IA generativa.** Determinístico, rápido (<3s/slide), gratuito.

## Templates disponíveis

| Template | Descrição | Quando usar | Placeholders principais |
|---|---|---|---|
| `default` | Print de tweet/X (card branco, foto+autor+handle+texto+data) | Slide com formato print de tweet, citação curta com chrome do X | `--texto` `--autor` `--handle` `--foto` `--data` `--numero` |
| `quote` | Quote autoral elegante (fundo preto + dourado, foto circular grande, frase em italic serifa) | Citação forte do operador (ou outro autor) com aparência editorial/livro | `--texto` `--autor` `--handle` `--foto` `--numero` |
| `lista` | Lista numerada (fundo claro, números dourados, items em cards) | "5 dicas pra...", "3 sinais de...", listas curtas (até 5 items) | `--titulo` `--item1`...`--item5` `--numero` |
| `antes-depois` | Divisão 50/50 horizontal (esquerda cinza = antes, direita dourada = depois) | Comparação problema vs solução, transformação | `--titulo` `--antes` `--depois` `--numero` |
| `story` | Narrativa sequencial (número GIGANTE outlined dourado + headline + sub) | Slides de storytelling em sequência ("1/7", "2/7"...), abertura de carrossel narrativo | `--numero` (formato `1/7`) `--headline` `--sub` |

## Quando usar (geral)

- Slides de carrossel Instagram (1080x1350)
- Citações, listas, comparações, narrativas em série
- Texto + tipografia + diagramação simples (sem ilustração)

**Não usar para:** ilustrações, ícones, fotos compostas, antes/depois com imagens. Pra esses, usar `/gerar-imagem` (Gemini/Flux via OpenRouter — ainda não disponível).

## Inputs (todas as flags)

| Flag | Obrigatório? | Default | Aplica a |
|---|---|---|---|
| `--template` | não | `default` | (escolhe o template — `default`, `quote`, `lista`, `antes-depois`, `story`) |
| `--texto` | sim p/ default,quote | — | default, quote |
| `--autor` | não | `{{NOME_OPERADOR}}` | default, quote |
| `--handle` | não | `@{{HANDLE_OPERADOR}}` | default, quote |
| `--foto` | não | fallback inicial | default, quote |
| `--numero` | não | (oculto) | todos (pill numérico — se vazio fica oculto) |
| `--data` | não | hoje pt-BR | default |
| `--titulo` | sim p/ lista,antes-depois | — | lista, antes-depois |
| `--item1`..`--item5` | não (mín 1 p/ lista) | — | lista (vazios são ignorados) |
| `--antes` | sim p/ antes-depois | — | antes-depois |
| `--depois` | sim p/ antes-depois | — | antes-depois |
| `--headline` | sim p/ story | — | story |
| `--sub` | não | — | story |
| `--output` | sim | — | todos |
| `--template-file` | não | (auto) | override completo do path do template HTML |

Texto suporta `**bold**` e `\n` em qualquer flag de conteúdo.

## Pipeline

1. Carrega template HTML em `Páginas Astro {{NOME_OPERADOR}}/scripts/tweet-templates/{template}.html`
2. Substitui placeholders conforme template selecionado
3. Lança Playwright headless Chromium em viewport 1080x1350
4. `page.setContent(html)` + espera imagens carregarem
5. Screenshot com clip exato 1080x1350
6. Salva em path indicado (cria diretório se não existe)

## Como rodar

Sempre dentro de `Páginas Astro {{NOME_OPERADOR}}/` (onde Playwright está instalado).

### default (tweet/X)
```bash
cd "Páginas Astro {{NOME_OPERADOR}}"
node scripts/tweet-imagem.mjs \
  --template default \
  --texto "A maioria dos negócios digitais morrem porque o **dono virou o gargalo**" \
  --autor "{{NOME_OPERADOR}}" --handle "@{{HANDLE_OPERADOR}}" \
  --foto /caminho/foto-perfil.jpg \
  --numero "1/5" \
  --output "../Squad Empresa {{NOME_OPERADOR}}/workspace/output/imagens/2026-05-07/teste/slide-1.png"
```

### quote (autoral elegante)
```bash
node scripts/tweet-imagem.mjs \
  --template quote \
  --texto "Squad de agentes existe pra **destravar o dono**" \
  --autor "{{NOME_OPERADOR}}" --handle "@{{HANDLE_OPERADOR}}" \
  --foto /caminho/foto-perfil.jpg \
  --numero "2/7" \
  --output ".../slide-2.png"
```

### lista (até 5 items)
```bash
node scripts/tweet-imagem.mjs \
  --template lista \
  --titulo "5 sinais de que você **virou o gargalo**" \
  --item1 "Toda decisão passa por você" \
  --item2 "Time trava esperando aprovação" \
  --item3 "Você responde mais Slack do que faz estratégia" \
  --item4 "Crescimento exige mais horas suas" \
  --item5 "Sair de férias trava operação" \
  --numero "3/7" \
  --output ".../slide-3.png"
```

### antes-depois (problema vs solução)
```bash
node scripts/tweet-imagem.mjs \
  --template antes-depois \
  --titulo "Operação travada vs **squad rodando**" \
  --antes "Você no Slack 12h/dia, decisão dura uma semana, lançamento empurrado." \
  --depois "Squad resolve 70% do operacional, decisões no mesmo dia, lançamento na data." \
  --numero "4/7" \
  --output ".../slide-4.png"
```

### story (narrativa sequencial)
```bash
node scripts/tweet-imagem.mjs \
  --template story \
  --numero "1/7" \
  --headline "O **dono virou o gargalo** — e o negócio parou de crescer" \
  --sub "Toda empresa digital chega num teto onde escalar significa o dono trabalhar mais. Esse teto tem nome: gargalo humano." \
  --output ".../slide-1.png"
```

## Convenção de output

Sempre em `workspace/output/imagens/YYYY-MM-DD/{slug}/slide-N.png`.

- `YYYY-MM-DD` = data do carrossel
- `{slug}` = 2-4 palavras do tema em kebab-case (mesmo slug usado em `/criar-carrossel`)
- `slide-N.png` = N começando em 1, com zero-padding opcional (`slide-01.png` se ≥10 slides)

## Restrições

- **Web fonts:** usar **system fonts** (já configurado em todos os 5 templates). Inter via CDN não é garantido em headless offline. Se precisar Inter, embutir como `@font-face` com base64.
- **Cormorant Garamond proibido** em qualquer dígito (Regra absoluta — bug histórico #188). Templates usam Georgia em italic quando precisam de feel literário.
- **Não chamar OpenRouter** — esta skill é local-only.
- **Não confundir com `/gerar-imagem`** (futuro) — aquela vai usar IA. Esta é determinística.
- **Tamanho de output:** alvo <500KB/PNG. Templates com gradientes radiais (`story`) podem chegar a ~530KB — aceitável (Instagram aceita até 8MB).

## Fluxo

```
[ Skill chamada com flags --template --texto --output etc ]
        ↓
[ 1. Resolve template: default|quote|lista|antes-depois|story ] → tweet-imagem.mjs
        ↓
[ 2. Carrega scripts/tweet-templates/{template}.html ] → tweet-imagem.mjs
        ↓
[ 3. Substitui placeholders específicos do template ] → tweet-imagem.mjs
        ↓
[ 4. Resolve foto (se aplicável): path → file://, url → http, vazio → inicial ]
        ↓
[ 5. Playwright launch chromium 1080x1350 ] → tweet-imagem.mjs
        ↓
[ 6. page.setContent(html) + wait images ] → tweet-imagem.mjs
        ↓
[ 7. screenshot clip 1080x1350 → arquivo PNG ] → tweet-imagem.mjs
        ↓
[ 8. Caller (geralmente /criar-carrossel) recebe path do PNG ]
        ↓
   ⟶ FIM
```

## Integração com /criar-carrossel

`/criar-carrossel` chama `/tweet-imagem` 1x por slide (loop sequencial). Cada slide pode usar template diferente (ex: slide 1 = `story`, slide 2-5 = `lista`/`quote`, slide 6 = `antes-depois`, slide 7 = `default`). Depois `@designer-revisor` audita e `@analista-qa` valida arquivos antes de mandar pro {{FERRAMENTA_CONTEUDO}} via `criar_conteudo`.

## Aprendizados

Registrar em `squads/dev/agentes/desenvolvedor-frontend-dev/aprendizados.md` qualquer ajuste de template/script (novo placeholder, fix de fonte, novo formato de output, novo template).

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro operador testar — testa antes.
