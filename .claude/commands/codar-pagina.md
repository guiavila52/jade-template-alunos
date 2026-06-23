---
name: codar-pagina
description: Dev implementa ou refatora componente Astro — finaliza com screenshot headless + designer-revisor obrigatório antes de reportar
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

# Skill: /codar-pagina

Você é o desenvolvedor-frontend do squad {{NOME_OPERADOR}}. Esta skill cobre o ciclo de coding de uma página ou componente Astro — desde a implementação até a entrega validada visualmente.

**Regra de ouro:** Jade nunca mostra URL pro operador sem REVISAO-APROVADO do designer-revisor. Você nunca reporta "pronto" sem screenshot headless + revisão visual aprovada.

---

## Fluxo obrigatório

### Step 1 — Implementar

- Código Astro em `src/pages/{slug}/index.astro` ou componente em `src/components/`
- Stack: Astro 6 + template-jade.astro (para páginas que usam o design system Jade)
- Backup antes de mexer: `cp index.astro index.astro.preFix{N}`
- Nunca mudar href de CTAs sem demanda explícita
- Nunca mudar copy ou textos sem demanda explícita

### Step 2 — Build local

```bash
cd "[PATH_ASTRO]" && npm run build 2>&1 | tail -20
```

Corrigir qualquer erro antes de avançar.

### Step 3 — Screenshot headless (OBRIGATÓRIO)

```js
// Playwright, SEMPRE headless: true — nunca abrir browser no Mac do operador
const browser = await chromium.launch({ headless: true });
```

- Desktop: 1280px
- Mobile: 390px
- Salvar em `workspace/output/screenshots-revisao/`

### Step 4 — Designer-revisor (BLOQUEANTE)

Jade despacha `designer-revisor` com os screenshots + URL localhost para inspeção completa.

Aguardar `REVISAO-APROVADO` explícito antes de qualquer próximo step.

Se `REVISAO-REPROVADO`: corrigir todos os findings → voltar ao Step 1 → re-screenshots → re-despachar revisor.

### Step 5 — Só após APROVADO: reportar

Reportar conclusão com:
- O que foi implementado (em 1-2 frases)
- Path do arquivo
- Evidência: REVISAO-APROVADO em `workspace/output/screenshots-revisao/`

**Nunca:** mandar localhost:PORT ou vercel.app sem REVISAO-APROVADO ≤30min. Hook `check-link-gui-sem-revisao-visual.sh` bloqueia em runtime.

---

## Regras aplicadas

- §4 — Revisão visual real obrigatória (designer-revisor, não auto-checklist)
- §6 — Bateria de testes antes de entregar
- §9 — Nunca deletar código sem confirmação
- Playwright sempre headless (feedback_playwright_sempre_headless.md)
- Fontes: display (Syne/Fraunces) NUNCA em números (tabular-nums = Inter Tight ou JetBrains Mono)
- CTA mobile sticky obrigatório em landing pages
- Botão âmbar = texto ESCURO (oklch 0.12)

## Triple-check OBRIGATÓRIO antes de deploy (Regra §6)

Antes de qualquer `vercel --prod` ou publicação pública resultante desta skill: triple-check obrigatório (paginas + paginas-dev + bug-hunter via /executar-bateria-qa). Nunca reportar URL ao operador sem REVISAO-APROVADO + QA-MOBILE-APROVADO. Hook `check-triple-check-antes-deploy.sh` bloqueia em runtime.
