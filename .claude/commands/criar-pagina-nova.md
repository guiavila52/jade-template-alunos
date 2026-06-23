---
name: criar-pagina
description: Orquestra criacao ponta-a-ponta de pagina Astro com pipeline template-first canonico. Anti-improviso. Template (premium/clean/{{plataforma_newsletter}}) + frontend-design oficial Anthropic + designer-ui (DESIGN.md) + estrategista + copy + dev extends template + revisor visual real + triple-check + publicar.
type: skill
---

<!-- Modelo recomendado: claude-opus-4-5 -->

# Skill: /criar-pagina-nova (v2 — template-first)

Voce eh a Jade, COO do squad. Esta skill orquestra pipeline canonico template-first pra criar pagina Astro do zero ou redesign completo. Cada step encadeia agentes especialistas via SKILL_INTERNAL=true (libera hook check-agent-sem-skill).

**Stack alvo:** projeto `Paginas Astro {{NOME_OPERADOR}}/` (Astro 6 + Tailwind v4 + 3 templates canonicos em `src/layouts/template-*.astro`).

**Anti-improviso:** Jade nao despacha agente de producao sem rodar skill. Hooks bloqueantes (Regra 3 + 4) impedem fisicamente.

---

## Quando invocar

- Pagina nova (rota inexistente)
- Redesign completo de pagina existente (mudanca visual + estrutural)

## NAO invocar quando

- Fix ciru rgico em pagina existente: usar `/ajustar-pagina` direto
- Migracao de pagina externa (GHL/Framer): usar `/migrar-pagina`
- Ajuste pequeno de copy: usar `/escrever-pagina` direto

## Pre-requisitos (verificar ANTES de iniciar)

1. 3 templates Astro disponiveis em `Paginas Astro {{NOME_OPERADOR}}/src/layouts/template-{premium,clean,{{plataforma_newsletter}}}.astro` (se faltar algum, despachar criacao em branch separada antes)
2. Estrategia viva atualizada em `Segundo Cerebro/04-decisoes/estrategia-viva.md`
3. Skill oficial Anthropic `frontend-design` ativada (`/plugin list` deve mostrar)

## Inputs (perguntar ao {{NOME_OPERADOR_CURTO}} se faltar)

1. Tipo de pagina (vitrine, venda high-ticket, captura lead, blog, docs, dashboard, vitrine SaaS)
2. Audiencia primaria (ICP)
3. Objetivo conversao (lead magnet, venda direta, awareness, login)
4. URL slug
5. Origem trafego esperada (organico, anuncio Meta, email, parceiro)
6. Tem video pra embedar? URL do canal {{NOME_OPERADOR}}

---

## Pipeline (10 steps obrigatorios — Jade orquestra)

```
[0] ESCOLHA TEMPLATE → Jade decide premium/clean/{{plataforma_newsletter}} com justificativa
        |
        v
[1] DESIGN.md → designer-ui (invoca frontend-design oficial Anthropic)
        |
        v
[2] BRIEFING ESTRATEGICO → estrategista (11 secoes)
        |
        v
[3] DESIGN.md + briefing VALIDADOS por revisor independente (NAO {{NOME_OPERADOR_CURTO}})
        |   {{NOME_OPERADOR_CURTO}} valida APENAS codigo rodando localhost (Step 9)
        v
[4] COPY → copywriter
        |
        v
[5] REVISOR COPY → revisor-copy (gate tecnico texto)
        |
        v
[6] CODIGO → desenvolvedor-frontend extends template
        |
        v
[7] REVISAO VISUAL REAL → designer-revisor (Regra 4)
        |   - Passada 1: estetica humana (impressiona? alinhado DESIGN.md?)
        |   - Se aprova: Passada 2 tecnica (Playwright, WCAG, DS)
        v
[8] TRIPLE-CHECK PARALELO → copywriter (revisao copy contextual) + dev-frontend (code review) + analista-qa (12 itens funcional)
        |
        v
[9] PREVIEW VERCEL — PR + auto-deploy + URL pro {{NOME_OPERADOR_CURTO}} (hook §4 libera quando REVISAO-APROVADO presente)
        |
        v
[10] GATE GUI APROVA → merge main → producao
```

