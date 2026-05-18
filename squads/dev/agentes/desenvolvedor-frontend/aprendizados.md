# aprendizados.md — desenvolvedor-frontend (squad-dev)

> Lições do executor: Astro 6, sliders, sticky, iframes, pixel perfect, design systems.
> Backup completo (2984 linhas, narrativo) em
> `workspace/historico-mudancas/2026-05-16-aprendizados-enxugados/desenvolvedor-frontend-original-pre-enxugamento.md`.
> Reincidência = bug processual (Regra §5). Skills: `/codar-pagina`, `/migrar-pagina`, `/testar-pagina`, `/revisar-codigo-pagina`, `/publicar-pagina`.

---

## SCROLL / STICKY / OBSERVERS

### #131 — Scroll global é gate inviolável
**Regra:** Páginas com `position:sticky`, IO, `scroll`/`resize` listener ou GSAP ScrollTrigger exigem rolar top→bottom mobile (390x844) E desktop (1440x900) antes de entregar (Playwright `mouse.wheel` 8x, scroll monotônico, flap ≤ 3 toggles). Markup grep não substitui.
**Citação {{OPERADOR}}:** "Bati scroll e o site ficou todo tremendo. Como é que o agente que fez a revisão deixou passar furo desse?"

### #163 — Estados visuais por classe, nunca global no base
**Regra:** Propriedade CSS com 2 estados (collapsed/expanded) declarada por classe estado, NUNCA global no elemento base (cascade ofusca filho). Ex: `.elem { min-height: 480px }` + `.elem.is-collapsed { min-height: 64px }`.

### Sticky com altura variável → `overflow-anchor: none` + `min-height` reservado
**Regra:** Sticky cuja altura muda no toggle precisa reservar altura via `min-height` no container externo E `overflow-anchor: none` no ancestral. Senão browser ajusta scrollY → listener roda de novo → loop infinito (~21 toggles em 2s).

### IO defasado pra direção de scroll — use rAF + getBoundingClientRect
**Regra:** Pra "passei desse ponto?" use scroll listener passive + `requestAnimationFrame` + `getBoundingClientRect()`. `entry.boundingClientRect` chega async/defasado. IO serve pra "está visível?", não direção.

### Antipadrões scroll (REPROVA)
**Banido:** scroll listener síncrono mexendo classe/estilo; animar `top`/`height` em scroll handler (use `transform`); IO alterando o próprio observado sem rAF; sticky encadeado no mesmo container; rail horizontal sem `touch-action: pan-x`.

---

## SLIDERS / RAIL

### Slider canônico — rAF + drag mouse+touch + click guard
**Regra:** Sempre `<Slider mode="rail|marquee">` (componente em `src/components/Slider.astro`). Auto-scroll rAF + drag mouse/touch que sobrescreve auto + retoma. `cursor: grab`/`grabbing`, `user-select: none`, `touch-action: pan-y`. Rail inline custom (`<div data-rail>`) BANIDO.
**Banido:** hover-pause `:hover { animation-play-state: paused }`; mouseenter/leave com flag `hovered`; slider sem drag; mouse drag sem touch drag paritário.
**Validação:** `scripts/test-slider-drag.mjs` Playwright headless CDP `Input.dispatchTouchEvent` (page.touchscreen não suporta drag, só tap). Mede DURANTE drag, não antes/depois.
**Citação {{OPERADOR}}:** 3 rejeições em sliders sem drag.

### Drag macio — pointer capture + threshold + click guard
**Regra:** `rail.setPointerCapture(e.pointerId)` (não perde drag fora do container) + threshold 6px pra distinguir click/drag + momentum decay 0.94 + `addEventListener('click', preventDefault, true /*capture*/)` quando `dragHappened` (senão filho consome antes). Suavização velocity: 70% novo + 30% antigo.

### CSS escopado Astro não pega filho slot — use `:global()`
**Regra:** No `.astro` consumidor, customizar interno do componente exige `:global(.gui-slider__rail) { ... }`.

