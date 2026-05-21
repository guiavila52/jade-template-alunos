---
name: executar-bateria-qa
description: Roda bateria automatizada de QA funcional em paginas (regressoes, console, 404, acessibilidade, performance, SEO) antes do deploy.
type: skill
---

## ⚠️ Playwright SEMPRE headless (Regra §5 — memória feedback_playwright_sempre_headless)

NUNCA `headless: false` nem `devtools: true`. Browser visível no Mac do {{NOME_OPERADOR}} atrapalha trabalho dele.

```js
// ✅ Correto
await chromium.launch({ headless: true });
```

Pra inspeção visual, usa `page.screenshot()` + leitura do arquivo. Pra inspecionar DOM ao vivo, usa `page.evaluate()` retornando valores computed.


# Skill: /executar-bateria-qa

**Agente:** @analista-qa (squad-dev)  
**Maturidade:** 🟡 FUNCIONAL  
**Propósito:** Bateria automatizada de QA funcional em páginas antes do deploy em produção. Detecta regressões funcionais, console errors, 404s, acessibilidade básica, performance e SEO.

---

## Input

- **páginas:** lista de URLs em produção a testar (default: 10 páginas prioritárias em `sites.{{DOMINIO}}`)
- **modo:** `pre-prod` (testa preview antes de --prod) ou `prod` (auditoria em produção)

**Default (se não especificado):**
```json
[
  "https://sites.{{DOMINIO}}/",
  "https://sites.{{DOMINIO}}/squad-time-ia",
  "https://{{DOMINIO}}/automacoes",
  "https://sites.{{DOMINIO}}/mentoria",
  "https://sites.{{DOMINIO}}/consultoria",
  "https://sites.{{DOMINIO}}/imersao",
  "https://sites.{{DOMINIO}}/ferramentas",
  "https://sites.{{DOMINIO}}/sistema-reverso",
  "https://sites.{{DOMINIO}}/sobre",
  "https://sites.{{DOMINIO}}/templates"
]
```

---

## O que fazer

Executar 10 categorias de testes funcionais automatizados via Playwright:

### 1. **Regressões funcionais**
- Sliders rail: drag fluido, `scroll-snap-type: none` obrigatório, momentum presente
- Vídeos: `readyState >= 3` (loaded metadata + canplay)
- Forms: submit funcional (POST 200 ou redirect após submit)
- Links: nenhum `href="#"` ou `href="javascript:void(0)"` sem handler
- Sticky elements: sem flap loop (observer não causa re-scroll infinito)

### 2. **Console errors**
Classificação por severidade:
- **CRITICAL:** JS error que quebra funcionalidade (uncaught exception, network 5xx em API crítica)
- **HIGH:** 404 em asset visível (imagem, CSS crítico, fonte hero)
- **MEDIUM:** warning de terceiros (analytics, GTM, chatbot), 404 em script não-crítico
- **LOW:** LC Tracking errors (pré-existentes, documentados), deprecation warnings

**Exceção conhecida:** `LC Tracking` errors são MEDIUM (não reprovam, apenas anotam).

### 3. **404s em assets**
- Network log com `status >= 400`
- HIGH se asset visível (img, CSS, font)
- MEDIUM se script analítico (gtag, fbpixel, etc)
- Ignora: `/favicon.ico` legacy paths (não crítico se `Base.astro` tem o canônico)

### 4. **Acessibilidade básica**
- `<html lang="pt-BR">` presente
- `<title>` presente e não-vazio
- `<h1>` único (apenas 1 por página)
- `<img>` tem `alt` (vazio ok em decorativas)
- Contraste WCAG AA mínimo (4.5:1 text, 3:1 large text) em hero/CTAs
- Botões têm texto visível ou `aria-label`

### 5. **Performance**
- LCP (Largest Contentful Paint) < 2.5s
- CLS (Cumulative Layout Shift) < 0.1
- TBT (Total Blocking Time) razoável (< 300ms)