---

## Detalhe dos Steps

### Step 0 — Escolha de Template

Matriz de decisao (Jade segue, Regra 15):

| Template | Usar quando | Refs |
|---|---|---|
| premium | Venda high-ticket (mentoria, curso premium, consultoria) | sites.{{DOMINIO}}/mentoria, /seu-produto |
| clean | Vitrine tecnica, docs, captura lead tecnica (squad-template), tutoriais | resend.com, linear.app |
| {{plataforma_newsletter}} | Produto SaaS energetico, features/pricing | {{plataforma_newsletter}}.{{DOMINIO}} |

Jade escolhe + justifica em 1 frase. Apresenta pro {{NOME_OPERADOR_CURTO}} em mensagem curta. Se {{NOME_OPERADOR_CURTO}} discordar, ajusta.

### Step 1 — DESIGN.md canonico

Despachar `designer-ui` (subagent_type=designer-ui) — agente do squad-dev criado pra esta funcao.

```
export SKILL_INTERNAL=true
Agent(subagent_type="designer-ui", prompt="""
INVOCAR skill oficial Anthropic frontend-design ANTES de produzir.

Input:
- Template escolhido: {premium|clean|{{plataforma_newsletter}}}
- Tipo pagina, audiencia, objetivo (do briefing Jade)
- DS correspondente em workspace/design-systems/{{NOME_OPERADOR}}-{template}.md
- Research best practices: workspace/output/research/2026-05-17-frontend-research-comunidade.md

Output: workspace/output/paginas/YYYY-MM-DD-{slug}-design.md
Estrutura: 4 dimensoes frontend-design (Proposito, Tone, Constraints, Differentiation)
         + 3 refs visuais reais aprovadas (URLs verificaveis)
         + tokens OKLCH derivados do template
         + hierarquia visual por dobra
         + lista micro-interactions
         + anti-patterns explicitos (sem gradient azul-roxo-rosa, sem 4 cards iguais, etc)
""")
```

Critério aceitacao DESIGN.md: especifico pra ESSA pagina (nao generico), refs verificaveis, tokens validaveis, anti-AI-slop explicito.

### Step 2 — Briefing estrategico

Despachar `estrategista`:

```
export SKILL_INTERNAL=true
Agent(subagent_type="estrategista", prompt="""
Input: DESIGN.md da Step 1 + tipo pagina + audiencia + objetivo {{NOME_OPERADOR_CURTO}}
Output: workspace/output/estrategia/YYYY-MM-DD-{slug}-estrategia.md
Estrutura: 11 secoes canonicas (posicionamento, angulo, ICP, promessa, prova, jornada emocional, dores, objecoes, headlines, CTA, vinculo com produto principal)
Ler antes: Segundo Cerebro/01-identidade/icp.md + tom-de-voz.md + 04-decisoes/estrategia-viva.md
""")
```

### Step 3 — Validacao independente (NAO {{NOME_OPERADOR_CURTO}})

{{NOME_OPERADOR_CURTO}} NAO revisa DESIGN.md nem briefing em markdown (aprendizado 17/05: ele valida APENAS codigo rodando, ver memoria `feedback_gui_valida_no_codigo_nao_markdown.md`).

DESIGN.md + briefing sao validados por:
1. **Revisor independente do output** (revisor-pagina audita briefing; designer-ui audita proprio output via skill frontend-design oficial Anthropic)
2. **Coerencia interna** (DESIGN.md cita template real, tokens OKLCH reais, refs visuais verificaveis)

Se validacao interna OK, prosseguir DIRETAMENTE pra Step 4 sem pausar pra {{NOME_OPERADOR_CURTO}}.

