---
name: migrar-pagina
description: Migra uma página do GoHighLevel ou Framer para o sistema de páginas do squad (Astro 6). Extrai copy, estrutura e CTAs, gera markdown padronizado e encadeia /ajustar-pagina → /revisar-codigo-pagina → /publicar-pagina.
---

# Skill: /migrar-pagina

## ⚠️ DIRETIVA CRÍTICA — Pixel Perfect

A skill `/migrar-pagina` entrega **CLONE IDÊNTICO** da página original. Sem reinterpretar design, sem aplicar design system "novo", sem mexer em layout, sem trocar fontes, cores, espaçamentos, animações.

- Se a original usa Cormorant Garamond → mantém Cormorant.
- Se a original usa GSAP → mantém GSAP.
- Se a original usa CSS animations → mantém CSS animations.
- Se a original tem cor X → mantém cor X.
- Se a original tem rodapé custom → mantém rodapé custom (passar `footer={false}` no Base.astro).

**Mudança de design pós-migração é ciclo SEPARADO** (futura skill `/redesign-pagina`, ou refazer com `/criar-pagina-nova`). Nunca dentro de `/migrar-pagina`.

> **Sliders na original (override AGENTS.md #19):** mesmo em modo pixel perfect, o **comportamento canônico do squad** sobrescreve o original — auto-scroll contínuo + drag mouse/touch obrigatório, SEM hover-pause (ver `/ajustar-pagina` seção "Sliders — comportamento canônico OBRIGATÓRIO"). Se a original tinha slider sem drag, ou com hover-pause, o clone GANHA drag e PERDE hover-pause. Não é "reinterpretar design" — é padrão de UX que vale pra qualquer página do squad. Diff visual continua exigido (≤ 5%) — ganhar drag não muda layout.

A skill TERMINA com **diff visual obrigatório** original vs novo via Playwright (`scripts/validate-visual.mjs --compare`). Diff de layout/cor/espaçamento **> 5%** em mobile ou desktop = REPROVADO e refaz no ponto que divergiu.

A `/migrar-pagina` pode quebrar a página em componentes Astro (`Section`, `Button`, `FAQ`, `LogoSlider`, `Footer`) DESDE QUE o resultado visual seja idêntico ao original. Se um componente padrão renderiza diferente da original, NÃO USAR — replicar o markup/CSS da original na própria página.

---


Você é o agente de migração de páginas do squad {{NOME_OPERADOR}}. Sua tarefa é migrar uma página existente (GoHighLevel, Framer, ou outro builder) para o sistema do squad — começa com extração + diagnóstico, gera markdown padronizado, e na sequência alimenta a esteira `/ajustar-pagina` → `/revisar-codigo-pagina` → `/publicar-pagina`.

⚠️ **Stack alvo:** projeto `Páginas Astro {{NOME_OPERADOR}}/` (Astro 6 + Tailwind v4). Não tocar no projeto Next legado em `Sites {{NOME_OPERADOR}}/`.

⚠️ **Posição na esteira:** `/migrar-pagina` faz o papel de `/escrever-pagina` (cria o markdown), mas em vez de escrever do zero, **extrai do original e diagnostica**. A partir do markdown aprovado, a esteira é idêntica à de `/criar-pagina-nova`.

---

---

## ⚠️ DIRETIVA CRÍTICA — Assets externos: clonar SEMPRE (Regra Inviolável #19, hotfix #86)

Toda migração DEVE clonar TODOS os assets referenciados pelo HTML para `Páginas Astro {{NOME_OPERADOR}}/public/`. Não é opcional. Não depende de "se a página vai pra mesmo projeto Vercel".

**Por quê:** se o `.astro` mantém URL absoluta (`https://sites.{{DOMINIO}}/[slug]/img/...`) ou referencia path relativo `/[slug]/img/...` sem o asset em `public/`, em PRODUÇÃO num projeto Vercel novo (ou em qualquer ambiente local) os assets retornam 404. Pior: diff visual mascara a regressão, porque se ambos os lados (`original` + `novo`) puxam da mesma CDN antiga, a comparação dá "PASS" enganoso.

**Procedimento OBRIGATÓRIO em toda migração:**

```bash
cd "Páginas Astro {{NOME_OPERADOR}}"

# 1. Extrair TODAS as URLs absolutas do .astro (e relativas, se houver)
grep -hoE 'https://sites\.{{github_user}}\.com/[a-z0-9_-]+/(img|assets|files|cdn|fonts|videos)/[^"\)]+\.(jpg|jpeg|png|webp|svg|gif|mov|mp4|webm|woff|woff2|ttf|otf|css|js|ico)' src/pages/[slug]/index.astro | sort -u

# 1b. Reforçar com grep que aceita espaço em nome de arquivo (logos com nomes "banco do brasil.png")
grep -hoE 'src="https://sites\.{{github_user}}\.com/[^"]+\.(jpg|jpeg|png|webp|svg|gif|mov|mp4|webm|woff|woff2|ttf|otf|css|js|ico)"' src/pages/[slug]/index.astro | sort -u

# 2. Pra cada URL: criar pasta + baixar
mkdir -p public/[slug]/img public/[slug]/img/logos
curl -sL "https://sites.{{DOMINIO}}/[slug]/img/[arquivo]" -o "public/[slug]/img/[arquivo]"

# 3. Validar tipo (binário, não HTML 404 mascarado)
file public/[slug]/img/[arquivo]   # deve mostrar PNG/JPEG/WebP/MP4/etc, NUNCA "HTML document"

# 4. Validar tamanho (> 0 bytes)
test -s public/[slug]/img/[arquivo] || echo "FAIL: arquivo vazio"

# 5. Validar HTTP 200 local
curl -s -o /dev/null -w "%{http_code}" "http://localhost:4321/[slug]/img/[arquivo]"   # tem que ser 200

# 6. Re-rodar diff visual (vai dar PASS) E executar test isolado bloqueando CDN antiga:
node -e "/* abrir Playwright + page.route bloqueando sites.{{DOMINIO}} */"
# Com a CDN bloqueada, qualquer img.naturalWidth === 0 = asset que não está em public/
```

**Cobertura mínima:** validar zero `<img>` quebrado quando navegador bloqueia `sites.{{DOMINIO}}` (cenário "Vercel novo"). Documentar count de assets clonados na linha do mapa.md.

**Bug histórico que motivou esta regra:** 06/05/2026 — Onda 6 migrou 6 páginas sem clonar assets. /clickup8x detectado pelo {{NOME_OPERADOR}} (vídeo de fundo `.mov` 36MB faltava). Auditoria revelou ~70 assets faltando em outras 4 páginas (/reverso, /inscricao-aula-{{NOME_OPERADOR_SLUG}}-{{slug_produto_parceiro}}, /oferta-irresistivel-{{slug_produto_parceiro}}, /mentoria-precos). Hotfix sistêmico em #86 clonou 46 únicos. Risco que escapou: se URL absoluta `sites.{{DOMINIO}}` for desativada (ou domínio mudar), todas as páginas migradas quebram em produção.

**Detalhe técnico crítico:** quando o `.astro` original referencia URL absoluta (`https://sites.{{DOMINIO}}/...`), o navegador continua puxando da CDN antiga MESMO com asset clonado em `public/`. Para o asset local "ativar", uma das duas opções:
- (a) refatorar `.astro` pra path relativo (`/[slug]/img/...`) — recomendado, ciclo de migração separado;
- (b) deixar URL absoluta e contar com fallback — aceita risco se o domínio antigo cair.

A migração pixel perfect aceita (a) ou (b) durante o ciclo de copy/codar — mas **clonar pra public/ é OBRIGATÓRIO em ambos os casos** (sem isso, opção (a) nem é possível sem nova rodada de hotfix).


## Fluxo

```
PEDIDO: migrar /[slug] (URL ou descrição)
        │
        ▼
[1] Extração de conteúdo
    Se URL → WebFetch
    Se descrição → pedir copy ao {{NOME_OPERADOR}}
    Capturar: H1, subheadline, seções, CTAs, prova social, FAQ, garantia, preço
        │
        ▼
[2] Diagnóstico da página original
    ICP correto? Tom de voz alinhado? Algo desatualizado?
    Anotar problemas (saem como bloco "Diagnóstico" no markdown)
        │
        ▼
[3] Gerar markdown padronizado
    workspace/output/paginas/YYYY-MM-DD-[slug].md
    Estrutura: briefing + diagnóstico + copy completo + notas técnicas
        │
        ▼
[4] Atualizar workspace/output/paginas/mapa.md
    Linha "Outputs produzidos" + atualizar "Última atualização"
        │
        ▼
[5] Apresentar ao {{NOME_OPERADOR}}
    Resumo do diagnóstico (3-5 bullets)
    Caminho do arquivo
    Pergunta: "implementar agora ou ajustar copy antes?"
        │
        ├── {{NOME_OPERADOR}} pediu ajuste? ─ sim → revisar markdown e voltar a [5]
        │
        ▼ {{NOME_OPERADOR}} aprovou
[6] Despachar /ajustar-pagina
    Input: caminho do markdown aprovado
    Output esperado: Páginas Astro {{NOME_OPERADOR}}/src/pages/[slug]/index.astro
        │
        ▼
[7] Aguardar componente Astro
        │
        ▼
[8] Despachar /revisar-codigo-pagina
        │
        ├── aprovada? ─ não ─→ devolver ao Agente Dev
        │                       (passar markdown + apontamentos)
        │                       Voltar a [8]
        ▼ sim
[8.5] Diff visual original vs novo (Playwright)
      cd "Páginas Astro {{NOME_OPERADOR}}"
      node scripts/validate-visual.mjs --compare \
        --slug=[slug] \
        --original=https://sites.{{DOMINIO}}/[slug] \
        --novo=http://localhost:4321/[slug]
      Compara mobile (390x844) + desktop (1440x900)
      Salva screenshots lado a lado em
      screenshots/[slug]-comparacao-{mobile,desktop}.png
        │
        ├── diff > 5% em algum viewport? ─ sim ─→ REPROVADO
        │     Listar diferenças (cor/layout/espaçamento)
        │     Voltar ao /ajustar-pagina com lista
        │     Bateria roda do zero após correção
        │
        ▼ diff ≤ 5% (clone fiel)
[9] Despachar /publicar-pagina (modo preview)
    Retorna: http://localhost:4321/[slug]
        │
        ▼
[10] Apresentar URL localhost ao {{NOME_OPERADOR}}
        │
        ├── {{NOME_OPERADOR}} pediu ajuste? ─ sim → voltar a [6]
        │
        ▼ {{NOME_OPERADOR}} aprovou
[11] Despachar /publicar-pagina (modo produção)
     vercel --prod no projeto Páginas Astro {{NOME_OPERADOR}}/
        │
        ├── deploy falhou? ─ sim → reportar ao {{NOME_OPERADOR}}, NÃO retentar
        │
        ▼ deploy OK
[12] Atualizar registros finais:
     - workspace/output/paginas/mapa.md (URL produção na linha)
     - workspace/processos/pipeline-paginas.md (entrada da migração + URL final)
     - squads/dev/tarefas.md (status: publicado)
        │
        ▼
[13] Notificar {{NOME_OPERADOR}}:
     "https://[url-vercel] está no ar. Migração de /[slug] concluída."
```

---

## Pré-requisitos obrigatórios

Antes de começar, leia:
1. `segundo-cerebro/01-identidade/icp.md` — para entender o público
2. `segundo-cerebro/01-identidade/tom-de-voz.md` — para manter a voz do {{NOME_OPERADOR}}
3. `workspace/output/paginas/mapa.md` — padrão de entrega + fila de migração
4. `Páginas Astro {{NOME_OPERADOR}}/mapa.md` — componentes/tokens disponíveis no projeto Astro

## Input esperado

```
/migrar-pagina [URL ou descrição da página a migrar]
```

Exemplos:
- `/migrar-pagina https://sites.{{DOMINIO}}/reverso`
- `/migrar-pagina página de vendas do Sistema Reverso (GoHighLevel)`

## Processo de migração

### 1. Extração de conteúdo

Se for URL, use WebFetch para capturar o conteúdo. Se for descrição, peça ao {{NOME_OPERADOR}} que cole o copy da página.

Extrair:
- [ ] Headline principal (H1)
- [ ] Subheadline / promessa
- [ ] Seções da página (em ordem)
- [ ] Todos os CTAs e o que cada um faz
- [ ] Prova social (depoimentos, números, certificações)
- [ ] FAQ (se houver)
- [ ] Garantia (se houver)
- [ ] Preço e condições (se for página de venda)

### 2. Diagnóstico da página original

Antes de migrar, avaliar:
- O ICP está correto? A página fala com infoprodutor/fundador digital?
- O tom de voz bate com o segundo-cerebro?
- Algum elemento está desatualizado (preço, produto, CTA quebrado)?
- O design mobile está ruim? (Considerar no output)

Anotar os problemas encontrados — entregar junto com a migração.

### 3. Output — arquivo markdown padronizado

Criar arquivo em `workspace/output/paginas/YYYY-MM-DD-[slug].md` com esta estrutura:

```markdown
# [Nome da Página] — Migração

**Data:** YYYY-MM-DD
**Origem:** [URL ou plataforma de origem]
**Slug final:** sites.{{DOMINIO}}/[slug]
**Tipo:** [Captura / Venda / Institucional]
**Status:** Migrado — aguarda implementação

---

## Diagnóstico da página original

[Problemas encontrados, sugestões de melhoria]

---

## Copy completo

### Hero
**Headline:** [texto]
**Subheadline:** [texto]
**CTA principal:** [texto do botão] → [destino]

### [Seção 2]
...

### [Seção N]
...

---

## Notas técnicas para implementação (Astro 6)

- ⚠️ **PIXEL PERFECT:** clone visual idêntico da original. Se houver conflito entre design system do squad e o que a página original tem, manter o que a página original tem. Mudança de design é ciclo separado.
- Componentes a reutilizar de Páginas Astro {{NOME_OPERADOR}}/src/components/ APENAS se renderizarem idêntico ao original: [lista]
- Componentes/markup customizados a manter da original: [lista]
- Animações: replicar EXATAMENTE como na original (GSAP se GSAP, CSS se CSS, IntersectionObserver se IO)
- Mobile: replicar breakpoints e media queries da original
- Fontes: replicar EXATAMENTE como na original (incluindo @import / link Google Fonts)
- Cores e tokens: replicar EXATAMENTE como na original (mesmos hex / mesmas vars)
- Footer: se a original tem rodapé custom, passar `footer={false}` no `<Base>` e replicar inline

---

## Checklist de migração

- [ ] Copy extraído e revisado
- [ ] Tom de voz alinhado com segundo-cerebro
- [ ] CTAs verificados e atualizados
- [ ] Preços conferidos com produtos-servicos.md
- [ ] mapa.md atualizado
- [ ] Aguarda aprovação do {{NOME_OPERADOR}} antes de seguir para /ajustar-pagina
- [ ] Após dev: rodar `node scripts/validate-visual.mjs --compare --slug=[slug] --original=[URL] --novo=http://localhost:4321/[slug]` — diff < 5% mobile + desktop
- [ ] Após dev: rodar `node scripts/audit-fonts.mjs <urlOriginal> http://localhost:4321/[slug]` — 0 mismatches obrigatório
```

### 4. Atualizar o MAPA

Obrigatório: adicionar/atualizar a página migrada na tabela de `workspace/output/paginas/mapa.md`. Quando o deploy concluir (passo [12]), atualizar a mesma linha com a URL de produção.

### 5. Apresentar ao {{NOME_OPERADOR}}

Entregar:
1. Resumo do diagnóstico (3-5 bullets)
2. O arquivo markdown criado
3. Próximo passo: implementar em Astro (encadeia /ajustar-pagina) ou ajustar copy antes?

### 6+ — Pipeline Astro

Após o OK do {{NOME_OPERADOR}} no markdown, encadear automaticamente:
1. `/ajustar-pagina` → gera componente Astro em `Páginas Astro {{NOME_OPERADOR}}/src/pages/[slug]/index.astro`
2. `/revisar-codigo-pagina` → checklist Astro completo
3. `/publicar-pagina` → preview localhost → OK do {{NOME_OPERADOR}} → `vercel --prod`

A esteira é idêntica à de `/criar-pagina-nova` a partir desse ponto.

## Auditoria de fontes — OBRIGATÓRIA antes de marcar migração entregue

Toda migração DEVE incluir auditoria sistemática de `font-family` de cada elemento textual da página, comparando com a original. Não basta "achar que tá igual" — comparar computed styles é mandatório.

**Bug histórico (06/05/2026):** homepage `/` foi migrada e passou na bateria #15 (12/12) com diff visual ~5%, mas o {{NOME_OPERADOR}} apontou que fontes do footer estavam diferentes da original (CURSOS, GUI ÁVILA, SISTEMA REVERSO, {{slug_produto_parceiro}}). Causa raiz: `global.css` do squad declara `h1,h2,h3,h4 { font-family: var(--font-display) /* Syne */ }`, e o style inline da página migrada não fazia override de font-family pros h4 — Syne vazou pro footer da home. Pixel diff visual não capturou porque Syne e Inter têm tamanho/peso semelhantes nesses tamanhos pequenos. Esta seção é a resposta.

**Como auditar:**

1. **Inventário de elementos textuais** — listar todos os seletores que renderizam texto: hero h1/h2/h3, body, parágrafos, links, botões, badges, FAQ, footer (cada coluna, cada link, cada texto), forms, labels, placeholders.

2. **Capturar computed `font-family`** via Playwright em ambos (original + local). Script reutilizável já disponível em `Páginas Astro {{NOME_OPERADOR}}/scripts/audit-fonts.mjs`:

   ```bash
   cd "Sites Astro {{NOME_OPERADOR}} Avila" && node scripts/audit-fonts.mjs https://sites.{{DOMINIO}}/[slug] http://localhost:4321/[slug]
   ```

   Imprime tabela markdown `seletor | original | local | match` e exit 1 se houver mismatch.

3. **Diff:**
   - Match exato (ignorando ordem alternativa, "Inter, sans-serif" == "sans-serif, Inter") = OK
   - Qualquer divergência (ex: Syne local vs Inter original, ou fonte ausente vs presente) = REPROVAÇÃO da migração
   - Exceção: `html` (browser default vs Tailwind reset) é informativo — não trava

4. **Fix típico:** quando o `global.css` do squad sobrescreve via tag (`h1,h2,h3,h4 { font-family: ... }`) e a original usa outra fonte, adicionar override `!important` no `<style is:inline>` da página com selector `html body h1, html body h2, ... html body h6 { font-family: '<fonte original>' !important }`. Em seguida, classes específicas que devem manter outra fonte (ex: `.hero-name` em Space Grotesk) também precisam de `!important` para vencer essa regra. **Cuidado com comentários CSS aninhados** (`/* foo /* bar */ baz */`) — CSS não suporta e quebra silenciosamente o parsing das regras seguintes.

5. **Carregar weights e families no `<slot name="head">`** se houver fonte custom não compartilhada com o design system padrão.

6. **Não confiar só em diff visual de pixelmatch** — pixel diff pode mascarar uma fonte errada se tiver tamanho parecido. Auditoria de fonte é teste DE QUALIDADE complementar, não substituto.

## Regras críticas

- **Pixel perfect, sempre.** Migração = clone visual idêntico. Diff visual via Playwright é OBRIGATÓRIO antes de aprovar (≤ 5% diferença mobile + desktop). Diff > 5% = REPROVADO. Mudança de design só em ciclo separado.
- **Nunca inventar copy** — extrair do original. Sugestões de melhoria ficam separadas como "Diagnóstico".
- **Nunca subir direto para produção** — o output passa pelo `/revisar-codigo-pagina` e pelo OK do {{NOME_OPERADOR}} no preview localhost.
- **Preços e CTAs devem ser conferidos** com `02-negocios/produtos-servicos.md` antes de entregar
- **mapa.md é obrigatório** — toda migração que não atualiza o MAPA está incompleta
- **Stack obrigatória:** Astro 6 + Tailwind v4 no projeto `Páginas Astro {{NOME_OPERADOR}}/`. Sem fallback HTML.
- **Não tocar no Next legado** (`Sites {{NOME_OPERADOR}}/`) — ele permanece como está até toda a migração concluir.

---

## ⚠️ Triple-check OBRIGATÓRIO antes de deploy (Regra Inviolável #23 — 10/05/2026)

ANTES de qualquer `vercel --prod` (ou equivalente), TODA mudança em página/produto DEVE passar pelos 3 revisores:

1. **`paginas`** (squad-copy) — APROVA copy?
   - Light Copy validation
   - Cormorant em dígitos = REJEIÇÃO (Regra #188)
   - Métricas públicas: nunca faturamento (Regra `feedback_metricas_publicas_gui.md`)
   - Vocabulário banido: qualificação/avaliação/screening/triagem/fit

2. **`paginas-dev`** (squad-dev) — APROVA código?
   - HTML válido (h1 único, semântica)
   - GTM-NN36ZRZ presente (Regra #147)
   - Favicon canônico (Regra #149)
   - Astro nativo (`/_astro/` no HTML servido)
   - Headers de segurança
   - Confiabilidade (Regra #22): comandos externos com timeout + retry

3. **`bug-hunter`** (squad-dev) — APROVA funcional? (Playwright em produção)
   - Console errors = 0
   - 404s em assets = 0
   - Drag funcional em sliders
   - Vídeos readyState ≥ 3
   - Forms submetem
   - Links navegam
   - Acessibilidade básica

**Se qualquer dos 3 reprovar:** corrige + re-roda os 3 até passar. **Sem exceção.**

**Hook PreToolUse ativo:** `.claude/hooks/check-triple-check-antes-deploy.sh` detecta `vercel --prod` e dispara lembrete se triple-check não rodou.

**Memória correlata:** `feedback_triple_check_obrigatorio.md`. Regra AGENTS.md #23.

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{NOME_OPERADOR}} testar — testa antes.

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{NOME_OPERADOR}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
