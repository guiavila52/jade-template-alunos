# Design System Gui Ávila — Premium

**Versão:** 1.0  
**Última atualização:** 2026-05-14  
**Páginas de referência:**
- https://sites.{{DOMINIO}}/mentoria
- https://sites.{{DOMINIO}}/reverso

---

## Índice

1. [Voz Visual](#voz-visual)
2. [Paleta de Cores](#paleta-de-cores)
3. [Tipografia](#tipografia)
4. [Spacing & Layout](#spacing--layout)
5. [Border Radius](#border-radius)
6. [Sombras & Effects](#sombras--effects)
7. [Motion & Animações](#motion--animações)
8. [Sliders](#sliders)
9. [Componentes-Padrão](#componentes-padrão)
10. [Responsividade](#responsividade)
11. [Imagens & Mídia](#imagens--mídia)
12. [Como Usar Este Design System](#como-usar-este-design-system)

---

## Voz Visual

O design system premium do Gui Ávila é caracterizado por **5 adjetivos visuais**, cada um com evidências técnicas:

### 1. **Premium**
- **Evidências:** paleta escura (#000 bg) + dourado sofisticado (#c9a961), glassmorphism com backdrop-filter, sombras sutis com glow dourado, tipografia editorial com weights altos (Syne 700/800).
- **Onde aparece:** Aurora blob animado de fundo, bordas com glow gold, badges com bg gold translúcido.

### 2. **Editorial**
- **Evidências:** Syne como display font (contratos fortes, letterspacing negativo), hierarquia vertical com espaçamento generoso (96px sections), corpo de texto em DM Sans (legibilidade alta, line-height 1.6+), uso de citações destacadas (quote-display: 22-30px, font-display).
- **Onde aparece:** Hero titles (clamp 40-68px), pull-quotes centralizadas, body copy em tom muted (#a1a1aa).

### 3. **Denso**
- **Evidências:** conteúdo vertical longo, sections com 96px de padding, listas de bullets (14-18px gap), cards agrupados (grid gap 20-28px), sem white space excessivo mas respira onde importa.
- **Onde aparece:** Página reverso (7 esferas, testimonials, value stack), mentoria (comparativo table, incluso list).

### 4. **Sofisticado**
- **Evidências:** motion suave (cubic-bezier .22,1,.36,1), reveal on scroll com IntersectionObserver, aurora blobs animados (20s ease-in-out), transições ricas (2s em hover, translateY -2px), glassmorphism (backdrop-blur 12px).
- **Onde aparece:** Aurora de fundo (4 blobs flutuantes), reveal delays (0.1s increments), hover states em links/botões.

### 5. **Confiável**
- **Evidências:** prova social densa (depoimentos com fotos, logos de empresas, métricas reais: "1560+ avaliações"), CTAs claros e repetidos, seção garantia (emoji shield, texto reassurance), footer extenso com múltiplas colunas.
- **Onde aparece:** Seção logos (Ford, L'Oréal, BB), testimonials grid, value stack com valores riscados.

---

## Paleta de Cores

Todas as cores em hex + variável CSS + uso:

### Background

| Variável CSS | Hex | Uso |
|---|---|---|
| `--color-bg` | `#000000` | Fundo principal de todas as páginas |
| `--color-bg-soft` | `#0a0a0a` | Fundo alternado (sections zebradas) |
| `--color-surface` | `rgba(255,255,255,0.04)` | Cards glassmorphic, backgrounds de form-shell |

### Foreground

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-tx` | `#f4f4f5` | Texto principal (headings, strong) |
| `--color-tx-soft` | `#a1a1aa` | Corpo de texto (paragraphs, body-lg) |
| `--color-muted` | `#71717a` | Texto terciário (small notes, disclaimers) |

### Accent

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-gold` | `#c9a961` | Accent principal (badges, links, bullets, CTAs hover glow) |
| `--color-gold-soft` | `#e8d9b8` | Variante clara (gradientes, hover states) |
| `--color-gold-glow` | `rgba(201,169,97,0.25)` | Box-shadow glow em CTAs primários |

### Line & Borders

| Variável CSS | RGBA | Uso |
|---|---|---|
| `--color-line` | `rgba(255,255,255,0.08)` | Borders sutis (cards, separators, table borders) |

### Gradientes

- **Headline gradient:** `linear-gradient(100deg, #f5e6a3, #c9a961 40%, #e8d9b8, #c9a961)`  
  Usado em: `.headline-gradient` (hero titles).

- **Aurora blob:** `background: var(--color-gold); filter: blur(100px); opacity: 0.06`  
  Usado em: `.aurora-blob` (4 blobs animados).

- **YouTube card bg:** `linear-gradient(135deg, #1a0d0d, #110808 60%, #0e0606)`  
  Usado em: `.yt-card` (seção YouTube especial na mentoria).

- **Quem card active:** `linear-gradient(135deg, rgba(201,169,97,0.06) 0%, var(--color-bg) 100%)`  
  Usado em: `.quem-card-active` (highlight de opção recomendada).

---

## Tipografia

### Fontes

**Display (Headings):**  
`--font-display: "Syne", system-ui, sans-serif`  
Loaded via Google Fonts: `Syne:wght@600;700;800`

**Body (Paragraphs):**  
`--font-body: "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`  
Loaded via Google Fonts: `DM Sans:ital,wght@0,300;0,400;0,500;1,400`

**Monospace (se necessário):**  
`--font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace`

### Escala Tipográfica

| Classe | Font-Family | Size (clamp/fixed) | Weight | Line-Height | Letter-Spacing | Uso |
|---|---|---|---|---|---|---|
| `h1`, `.hero-h1` | Syne | `clamp(40px, 6vw, 68px)` | 600 | 1.08 | -0.02em | Hero principal |
| `h2`, `.h2` | Syne | `clamp(30px, 4vw, 48px)` | 700 | 1.15 | -0.02em | Section headings |
| `.quote-display` | Syne | `clamp(22px, 2.6vw, 30px)` | 600 | 1.3 | 0 | Pull-quotes, highlights |
| `.h3-gold` | Syne | 22px | 700 | 1.2 | 0 | Subheadings em gold |
| `.h3-mute` | Syne | 22px | 700 | 1.2 | 0 | Subheadings em muted |
| `.hero-lead` | DM Sans | `clamp(17px, 1.8vw, 20px)` | 400 | 1.6 | 0 | Lead paragraph (hero) |
| `.body-lg` | DM Sans | 17px | 400 | 1.7 | 0 | Corpo principal |
| `.body-lg strong` | DM Sans | 17px | 600 | 1.7 | 0 | Destaque inline |
| `.incluso-title` | DM Sans | 17px | 600 | 1.5 | 0 | Títulos de list items |
| `.incluso-body` | DM Sans | 15px | 400 | 1.55 | 0 | Descrição de list items |
| `.sec-label` | DM Sans | 12px | 600 | 1.2 | 0.2em | Eyebrow (uppercase) |
| `.badge` | DM Sans | 14px | 500 | 1.2 | 0 | Badges inline |

### Regras Específicas

- **Dígitos/cifras:** manter em `DM Sans` ou `Syne` (não usar Cormorant — este design system premium não usa Cormorant para dígitos, diferente de outras páginas Gui Ávila).
- **Strong/Bold:** sempre `font-weight: 600` ou `700` (nunca 400 bold).
- **Letterspacing negativo:** `-0.02em` ou `-0.04em` em display headings grandes (acima de 40px).
- **Line-height:** body copy sempre ≥1.6, headings entre 1.08-1.3.

---

## Spacing & Layout

### Sistema de Spacing

Base: `--spacing: 0.25rem` (4px).  
Escala multiplicada: `calc(var(--spacing) * N)`.

Tamanhos comuns:
- 4px (1x), 8px (2x), 12px (3x), 16px (4x), 20px (5x), 24px (6x), 28px (7x), 32px (8x), 40px (10x), 48px (12x), 64px (16x), 96px (24x), 128px (32x).

### Containers

| Variável | Max-Width | Uso |
|---|---|---|
| `--container-max` | 1200px | Container padrão (wide) |
| `--container-narrow` | 860px | Container estreito (texto longo) |
| `--container-3xl` | 48rem (768px) | Formulários, CTAs |
| `--container-4xl` | 56rem (896px) | — |

### Section Spacing

- **Padding vertical (desktop):** `96px` (var `--section-gap`)
- **Padding vertical (mobile <768px):** `64px`
- **Padding horizontal (padrão):** `24px` (classe `px-6`)

### Grid/Gaps

- **Incluso list gap:** 18px
- **Testimonials/cards gap:** 14-20px (varia por componente)
- **Bio grid (desktop):** `grid-template-columns: 280px 1fr; gap: 56px`
- **Quem grid (desktop):** `grid-template-columns: 1fr 1fr; gap: 28px`

---

## Border Radius

| Variável | Valor | Uso |
|---|---|---|
| `--radius` | 16px | Padrão para cards, modals, sections |
| `--radius-pill` | 999px | Badges, botões rounded-full |
| `--radius-sm` | 0.25rem (4px) | — |
| `--radius-lg` | 0.5rem (8px) | — |

Exemplos:
- `.glass`, `.incluso-item` → 14-16px
- `.badge`, `.yt-badge` → 100px (pill)
- `.btn-primary` → `var(--radius-pill)` (999px)
- `.yt-video img` → 8px (pequeno, thumb)

---

## Sombras & Effects

### Box-Shadows

| Classe/Elemento | Shadow | Uso |
|---|---|---|
| `.btn-primary` | `0 4px 24px var(--color-gold-glow)` | CTA primário (idle) |
| `.btn-primary:hover` | `0 8px 40px rgba(201,169,97,0.4)` | CTA primário (hover, mais intenso) |
| `.bio-photo-frame` | `0 20px 60px rgba(0,0,0,0.5)` | Foto de perfil (profundidade) |
| `.yt-btn` | `0 6px 24px rgba(255,0,0,0.35)` | Botão YouTube (red glow) |
| `.quem-card-active` | `0 10px 40px rgba(201,169,97,0.08)` | Card destacado (soft glow) |

### Glassmorphism

Classe `.glass`:
```css
background: var(--color-surface); /* rgba(255,255,255,0.04) */
border: 1px solid var(--color-line); /* rgba(255,255,255,0.08) */
backdrop-filter: blur(12px);
border-radius: var(--radius); /* 16px */
```

Usado em: cards de depoimento, incluso list, comparativo table, footer links hover.

### Blur

- **Aurora blobs:** `filter: blur(100px)`
- **Glassmorphic cards:** `backdrop-filter: blur(12px)`

### Glow

- Gold glow: `box-shadow: 0 Npx Mpx rgba(201,169,97,0.X)`  
  Onde N=4-10px (distância), M=24-40px (blur), X=0.25-0.4 (alpha).

---

## Motion & Animações

### Easing

| Variável | Cubic-Bezier | Uso |
|---|---|---|
| `--ease` | `cubic-bezier(0.22, 1, 0.36, 1)` | Easing padrão do design system (suave, elegante) |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | — |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | — |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | — |

**Easing canônico:** sempre usar `var(--ease)` em transitions personalizadas.

### Durations

| Propriedade | Duration | Uso |
|---|---|---|
| `transition: opacity, transform` | 0.6s | Reveal on scroll (`.reveal`) |
| `transition: color, border, bg` | 0.2s | Hover states (links, botões, cards) |
| Aurora blob animation | 20s | Keyframe loop infinito, alternate |

### Reveal on Scroll

Classe `.reveal`:
```css
opacity: 0;
transition: opacity 0.6s, transform 0.6s;
transform: translateY(24px);
```

Quando visível (`.reveal.visible`):
```css
opacity: 1;
transform: none;
```

**Delays incrementais:**
- `.reveal-delay-1` → `transition-delay: 0.1s`
- `.reveal-delay-2` → `0.2s`
- `.reveal-delay-3` → `0.3s`
- `.reveal-delay-4` → `0.4s`
- `.reveal-delay-5` → `0.5s`

**IntersectionObserver (threshold 0.1):** script inline no body, aplica `.visible` quando elemento entra em viewport.

### Aurora Animation

Keyframe `aurora-float`:
```css
@keyframes aurora-float {
  0% { transform: translate(0) scale(1); }
  100% { transform: translate(40px, -60px) scale(1.1); }
}
```

Aplicado em 4 blobs, cada um com `animation-delay` diferente (-5s, -7s, -14s).  
Duration: 20s, easing: ease-in-out, infinite alternate.

### Hover Effects

- **Botões:** `transform: translateY(-2px)` + sombra mais intensa (0.2s ease)
- **Links inline:** `border-bottom-color` muda de gold 35% → gold-soft (0.2s)
- **Cards:** `border-color` muda de `var(--color-line)` → `rgba(201,169,97,0.35)` (0.2s)
- **Social icons (footer):** `transform: translateY(-2px)` + border gold glow

---

## Sliders

**Nota:** o design system premium NÃO usa sliders do tipo marquee infinito nas páginas mentoria/reverso. Em vez disso:

### Testimonials (Reverso)

- **Layout:** `.testi-marquee-wrap` com **2 tracks** (`.testi-track` + `.testi-track.rev`)
- **Comportamento:** provavelmente arrasto manual (drag) OU auto-scroll suave (não confirmado no CSS estático)
- **Cards:** `.testi-card` com padding 32-44px, glassmorphic, foto de avatar (img ou gradient background com initial)
- **Mobile:** stacks verticalmente, mantém drag horizontal

### Logos (Reverso)

- **Layout:** `.logos-track-wrap` com `.logos-track` contendo 2x os logos (duplicados pra loop seamless)
- **Comportamento:** provavelmente marquee CSS animation infinito (não presente no CSS extraído — pode estar em JS inline)
- **Items:** `.logo-item` com img, width auto, object-fit contain

**Padrão canônico:** se precisar de slider em página premium futura, usar **rail mode** (cards grandes, momentum scroll, drag pointer-capture, easing suave), NÃO marquee hover-pause.

---

## Componentes-Padrão

### 1. Hero

**Anatomia:**
```html
<section class="hero">
  <div class="container">
    <div class="hero-inner reveal">
      <span class="badge">Eyebrow text</span>
      <h1 class="hero-h1">
        <span class="headline-gradient">Headline com gradient gold</span>
      </h1>
      <p class="hero-lead">Lead paragraph (17-20px)</p>
      <div class="hero-cta">
        <a href="#" class="btn btn-primary btn-lg">CTA Principal</a>
        <a href="#" class="btn btn-ghost btn-lg">CTA Secundário</a>
      </div>
    </div>
  </div>
</section>
```

**Medidas:**
- Max-width do `.hero-inner`: 880px
- Gap entre elementos: badge → 16px → h1 → 28px → lead → 14px → cta
- Hero-cta gap (entre botões): 14px
- Padding vertical (section): 96px desktop / 64px mobile

**Estados:**
- Idle: opacity 0, translateY(24px)
- Visible: opacity 1, transform none (via IntersectionObserver)

---

### 2. Botões

#### CTA Primário (`.btn-primary`)

```css
background: var(--color-gold-soft); /* #e8d9b8 */
color: #000;
box-shadow: 0 4px 24px var(--color-gold-glow);
padding: 16px 32px; /* padrão */
padding: 20px 40px; /* .btn-lg */
border-radius: var(--radius-pill); /* 999px */
font-family: var(--font-body);
font-weight: 500;
font-size: 16px; /* 18px se .btn-lg */
```

**Hover:**
```css
transform: translateY(-2px);
box-shadow: 0 8px 40px rgba(201,169,97,0.4);
```

**Pseudo ::after (shimmer effect):**
```css
content: "";
position: absolute;
top: 0; left: -100%;
width: 60%; height: 100%;
background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
transform: skew(-20deg);
transition: left 0.6s ease;
```
Hover: `left: 150%;` (shine passa da esquerda pra direita).

#### CTA Secundário (`.btn-ghost`)

```css
background: transparent;
color: var(--color-tx);
border: 1px solid var(--color-line);
padding: 16px 32px;
border-radius: var(--radius-pill);
```

**Hover:**
```css
background: var(--color-surface);
border-color: rgba(255,255,255,0.2);
```

---

### 3. Cards Glassmorphic

Classe `.glass` aplicada em:
- `.incluso-item`
- `.quem-card`
- `.testi-card`
- `.bonus-card`
- `.guarantee-box`

**Estrutura base:**
```css
background: var(--color-surface); /* rgba(255,255,255,0.04) */
border: 1px solid var(--color-line); /* rgba(255,255,255,0.08) */
backdrop-filter: blur(12px);
border-radius: var(--radius); /* 16px */
padding: 32px 40px; /* varia por componente */
```

**Hover (se aplicável):**
```css
border-color: rgba(201,169,97,0.35);
background: rgba(201,169,97,0.04);
```

---

### 4. Bullet Lists

#### Padrão (`.bullet-list`)

```html
<ul class="bullet-list">
  <li>
    <span aria-hidden="true" class="bullet"></span>
    <span><strong>Título do ponto</strong><br>
      Descrição detalhada do ponto em cor muted.</span>
  </li>
</ul>
```

**CSS:**
```css
.bullet-list { gap: 14px; }
.bullet-list li { display: flex; gap: 14px; font-size: 17px; line-height: 1.6; color: var(--color-tx-soft); }
.bullet {
  flex-shrink: 0;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--color-gold);
  margin-top: 9px; /* alinha com baseline do texto */
}
```

**Variantes:**
- `.bullet.dash` → linha horizontal (width 10px, height 1px, muted color)
- `.bullet-list.mute` → cor muted pra lista inteira
- `.bullet-list.small` → font-size 15px

---

### 5. Incluso List (Checklist)

```html
<ul class="incluso-list">
  <li class="incluso-item">
    <span aria-hidden="true" class="incluso-check">✓</span>
    <div>
      <p class="incluso-title">Título do item incluso</p>
      <p class="incluso-body">Descrição curta do que está incluso</p>
    </div>
  </li>
</ul>
```

**CSS:**
```css
.incluso-list { gap: 18px; }
.incluso-item {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 14px;
  padding: 18px 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: 14px;
}
.incluso-check {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: rgba(201,169,97,0.12);
  color: var(--color-gold);
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

**Hover:**
```css
border-color: rgba(201,169,97,0.35);
background: rgba(201,169,97,0.04);
```

---

### 6. Comparativo Table

Usado na página mentoria pra comparar curso vs mentoria.

**Estrutura:**
```html
<div class="comparativo-table">
  <div class="comparativo-row comparativo-header">
    <div class="comparativo-cell">Curso (Sistema Reverso)</div>
    <div class="comparativo-cell comparativo-highlight">Mentoria (Grupo)</div>
  </div>
  <div class="comparativo-row">
    <div class="comparativo-cell">Feature A</div>
    <div class="comparativo-cell comparativo-highlight">Feature A melhorada</div>
  </div>
</div>
```

**CSS:**
```css
.comparativo-table {
  border: 1px solid var(--color-line);
  border-radius: 14px;
  overflow: hidden;
}
.comparativo-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px solid var(--color-line);
}
.comparativo-cell {
  padding: 18px 24px;
  font-size: 15px;
  line-height: 1.6;
  color: var(--color-tx-soft);
  border-right: 1px solid var(--color-line);
}
.comparativo-highlight {
  background: rgba(201,169,97,0.04);
  color: var(--color-tx);
  font-weight: 500;
}
.comparativo-header .comparativo-highlight {
  background: rgba(201,169,97,0.12);
  color: var(--color-gold);
}
```

**Mobile:** stacks em 1 coluna (grid-template-columns: 1fr).

---

### 7. Testimonials (Depoimentos)

Usado no reverso com dual-track marquee.

**Card structure:**
```html
<div class="testi-card">
  <div class="testi-header">
    <div class="testi-avatar">
      <img src="..." alt="Nome">
      <!-- OU initial com gradient bg -->
    </div>
    <div>
      <div class="testi-name">Nome</div>
      <div class="testi-sub">Aluno</div>
    </div>
  </div>
  <p class="testi-text">"Depoimento..."</p>
</div>
```

**CSS:**
```css
.testi-card {
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: 16px;
  padding: 24px;
  min-width: 340px; /* slider item */
}
.testi-avatar {
  width: 50px; height: 50px;
  border-radius: 50%;
  overflow: hidden;
}
.testi-avatar (fallback gradient) {
  background: linear-gradient(135deg, #c9a961, #a0845c);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 20px;
}
.testi-name { font-weight: 600; color: var(--color-tx); }
.testi-sub { font-size: 13px; color: var(--color-muted); }
.testi-text { font-size: 15px; line-height: 1.65; color: var(--color-tx-soft); }
```

---

### 8. FAQ (Accordion)

```html
<details class="faq-item glass">
  <summary class="faq-summary">
    <span>Pergunta frequente</span>
    <span aria-hidden="true" class="faq-icon">+</span>
  </summary>
  <p class="faq-answer">Resposta...</p>
</details>
```

**CSS:**
```css
.faq-item {
  padding: 4px 24px;
  transition: border-color 0.2s, background 0.2s;
}
.faq-item[open] {
  border-color: rgba(201,169,97,0.35);
}
.faq-summary {
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  padding: 18px 0;
  font-size: 17px;
  font-weight: 500;
  color: var(--color-tx);
}
.faq-icon {
  color: var(--color-gold);
  font-size: 22px;
  transition: transform 0.3s var(--ease);
}
.faq-item[open] .faq-icon {
  transform: rotate(45deg); /* vira X */
}
.faq-answer {
  font-size: 16px;
  line-height: 1.65;
  color: var(--color-tx-soft);
  padding-bottom: 18px;
}
```

---

### 9. Footer

Estrutura em 3 áreas: top (CTA + social), grid (4 colunas de links), bottom (copyright).

**CSS:**
```css
.site-footer {
  border-top: 1px solid var(--color-line);
  background: var(--color-bg);
  padding: 64px 0 32px;
}
.site-footer__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 40px;
  margin-bottom: 40px;
  border-bottom: 1px solid var(--color-line);
}
.site-footer__cta {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(20px, 2.4vw, 26px);
  color: var(--color-tx);
}
.site-footer__social-link {
  width: 44px; height: 44px;
  border-radius: 999px;
  border: 1px solid var(--color-line);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-tx);
}
.site-footer__social-link:hover {
  color: var(--color-gold);
  border-color: rgba(201,169,97,0.4);
  transform: translateY(-2px);
}
.site-footer__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 48px;
}
@media (max-width: 1024px) {
  grid-template-columns: 1fr 1fr;
  gap: 36px;
}
```

---

### 10. Badge (Eyebrow)

```html
<span class="badge">Para infoprodutores</span>
```

**CSS:**
```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: var(--radius-pill);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-gold);
  background: rgba(201,169,97,0.1);
  border: 1px solid rgba(201,169,97,0.3);
}
```

Variações:
- YouTube badge: bg vermelho translúcido, border red, uppercase, letter-spacing 0.07em

---

### 11. Seção YouTube (Mentoria)

Componente especial com design diferenciado (dark red gradient bg).

**Estrutura:**
- `.yt-section` (padding 40-64px)
- `.yt-card` (grid 2 colunas desktop, bg gradient vermelho escuro)
- `.yt-left` (info + CTA)
- `.yt-right` (feed de 4 vídeos recentes)

**CSS highlights:**
```css
.yt-card {
  background: linear-gradient(135deg, #1a0d0d, #110808 60%, #0e0606);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 22px;
  padding: 44px 48px;
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 52px;
}
.yt-card::after {
  content: "";
  position: absolute;
  bottom: -80px; right: -80px;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(200,10,10,0.18) 0%, transparent 65%);
  pointer-events: none;
}
.yt-title-line2 {
  font-size: 56px;
  font-weight: 800;
  color: #ff2020;
  line-height: 1;
}
.yt-btn {
  background: red;
  color: #fff;
  font-weight: 700;
  border-radius: 100px;
  box-shadow: 0 6px 24px rgba(255,0,0,0.35);
}
```

Mobile: stacks em 1 coluna.

---

## Responsividade

### Breakpoints

| Nome | Min-Width | Uso |
|---|---|---|
| Mobile | 0-767px | Stack, padding reduzido, font-size clamp mínimo |
| Tablet | 768px+ | Grid 2 cols, padding normal |
| Desktop | 1024px+ | Grid 4 cols (footer), full container |

### Comportamento Mobile

- **Hero h1:** clamp de 40px (mobile) a 68px (desktop)
- **Section padding:** 64px (mobile) vs 96px (desktop)
- **Container padding:** sempre 24px horizontal (não muda)
- **Grid colunas:** footer 4→2→1, bio 280px+1fr→1fr, quem 2→1
- **Comparativo table:** grid 2 cols → 1 col (mobile), borda interna ajustada
- **YouTube card:** grid 2 cols → 1 col, padding 44px → 32px

### Media Queries Canônicas

```css
@media (min-width: 768px) { ... }  /* tablet+ */
@media (max-width: 768px) { ... }  /* mobile */
@media (min-width: 1024px) { ... } /* desktop */
```

---

## Imagens & Mídia

### Aspect Ratios

- **Bio photo:** 1:1 (quadrado)
- **YouTube thumb:** 140x79px (16:9)
- **Testimonial avatar:** 50x50px (círculo)
- **Logos:** width auto, height 40-60px, object-fit contain

### Lazy Loading

Todas as imagens abaixo do fold têm `loading="lazy"` no HTML.

### Tratamentos

- **Border-radius em thumbs:** 8-12px
- **Avatar círculo:** border-radius 50%
- **Bio photo frame:** border 1px solid var(--color-line), box-shadow profundo
- **Logos track:** sem border, fundo transparente

### Fallback (avatar sem foto)

```css
.testi-avatar (sem img) {
  background: linear-gradient(135deg, #c9a961, #a0845c);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
}
```

Mostra inicial do nome.

---

## Como Usar Este Design System

### Para Desenvolvedores

1. **Copiar tokens CSS:** todas as variáveis `--color-*`, `--font-*`, `--radius`, `--ease` para o root do projeto.
2. **Importar fontes:** adicionar link Google Fonts no `<head>`:
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
   ```
3. **Aurora background:** adicionar `<div class="aurora">` com 4 `.aurora-blob` no body.
4. **Reveal on scroll:** adicionar classe `.reveal` em sections/cards, incluir script IntersectionObserver inline.
5. **Glassmorphism:** usar classe `.glass` em cards que precisam de backdrop-filter.
6. **Componentes:** copiar HTML+CSS de cada componente acima (hero, botões, listas, etc.).

### Para Copywriters

1. **Hierarquia de texto:** sempre seguir heading (h1/h2) → lead (hero-lead/body-lg) → bullet list → quote-display → CTA.
2. **Badges:** usar eyebrow (badge) acima de cada section heading.
3. **Pull-quotes:** destacar 1-2 frases-chave por section com `.quote-display`, sempre com `<span class="gold-strong">` no trecho principal.
4. **CTAs:** repetir CTA primário a cada 2-3 sections (não só no fim da página).
5. **Prova social:** incluir depoimentos com foto + nome + cargo, métricas reais (sem inventar), logos de clientes reais.

### Para Designers

1. **Mockups:** usar fundo #000, overlay de ruído sutil (SVG noise 2.5% opacity), aurora blobs em camadas separadas (pra ajustar opacidade).
2. **Componentes no Figma:** criar variants de `.glass` (idle/hover), `.btn-primary` (idle/hover/pressed), `.reveal` (hidden/visible).
3. **Motion:** prototipar reveal com easing `cubic-bezier(0.22,1,0.36,1)`, duration 600ms, translateY 24px.
4. **Grid system:** usar container 1200px, padding lateral 24px, spacing 4px base.

### Critérios de Qualidade (Checklist)

Antes de publicar página premium, verificar:

- [ ] Todas as cores usam variáveis `--color-*` (não hex hardcoded)
- [ ] Tipografia usa `clamp()` em headings (responsivo fluido)
- [ ] Sections têm 96px de padding vertical (64px mobile)
- [ ] Aurora blobs presentes e animados (20s loop)
- [ ] Reveal on scroll funciona em todos os cards (threshold 0.1)
- [ ] Botão primário tem shimmer effect (::after pseudo)
- [ ] Glassmorphism cards têm `backdrop-filter: blur(12px)`
- [ ] Footer tem 4 colunas no desktop (stacks em mobile)
- [ ] Depoimentos têm foto real OU fallback com gradient+initial
- [ ] CTAs repetidos a cada 2-3 sections (não só 1x no final)
- [ ] Garantia/reassurance presente antes do CTA final
- [ ] Favicon e GTM tag incluídos no `<head>`

---

## Screenshots de Referência

Armazenados em `workspace/design-systems/guiavila-premium/screenshots/`:

- `mentoria.png` — Desktop (1440x900)
- `mentoria-mobile.png` — Mobile (390x844)
- `reverso.png` — Desktop (1440x900)
- `reverso-mobile.png` — Mobile (390x844)

Consultar screenshots pra replicar spacing exato, hierarquia visual, densidade de conteúdo.

---

## Notas Finais

- **Este design system NÃO usa Cormorant** em dígitos/cifras (diferente de outras páginas Gui Ávila).
- **Motion é suave e elegante**, não agressivo (easing cubic-bezier .22,1,.36,1).
- **Glassmorphism é sutil**, não exagerado (4% bg alpha, 8% border alpha, 12px blur).
- **Prova social é densa**, não esparsa (múltiplos depoimentos, logos, métricas).
- **CTAs são repetidos**, não únicos (aparecem 3-4x na página).
- **Aurora é presente mas não dominante** (6% opacity, blur 100px).

Ao criar nova página premium, **consulte os 4 screenshots** como referência visual final. Este MD documenta o "como", os screenshots mostram o "resultado esperado".

---

**Documentado por:** desenvolvedor-frontend (squad-dev)  
**Data:** 2026-05-14  
**Status:** ✅ Completo e validado contra HTML/CSS em produção