**Gate {{NOME_OPERADOR_CURTO}} acontece APENAS no Step 9** (preview localhost depois de tudo codado + revisado). {{NOME_OPERADOR_CURTO}} reporta correcoes → aprendizado §5 vai pro agente que produziu o output original.

### Step 4 — Copy

Despachar `copywriter`:

```
export SKILL_INTERNAL=true
Agent(subagent_type="copywriter", prompt="""
Input: briefing estrategico aprovado + DESIGN.md (pra saber tom + tokens)
Output: workspace/output/paginas/YYYY-MM-DD-{slug}-copy.md
Aplicar: Light Copy + tom {{NOME_OPERADOR_CURTO}} + Headline canonica (do briefing) + sem vocabulario banido
""")
```

### Step 5 — Revisor copy

Despachar `revisor-copy`. Gate texto. Se reprovar, voltar Step 4.

### Step 6 — Implementacao

Despachar `desenvolvedor-frontend`:

```
export SKILL_INTERNAL=true
Agent(subagent_type="desenvolvedor-frontend", prompt="""
Input:
- DESIGN.md (specs visuais — implementar fiel)
- Copy aprovada (texto pronto)
- Template escolhido (EXTENDER, NAO inventar visual)

Tarefa:
- Criar branch feature/{slug}
- Criar src/pages/{slug}/index.astro extendendo src/layouts/template-{template}.astro
- Invocar skill oficial Anthropic frontend-design quando tomar decisao visual
- Usar Shadcn MCP se precisar componente complexo
- Build limpo
- Scripts validacao (test-logo-weight, test-modal-click-outside, test-accordion) passam

Output: branch + commit hash + path do arquivo
""")
```

### Step 7 — Revisao visual real (Regra 4)

Despachar `designer-revisor`:

```
export SKILL_INTERNAL=true
Agent(subagent_type="designer-revisor", prompt="""
Auditoria 2 passadas obrigatorias:

Passada 1 - ESTETICA HUMANA (gate principal):
- Olhar screenshot inteiro como {{NOME_OPERADOR_CURTO}} olharia
- "Impressiona? Alinhado com DESIGN.md? Sem AI default look?"
- Inspecionar hierarquia, composicao, atmosfera (subjetivo mas critico)
- Se REPROVA passada 1: nem roda passada 2. Devolve dev com defeitos prosa.

Passada 2 - TECNICA (so se passou 1):
- Playwright headless desktop 1280x720 + mobile 390x844 (JPEG quality 70)
- Validacao computed styles, ARIA, WCAG
- Console errors, 404 assets, links externos
- Bate com tokens OKLCH do template

Output: workspace/output/screenshots-revisao/{data}-{slug}/REVISAO-APROVADO.md OU REVISAO-REPROVADO.md
""")
```

### Step 8 — Triple-check paralelo (Regra 6)

Despachar 3 agents em paralelo:
- `copywriter` (revisao copy contextual no codigo renderizado)
- `desenvolvedor-frontend` (code review proprio output: build, perf, SEO, GTM, favicon)
- `analista-qa` (bateria 12 itens funcional)

Se algum reprovar bloqueante, voltar step correspondente.

### Step 9 — Preview Vercel + link pro {{NOME_OPERADOR_CURTO}}

```bash
cd ../Paginas Astro {{NOME_OPERADOR}}/
git push origin feature/{slug}
gh pr create --base main --head feature/{slug} --title "..." --body "..."
# Vercel auto-cria preview do PR
gh pr view --json comments | jq '.comments[] | select(.author.login=="vercel")'
```

Link preview pro {{NOME_OPERADOR_CURTO}}:
- Hook `check-mostrar-pro-gui-sem-revisor.sh` libera se REVISAO-APROVADO recente presente
- Senao bloqueia (forca nova auditoria)

### Step 10 — Gate {{NOME_OPERADOR_CURTO}} aprova → merge

