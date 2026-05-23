# MAPA — Design Systems

**Propósito:**  
Documentar design systems implícitos do Gui Ávila extraídos de páginas em produção. Cada design system congela tokens (paleta, tipografia, spacing, motion) de uma linguagem visual específica, permitindo replicação fiel em novas páginas.

---

## Estrutura

```
workspace/design-systems/
├── mapa.md                          [este arquivo — índice dos design systems]
├── guiavila-premium.md              [design system extraído de /mentoria e /reverso]
├── guiavila-premium/
│   └── screenshots/
│       ├── mentoria.png             [desktop 1440x900]
│       ├── mentoria-mobile.png      [mobile 390x844]
│       ├── reverso.png              [desktop 1440x900]
│       └── reverso-mobile.png       [mobile 390x844]
├── guiavila-{{plataforma_conteudo}}.md              [design system extraído de {{plataforma_conteudo}}.{{DOMINIO}}]
├── guiavila-{{plataforma_conteudo}}/
│   └── screenshots/
│       ├── {{plataforma_conteudo}}-desktop.png      [desktop 1440x900]
│       └── {{plataforma_conteudo}}-mobile.png       [mobile 390x844]
├── guiavila-clean.md                [design system baseado em Resend — técnico-acolhedor]
└── guiavila-clean/
    └── screenshots/
        ├── resend-home-desktop.png  [desktop 1440x900]
        ├── resend-home-mobile.png   [mobile 390x844]
        ├── resend-docs-desktop.png  [desktop 1440x900]
        └── resend-pricing-desktop.png [desktop 1440x900]
```

---

## Design Systems Ativos

### 1. **guiavila-premium**

- **Páginas de referência:**
  - https://sites.{{DOMINIO}}/mentoria
  - https://sites.{{DOMINIO}}/reverso

- **Características:**
  - Fundo preto (#000) + dourado premium (#c9a961)
  - Tipografia editorial (Syne display + DM Sans body)
  - Glassmorphism sutil (backdrop-blur 12px)
  - Aurora blobs animados (20s ease-in-out loop)
  - Motion suave (cubic-bezier .22,1,.36,1)
  - Prova social densa (depoimentos, logos, métricas)
  - CTAs repetidos a cada 2-3 sections

- **Voz visual:**  
  Premium, editorial, denso, sofisticado, confiável

- **Documentação:**  
  `guiavila-premium.md` (completo, 500+ linhas)

- **Screenshots:**  
  4 arquivos em `guiavila-premium/screenshots/`

- **Status:**  
  ✅ Completo e validado (2026-05-14)

---

### 2. **guiavila-{{plataforma_conteudo}}**

- **Páginas de referência:**
  - https://{{plataforma_conteudo}}.{{DOMINIO}}

- **Características:**
  - Deep purple background (#030014, não puro black)
  - Gradientes multi-cor vibrantes (violet → fuchsia → orange)
  - Tipografia tech-friendly (Syne display + DM Sans body)
  - Aurora blobs intensos (violet-600, fuchsia-600, pink-600)
  - Dot grid pattern técnico (32px radial)
  - Motion snappy (200ms padrão, produto SaaS)
  - Glassmorphism sutil (violet tint, 8px blur)
  - UPPERCASE tracking largo obrigatório em badges (0.2em)

- **Voz visual:**  
  SaaS moderno, energético, tech/produto, ousado, focado

- **Documentação:**  
  `guiavila-{{plataforma_conteudo}}.md` (completo, 500+ linhas)

- **Screenshots:**  
  2 arquivos em `guiavila-{{plataforma_conteudo}}/screenshots/`

- **Status:**  
  ✅ Completo e validado (2026-05-14)

---

### 3. **guiavila-clean**

- **Página de referência:**  
  https://resend.com

- **Características:**
  - Cinza muito escuro (#09090b, não puro preto)
  - Accent azul funcional único (#3b82f6)
  - Tipografia Inter (clean, weights 400-600)
  - Sem glassmorphism (bordas limpas)
  - Motion contido (300-400ms, não agressivo)
  - Spacing respirável (64-80px sections)
  - Line-height generoso (1.65)
  - Bordas ultra-sutis (rgba 0.06)
  - Code blocks com Commit Mono

- **Voz visual:**  
  Contemporâneo, técnico-acolhedor, respirável, preciso, confiável

- **Documentação:**  
  `guiavila-clean.md` (completo, 700+ linhas)

- **Screenshots:**  
  4 arquivos em `guiavila-clean/screenshots/`

- **Status:**  
  ✅ Completo e validado (2026-05-14)

---

## Quando Usar Cada Design System

| Design System | Usar quando... | NÃO usar quando... |
|---|---|---|
| **premium** | Página de venda high-ticket (mentoria, consultoria, curso premium), lançamento de produto premium, landing page de conversão | Página institucional simples, blog post, painel de produto SaaS |
| **{{plataforma_conteudo}}** | Páginas do produto {{Plataforma_Conteudo}}, features/pricing do {{Plataforma_Conteudo}}, onboarding {{Plataforma_Conteudo}} | Venda de outros produtos (mentoria, curso), conteúdo educacional |
| **clean** | Squad-template pra alunos, /tools, /docs, tutoriais técnicos, dashboards internos, páginas que precisam transmitir competência técnica sem vender | Landing page high-ticket, páginas que precisam energia/vibrância, conteúdo editorial denso |

---

## Como Criar Novo Design System

1. **Identificar páginas de referência** (mínimo 2 páginas em produção da mesma linguagem visual)
2. **Baixar HTML + CSS** de cada página via `curl`
3. **Tirar screenshots** (desktop 1440x900 + mobile 390x844) via Playwright
4. **Extrair tokens:**
   - Paleta (variáveis `--color-*` + hex + uso)
   - Tipografia (families, weights, sizes, line-heights, letter-spacing)
   - Spacing (scale, containers, section padding)
   - Border-radius, sombras, effects
   - Motion (easings, durations, keyframes)
5. **Documentar componentes-padrão** (hero, botões, cards, listas, footer, etc.) com anatomia + medidas + estados
6. **Descrever voz visual** (3-5 adjetivos com justificativa técnica/visual)
7. **Criar seção "Como usar"** (guia rápido dev/copywriter/designer)
8. **Criar pasta `{nome}/screenshots/`** e salvar os PNGs
9. **Criar `{nome}.md`** no formato do `guiavila-premium.md`
10. **Atualizar este mapa.md** com entrada do novo design system

---

## Última Atualização

2026-05-14 — Design systems **premium**, **{{plataforma_conteudo}}** e **clean** documentados e validados.