**Nota:** performance de terceiros (GTM, fbpixel) NÃO reprova — apenas anota se exceder 500ms.

### 6. **SEO básico**
- `<link rel="canonical">` correto (aponta pra URL atual)
- `<meta name="description">` presente
- OG tags (`og:title`, `og:description`, `og:image`)
- GTM-NN36ZRZ presente >= 2 ocorrências (script head + noscript body)
- Favicon canônico (`/images/favicon-gui.ico` + `/images/favicon-gui.png`)

### 7. **Regras Invioláveis específicas**
- Astro nativo: `/_astro/` presente em network log (> 0 requests)
- Snapshot externo PROIBIDO: `framerusercontent.com` = 0 requests
- Slider rail: `scroll-snap-type: none` (nunca `mandatory` ou `proximity`)
- Cursor grab desktop: sliders drag-enabled têm `cursor: grab` em `@media (hover: hover)`

### 8. **Scroll global funcional**
- Página scrolla de top → bottom sem travamento
- Sticky headers não causam flap (re-observação infinita)
- IntersectionObserver targets existem no DOM (não undefined)
- Mobile (375px) + Desktop (1440px) ambos funcionais

### 9. **Drag de slider**
- Rail mode: drag altera `scrollLeft` ou `translateX`
- Momentum continua após soltar (rAF decay loop)
- Pointer capture ativo (não perde drag ao sair da área)
- Mobile touch + Desktop mouse ambos funcionais

### 10. **Iframe altura correta**
- GHL forms: altura ajusta ao conteúdo (sem corte)
- Min-height modesto (720px desktop, 640px mobile)
- Watchdog visibilidade ativo (form_embed.js)
- Sem buraco gigante (1500px+ sem conteúdo)

---

## Fluxo

```
┌─────────────────────────────────────────────┐
│ 1. Recebe lista de páginas (ou default)     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 2. Prepara Playwright (headless, timeout)   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 3. Para cada página:                        │
│    - Navega + aguarda networkidle           │
│    - Coleta console errors                  │
│    - Coleta network log (404s)              │
│    - Executa 10 baterias de testes          │
│    - Classifica severidade                  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 4. Gera relatório markdown:                 │
│    - Summary (total CRITICAL/HIGH/MEDIUM)   │
│    - Por página (tabela de defeitos)        │
│    - Veredicto: APROVADO / REPROVADO       │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 5. Salva em workspace/output/auditorias/        │
│    bug-hunt-{timestamp}.md                  │
└─────────────────────────────────────────────┘
```

---

## Regras

### Regra Inviolável #22 (Confiabilidade)
- Timeout 30s por página (timeout = anota MEDIUM "timeout navegação")
- Captura stderr + exit code de comandos externos
- Graceful degradation: se Playwright crashar, continua próxima página (não aborta bateria inteira)

### Regra Inviolável #24 (Bateria de testes)
Toda skill de teste TEM bateria própria que valida a skill antes de commit. Aqui:
- Testa contra 3 páginas conhecidas (1 limpa, 1 com warnings, 1 com erro crítico)
- Valida que classifica severidade corretamente
- Valida que relatório é gerado mesmo se 1 página falhar

### Regra Inviolável #23 (Triple-check)
Bug-hunter é 1 dos 3 pilares do triple-check antes de `vercel --prod`. Nunca rodar sozinho — sempre com `paginas` (copy/UX) + `paginas-dev` (código).

### Quando reprovar
- **CRITICAL >= 1:** REPROVAR (bloqueia deploy)
- **HIGH >= 3:** REPROVAR
- **MEDIUM >= 10:** APROVAR COM RESSALVAS (deploy ok, mas criar issue pra corrigir)
- **LOW qualquer quantidade:** APROVAR (apenas anota)