{{NOME_OPERADOR_CURTO}} valida visualmente preview Vercel. Se aprova: merge PR pra main → auto-deploy producao. Se rejeita: volta Step 4 ou 6 conforme escopo da mudanca.

---

## Anti-improviso (Jade nao pode)

- Despachar dev sem DESIGN.md (designer-ui produz Step 1)
- Despachar revisor sem code pronto
- Mandar URL pro {{NOME_OPERADOR_CURTO}} sem REVISAO-APROVADO
- Pular triple-check
- Pular Step 3 (Gate {{NOME_OPERADOR_CURTO}} no mockup)
- Improvisar briefing visual ("use Linear como ref" sem DESIGN.md formal)

Hooks bloqueantes ativos garantem cumprimento:
- `check-agent-sem-skill-recente.sh` (Regra 3)
- `check-mostrar-pro-gui-sem-revisor.sh` (Regra 4)

---

## Critério de aceitação da entrega final

- DESIGN.md vivo (atualiza se {{NOME_OPERADOR_CURTO}} mudar direcao)
- Pagina extends template (sem visual inventado)
- Build limpo
- Scripts validacao passam
- Triple-check 3/3 aprovado
- Preview Vercel APROVADO {{NOME_OPERADOR_CURTO}}
- Merge main → producao
- Aprendizado §5 propagado se houve correcao do {{NOME_OPERADOR_CURTO}} no caminho

---

## Histórico

- 2026-05-17 v2: refactor template-first apos incidente 8 iteracoes na /sua-pagina-v2 (improviso de despacho). Aval {{NOME_OPERADOR_CURTO}} registrado. Task ClickUp {{CLICKUP_TASK_EXEMPLO}}.
- (versoes anteriores em .preFix-template-first)

---

## 🔴 CHECKLIST OBRIGATÓRIO BLOQUEANTE (anti-omissão)

Criado 17/05/2026 (aprendizado §5 — {{NOME_OPERADOR_CURTO}} pegou rodapé faltando + visual sem graça + logo invisível 4 vezes).

**Dev NÃO entrega + revisor NÃO aprova sem TODOS estes itens validados via Playwright real.** Cada falha = REPROVADO automático, sem negociação.

### Estrutura essencial (NÃO PODE FALTAR)
- [ ] **Header com logo visível:** `width >= 100px desktop / >= 90px mobile`, `height >= 24px`
- [ ] **Footer presente:** componente Footer renderizado, com links institucionais ({{PRODUTO_PRINCIPAL}}, GitHub, contato)
- [ ] **Hero acima da dobra:** headline + subheadline + CTA visível sem scroll
- [ ] **Conteúdo principal:** todas as dobras do DESIGN.md implementadas (sem pular nenhuma)

### Microtexto
- [ ] **Pluralização correta:** `count === 1 ? 'agente' : 'agentes'` (idem workspace/skill/aluno/etc)
- [ ] **Sem typos** (PT-BR correto, acentuação, concordância)
- [ ] **Hyperlinks inline** (nunca URL exposta entre parênteses)

### Form / CTA
- [ ] **Form GHL renderiza completo:** altura nativa, SEM `max-height`/`overflow:auto/hidden` no wrapper
- [ ] **Watchdog JS ativo** se for iframe form_embed.js GHL
- [ ] **CTA primário destacado:** botão grande, gradient/glow azul accent
- [ ] **CTA secundário sutil:** link inline ou botão ghost

### Fidelidade ao DESIGN.md
- [ ] **Cada dobra implementada COMO descrita** (organograma assimétrico se DESIGN.md pede assimétrico — não improvisar grid)
- [ ] **Tokens OKLCH do template aplicados** (sem hex inventado)
- [ ] **14 anti-AI-slop respeitados** (sem gradient azul→roxo→rosa, sem conic rotation, sem 4 cards iguais, sem glow neon, sem emojis decorativos)
- [ ] **Hierarquia visual com 3+ pesos tipográficos diferentes**