### Bug template literal — `<script is:inline>{`...`}</script>` não executa
**Regra:** Chaves Astro com template literal emitem o texto como statement. Use `<script is:inline>código direto</script>` sem `{` `}` `` ` ``. Grep `<script is:inline>{` deve retornar 0.

---

## IFRAMES (GHL/Typeform/Calendly)

### Iframe NUNCA tem container visual concorrente
**Regra:** Wrapper Astro tem APENAS layout (largura, margin, overflow visible). Sem border/background/padding/border-radius — decoração é do iframe. Caixa+caixa quebra o container.
**Citação {{OPERADOR}}:** "Olha o tamanho desse buraco" (sobre /mentoria com min-height fixo herdado de /consultoria).

### Altura iframe validada via Playwright contra URL real
**Regra:** Antes de definir `min-height`, abrir URL do iframe em Playwright com viewport final (a calculada pelo CSS) + UA correto (iPhone pra mobile, macOS Chrome pra desktop — GHL detecta UA). Medir `document.documentElement.scrollHeight` após 6s + reservar +150px. `min-height` = floor de fallback sem JS, NUNCA valor "esperado".

### GHL handshake é proprietário — `form_embed.js` + watchdog 4s
**Regra:** Use `<script src="https://link.msgsndr.com/js/form_embed.js">` oficial (não reimplementar postMessage custom). Watchdog 4s força `opacity:1;visibility:visible` se 3rd-party cookies bloqueados ou headless.

### Retrofit sistêmico — auditar TODAS as páginas com iframe
**Regra:** Fix de bug em iframe em página X → `grep -rln "<iframe\b" src/pages/ --include="*.astro"` + validar cada. Entrega completa = página citada + retrofit em todas + skill atualizada + screenshot de cada.

---

## PIXEL PERFECT / MIGRAÇÃO

### Migração = clone literal, NÃO reinterpretar design
**Regra:** Skill `/migrar-pagina` = modo clone. `Base.astro` esqueleto, `aurora={false}` + `footer={false}` desligando opcionais conflitantes. CSS/HTML/JS literais; componentes só se renderizam idênticos. CSS aparentemente buggy (regras inócuas) NÃO consertar — "consertar" muda comportamento real.
**Citação {{OPERADOR}}:** "Tem que ser 100% pixel perfect, ser uma cópia idêntica."
**Validação:** `validate-visual.mjs --compare` mobile+desktop < 5% (item 13 BLOCKER bateria #15).

### Reset prévio + bodyClass="" primeiro
**Regra:** Primeiro passo: `bodyClass=""` + reset (`body { line-height: normal; font-family: inherit }`). Sem isso, diff fica 5-15% por shift acumulado de font/line-height herdados. COM, diff <2%.

### Referência visual aprovada = replicar ANATOMIA
**Regra:** Briefing aponta HTML/Figma/screenshot aprovado → Astro mantém MESMA anatomia (sticky/fixed, scroll direction, SVG conectores, hierarquia). Trocar implementação técnica OK; anatomia = REJEIÇÃO. Listar 5-7 pontos de anatomia + confirmar antes de codar. Divergir = perguntar {{OPERADOR}} ANTES.
**Citação {{OPERADOR}}:** "Gostei daquele que mostra a Jade com linhas, conectada nos squads, carrossel. Fica mais visual."

### Receita HTML estático → Astro pixel perfect
**Regra:** (1) `curl -A "Mozilla..." [url] > /tmp/orig.html`; (2) `python3 /tmp/migrate_page.py slug title desc fonts`; (3) `npm run build` exit 0; (4) `curl localhost/[slug]` 200; (5) `validate-visual.mjs --compare` < 5% mobile+desktop; (6) screenshots em `workspace/output/paginas/`.

### Framer pós-hidratação não migra por clone HTML
**Regra:** Snapshot preserva markup, NÃO runtime — sliders/drag/eventos JS viram estáticos. Triage: quick-win (h1, alt, GTM) vs requer migração completa. Não prometer fix de runtime sem migração.

### Remover `<link rel=modulepreload>` órfãos pós-snapshot
**Regra:** Auditar refs a runtime externo (`<link rel=modulepreload>`, `<script type=module>`). Se path não existe em `/public/<slug>/assets/`, remover via regex. Playwright Network 404+ = 0 antes de entregar. /automacoes tinha 16 .mjs 404 no console.

### Find/replace URL→path com regex restrito por extensão
**Regra:** Find/replace de asset usa regex com extensão (`\.(png|jpg|webp|svg|mov|mp4|webm|woff2?|ttf|otf|ico|pdf)`), NUNCA `https://sites\.{{handle}}\.com/...` genérico (pega canonical/nav/comentário). Skip de comentário. Constantes `const IMG = "..."` exigem segundo regex.

---

## ASSETS EXTERNOS / LOGOS

### Clonar SEMPRE assets externos pra `public/`
**Regra:** Todo asset com URL absoluta `https://sites.{{handle}}.com/[slug]/...` precisa estar em `public/[slug]/img/`. Em projeto Vercel novo, sem clonagem = 404 total.
**Comando:** `grep -hoE 'src="https://sites\.{{handle}}\.com/[^"]+\.(jpg|png|webp|svg|mov|mp4)"' src/pages/[slug]/index.astro | sort -u` (delimitador aspa, aceita espaço — `banco do brasil.png`).
**Validação tripla:** `file` (binário, não HTML 404 mascarado) + `test -s` (>0 bytes) + `curl localhost:4321/[caminho]` (200).
**[CRITICO]** Diff visual MASCARA — quando original e novo puxam mesma CDN, "PASS" enganoso. Validar via Playwright `page.route` bloqueando domínio antigo.

### Logos: SVG oficial + frame branco, nunca letra-em-quadrado
**Regra:** Ferramenta/parceiro renderiza com logo oficial. Fontes: (1) `cdn.simpleicons.org/<slug>`; (2) `cdn.jsdelivr.net/npm/simple-icons@v11/icons/<slug>.svg`; (3) brand pack oficial; (4) favicon. Sem brand kit = placeholder dourado + pendência (NUNCA inventar logo). Marcas BR (Notazz, Inter, Supermetrics) raramente em simpleicons.
**Render:** `<img src="/logos/<slug>.svg" loading="lazy" decoding="async" width="40" height="40" />` em frame `background: rgba(255,255,255,0.94); padding: 6px`. Sem fundo claro logos coloridas somem em pages dark.
**Validação:** `file *.svg` SVG; `head -c 100` sem `<!DOCTYPE html>`; size > 100 bytes.

---

## TIPOGRAFIA

### Auditoria de fontes obrigatória em migração
**Regra:** `node scripts/audit-fonts.mjs <urlOrig> http://localhost:4321/[slug]` → 0 mismatches em 17+ seletores ANTES de marcar migração entregue. Diff visual ~5% NÃO captura fonte errada de tamanho parecido.

### Tag selector global vaza — use `!important` no `<style is:inline>` da página
**Regra:** `h1,h2,h3,h4 { font-family: var(--font-display) }` em `global.css` vaza pra todas. Em migração pixel perfect: `<Fragment slot="head"><style is:inline> html body h1..h6 { font-family: 'Inter' !important }`. No Astro dev, Vite injeta global.css DEPOIS do inline — specificity igual = global vence por ordem. `!important` aqui não é code smell.

### Comentário CSS sempre plano, NUNCA aninhado
**Regra:** `/* texto /* nested */ resto */` quebra parser silenciosamente — `*/` interno fecha externo, regras seguintes viram tokens inválidos e somem do `CSSStyleSheet`. Diagnóstico: `document.styleSheets[i].cssRules` mostra que sumiu.

### Syne weight ≤ 600 em hero/h1/h2/h3 grandes
**Regra:** Syne com font-size > 3.5rem → weight máximo **600** (acima distorce/achata). Letter-spacing nunca abaixo de -0.02em em hero grande. Mais peso visual = `.headline-gradient`, não aumentar weight. Exceção: números puros (`0-9 R$`) podem usar 800 — glyphs numéricos não distorcem. Antes de definir hero, copiar padrão de `/reverso` (`clamp(36px, 5vw, 58px)` + weight 700).

### Cormorant NUNCA em texto pequeno / dígitos
**Regra:** Cormorant removida. `--font-display` agora é Syne, só em h1/h2/h3 (≥ 20px). Texto pequeno/parágrafo/badge/label/número/botão = DM Sans. Cormorant peso 400 some em mobile.

### Tipografia clamp fluida obrigatória
**Regra:** Hero h1 `clamp(40px, 6vw, 68px)` weight 600 line-height 1.08. H2 `clamp(30px, 4vw, 48px)` weight 700 line-height 1.15. Lead `clamp(17px, 1.8vw, 20px)`. Font-size fixo em heading = REPROVA.

---

## HIPERLINKS

### Hiperlink na palavra, NUNCA URL em parênteses
**Regra:** Menção a produto/canal do {{OPERADOR}} ({{EMPRESA_COFUNDADA}}, {{EMPRESA_NEGOCIO}}, Reverso, Consultoria, Mentoria, Imersão, ClickUp 8x, Automações, YouTube) = `<a href="https://{{handle}}.com/[slug]" class="link-inline" target="_blank" rel="noopener">palavra</a>`. URL em parênteses como texto = REPROVA. Validação: grep `{{handle}}\.com` em texto puro = 0.
**Citação {{OPERADOR}}:** "Não faz sentido botar entre parênteses como texto que a pessoa vai ter que copiar e colar. Vacilo."

### Nunca inventar slug — verificar via curl
**Regra:** Slug não confirmado em `project_hiperlinks_padrao.md` → `curl -sL -w "%{url_effective}" https://{{handle}}.com/[slug]`. 404 = `TODO(jade)` no código + perguntar {{OPERADOR}}. Correto: `magicaonline` (não `magica`).

---

## GTM

### GTM-NN36ZRZ obrigatório em TODA página (vem do Base.astro)
**Regra:** Script no `<head>` cedo + noscript iframe após `<body>` open. Validação canônica usa `grep -o ... | wc -l` (conta ocorrências), NUNCA `grep -c` (conta linhas — HTML minificado de prod é uma linha, subconta).
```bash
echo "$HTML" | grep -o 'GTM-NN36ZRZ' | wc -l  # >= 2
echo "$HTML" | grep -o 'googletagmanager.com/gtm.js' | wc -l  # >= 1
echo "$HTML" | grep -o 'googletagmanager.com/ns.html' | wc -l  # >= 1
```

### Console errors podem vir de GTM, não do código
**Regra:** Investigar origem antes de mexer no código: (1) `grep -rn src/`; (2) `curl URL | grep`; (3) `curl googletagmanager.com/gtm.js?id=GTM-NN36ZRZ | grep`. Scripts tracking via GTM que falham na init geralmente são legacy.

---

## ESTRUTURA

### Base.astro renderiza Footer/Header default — NÃO duplicar
**Regra:** Base tem `footer=true`/`header=true` default. NUNCA `<Footer />`/`<Header />` manual em pages que estendem Base — passa `footer={false}` se precisar desligar. Validação: `grep -c '<Footer' src/pages/[slug]/index.astro` = 0.

### Componente novo só se aparece em ≥ 2 páginas
**Regra:** Padrão visual em < 2 páginas = `<style>` local. Componente novo = responsabilidade (MAPA, design system, manutenção). /reverso (16 seções) coube em `Base + Section + Button + FAQ + LogoSlider`.

### Backup `.preFix{N}` antes de qualquer edição estrutural (§9)
**Regra:** Sem backup `.preFix{tarefa}` ou `.preFix-{onda}` em arquivo original = REPROVA.

---

## REVISÃO (§4 + §6)

### Auto-revisão técnica não basta — bateria formal obrigatória
**Regra:** Checklist mental é permeável. `/testar-pagina` com 12 itens (build, curl, grep, Playwright). Aprovação do `/revisar-codigo-pagina` sozinha NÃO basta — precisa 100% verde na bateria.
**Citação {{OPERADOR}}:** "Documento preto e branco" (após auto-revisão aprovar /consultoria com 5 erros).

### Smoke test Playwright = gate inviolável pra interação
**Regra:** Sticky/collapse/drag/animation/scroll-trigger só valem com Playwright validando comportamento real. Markup grep + leitura de código NÃO substituem rodar. Templates: `scripts/test-jade-collapse-117.mjs`, `scripts/test-slider-drag.mjs`.

### Diff visual com diagnóstico por bucket
**Regra:** Diff alto sem elementos faltando = shift acumulativo. Dividir altura em buckets 1500-2000px, em cada um procurar offset Y entre [-200, +200] que minimize diff. Salto abrupto revela divergência estrutural.

### Agent travado > 30min — Jade verifica e re-despacha
**Regra:** Status "em andamento" no tarefas.md NÃO é evidência. Sem sinal > 30min → mtime do arquivo alvo + grep da classe esperada + re-despacha. Adendo após despacho NÃO chega ao agent rodando — fix em iteração separada após voltar.

---

## DESIGN SYSTEMS (3 oficiais)

### Premium (mentoria/reverso) — high-ticket editorial
**Tokens:** `--color-bg: #000`; `--color-gold: #c9a961`; `--ease: cubic-bezier(0.22, 1, 0.36, 1)`; `--section-gap: 96px`; `--radius: 16px`. Syne + DM Sans.
**Padrões:** aurora blobs 4 layers (`blur(100px); opacity:0.06; animation 20s aurora-float`); glass `rgba(255,255,255,0.04) + border 0.08 + backdrop-filter blur(12px)`; shimmer `::after` btn primário; reveal `.reveal` opacity 0 + translateY 24px → visible delays incrementais 0.1s steps.
**Doc:** `Páginas Astro {{NOME_OPERADOR}}/DESIGN-SYSTEM.md` + `workspace/design-systems/{{handle}}-premium.md`.

### {{APP_PESSOAL}} (SaaS) — produto energético
**Tokens:** `#030014` deep purple (NÃO black); multi-cor `#a78bfa`/`#f0abfc`/`#fb923c`; border `rgba(167,139,250,0.30)`. Hero `clamp(40px, 6vw, 76px)` tracking `-0.035em` line-height 1.02. Badges UPPERCASE `tracking-[0.2em]`. Motion 200ms snappy ease-out Tailwind.

### Clean (Resend-based) — técnico-acolhedor
**Tokens:** `#09090b` cinza escuro + azul único `#3b82f6`. Inter weights 400-600. Motion 300-400ms. Bordas `rgba(255,255,255,0.06)`. SEM glassmorphism. Spacing respirável 64-80px. Code blocks Commit Mono. NÃO usar em landing high-ticket.

### Pegadinhas cross-system
**Regra:** Aurora blob precisa `overflow: hidden` no container. Backdrop-filter NÃO funciona sem `background`. Shimmer btn exige `overflow: hidden`. Reveal delay sempre incremental 0.1s (nunca aleatório). Letter-spacing negativo só em headings >40px. FAQ rotate(45deg) só em "+", não seta.

---

## STACK

### Astro 6 + Tailwind v4 → PostCSS, NÃO `@tailwindcss/vite`
**Regra:** Astro 6 (Vite 7 rolldown/oxc) quebra com `@tailwindcss/vite@4.2.x` (`Missing field tsconfigPaths`). Use `@tailwindcss/postcss` + `postcss.config.mjs` raiz. Reavaliar a cada release.

### Astro hot-reloada novas rotas — não matar dev server
**Regra:** Criar `src/pages/[slug]/index.astro` e `curl /[slug]` retorna 200 em ~2s. `npm run build` em terminal separado valida sem afetar dev.

### Panzoom v4.6 `startScale` é BUG — CSS transform manual + override
**Regra:** Panzoom 4.6.2 ignora `startScale`, `.zoom(s, {force, animate:false})`, `.setStyle`, `.zoomOut()` iterativo. Workaround: `canvas.style.transform = scale(fit)` ANTES de criar Panzoom + override `.zoomIn/.zoomOut/.reset/.getScale`. Panzoom fica só pra pan/drag.
**Validação:** Playwright medindo `.zoom-level` < 95% no `window.load` + 1500ms.

### GSAP recomendado, não obrigatório — não em primeira dobra com `opacity:0`
**Regra:** GSAP é lib sugerida. Pixel perfect replica EXATO da original (CSS vs GSAP). `gsap.from(opacity:0)` SÓ abaixo da dobra — primeira dobra usa `.reveal` + IO ou `gsap.from(y:16)` sem opacity. Screenshot full-page fica preto se ScrollTrigger ainda não disparou.

---

## PROCESSO

### Páginas públicas NÃO expõem detalhes técnicos (MCP/API/lib)
**Regra:** Vitrine fala "ferramentas conectadas"/"integração", nunca "MCP"/"API"/protocolo. Classes CSS refletem função (`.tool-card` > `.mcp-card`). Mudança arquitetural → auditar TODAS as páginas (prod + arquivadas).

### Skills manipulando template externo AUDITAM antes de assumir
**Regra:** `/configurar-squad`, `/migrar-pagina`, `/publicar-jade` fazem auditoria dinâmica (grep/curl/API) ANTES de assumir estrutura fixa. Teste E2E em clone/snapshot REAL antes de marcar madura. Memória: `feedback_skill_template_sync.md`.

### Migração de nomenclatura preserva contexto histórico
**Regra:** Substituições NÃO apagam histórico — adicionar nota "(data: X descontinuado, migração pra Y)". Script Python regex controlado. `.claude/*` via Bash heredoc/sed/python — NUNCA Edit/Write (Regra §11).

### GHL API v2 NÃO suporta criar email campaign — UI híbrido
**Regra:** POST `/marketing/campaigns` = 404. Skill `/disparar-newsletter` gera HTML inline CSS pro builder GHL + instruções de cola; {{OPERADOR}} dispara via UI (~2 min); skill registra disparo no {{APP_PESSOAL}} API REST. Secret em `app/.env.local` (Regra §8).

### Render HTML rich de markdown (newsletter)
**Regra:** Storage ({{APP_PESSOAL}} API) separado de template (squad). Skill `/renderizar-newsletter-html` gera HTML table-based 600px email-safe (header logo 200px, h1 32px, preheader itálico, assinatura 2 cols com foto circular, hyperlinks `#c9a961`, tags GHL `{{contact.first_name}}` preservadas). Detecção auto produção via `curl -I` → file:// fallback.

---

## 🔴 REINCIDENTE 17/05/2026 — Logo header invisível (3ª vez no mesmo dia)

**Bug recorrente:** logo header `/assets-gui/logo-gui-assinatura-fundo-escuro.png` renderiza com dimensões erradas (invisível, 0px, cortado, ou tamanho gigante esticado).

**Histórico das 3 ocorrências:**
1. Commit `6f3dfae` — logo width=auto sem height fixo → renderizou gigante quebrado
2. Commit `0f3b91e` — fix com !important + max-width — pareceu OK mas designer-revisor depois pegou que estava invisível mobile
3. Commit `???` (3a vez 17/05 tarde, pipeline canonico) — {{OPERADOR}} voltou e logo quase invisível

**CAUSA RAIZ identificada:**
- PNG da assinatura é desenho fino branco em fundo transparente
- Quando o container header é estreito + sem padding adequado, o PNG renderiza com width MUITO pequeno (parece traço quase invisível)
- O template-clean.astro pode ter um wrapper apertado por default

**FIX OBRIGATÓRIO (aplicar SEMPRE em qualquer página que use a assinatura no header):**

```css
.site-header img[alt*="{{NOME_OPERADOR}}"],
.header-logo img,
header img[src*="logo-gui-assinatura"] {
  height: 36px !important;
  width: auto !important;
  min-width: 140px !important;   /* CRÍTICO: garante PNG renderiza largo o suficiente */
  max-width: 240px;
  display: block;
  object-fit: contain;
  object-position: left center;
}

@media (max-width: 768px) {
  .site-header img[alt*="{{NOME_OPERADOR}}"],
  .header-logo img,
  header img[src*="logo-gui-assinatura"] {
    height: 28px !important;
    min-width: 110px !important;
  }
}
```

**MIN-WIDTH é o segredo.** Sem ele, mesmo com height: 36px, o navegador pode calcular width muito pequeno se o container for estreito.

**Validação obrigatória ANTES de devolver:**
- Playwright `getBoundingClientRect()` da imagem: `width >= 140px desktop, >= 110px mobile`
- Visualmente: assinatura LEGÍVEL (não traço fino), à esquerda, padding do header em volta
- Screenshot JPEG quality 70 (anti-API-bloat)

**Anti-reincidência:**
- Esse CSS deve ir EMBUTIDO no template-clean.astro / template-premium.astro / template-{{app_pessoal}}.astro (todos templates que usam header com assinatura).
- Designer-revisor passada 1 estética DEVE pegar logo invisível como CRITICAL bloqueante na 1ª inspeção humana — não esperar {{OPERADOR}} apontar.

**Se reincidir 4ª vez:** parar pipeline, escalar pro {{OPERADOR}}, repensar template canonico do header.

---

## 🔴 INCIDENTES 17/05/2026 TARDE — 3 padrões reincidentes

### 1. Form GHL iframe NUNCA em wrapper com altura limitada
**Bug:** wrapper com `max-height` ou `overflow:auto` cria barra de rolagem interna que corta o form.
**Correção canônica:**
- Iframe form GHL deve renderizar na altura NATIVA dele (não limitar)
- Wrapper deve ter `min-height` calculado pra acomodar form inteiro (~720px desktop, ~640px mobile)
- NUNCA `max-height` ou `overflow:hidden/auto` no wrapper do iframe
- Watchdog JS continua válido pra combater form_embed.js esconder
**Como aplicar:** se precisa "frame visual" em volta do form, usar `padding` + `border` no wrapper, NUNCA `max-height`.

### 2. Microtexto plural/singular ("1 agente" vs "X agentes")
**Bug:** renderizar "1 agentes" (plural errado).
**Correção canônica:**
```js
const label = count === 1 ? 'agente' : 'agentes';
```
Aplicar em TODA pluralização dinâmica de UI (agentes, skills, squads, etc).

### 3. Organograma DEVE seguir DESIGN.md (assimétrico, não grid)
**Bug:** dev implementou grid simétrico 5+3 cards iguais, contradizendo DESIGN.md que pedia "órbita assimétrica" + "Jade GRANDE central".
**Causa raiz:** dev tratou DESIGN.md como sugestão, não como spec.
**Correção canônica:**
- DESIGN.md é SPEC, não inspiração. Fidelidade ao layout descrito.
- Se DESIGN.md diz "Jade central GRANDE + 8 squads em órbita assimétrica", implementar literal:
  - Jade no centro com tamanho maior (ex: 160x160px vs cards 200x100px)
  - 8 cards posicionados com `position: absolute` em ângulos diferentes (não grid)
  - OU SVG/CSS grid com células de tamanhos DIFERENTES
- ANTI-AI-SLOP §"sem 4 cards iguais" é violação grave do template-clean.astro

### 4. 🔴 LOGO HEADER — 4ª reincidência mesmo dia
**Padrão claro:** PNG da assinatura precisa CSS no template-clean canônico, não nas páginas individuais.
**Decisão estrutural:** próxima vez que reincidir = pausar pipeline + escalar pro {{OPERADOR}} + repensar Header component do template (talvez extrair pra `src/components/HeaderClean.astro` com tamanho hardcoded).
**Validação obrigatória ANTES de devolver qualquer página:**
```js
const logo = document.querySelector('header img');
const rect = logo.getBoundingClientRect();
if (rect.width < 100 || rect.height < 24) throw new Error('LOGO INVISIVEL');
```

---

**Anti-reincidência geral:**
- Designer-revisor passada 1 estética é GATE — não passar sem ler DESIGN.md primeiro e comparar cada dobra implementada vs especificada
- Se dev não consegue implementar DESIGN.md literal, escalar pra Jade (não improvisar layout diferente)

---

## 🔴 5ª REINCIDÊNCIA — Logo header (escalado, problema sistêmico)

17/05 noite — {{OPERADOR}} voltou e apontou logo header quebrada NOVAMENTE. CSS com `min-width: 140px` e `height: 36px !important` está no código mas browser renderiza como traço fino quase invisível.

**Causa raiz suspeita:** o PNG `/assets-gui/logo-gui-assinatura-fundo-escuro.png` é uma assinatura cursiva FINA e FRÁGIL — qualquer largura abaixo de 180-200px renderiza como traço quase invisível. CSS forçando 140px width não é suficiente.

**Fix definitivo (5ª vez):**
- Aumentar `min-width: 200px` (não 140px)
- height pode ficar 36px desktop / 32px mobile
- Considerar trocar PNG por SVG inline (mais nítido em qualquer tamanho)
- OU trocar por logo "{{NOME_OPERADOR}}" texto + foto circular pequena (mais robusto)

Se 6ª reincidência → trocar PNG por componente HeaderLogo.astro reusável com width hardcoded + fallback texto.