### O que NÃO faz
- **NÃO corrige** bugs — só detecta e reporta
- **NÃO modifica** código — read-only (Bash, Read, WebFetch, Playwright)
- **NÃO faz deploy** — correção fica com `paginas-dev` ou `paginas` conforme natureza

---

## Bateria de testes da skill

Antes de dar commit nesta skill, validar:

```bash
# 1. Testa contra página limpa (deve APROVAR)
/executar-bateria-qa --paginas='["https://sites.{{DOMINIO}}/sobre"]' --modo=prod

# 2. Testa contra página com warnings (deve APROVAR COM RESSALVAS)
/executar-bateria-qa --paginas='["https://sites.{{DOMINIO}}/sistema-reverso"]' --modo=prod

# 3. Testa contra página com erro crítico conhecido (deve REPROVAR)
# (não temos uma em prod — simular com preview quebrada)

# 4. Valida que relatório é gerado em workspace/output/auditorias/
ls -lh /Users/{{SEU_USUARIO}}/Documents/Projetos\ IA\ {{NOME_OPERADOR}}\ Ávila/Squad\ Empresa\ {{NOME_OPERADOR}}\ Ávila/workspace/output/auditorias/bug-hunt-*.md

# 5. Valida classificação de severidade (grep no relatório)
grep -E "CRITICAL|HIGH|MEDIUM|LOW" workspace/output/auditorias/bug-hunt-*.md | head -20
```

**Critérios de sucesso:**
- Relatório gerado mesmo se 1 página timeout
- Classificação severidade correta (LC Tracking = MEDIUM, não CRITICAL)
- Veredicto correto (REPROVAR se CRITICAL >= 1)
- Tempo de execução razoável (< 3 min pra 10 páginas)

---

## Integrações

- **Playwright:** automação de browser (via `npx playwright test` ou Python `playwright.sync_api`)
- **Network log:** captura via `page.on("response")` ou Chrome DevTools Protocol
- **Console errors:** captura via `page.on("console")` + classificação por tipo (`error`, `warning`)
- **Lighthouse:** opcional (se performance for gargalo) — `npx lighthouse --quiet --output=json`

---

## Memórias persistentes

Consultar antes de executar:
- `feedback_drag_fluido_obrigatorio.md` (#165) — slider rail rules
- `feedback_cursor_grab_sliders.md` (#139) — cursor grab desktop
- `feedback_gtm_obrigatorio.md` (#147) — GTM-NN36ZRZ
- `feedback_favicon_padrao.md` (#149) — favicon canônico
- `feedback_smoke_test_funcional_revisor.md` — markup ≠ comportamento
- `feedback_teste_scroll_obrigatorio.md` — sticky/scroll global
- `feedback_teste_funcional_slider.md` — sliders

---

## Output canônico

Path: `workspace/output/auditorias/bug-hunt-{YYYY-MM-DD-HHMM}.md`

Estrutura:
```markdown
# Bateria QA — {modo} — {timestamp}

## Summary
- Total páginas testadas: 10
- CRITICAL: 0
- HIGH: 2
- MEDIUM: 5
- LOW: 8

## Veredicto
APROVADO COM RESSALVAS

---

## Página: https://sites.{{DOMINIO}}/squad-time-ia

### Console errors
- [HIGH] Uncaught ReferenceError: foo is not defined (linha 42)
- [MEDIUM] LC Tracking: session timeout (conhecido)

### 404s
- [HIGH] /images/hero-bg.webp (404) — asset visível

### Acessibilidade
✅ Tudo ok

### Performance
- LCP: 1.8s ✅
- CLS: 0.05 ✅
- TBT: 120ms ✅

### SEO
✅ Tudo ok

### Regras Invioláveis
✅ Astro nativo (/_astro/ presente)
✅ Sem snapshot externo (framerusercontent = 0)

---

[... próximas páginas ...]
```

---

## Última atualização
11/05/2026 — skill criada (Onda B4)

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{NOME_OPERADOR}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