### Visual NÃO-PRETO-CHAPADO (anti "sem graça") + EMOCIONA (anti template genérico)
- [ ] **CRITÉRIO MESTRE: Página EMOCIONA?** Aluno diria WOW ao entrar? (se não, REPROVADO)
- [ ] **3+ dobras visualmente DIFERENTES** entre si (não monotonia)
- [ ] **Comparação direta com Linear/Vercel/Stripe** — nível visual equivalente?
- [ ] **Cada dobra tem peça-âncora visual** (não é "só texto sobre fundo")
- [ ] **Aurora/gradient mesh PERCEPTÍVEL** (não 1% opacidade que vira preto chapado — alvo 6-12% opacidade visível mas sutil)
- [ ] **Variação de superfície:** cards com frosted glass aparente, secções com background sutil diferente do base
- [ ] **Micro-interactions presentes:** hover states em cards, scroll reveals, pulse na Jade central
- [ ] **Tipografia editorial nos números:** Source Serif 4 600 nos counters (não Inter monotonia)
- [ ] **Bento grid com hierarquia real** (Jade GRANDE central + cards de tamanhos variados, não grid uniforme)

### Mobile
- [ ] **Font-size ≥16px** em parágrafos
- [ ] **Sem horizontal scroll** em 390px viewport
- [ ] **Touch targets ≥44px** em CTAs
- [ ] **Logo mobile ≥24px height**

### Performance & SEO
- [ ] **`npm run build` limpo** (zero erros TypeScript/Astro)
- [ ] **Console errors do nosso código = zero** (analytics externo OK)
- [ ] **`<title>` único e descritivo**
- [ ] **`<meta name="description">` 120-160 chars**
- [ ] **`<link rel="canonical">` correto**
- [ ] **`<html lang="pt-BR">`**
- [ ] **{{GTM_CONTAINER_ID}} presente** (se aplicável ao projeto)
- [ ] **Favicon carregando**
- [ ] **OG image declarada** (mesmo placeholder)

### Acessibilidade
- [ ] **ARIA correto** (role, aria-label, aria-expanded)
- [ ] **Keyboard navigation** funciona
- [ ] **Focus visible** outline
- [ ] **prefers-reduced-motion** respeitado

### Bug reincidente — logo header (4 incidentes 17/05)
- [ ] **CSS embutido no template** com `min-width: 140px desktop / 110px mobile`
- [ ] **Validação Playwright:** `getBoundingClientRect()` retorna width/height esperados em ambos viewports
- [ ] **Inspeção visual:** logo LEGÍVEL (não traço fino quase invisível)

### Como rodar o checklist (obrigatório antes de devolver)

```js
// Playwright real, viewport desktop 1280x720 + mobile 390x844
const checklist = {
  logo: () => {
    const r = document.querySelector('header img').getBoundingClientRect();
    return r.width >= 100 && r.height >= 24;
  },
  footer: () => !!document.querySelector('footer'),
  formNoScroll: () => {
    const w = document.querySelector('[class*="form-wrapper"]');
    if (!w) return true;
    const s = getComputedStyle(w);
    return s.overflow !== 'auto' && s.overflow !== 'hidden' && s.maxHeight === 'none';
  },
  mobileFonts: () => {
    return Array.from(document.querySelectorAll('p, li, span'))
      .every(el => parseFloat(getComputedStyle(el).fontSize) >= 16);
  },
  // ... (todos os critérios acima)
};
const results = Object.entries(checklist).map(([k, fn]) => [k, fn()]);
const failures = results.filter(([_, ok]) => !ok);
if (failures.length) throw new Error(`CHECKLIST FAIL: ${JSON.stringify(failures)}`);
```

### Validação dupla
1. **Dev valida no Playwright local ANTES de commit** (não pode commitar sem)
2. **Revisor revalida via Playwright independente** (passada 1 estética humana + passada 2 técnica com checklist)
3. **Hook bloqueante** garante que nada vai pro {{NOME_OPERADOR_CURTO}} sem REVISAO-APROVADO recente