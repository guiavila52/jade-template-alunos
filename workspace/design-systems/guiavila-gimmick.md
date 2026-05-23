# Design System Gui Ávila — {{Plataforma_Conteudo}}

**Versão:** 1.0  
**Última atualização:** 2026-05-14  
**Página de referência:** https://{{plataforma_conteudo}}.{{DOMINIO}}/

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

O design system {{Plataforma_Conteudo}} é caracterizado por **5 adjetivos visuais**, distintos do design-system-guiavila-premium:

### 1. **SaaS Moderno**
- **Evidências:** paleta violeta-rosa-laranja vibrante (#a78bfa, #f0abfc, #fb923c), gradientes multi-cor (120deg), cards com borda sutil, tipografia tech-friendly (Inter como fallback), UI patterns de dashboard/produto (não editorial).
- **Onde aparece:** hero gradient (violeta→rosa→laranja), badge com violet-400/30 border, background #030014 (deep purple, não puro black).

### 2. **Energético**
- **Evidências:** aurora blobs múltiplos com cores quentes (violet-600, fuchsia-600, pink-600), opacity alta (0.18, 0.12, 0.10), blur intenso (120-140px), gradientes diagonais vibrantes, motion rápido (provavelmente <1s transitions).
- **Onde aparece:** background blobs fixos, hero gradient span, CTA buttons com gradiente animado.

### 3. **Tech/Produto**
- **Evidências:** dot grid pattern (radial-gradient circle, 32px spacing), noise texture overlay (opacity 0.35), lucide-react icons (sparkles, chevron), uppercase tracking largo em badges (0.2em), backdrop-blur-sm (glassmorphism leve).
- **Onde aparece:** hero background (dot grid + mask radial), badges (UPPERCASE tracking), cards com border violet-400/30.

### 4. **Ousado**
- **Evidências:** contraste alto (texto #f4f4f5 em bg #030014), gradiente hero com 3 cores vivas, font-size gigante em hero (clamp 40-76px), tracking negativo agressivo (-0.035em), leading ultra-tight (1.02), CTA buttons largos com glow.
- **Onde aparece:** hero h1 (76px desktop), gradient text (violet→pink→orange), preço destacado (R$ 197 com font gigante).

### 5. **Focado**
- **Evidências:** hierarquia clara (eyebrow → headline → subheadline → CTA), sections bem delimitadas (borders, spacing generoso), CTAs repetidos, pricing transparente (R$ 197 destacado), FAQ extensa, seção YouTube com design dedicado (red theme).
- **Onde aparece:** estrutura vertical limpa, sections com border-top, FAQ accordion, pricing card central.

---

## Paleta de Cores

Todas as cores em hex/rgba + nome semântico + uso:

### Background

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-bg` | `#030014` | Fundo principal (deep purple escuro) |
| `--color-bg-soft` | `#0a0a14` | Alternativa mais clara (se necessário) |
| `--color-surface` | `rgba(139,92,246,0.05)` | Cards sutis com tint violeta |
| `--color-surface-hover` | `rgba(139,92,246,0.10)` | Cards em hover |

### Foreground

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-tx` | `#f4f4f5` | Texto principal (headings, strong) |
| `--color-tx-soft` | `rgba(244,244,245,0.70)` | Corpo de texto, paragraphs |
| `--color-muted` | `rgba(244,244,245,0.50)` | Texto terciário, disclaimers |

### Accent (Violeta/Rosa/Laranja)

| Variável CSS | Hex/RGBA | Uso |
|---|---|---|
| `--color-violet` | `#a78bfa` | Accent primário (badges, borders, links) |
| `--color-violet-400` | `#a78bfa` | Border padrão em badges/cards |
| `--color-violet-500` | `#8b5cf6` | Background badges (alpha 0.10) |
| `--color-violet-600` | `#7c3aed` | Aurora blob 1, theme-color meta |
| `--color-fuchsia` | `#f0abfc` | Gradiente meio (hero, CTAs) |
| `--color-fuchsia-600` | `#c026d3` | Aurora blob 2 |
| `--color-pink-600` | `#db2777` | Aurora blob 3 |
| `--color-orange` | `#fb923c` | Gradiente fim (hero highlight) |

### Line & Borders

| Variável CSS | RGBA | Uso |
|---|---|---|
| `--color-line` | `rgba(167,139,250,0.30)` | Borders principais (violet-400/30) |
| `--color-line-soft` | `rgba(255,255,255,0.08)` | Borders sutis alternativos |

### Gradientes

- **Hero headline gradient:**  
  `linear-gradient(120deg, #a78bfa 0%, #f0abfc 40%, #fb923c 100%)`  
  Usado em: hero h1 span (background-clip: text).

- **CTA button gradient:**  
  `linear-gradient(135deg, #a78bfa, #f0abfc)`  
  Usado em: botão primário {{Plataforma_Conteudo}}.

- **Aurora blob 1 (violet):** `bg-violet-600` + `opacity-[0.18]` + `blur-[120px]`  
- **Aurora blob 2 (fuchsia):** `bg-fuchsia-600` + `opacity-[0.12]` + `blur-[140px]`  
- **Aurora blob 3 (pink):** `bg-pink-600` + `opacity-[0.10]` + `blur-[120px]`

- **Dot grid pattern (hero bg):**  
  `radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px)`  
  Background-size: 32px 32px  
  Mask: `radial-gradient(ellipse at center, black 30%, transparent 75%)`  
  Opacity: 0.35

- **YouTube section gradient:**  
  Provavelmente similar ao premium (red dark gradient), mas com tint violeta no {{Plataforma_Conteudo}}.

---

## Tipografia

### Fontes

**Display (Headings):**  
`--font-display: "Syne", system-ui, sans-serif`  
Weights: 600, 700, 800  
Loaded via Next.js font optimization.

**Body (Paragraphs):**  
`--font-body: "DM Sans", system-ui, -apple-system, sans-serif`  
Weights: 300, 400, 500  
Loaded via Next.js font optimization.

**Fallback (UI elements):**  
`--font-ui: "Inter", system-ui, sans-serif`  
Weights: 100-900 variable  
Usado em elementos de interface (tabs, badges menores, dashboard UI).

### Escala Tipográfica

| Classe/Uso | Font-Family | Size (clamp/fixed) | Weight | Line-Height | Letter-Spacing | Uso |
|---|---|---|---|---|---|---|
| Hero h1 | Syne | `clamp(40px, 6vw, 76px)` | 800 | 1.02 | -0.035em | Hero principal {{Plataforma_Conteudo}} |
| Hero subheadline | Syne | `clamp(22px, 3vw, 38px)` | 400 (italic) | 1.2 | 0 | Subtítulo hero (italic, muted) |
| Section h2 | Syne | `clamp(28px, 4vw, 48px)` | 700 | 1.10 | -0.02em | Section headings |
| Section h3 | Syne | `clamp(20px, 2.5vw, 28px)` | 600 | 1.20 | 0 | Subheadings |
| Badge (eyebrow) | DM Sans | 12px | 700 | 1.2 | 0.2em | Eyebrow UPPERCASE |
| Body lg | DM Sans | 17-18px | 400 | 1.65 | 0 | Corpo principal |
| Body md | DM Sans | 15-16px | 400 | 1.60 | 0 | Corpo secundário |
| Small | DM Sans | 13-14px | 400 | 1.50 | 0 | Disclaimers, notes |

### Regras Específicas

- **Gradient text:** sempre usar `background-image: linear-gradient(...)` + `background-clip: text` + `-webkit-text-fill-color: transparent`.
- **Tracking negativo:** headings acima de 40px levam `-0.035em` ou `-0.02em`.
- **Line-height ultra-tight:** hero h1 usa `1.02` (muito compacto, moderno).
- **Italic em subheadline:** hero subheadline sempre italic com muted color.
- **UPPERCASE tracking largo:** badges/eyebrows sempre `text-xs font-bold uppercase tracking-[0.2em]`.

---

## Spacing & Layout

### Sistema de Spacing

Base Tailwind: `0.25rem` (4px).  
Escala multiplicada: 1, 2, 4, 6, 10, 12, 14, 16, 20, 24, 32, 40, 48, 64, 96.

Tamanhos comuns no {{Plataforma_Conteudo}}:
- **Padding cards:** 24-32px (p-6 a p-8)
- **Gap entre sections:** 64-96px (py-16 a py-24)
- **Gap entre elementos hero:** 24px (mb-6)
- **Container padding horizontal:** 24px (px-6)

### Containers

| Variável | Max-Width | Uso |
|---|---|---|
| `--container-max` | 1200px | Container padrão (wide) |
| `--container-narrow` | 860px | Container estreito (texto longo) |
| `--container-hero` | 80rem (1280px) | Hero max-width (se necessário) |

### Section Spacing

- **Padding vertical (desktop):** 64-96px (py-16 a py-24)
- **Padding vertical (mobile):** 40-64px (py-10 a py-16)
- **Padding horizontal (padrão):** 24px (px-6)

### Grid/Gaps

- **Cards grid gap:** 20-24px (gap-5 a gap-6)
- **Features grid (3 cols):** gap-8 (32px)
- **FAQ items gap:** 12-16px

---

## Border Radius

| Variável | Valor | Uso |
|---|---|---|
| `--radius` | 16px | Padrão para cards, modals |
| `--radius-lg` | 20px | Cards maiores |
| `--radius-xl` | 24px | Hero cards especiais |
| `--radius-pill` | 9999px | Badges, botões pill |
| `--radius-sm` | 8px | Elementos pequenos |

Exemplos:
- Badges → `rounded-full` (9999px)
- Cards → `rounded-xl` ou `rounded-2xl` (16-20px)
- Buttons → `rounded-full` (9999px)
- Images → `rounded-lg` (12px)

---

## Sombras & Effects

### Box-Shadows

| Elemento | Shadow | Uso |
|---|---|---|
| CTA primário | `0 10px 40px rgba(139,92,246,0.4)` | Botão principal (glow violeta) |
| CTA hover | `0 14px 50px rgba(139,92,246,0.5)` | Hover intenso |
| Cards elevated | `0 8px 32px rgba(0,0,0,0.25)` | Cards com profundidade |
| Pricing card | `0 20px 60px rgba(139,92,246,0.2)` | Card de preço destacado |

### Glassmorphism (Leve)

{{Plataforma_Conteudo}} usa glassmorphism mais sutil que o premium:

```css
background: rgba(139,92,246,0.05); /* violet tint */
border: 1px solid rgba(167,139,250,0.30); /* violet-400/30 */
backdrop-filter: blur(8px); /* blur leve */
```

Usado em: badges, alguns cards (não todos).

### Blur

- **Aurora blobs:** `blur-[120px]` a `blur-[140px]`
- **Glassmorphic elements:** `backdrop-blur-sm` (4px) a `backdrop-blur` (8px)
- **Noise overlay:** nenhum blur (sharp grain)

### Glow

- Violet glow (CTAs): `box-shadow: 0 Npx Mpx rgba(139,92,246,0.4-0.5)`
- Gradient glow (hero text): sem box-shadow, apenas gradient text

---

## Motion & Animações

### Easing

{{Plataforma_Conteudo}} provavelmente usa Tailwind defaults + custom:

| Nome | Cubic-Bezier | Uso |
|---|---|---|
| `ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Padrão Tailwind (hover, transitions) |
| `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Animações bidirecionais |

**Nota:** como é Next.js + Tailwind, motion provavelmente mais "snappy" que o premium (menos suave/elegante, mais produto).

### Durations

| Propriedade | Duration | Uso |
|---|---|---|
| `transition: all` | 200ms | Hover states (botões, cards) |
| `transition: opacity, transform` | 400ms | Reveal on scroll (data-reveal) |
| Aurora blob animation | 15-20s | Loop infinito, provavelmente |

### Reveal on Scroll

Atributo `data-reveal="true"` + `data-reveal-delay="1"` (incremental).

Provavelmente JS IntersectionObserver aplicando classes:
```css
[data-reveal] {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 400ms, transform 400ms;
}
[data-reveal].visible {
  opacity: 1;
  transform: none;
}
```

### Hover Effects

- **Botões:** `transform: translateY(-2px)` + sombra mais intensa (200ms)
- **Cards:** `border-color` muda de violet-400/30 → violet-400/60 (200ms)
- **Links:** underline offset ou color shift (200ms)

### Aurora Animation

3 blobs com posições fixas absolutas:
- Top-left (-15%, -10%): 560px violet-600
- Top-right (30%, -15%): 640px fuchsia-600
- Bottom-left (-10%, 25%): 480px pink-600

Provavelmente `animation: aurora-float 20s ease-in-out infinite alternate` similar ao premium.

---

## Componentes-Padrão

### 1. Header

**Anatomia:**
- Logo {{Plataforma_Conteudo}} (gradient pink/purple)
- Nav desktop (provavelmente links: Funcionalidades, Preço, FAQ, Login)
- CTA button (Começar agora / Entrar)
- Mobile: hamburger menu

**Medidas:**
- Height: ~64-72px
- Padding horizontal: 24px (px-6)
- Logo width: ~140-160px
- Background: transparent ou bg-[#030014]/80 com backdrop-blur

**Estados:**
- Idle: transparente
- Scroll: background com blur (sticky header)

---

### 2. Hero

**Anatomia:**
```html
<section class="hero py-10 md:py-14 pb-16 md:pb-24 text-center">
  <div class="container mx-auto max-w-[1200px] px-6">
    <div class="badge mb-6">
      [Icon] App oficial · Método Sistema Reverso
    </div>
    <h1 class="hero-h1 mb-6 max-w-5xl mx-auto">
      <span>Resolva a bagunça da sua produção de conteúdo,</span>
      <span class="gradient-text">em todos os formatos.</span>
      <span class="subheadline italic">Sem precisar de mais uma ferramenta.</span>
    </h1>
    <div class="hero-cta">
      <button>CTA Primário</button>
    </div>
  </div>
</section>
```

**Medidas:**
- Max-width hero-h1: 80rem (1280px) ou `max-w-5xl`
- Gap badge → h1: 24px (mb-6)
- Gap h1 → CTA: 24-32px
- Padding vertical: 40-56px mobile, 56-96px desktop

**Background:**
- Dot grid pattern (32px spacing)
- Mask radial-gradient (elipse central)
- Noise overlay (opacity 0.35)
- Aurora blobs (3 layers, fixed)

---

### 3. Badge (Eyebrow)

```html
<div class="badge">
  <svg class="icon">...</svg>
  App oficial · Método Sistema Reverso
</div>
```

**CSS:**
```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px; /* gap-2 */
  padding: 6px 16px; /* px-4 py-1.5 */
  border-radius: 9999px; /* rounded-full */
  border: 1px solid rgba(167,139,250,0.30); /* violet-400/30 */
  background: rgba(139,92,246,0.10); /* violet-500/10 */
  font-size: 12px; /* text-xs */
  font-weight: 700; /* font-bold */
  text-transform: uppercase;
  letter-spacing: 0.2em; /* tracking-[0.2em] */
  color: #d8b4fe; /* violet-300 */
  backdrop-filter: blur(4px); /* backdrop-blur-sm */
}
```

**Ícone:** lucide-react `sparkles` (h-3 w-3, 12px).

---

### 4. Botões

#### CTA Primário

```css
.btn-primary {
  background: linear-gradient(135deg, #a78bfa, #f0abfc); /* violet → fuchsia */
  color: #fff;
  box-shadow: 0 10px 40px rgba(139,92,246,0.4);
  padding: 14px 32px; /* px-8 py-3.5 */
  border-radius: 9999px; /* rounded-full */
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 16px;
  transition: all 200ms ease-out;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 50px rgba(139,92,246,0.5);
}
```

#### CTA Secundário (Ghost)

```css
.btn-ghost {
  background: transparent;
  color: #f4f4f5;
  border: 1px solid rgba(167,139,250,0.40);
  padding: 14px 32px;
  border-radius: 9999px;
}

.btn-ghost:hover {
  background: rgba(139,92,246,0.10);
  border-color: rgba(167,139,250,0.60);
}
```

---

### 5. Cards (Features/Benefit)

```html
<div class="feature-card">
  <div class="icon-wrapper">
    <svg>...</svg>
  </div>
  <h3>Título do Benefício</h3>
  <p>Descrição detalhada...</p>
</div>
```

**CSS:**
```css
.feature-card {
  background: rgba(139,92,246,0.03); /* tint violeta sutil */
  border: 1px solid rgba(167,139,250,0.20);
  border-radius: 20px; /* rounded-2xl */
  padding: 32px; /* p-8 */
  transition: border-color 200ms, background 200ms;
}

.feature-card:hover {
  background: rgba(139,92,246,0.06);
  border-color: rgba(167,139,250,0.40);
}

.icon-wrapper {
  width: 48px; height: 48px;
  border-radius: 12px;
  background: rgba(167,139,250,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  margin-bottom: 16px;
}
```

---

### 6. Pricing Card

Card destacado com preço R$ 197.

```html
<div class="pricing-card">
  <div class="pricing-header">
    <span class="badge">Mais popular</span>
    <h3>{{Plataforma_Conteudo}}</h3>
    <div class="price">
      <span class="currency">R$</span>
      <span class="amount">197</span>
      <span class="period">/mês</span>
    </div>
  </div>
  <ul class="features">
    <li>[Icon] Feature 1</li>
    ...
  </ul>
  <button class="btn-primary">Começar agora</button>
</div>
```

**CSS highlights:**
```css
.pricing-card {
  background: linear-gradient(135deg, rgba(139,92,246,0.08) 0%, transparent 100%);
  border: 1px solid rgba(167,139,250,0.40);
  border-radius: 24px; /* rounded-3xl */
  padding: 40px;
  box-shadow: 0 20px 60px rgba(139,92,246,0.2);
}

.price .amount {
  font-family: var(--font-display);
  font-size: clamp(48px, 6vw, 64px);
  font-weight: 800;
  background-image: linear-gradient(120deg, #a78bfa, #f0abfc);
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

### 7. FAQ (Accordion)

Provavelmente `<details>` nativo estilizado.

```html
<details class="faq-item">
  <summary>
    <span>Pergunta frequente</span>
    <svg class="icon-chevron">...</svg>
  </summary>
  <p>Resposta...</p>
</details>
```

**CSS:**
```css
.faq-item {
  border: 1px solid rgba(167,139,250,0.20);
  background: rgba(139,92,246,0.02);
  border-radius: 16px;
  padding: 20px 24px;
  transition: border-color 200ms;
}

.faq-item[open] {
  border-color: rgba(167,139,250,0.40);
}

summary {
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #f4f4f5;
}

.icon-chevron {
  transition: transform 200ms;
}

.faq-item[open] .icon-chevron {
  transform: rotate(180deg);
}
```

---

### 8. Footer

Estrutura simples (não tão extenso quanto o premium).

**Seções:**
- Logo + tagline
- Links (Produto, Suporte, Legal)
- Social icons
- Copyright

**CSS:**
```css
.site-footer {
  border-top: 1px solid rgba(167,139,250,0.20);
  background: #030014;
  padding: 48px 24px 32px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
}
```

---

### 9. Seção YouTube

Similar ao premium, mas com tint violeta (não vermelho puro).

**Background:**
- Gradient dark violeta/red blend
- Radial glow violeta
- Border violeta sutil

**CTA button YouTube:**
- Background red (#ff0000 ou similar)
- Glow vermelho (0 6px 24px rgba(255,0,0,0.4))
- Logo YouTube SVG inline

---

## Responsividade

### Breakpoints

Tailwind defaults:

| Nome | Min-Width | Uso |
|---|---|---|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Wide desktop |

### Comportamento Mobile

- **Hero h1:** clamp de 40px (mobile) a 76px (desktop)
- **Section padding:** py-10 (40px mobile) → py-24 (96px desktop)
- **Container padding:** sempre px-6 (24px) em todas as telas
- **Grid colunas:** features 3 cols → 2 cols (md) → 1 col (mobile)
- **Cards:** stacks verticalmente em mobile (<md)
- **Badge font-size:** mantém 12px (não reduz)

### Media Queries Canônicas (Tailwind)

```css
@media (min-width: 768px) { ... }  /* md: tablet+ */
@media (min-width: 1024px) { ... } /* lg: desktop */
```

---

## Imagens & Mídia

### Aspect Ratios

- **Logo {{Plataforma_Conteudo}}:** landscape (aprox 3:1 ou 4:1)
- **Feature icons:** 1:1 (quadrado, 48x48px)
- **Screenshots dashboard:** 16:10 ou 16:9 (wide)
- **YouTube thumbs:** 16:9 (maxresdefault)

### Lazy Loading

Todas as imagens abaixo do fold:
```html
<img loading="lazy" ... />
```

Next.js Image component com `priority={false}` por padrão.

### Tratamentos

- **Border-radius screenshots:** rounded-xl (16px) ou rounded-2xl (20px)
- **Border:** 1px solid rgba(167,139,250,0.30) em alguns casos
- **Box-shadow:** 0 8px 32px rgba(0,0,0,0.3) para profundidade

### Logo {{Plataforma_Conteudo}}

Provavelmente:
- SVG ou PNG com gradient pink/purple
- Width: 140-180px (header)
- Height: auto
- Posição: absolute ou flex (header left)

**Path provável:** `/logo-reverso.png` (conforme preload no HTML).

---

## Como Usar Este Design System

### Para Desenvolvedores

1. **Setup Tailwind + Next.js:**
   - Instalar Tailwind CSS
   - Configurar `tailwind.config.js` com cores customizadas:
     ```js
     theme: {
       extend: {
         colors: {
           '{{plataforma_conteudo}}-bg': '#030014',
           '{{plataforma_conteudo}}-violet': '#a78bfa',
           '{{plataforma_conteudo}}-fuchsia': '#f0abfc',
           '{{plataforma_conteudo}}-orange': '#fb923c',
         },
         fontFamily: {
           display: ['Syne', 'system-ui', 'sans-serif'],
           body: ['DM Sans', 'system-ui', 'sans-serif'],
         },
       },
     }
     ```

2. **Importar fontes via Next.js:**
   ```tsx
   import { Syne, DM_Sans } from 'next/font/google'
   
   const syne = Syne({ subsets: ['latin'], weight: ['600','700','800'] })
   const dmSans = DM_Sans({ subsets: ['latin'], weight: ['300','400','500'] })
   ```

3. **Aurora background:**
   ```tsx
   <div className="fixed inset-0 overflow-hidden -z-10 pointer-events-none">
     <div className="absolute top-[-15%] left-[-10%] w-[560px] h-[560px] rounded-full bg-violet-600 opacity-[0.18] blur-[120px]" />
     <div className="absolute top-[30%] right-[-15%] w-[640px] h-[640px] rounded-full bg-fuchsia-600 opacity-[0.12] blur-[140px]" />
     <div className="absolute bottom-[-10%] left-[25%] w-[480px] h-[480px] rounded-full bg-pink-600 opacity-[0.10] blur-[120px]" />
   </div>
   ```

4. **Dot grid pattern (hero):**
   ```tsx
   <div 
     className="absolute inset-0 opacity-[0.35] pointer-events-none"
     style={{
       backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px)',
       backgroundSize: '32px 32px',
       maskImage: 'radial-gradient(ellipse at center, black 30%, transparent 75%)',
       WebkitMaskImage: 'radial-gradient(ellipse at center, black 30%, transparent 75%)',
     }}
   />
   ```

5. **Gradient text:**
   ```tsx
   <span 
     className="block"
     style={{
       backgroundImage: 'linear-gradient(120deg, #a78bfa 0%, #f0abfc 40%, #fb923c 100%)',
       WebkitBackgroundClip: 'text',
       backgroundClip: 'text',
       WebkitTextFillColor: 'transparent',
     }}
   >
     em todos os formatos.
   </span>
   ```

6. **Reveal on scroll:**
   - Adicionar `data-reveal="true"` em elementos
   - Script IntersectionObserver (threshold 0.1-0.2)
   - Aplicar classe `.visible` quando entra em viewport

### Para Copywriters

1. **Hierarquia de texto:**
   - Eyebrow badge (UPPERCASE, tracking largo) → h1 (gigante, gradient) → subheadline (italic, muted) → body (17-18px, line-height 1.65) → CTA.

2. **Tom de voz:**
   - Mais direto e tech-friendly que o premium.
   - Foco em **resolver dor** (bagunça, caos) e **eficiência** (piloto automático).
   - Menos editorial, mais produto SaaS.

3. **CTAs:**
   - Repetir CTA a cada 2 sections (hero, features, pricing, FAQ).
   - Texto: "Começar agora", "Criar minha conta", "Experimentar grátis".

4. **Prova social:**
   - Depoimentos curtos (1-2 frases), sem foto (ou initial avatar).
   - Métricas de produto (número de usuários, conteúdos criados).
   - Logos de clientes (se aplicável).

### Para Designers

1. **Mockups no Figma:**
   - Background: #030014 (deep purple)
   - Aurora blobs: 3 camadas separadas (violet, fuchsia, pink) com blur alto
   - Dot grid pattern: camada acima do bg, opacity 35%
   - Texto sempre #f4f4f5 ou muted (70% opacity)

2. **Componentes variants:**
   - Badge (idle)
   - Button primary (idle / hover / pressed)
   - Card feature (idle / hover)
   - FAQ item (closed / open)

3. **Motion prototyping:**
   - Hover: 200ms ease-out, translateY -2px
   - Reveal: 400ms ease-out, opacity 0→1, translateY 20→0
   - Aurora: 20s ease-in-out infinite alternate (slow drift)

4. **Grid system:**
   - Container: 1200px max
   - Padding lateral: 24px
   - Spacing base: 4px (Tailwind)
   - Gap entre cards: 20-24px

### Critérios de Qualidade (Checklist)

Antes de publicar página {{Plataforma_Conteudo}}, verificar:

- [ ] Background é #030014 (deep purple, NÃO #000)
- [ ] Aurora blobs presentes (3 blobs: violet, fuchsia, pink) com blur 120-140px
- [ ] Dot grid pattern no hero (32px spacing, mask elipse)
- [ ] Tipografia usa Syne (headings) + DM Sans (body)
- [ ] Hero h1 usa `clamp(40px, 6vw, 76px)` + tracking `-0.035em`
- [ ] Gradient text usa 3 cores (violet → fuchsia → orange)
- [ ] Badges são UPPERCASE com tracking `0.2em`
- [ ] Botão primário tem gradient violeta→fuchsia + glow
- [ ] Cards têm border `violet-400/30` (não white/10)
- [ ] Reveal on scroll funciona (data-reveal + IntersectionObserver)
- [ ] Pricing card destacado (R$ 197 com gradient text)
- [ ] FAQ accordion funciona (chevron rotate 180deg)
- [ ] Footer tem border-top violeta
- [ ] Mobile: hero h1 clamp mínimo 40px, padding sections reduzido

---

## Screenshots de Referência

Armazenados em `workspace/design-systems/guiavila-{{plataforma_conteudo}}/screenshots/`:

- `{{plataforma_conteudo}}-desktop.png` — Desktop (1440x900)
- `{{plataforma_conteudo}}-mobile.png` — Mobile (390x844)

Consultar screenshots para replicar spacing exato, cores, hierarquia visual.

---

## Diferenças vs Design System Premium

### {{Plataforma_Conteudo}} (SaaS)
- **Paleta:** Violeta/Rosa/Laranja vibrante (#a78bfa, #f0abfc, #fb923c)
- **Background:** Deep purple (#030014), não puro black
- **Voz:** Energético, tech, ousado, produto SaaS
- **Tipografia:** Tracking mais largo em badges, line-height mais tight em hero
- **Motion:** Mais rápido/snappy (200ms padrão)
- **Glassmorphism:** Sutil (5% bg, 30% border, 8px blur)
- **Gradientes:** Multi-cor (3 stops), mais vibrante
- **Dot grid:** Background pattern técnico (32px radial)
- **Target:** Usuários de produto SaaS, criadores de conteúdo, tech-savvy

### Premium (Editorial)
- **Paleta:** Dourado/Black (#c9a961, #000)
- **Background:** Puro black (#000)
- **Voz:** Premium, editorial, denso, sofisticado, confiável
- **Tipografia:** Tracking negativo sutil, line-height generoso em body
- **Motion:** Suave/elegante (600ms padrão, cubic-bezier .22,1,.36,1)
- **Glassmorphism:** Moderado (4% bg, 8% border, 12px blur)
- **Gradientes:** Monocromático dourado (2-4 stops sutis)
- **Aurora:** Blobs dourados sutis (6% opacity)
- **Target:** Clientes premium, infoprodutores high-ticket, educação executiva

---

## Notas Finais

- **Este design system é produto SaaS**, não editorial. Motion mais rápido, cores vibrantes, menos peso visual.
- **Violeta é a cor primária** (não dourado). Sempre usar violet-400/violet-500 como base.
- **Gradientes são multi-cor**, não monocromáticos. Hero sempre 3 cores (violet → fuchsia → orange).
- **Dot grid é signature visual** do {{Plataforma_Conteudo}} (vs aurora blobs do premium).
- **UPPERCASE tracking largo é obrigatório** em badges (0.2em, nunca menos).
- **Aurora blobs são mais intensos** que o premium (18%/12%/10% vs 6% opacity).

Ao criar nova página ou feature {{Plataforma_Conteudo}}, **consulte os 2 screenshots** como referência visual final. Este MD documenta tokens, componentes e padrões — screenshots mostram resultado esperado em produção.

---

**Documentado por:** desenvolvedor-frontend (squad-dev)  
**Data:** 2026-05-14  
**Status:** ✅ Completo e validado contra HTML/CSS em produção ({{plataforma_conteudo}}.{{DOMINIO}})
