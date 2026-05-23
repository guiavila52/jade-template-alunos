---
name: revisar-visual-pagina
description: Revisao visual REAL de pagina LP antes do triple-check + deploy. Playwright headless desktop+mobile, audit humano, APROVADO/REPROVADO. Squad-dev -> designer-revisor.
type: skill
---

## ⚠️ Playwright SEMPRE headless (Regra §5 — memória feedback_playwright_sempre_headless)

NUNCA `headless: false` nem `devtools: true`. Browser visível no Mac do Gui atrapalha trabalho dele.

```js
// ✅ Correto
await chromium.launch({ headless: true });
```

Pra inspeção visual, usa `page.screenshot()` + leitura do arquivo. Pra inspecionar DOM ao vivo, usa `page.evaluate()` retornando valores computed.


# Skill: /revisar-visual-pagina


## Fluxo

```
Input (path Astro + URL local + briefing + design system)
  ↓
1. Setup Playwright headless (chromium)
2. Screenshots obrigatórios (desktop 1440px + mobile 390px: full-page, foldA, foldB, blocos-âncora)
3. Checklist 13 itens (hero, tipografia, cor/contraste, espaçamento, sliders, iframe forms, sticky/scroll-trigger, motion, logos, responsividade, CTA final, voz visual vs DS, header/footer únicos)
4. Comparativo prod-vs-local (se URL prod informada)
5. Auditar como humano (olho nos screenshots — não só grep no código)
6. Gerar RELATORIO.md: veredito, 13 itens, bugs encontrados, screenshots, comparativo, sugestões
  ↓
Output (REVISAO-APROVADO → libera triple-check | REVISAO-REPROVADO → dev refaz)
```

**Agente:** @designer-revisor (squad-dev)
**Maturidade:** 🟡 FUNCIONAL
**Propósito:** Revisão visual REAL de página Astro (LP) renderizada em browser headless antes do triple-check e deploy. Cumpre Regra §4 (revisão visual obrigatória pra front-end). Diferente de `/revisar-visual` (genérica pra carrossel/criativo/thumb) — esta é específica pra LP em desenvolvimento, com checklist próprio de LP (hero, sliders, iframe forms, scroll, motion, sticky, responsivo).

Reprovar é melhor que aprovar com gap. Auto-checklist do produtor NÃO substitui.

---

## Quando invocar

- Após `/ajustar-pagina` entregar componente Astro
- Após `/revisar-codigo-pagina` aprovar markup/GTM/sliders
- ANTES do triple-check (paginas + paginas-dev + bug-hunter) e ANTES de `vercel --prod`
- Em refresh/redesign de página existente, sempre que dev alterou layout

---

## Input

- **path:** path do componente Astro (`src/pages/[slug]/index.astro` no repo Páginas Astro {{NOME_OPERADOR}})
- **url_local:** URL local pra renderizar (ex: `http://localhost:4321/[slug]`) — dev deve subir `astro dev` antes
- **url_prod_atual:** URL produção atual (ex: `https://sites.{{DOMINIO}}/[slug]`) — opcional pra antes/depois
- **briefing:** path do briefing estratégico que originou a copy (pra validar voz visual vs estratégia)
- **design_system:** path do design system aplicado (ex: `workspace/design-systems/{{operador_slug}}-premium.md`)

**Exemplo:**
```
/revisar-visual-pagina --path=src/pages/mentoria/index.astro --url_local=http://localhost:4321/mentoria --url_prod_atual=https://sites.{{DOMINIO}}/mentoria --briefing=workspace/output/estrategia/2026-05-14-mentoria-redesign-briefing.md --design_system=workspace/design-systems/{{operador_slug}}-premium.md
```

---

## O que o agente faz

### 1. Setup Playwright headless

```bash
npx playwright install chromium 2>/dev/null || true
```

### 2. Screenshots obrigatórios

Em `workspace/output/screenshots-revisao/[YYYY-MM-DD]-[slug]-revisao-visual/`:

- `desktop-1440x900-full.png` — full page desktop
- `mobile-390x844-full.png` — full page mobile
- `desktop-1440x900-foldA.png` — primeira dobra desktop
- `mobile-390x844-foldA.png` — primeira dobra mobile
- `desktop-foldB.png`, `mobile-foldB.png` — segunda dobra
- 1 screenshot por bloco-âncora (hero, oferta, prova, FAQ, CTA Final, form, footer)

Comparativo (se `url_prod_atual` informada):
- `prod-vs-local-desktop.png` (split lado-a-lado)
- `prod-vs-local-mobile.png`

### 3. Checklist de auditoria (12 itens — Regra §6)

Auditar como humano olhando screenshot por screenshot:

1. **Hero**
   - Headline legível em 1ª dobra mobile (não corta)
   - Eyebrow sem placeholder ("CTA, "EYEBROW", "TODO" — REPROVAR)
   - Foto/visual sem distorção, sem corte de cabeça, sem moiré
   - CTA visível na 1ª dobra (mobile + desktop)

2. **Tipografia**
   - Display (Syne/Fraunces) em headings; NUNCA em números
   - Números/preços/datas SEMPRE em Inter Tight tabular-nums ou JetBrains Mono (display jamais em números — Gui 18/05/2026, memória feedback_fonte_display_jamais_em_numeros)
   - Letter-spacing em hero (-0.02em mín se >4rem)
   - Line-height 1.5-1.7 body, 1.2-1.3 headings
   - Sem texto cortado, sem overflow horizontal

3. **Cor / Contraste**
   - WCAG AA (4.5:1 body, 3:1 headings)
   - Paleta consistente com design system declarado
   - CTA destaca-se do fundo
   - Sem texto em medium-on-medium

4. **Espaçamento**
   - `--space-section` consistente entre seções (sem buracos, sem aperto)
   - Gap iframe → próxima seção = `var(--space-section)` (bug histórico: form GHL gera buraco se min-height desalinhado — Regra #109/#116)
   - Padding simétrico em cards
   - Sem 32px gap em A-B e 48px em B-C

5. **Sliders / Marquee**
   - Cursor `grab` em sliders draggable
   - Drag macio (sem trancos, ease cubic-bezier(0.22,1,0.36,1) — padrão premium)
   - Marquee infinito sem "pulo" visível
   - Items não cortados nas bordas

6. **Iframe forms (GHL)**
   - Form renderiza (sem white-screen)
   - Sem "buraco" entre form e próxima seção
   - Mobile: sem scroll horizontal interno
   - Submit button visível
   - `data-height` do snippet GHL respeitado

7. **Sticky / Scroll-trigger**
   - Header sticky não cobre conteúdo
   - Scroll-trigger anima na entrada (reveal funciona)
   - Sem flash-of-unstyled-content (FOUC) na primeira renderização

8. **Motion**
   - Easings premium (cubic-bezier(0.22,1,0.36,1)) — não ease-out genérico
   - Reveal delays incrementais 0.1s
   - Aurora/glow em loop suave (não pisca)
   - Hover states em CTAs (border gold, glow sutil)

9. **Logos / Prova social**
   - Logos oficiais (não SVG genérico)
   - Tamanhos balanceados (sem 1 gigante e outros minúsculos)
   - Métricas legíveis mobile (font-size mínimo 14px)
   - Sem métricas privadas vazadas

10. **Responsividade**
    - Mobile (390px), tablet (768px), desktop (1440px) — testar os 3
    - Sem horizontal scroll
    - Imagens com aspect-ratio preservado
    - Stacking vertical adequado em mobile

11. **CTA Final**
    - Sem placeholder ("CTA, "EYEBROW")
    - Texto-âncora claro
    - Form GHL presente e funcional
    - Gap form → FAQ = `var(--space-section)` (NÃO 600-1000px de buraco — bug histórico)

12. **Voz visual vs design system declarado**
    - Ler `design_system` informado
    - Confirmar: paleta bate, tipografia bate, motion bate, voz adjetiva bate
    - Se desviar do DS sem justificativa → REPROVAR


13. **Header / Footer únicos (regra crítica — 2026-05-14)**
    - grep `<Footer` no source do index.astro deve ser `0` se a page usa Base.astro default
    - Capturar screenshot full-page e VER se há rodapé/header repetido
    - Bug histórico: /mentoria 2026-05-14 — dev adicionou <Footer /> manual + Base.astro já renderiza por default = 2 footers. Passou batido pelo revisor visual mesmo com 80 screenshots.
    - **Como detectar:** rolar screenshot full-page de cima a baixo SEM PULAR. Se mesmo bloco aparece 2x, REPROVAR.

### 4. Comparativo prod-vs-local (se informado)

- Sobrepor screenshots prod (atual) vs local (novo redesign)
- Listar: blocos novos, blocos removidos, blocos mantidos, blocos modificados
- Sinalizar regressões visuais (algo piorou)

### 5. Output canônico

Arquivo: `workspace/output/screenshots-revisao/[YYYY-MM-DD]-[slug]-revisao-visual/RELATORIO.md`

```markdown
# Revisão visual — /[slug] — [YYYY-MM-DD HH:MM]

**Agente:** @designer-revisor
**Path:** [path do astro]
**URL local:** [url]
**Design system:** [path]

## Veredito

✅ APROVADO  /  ❌ REPROVADO

## 12 itens

| # | Categoria | Status | Observação |
|---|---|---|---|
| 1 | Hero | ✅/❌ | ... |
| ... | ... | ... | ... |
| 12 | DS bate | ✅/❌ | ... |

## Bugs encontrados (se REPROVADO)

- [coordenada/bloco] — descrição — sugestão de fix

## Screenshots

- [lista completa de paths]

## Comparativo prod-vs-local

- Blocos novos: ...
- Removidos: ...
- Regressões visuais: ...

## Sugestões pro dev

[lista priorizada]
```

### 6. Marker canônico no final

Última linha do RELATORIO.md:
- `REVISAO-APROVADO` (libera triple-check)
- `REVISAO-REPROVADO` (dev refaz, novo loop)

---

## Critério de aceitação

- 12 itens auditados (não pular nenhum)
- Screenshots desktop+mobile pra cada bloco-âncora
- Comparativo prod-vs-local (se informado)
- Veredito claro com marker canônico
- Bugs com coordenada/bloco + sugestão de fix
- Path RELATORIO.md retornado pra Jade

---

## Tratamento de erros

- Servidor local não responde → reportar pro dev subir `astro dev`
- Playwright sem chromium → `npx playwright install chromium` automático
- url_prod_atual 404 → ok, pular comparativo (não bloquear)
- Iframe GHL com handshake quebrado headless → confirmar visualmente que iframe RENDERIZA (mesmo sem form interno carregar — limitação Playwright vs GHL)

---

## Aprendizado + pendência (Regra §5)

- Defeito visual recorrente (3+ páginas) → adicionar ao checklist como item permanente
- Falsa aprovação detectada pelo Gui → registrar em `squads/dev/agentes/designer-revisor/aprendizados.md` + atualizar critérios
- Bug bloqueante → criar pendência ClickUp via `/criar-pendencia` antes de reprovar (pra rastrear o loop dev→revisor)

---

## Relação com outras skills

- Chamada APÓS `/ajustar-pagina` + `/revisar-codigo-pagina`
- Gate ANTES de triple-check (paginas + paginas-dev + bug-hunter)
- NUNCA substitui `/revisar-codigo-pagina` (que cuida de markup/GTM/sliders no código)
- NUNCA substitui `/revisar-copy-pagina` (que cuida de COPY, não visual)
- Diferente de `/revisar-visual` (genérica pra carrossel/criativo/thumb — não tem checklist LP-específico de iframe/scroll/sticky)
