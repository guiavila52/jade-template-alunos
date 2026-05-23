# Design System {{NOME_OPERADOR}} — Clean

**Versão:** 1.0  
**Última atualização:** 2026-05-14  
**Página de referência:** https://resend.com/

---

## Índice

1. [Voz Visual](#voz-visual)
2. [Paleta de Cores](#paleta-de-cores)
3. [Tipografia](#tipografia)
4. [Spacing & Layout](#spacing--layout)
5. [Border Radius](#border-radius)
6. [Sombras & Effects](#sombras--effects)
7. [Motion & Animações](#motion--animações)
8. [Componentes-Padrão](#componentes-padrão)
9. [Responsividade](#responsividade)
10. [Imagens & Mídia](#imagens--mídia)
11. [Como Usar Este Design System](#como-usar-este-design-system)

---

## Voz Visual

O design system clean do {{NOME_OPERADOR}} é caracterizado por **5 adjetivos visuais**, distintos do premium (editorial/dourado) e do {{plataforma_conteudo}} (SaaS energético):

### 1. **Contemporâneo**
- **Evidências:** paleta cinza escuro (#09090b, não puro preto), tipografia Inter moderna (weights 400-600), accent único funcional (#3b82f6 azul), bordas ultra-sutis (rgba 0.06), cards com rounded moderado (12px), gradientes monocromáticos suaves.
- **Onde aparece:** background neutro respirável, hero com grid pattern sutil, cards sem glassmorphism, código syntax highlight com azul funcional.

### 2. **Técnico-Acolhedor**
- **Evidências:** voz "ferramenta que ajuda" (não fria como Linear, não vibrante como {{Plataforma_Conteudo}}), código em destaque com mono font (Commit Mono), badges discretos (#3b82f6/10 bg), documentação estruturada com hierarquia clara, CTAs informativos (não agressivos), seção FAQ/troubleshoot.
- **Onde aparece:** docs pages, quickstart guides, code snippets inline, navegação lateral clean, footer com links úteis.

### 3. **Respirável**
- **Evidências:** spacing generoso (64-80px sections), line-height alto (1.65), margins entre elementos (24-32px), cards com padding 32-40px, hero sem densidade vertical excessiva, white space estratégico (não densamente compactado como premium).
- **Onde aparece:** seções hero com muito ar acima/abaixo do título, paragraphs espaçados, grid de cards com gap 24px, header com padding vertical generoso.

### 4. **Preciso**
- **Evidências:** hierarquia clara (eyebrow 13px → headline 48px → body 16px), pesos de fonte controlados (400 body, 500 headings, 600 highlights), sem tracking negativo agressivo, bordas consistentes (1px solid), ícones alinhados ao baseline, métricas reais (não vagueza), tabelas estruturadas.
- **Onde aparece:** pricing table limpa, specs técnicas, comparativos, API reference, status/metrics dashboards.

### 5. **Confiável**
- **Evidências:** paleta estável (azul funcional, não multicolor), motion contido (300-400ms), código real em exemplos, logos de parceiros (não emojis), seção security/compliance, footer denso com links, dual mode preparado (light/dark), sem exageros visuais.
- **Onde aparece:** seção "built for developers", trust badges sutis, footer com GDPR/compliance, changelog/versioning, GitHub/status links.

---

## Paleta de Cores

Todas as cores em hex/rgba + nome semântico + uso:

### Background

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-bg` | `#09090b` | Fundo principal (cinza muito escuro, não puro preto) |
| `--color-bg-soft` | `#18181b` | Fundo alternado (sections zebradas, cards elevados) |
| `--color-surface` | `rgba(255,255,255,0.03)` | Cards sutis sem glassmorphism |
| `--color-surface-hover` | `rgba(255,255,255,0.06)` | Cards em hover |

### Foreground

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-tx` | `#fafafa` | Texto principal (headings, strong, links) |
| `--color-tx-soft` | `rgba(250,250,250,0.80)` | Corpo de texto (paragraphs, body copy) |
| `--color-muted` | `rgba(250,250,250,0.60)` | Texto terciário (captions, disclaimers, timestamps) |
| `--color-tx-code` | `#e4e4e7` | Texto inline code |

### Accent (Azul Funcional)

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-blue` | `#3b82f6` | Accent primário (links, CTAs, highlights, borders interativas) |
| `--color-blue-soft` | `#60a5fa` | Hover state do azul |
| `--color-blue-bg` | `rgba(59,130,246,0.10)` | Background badges/pills azuis |
| `--color-blue-glow` | `rgba(59,130,246,0.20)` | Box-shadow glow sutil em CTAs |

### Line & Borders

| Variável CSS | RGBA | Uso |
|---|---|---|
| `--color-line` | `rgba(255,255,255,0.06)` | Borders principais (cards, separators, table borders) |
| `--color-line-hover` | `rgba(255,255,255,0.12)` | Borders em hover/focus |

### Estados (Success/Warning/Error)

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-green` | `#10b981` | Success states, status ativo |
| `--color-green-bg` | `rgba(16,185,129,0.10)` | Background success badges |
| `--color-yellow` | `#f59e0b` | Warning states |
| `--color-yellow-bg` | `rgba(245,158,11,0.10)` | Background warning badges |
| `--color-red` | `#ef4444` | Error states |
| `--color-red-bg` | `rgba(239,68,68,0.10)` | Background error badges |

### Gradientes

- **Hero accent gradient (sutil):**  
  `linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(16,185,129,0.04) 100%)`  
  Usado em: backgrounds de hero sections, cards destacados (não em texto).

- **Code block gradient:**  
  `linear-gradient(180deg, #18181b 0%, #09090b 100%)`  
  Usado em: code snippets, pre blocks.

- **Button primary gradient (hover):**  
  `linear-gradient(135deg, #3b82f6, #60a5fa)`  
  Usado em: botão primário em hover state (sutil).

---

## Tipografia

Família primária: **Inter** (fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif)  
Família monospace: **Commit Mono** (fallback: "SF Mono", "Monaco", "Inconsolata", monospace)

### Escala de Tamanhos

| Nome | Tamanho Desktop | Tamanho Mobile | Line-height | Weight | Uso |
|---|---|---|---|---|---|
| `--text-hero` | 56px | 40px | 1.1 | 600 | Hero headlines |
| `--text-h1` | 48px | 36px | 1.15 | 600 | H1 |
| `--text-h2` | 36px | 28px | 1.2 | 600 | H2 |
| `--text-h3` | 28px | 22px | 1.25 | 600 | H3 |
| `--text-h4` | 22px | 18px | 1.3 | 500 | H4 |
| `--text-lg` | 18px | 17px | 1.6 | 400 | Lead paragraphs, intro text |
| `--text-base` | 16px | 15px | 1.65 | 400 | Body copy padrão |
| `--text-sm` | 14px | 13px | 1.5 | 400 | Captions, metadata |
| `--text-xs` | 13px | 12px | 1.4 | 500 | Badges, pills, labels |
| `--text-code` | 15px | 14px | 1.6 | 400 | Inline code |
| `--text-code-block` | 14px | 13px | 1.7 | 400 | Code blocks (pre) |

### Pesos Disponíveis (Inter)

- **400 (Regular):** body copy, paragraphs
- **500 (Medium):** headings secundários (h4, h5), labels
- **600 (Semibold):** headings principais (h1, h2, h3), CTAs

### Letter-spacing

- Headings grandes (hero, h1): `-0.015em` (sutil, não agressivo)
- Headings médios (h2-h4): `0em` (tracking normal)
- Body copy: `0em`
- Badges/labels: `0.01em` (tracking levemente aberto)
- Código: `0em`

### Regras

- **SEM tracking negativo agressivo** (diferente do premium que usa -0.035em)
- **SEM all-caps excessivo** (só em badges/labels quando necessário)
- **Line-height generoso** em body (1.65 vs 1.5 do {{plataforma_conteudo}})
- **Peso máximo 600** (sem 700/800 do premium)

---

## Spacing & Layout

### Escala de Spacing

Baseada em múltiplos de 4px (padrão sistema):

| Variável CSS | Valor | Uso |
|---|---|---|
| `--space-1` | 4px | Padding interno micro (badges) |
| `--space-2` | 8px | Gap pequeno (icon-text) |
| `--space-3` | 12px | Padding interno botões |
| `--space-4` | 16px | Gap padrão entre elementos próximos |
| `--space-5` | 20px | Padding interno cards pequenos |
| `--space-6` | 24px | Gap entre cards, margin entre sections internas |
| `--space-8` | 32px | Padding interno cards médios |
| `--space-10` | 40px | Padding interno cards grandes |
| `--space-12` | 48px | Margin entre sections pequenas |
| `--space-16` | 64px | Margin entre sections médias |
| `--space-20` | 80px | Margin entre sections grandes (hero → próxima section) |
| `--space-24` | 96px | Padding vertical hero |

### Container

- **Max-width:** 1280px (desktop), 100% (mobile)
- **Padding lateral:** 24px (mobile), 32px (tablet), 48px (desktop)
- **Centralization:** `margin: 0 auto`

### Grid

- **Colunas:** 12-column grid
- **Gap padrão:** 24px (desktop), 16px (mobile)
- **Breakpoints:** ver seção Responsividade

---

## Border Radius

| Variável CSS | Valor | Uso |
|---|---|---|
| `--radius-sm` | 6px | Badges, pills, small buttons |
| `--radius-md` | 10px | Botões padrão, inputs |
| `--radius-lg` | 12px | Cards, modais, containers |
| `--radius-xl` | 16px | Hero cards, feature cards grandes |

Nota: Resend usa rounded moderado (não sharp como Linear, não excessivo como alguns SaaS). Clean = 10-12px padrão.

---

## Sombras & Effects

### Sombras

Sutis, quase ausentes. Não há glassmorphism forte (diferente do premium).

| Variável CSS | Valor | Uso |
|---|---|---|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Hover sutil em cards |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.1)` | Dropdowns, popovers |
| `--shadow-glow-blue` | `0 0 24px rgba(59,130,246,0.15)` | CTA primary hover (opcional) |

### Backdrop Filter

- **Não usado** no clean (diferente do premium que usa backdrop-blur 12px)
- Se necessário (modais), usar: `backdrop-blur(8px)`

---

## Motion & Animações

### Durações

| Nome | Valor | Uso |
|---|---|---|
| `--duration-fast` | 150ms | Micro-interactions (hover icon, badge) |
| `--duration-base` | 300ms | Transições padrão (button hover, card hover) |
| `--duration-slow` | 400ms | Reveals on scroll, modais |

### Easings

| Nome | Cubic-bezier | Uso |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Padrão (smooth, não agressivo) |
| `--ease-in-out` | `cubic-bezier(0.45, 0, 0.55, 1)` | Modais, reveals |

### Reveal on Scroll

- **Efeito:** `opacity: 0 → 1` + `translateY(10px) → 0`
- **Delay incremental:** 100ms entre elementos
- **Threshold:** `0.1` (trigger cedo)
- **Não usar:** parallax, rotation, scale agressivo

### Hover States

- **Links:** `color: var(--color-blue)` + `text-decoration: underline`
- **Botões:** `background: var(--color-blue-soft)` + `box-shadow: 0 0 24px rgba(59,130,246,0.15)`
- **Cards:** `border-color: var(--color-line-hover)` + `shadow-sm`

### Animações de Background

- **Não usar:** aurora blobs animados (premium), dot grid pattern ({{plataforma_conteudo}})
- **Permitido:** gradiente sutil estático, grid lines finas (rgba 0.03)

---

## Componentes-Padrão

### 1. Header

**Anatomia:**
- Height: 64px
- Background: `rgba(9,9,11,0.90)` + `backdrop-blur(8px)` (sticky)
- Border-bottom: `1px solid var(--color-line)`
- Padding: `0 48px`
- Logo: height 24px, à esquerda
- Nav links: `--text-sm`, weight 500, gap 32px
- CTA button: à direita

**Código de referência:**
```css
.header {
  position: sticky;
  top: 0;
  height: 64px;
  background: rgba(9,9,11,0.90);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-line);
  padding: 0 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100;
}

.header-nav {
  display: flex;
  gap: 32px;
}

.header-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-tx-soft);
  transition: color var(--duration-fast) var(--ease-out);
}

.header-link:hover {
  color: var(--color-tx);
}
```

**Screenshot:** Ver `screenshots/resend-docs-desktop.png` (header fixo).

---

### 2. Hero

**Anatomia:**
- Padding vertical: 96px (desktop), 64px (mobile)
- Max-width conteúdo: 720px (centralizado)
- Eyebrow: `--text-xs`, uppercase, tracking 0.05em, color `--color-muted`, margin-bottom 16px
- Headline: `--text-hero`, weight 600, color `--color-tx`, margin-bottom 24px
- Subheadline: `--text-lg`, color `--color-tx-soft`, margin-bottom 40px
- CTA group: display flex, gap 16px

**Código de referência:**
```css
.hero {
  padding: 96px 48px;
  text-align: center;
}

.hero-content {
  max-width: 720px;
  margin: 0 auto;
}

.hero-eyebrow {
  font-size: 13px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-muted);
  margin-bottom: 16px;
}

.hero-headline {
  font-size: clamp(40px, 5vw, 56px);
  font-weight: 600;
  line-height: 1.1;
  color: var(--color-tx);
  margin-bottom: 24px;
  letter-spacing: -0.015em;
}

.hero-subheadline {
  font-size: 18px;
  line-height: 1.6;
  color: var(--color-tx-soft);
  margin-bottom: 40px;
}

.hero-cta-group {
  display: flex;
  gap: 16px;
  justify-content: center;
}
```

**Screenshot:** Ver `screenshots/resend-home-desktop.png` (hero "Email for developers").

---

### 3. Botões

#### Primary

- Background: `var(--color-blue)`
- Color: `#ffffff`
- Padding: `12px 24px`
- Border-radius: `var(--radius-md)`
- Font-size: `15px`, weight 500
- Hover: background `var(--color-blue-soft)` + `box-shadow: 0 0 24px rgba(59,130,246,0.15)`

```css
.btn-primary {
  background: var(--color-blue);
  color: #ffffff;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all var(--duration-base) var(--ease-out);
}

.btn-primary:hover {
  background: var(--color-blue-soft);
  box-shadow: 0 0 24px rgba(59,130,246,0.15);
}
```

#### Secondary

- Background: `transparent`
- Color: `var(--color-tx)`
- Border: `1px solid var(--color-line)`
- Hover: border-color `var(--color-line-hover)`, background `var(--color-surface-hover)`

```css
.btn-secondary {
  background: transparent;
  color: var(--color-tx);
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 500;
  border: 1px solid var(--color-line);
  cursor: pointer;
  transition: all var(--duration-base) var(--ease-out);
}

.btn-secondary:hover {
  border-color: var(--color-line-hover);
  background: var(--color-surface-hover);
}
```

---

### 4. Cards

**Anatomia:**
- Background: `var(--color-surface)`
- Border: `1px solid var(--color-line)`
- Border-radius: `var(--radius-lg)`
- Padding: 32px
- Hover: border-color `var(--color-line-hover)` + `box-shadow: var(--shadow-sm)`

**Código de referência:**
```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-lg);
  padding: 32px;
  transition: all var(--duration-base) var(--ease-out);
}

.card:hover {
  border-color: var(--color-line-hover);
  box-shadow: var(--shadow-sm);
}

.card-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-tx);
  margin-bottom: 12px;
}

.card-description {
  font-size: 15px;
  line-height: 1.65;
  color: var(--color-tx-soft);
}
```

**Screenshot:** Ver `screenshots/resend-docs-desktop.png` (cards de quickstart).

---

### 5. Code Blocks

**Inline code:**
- Background: `rgba(255,255,255,0.08)`
- Color: `var(--color-tx-code)`
- Padding: `2px 6px`
- Border-radius: `4px`
- Font-family: `Commit Mono`, monospace
- Font-size: `14px`

```css
code {
  background: rgba(255,255,255,0.08);
  color: var(--color-tx-code);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Commit Mono', monospace;
  font-size: 14px;
}
```

**Code block (pre):**
- Background: `linear-gradient(180deg, #18181b 0%, #09090b 100%)`
- Border: `1px solid var(--color-line)`
- Border-radius: `var(--radius-lg)`
- Padding: `20px`
- Overflow-x: auto
- Font-size: `14px`

```css
pre {
  background: linear-gradient(180deg, #18181b 0%, #09090b 100%);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-lg);
  padding: 20px;
  overflow-x: auto;
  font-family: 'Commit Mono', monospace;
  font-size: 14px;
  line-height: 1.7;
}
```

---

### 6. Badges/Pills

**Anatomia:**
- Background: `var(--color-blue-bg)` (ou green/yellow/red para estados)
- Color: `var(--color-blue)` (ou respectiva cor de estado)
- Padding: `4px 12px`
- Border-radius: `var(--radius-sm)`
- Font-size: `13px`, weight 500
- Letter-spacing: `0.01em`

```css
.badge {
  display: inline-flex;
  align-items: center;
  background: var(--color-blue-bg);
  color: var(--color-blue);
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.badge-success {
  background: var(--color-green-bg);
  color: var(--color-green);
}

.badge-warning {
  background: var(--color-yellow-bg);
  color: var(--color-yellow);
}

.badge-error {
  background: var(--color-red-bg);
  color: var(--color-red);
}
```

---

### 7. Footer

**Anatomia:**
- Background: `var(--color-bg-soft)`
- Border-top: `1px solid var(--color-line)`
- Padding: `64px 48px 32px`
- Grid: 4 colunas (desktop), 1 coluna (mobile)
- Gap: 48px
- Links: `--text-sm`, color `var(--color-tx-soft)`, hover `var(--color-tx)`

**Código de referência:**
```css
.footer {
  background: var(--color-bg-soft);
  border-top: 1px solid var(--color-line);
  padding: 64px 48px 32px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 48px;
  margin-bottom: 48px;
}

.footer-column-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-tx);
  margin-bottom: 16px;
}

.footer-link {
  display: block;
  font-size: 14px;
  color: var(--color-tx-soft);
  margin-bottom: 12px;
  transition: color var(--duration-fast) var(--ease-out);
}

.footer-link:hover {
  color: var(--color-tx);
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 32px;
  border-top: 1px solid var(--color-line);
  font-size: 13px;
  color: var(--color-muted);
}
```

---

### 8. Navegação Lateral (Docs)

**Anatomia:**
- Width: 280px (desktop), 100% (mobile)
- Background: `var(--color-bg)`
- Border-right: `1px solid var(--color-line)` (desktop)
- Padding: 24px
- Links: `--text-sm`, weight 400, color `var(--color-tx-soft)`
- Link ativo: weight 500, color `var(--color-tx)`, background `var(--color-surface)`

```css
.sidebar {
  width: 280px;
  background: var(--color-bg);
  border-right: 1px solid var(--color-line);
  padding: 24px;
  overflow-y: auto;
}

.sidebar-section-title {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-muted);
  margin-bottom: 12px;
  margin-top: 24px;
}

.sidebar-link {
  display: block;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-tx-soft);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  margin-bottom: 4px;
  transition: all var(--duration-fast) var(--ease-out);
}

.sidebar-link:hover {
  color: var(--color-tx);
  background: var(--color-surface-hover);
}

.sidebar-link.active {
  font-weight: 500;
  color: var(--color-tx);
  background: var(--color-surface);
}
```

**Screenshot:** Ver `screenshots/resend-docs-desktop.png` (sidebar esquerda).

---

## Responsividade

### Breakpoints

| Nome | Valor | Uso |
|---|---|---|
| `mobile` | 0-640px | Layout 1 coluna, texto menor |
| `tablet` | 641-1024px | Layout 2 colunas, ajustes intermediários |
| `desktop` | 1025px+ | Layout completo, texto padrão |

### Mobile-First

Todas as classes começam mobile e escalam com `@media (min-width: ...)`.

### Mudanças em Mobile

- **Hero headline:** 40px (vs 56px desktop)
- **Section padding:** 64px → 48px vertical
- **Container padding:** 48px → 24px lateral
- **Grid:** 4 colunas → 1 coluna
- **Footer:** 4 colunas → 1 coluna empilhada
- **Header:** logo centralizado, nav colapsado em menu hamburger
- **Sidebar:** colapsado em drawer/offcanvas

---

## Imagens & Mídia

### Fotos

- **Não usar:** fotos de stock genéricas, emojis como ícones principais
- **Usar:** screenshots reais de produto, código real, logos oficiais de parceiros (SVG/PNG), gráficos limpos

### Ícones

- **Biblioteca recomendada:** Lucide (clean, consistente)
- **Tamanho padrão:** 20px (inline com texto), 24px (standalone)
- **Stroke-width:** 2px
- **Color:** `currentColor` (herda do texto pai)

### Logos de Parceiros

- **Formato:** SVG (preferencial) ou PNG alta resolução
- **Height:** 32-40px
- **Filter:** `grayscale(1) opacity(0.6)` (padrão), `grayscale(0) opacity(1)` (hover)

### Videos

- **Background videos:** evitar (não há no Resend, não no clean)
- **Embeds (YouTube, etc):** border-radius `var(--radius-lg)`, aspect-ratio 16/9

---

## Como Usar Este Design System

### Quando usar Clean vs Premium vs {{Plataforma_Conteudo}}

| Caso de uso | Design System |
|---|---|
| Landing de mentoria/reverso (high-ticket, exclusivo) | **Premium** |
| Landing do {{Plataforma_Conteudo}} (SaaS energético, produto) | **{{Plataforma_Conteudo}}** |
| Squad-template pra alunos (técnico, acolhedor) | **Clean** |
| Páginas /tools, /docs (ferramenta, confiável) | **Clean** |
| Tutoriais técnicos (precisão, clareza) | **Clean** |
| Dashboards internos (status, infra) | **Clean** |
| Landing de newsletter (editorial, denso) | **Premium** |
| Landing de ferramenta nova energética | **{{Plataforma_Conteudo}}** |

### Comparativo visual rápido

| Aspecto | Premium | {{Plataforma_Conteudo}} | Clean |
|---|---|---|---|
| **Paleta** | Dourado + Preto puro (#000) | Violeta/Rosa/Laranja (#a78bfa, #f0abfc, #fb923c) | Azul funcional (#3b82f6) + Cinza escuro (#09090b) |
| **Background** | Preto puro (#000) | Deep purple (#030014) | Cinza muito escuro (#09090b) |
| **Tipografia** | Syne (editorial, 700-800) + DM Sans | Inter/Geist (tech, 400-600) | Inter (clean, 400-600) |
| **Tracking** | Negativo agressivo (-0.035em) | Negativo leve (-0.02em) | Neutro a levemente negativo (-0.015em) |
| **Motion** | Suave, lento (600ms) | Snappy, rápido (200ms) | Contido, educado (300-400ms) |
| **Glassmorphism** | Sim (backdrop-blur 12px) | Leve (backdrop-blur-sm) | Não (sem blur, bordas limpas) |
| **Patterns** | Aurora blobs animados | Dot grid + noise texture | Grid lines sutis (opcional) |
| **Accent** | 1 cor (dourado #c9a961) | 3 cores (violeta→rosa→laranja) | 1 cor (azul #3b82f6) |
| **Border-radius** | Moderado (12-16px) | Moderado (10-14px) | Moderado (10-12px) |
| **Sombras** | Sutis com glow dourado | Sutis | Quase ausentes |
| **Line-height** | 1.5-1.6 | 1.4-1.5 | 1.6-1.7 |
| **Spacing** | Denso (96px sections) | Médio (80px sections) | Respirável (64-80px sections) |
| **Voz** | Premium, editorial, sofisticado | Energético, tech, ousado | Contemporâneo, técnico-acolhedor, preciso |
| **Casos de uso** | Mentoria, Reverso, high-ticket | {{Plataforma_Conteudo}} SaaS, produtos consumer | Squad-template, /tools, /docs, tutoriais |

### Regra de ouro

- **Premium:** "vendo exclusividade, expertise, transformação high-ticket"
- **{{Plataforma_Conteudo}}:** "vendo produto SaaS, energia, eficiência, solução rápida"
- **Clean:** "entrego ferramenta/conhecimento técnico com confiança e clareza"

---

## Apêndice: Tokens CSS Completos

```css
:root {
  /* Colors - Background */
  --color-bg: #09090b;
  --color-bg-soft: #18181b;
  --color-surface: rgba(255,255,255,0.03);
  --color-surface-hover: rgba(255,255,255,0.06);
  
  /* Colors - Foreground */
  --color-tx: #fafafa;
  --color-tx-soft: rgba(250,250,250,0.80);
  --color-muted: rgba(250,250,250,0.60);
  --color-tx-code: #e4e4e7;
  
  /* Colors - Accent */
  --color-blue: #3b82f6;
  --color-blue-soft: #60a5fa;
  --color-blue-bg: rgba(59,130,246,0.10);
  --color-blue-glow: rgba(59,130,246,0.20);
  
  /* Colors - States */
  --color-green: #10b981;
  --color-green-bg: rgba(16,185,129,0.10);
  --color-yellow: #f59e0b;
  --color-yellow-bg: rgba(245,158,11,0.10);
  --color-red: #ef4444;
  --color-red-bg: rgba(239,68,68,0.10);
  
  /* Colors - Line */
  --color-line: rgba(255,255,255,0.06);
  --color-line-hover: rgba(255,255,255,0.12);
  
  /* Typography - Sizes */
  --text-hero: clamp(40px, 5vw, 56px);
  --text-h1: clamp(36px, 4vw, 48px);
  --text-h2: clamp(28px, 3vw, 36px);
  --text-h3: clamp(22px, 2.5vw, 28px);
  --text-h4: clamp(18px, 2vw, 22px);
  --text-lg: 18px;
  --text-base: 16px;
  --text-sm: 14px;
  --text-xs: 13px;
  --text-code: 15px;
  --text-code-block: 14px;
  
  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  
  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-glow-blue: 0 0 24px rgba(59,130,246,0.15);
  
  /* Motion */
  --duration-fast: 150ms;
  --duration-base: 300ms;
  --duration-slow: 400ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.45, 0, 0.55, 1);
  
  /* Fonts */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'Commit Mono', 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}
```

---

**Última atualização:** 2026-05-14  
**Autor:** Jade (COO) via squad dev  
**Aprovação:** Pendente {{NOME_OPERADOR}}
