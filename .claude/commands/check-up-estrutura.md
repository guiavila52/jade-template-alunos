---
name: check-up-estrutura
description: Auditoria automática da arquitetura do squad — verifica skills, MAPAs, squads, agentes, regras, memórias, produção e secrets. Use quando precisar saber se a estrutura tá conforme as Regras Invioláveis (especialmente #10 MAPA, #13 Fluxo, #18 backups, #19 propagação) ou rodar via cron diário. Output em `squad/output/auditorias/YYYY-MM-DD-checkup-estrutura.md`.
model: claude-sonnet-4-5
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

## Check-up Estrutura — Auditor da Arquitetura do Squad

Você é o Agente Auditor da arquitetura do squad-jade/squad-dev. Função: rodar uma bateria de 12 categorias de check em paralelo, agregar findings com severidade e gerar relatório com veredicto binário (APROVADO / APROVADO COM RESSALVAS / REPROVADO). Você **não corrige nada** — só detecta, classifica, reporta. Quem decide aplicar correções é o {{NOME_OPERADOR}} caso a caso.

Squad: dev (executa), Jade (orquestra)

⚠️ **Stakes:** o {{NOME_OPERADOR}} vai ensinar este squad ao vivo em 14/05/2026. A skill é desenhada pra rodar todo dia (cron futuro) garantindo que nenhum erro estrutural passa batido. Substitui a tarefa #153 (que aplicaria 7 ajustes às cegas) por um modelo de auditoria contínua + aprovação humana caso a caso.

---

## Propósito

Antes desta skill existir, ajustes estruturais (`memoria.md` faltando em agente, regras AGENTS.md duplicadas, MAPA.md ausente em pasta nova, slider fora do canônico, secret em git ls-files) só apareciam quando o {{NOME_OPERADOR}} notava — geralmente em momento ruim (durante demo, durante aula, em produção quebrada). A skill `/check-up-estrutura` automatiza a detecção desses problemas: lê toda a árvore do squad, roda 12 categorias de check, agrega findings com severidade (CRITICAL/HIGH/MEDIUM/LOW/INFO) e devolve um relatório priorizado.

A skill é **nondestrutiva por design** — só lê, nunca escreve nem aplica fix. O output é um relatório markdown salvo em `squad/output/auditorias/YYYY-MM-DD-checkup-estrutura.md` + sumário no chat. O {{NOME_OPERADOR}} aprova caso a caso o que vai ser corrigido (provavelmente dispara skills específicas como `/codar-pagina`, edição manual, ou criação de novo aprendizado em `feedback_*.md`).

Está alinhada com Regra #19 (propagação) — toda categoria de check vira aprendizado permanente: se um finding novo virar feedback do {{NOME_OPERADOR}}, basta adicionar uma categoria nova nesta skill (ver "Como adicionar nova categoria de check"). E está alinhada com Regra #10 (MAPA por pasta) — a categoria B audita exatamente isso.

---

## Fluxo

```
ENTRADA: nenhuma (auto-discovery do projeto)
    │
    ▼
[1] Mapear estrutura — ler todos os squads, agentes, skills, MAPAs, memórias
    │
    ▼
[2] Rodar 12 categorias de check em paralelo
    │   (A) Skills com ## Fluxo
    │   (B) Pastas com MAPA.md
    │   (C) Squads completos (memoria/aprendizados/tarefas/MAPA)
    │   (D) Agentes completos (memoria/aprendizados/MAPA)
    │   (E) Regras AGENTS.md sem duplicidade numérica
    │   (F) Quadro de squads consistente entre docs
    │   (G) Memórias persistentes válidas (frontmatter + index)
    │   (H) Backups Regra #18 preservados
    │   (I) Páginas em produção HTTP 200
    │   (J) Padrões obrigatórios (GTM + favicon + Astro)
    │   (K) Sliders canônicos (Slider.astro)
    │   (L) Secrets / segurança
    │
    ▼
[3] Agregar findings com severidade
    CRITICAL / HIGH / MEDIUM / LOW / INFO
    │
    ▼
[4] Gerar relatório em
    squad/output/auditorias/YYYY-MM-DD-checkup-estrutura.md
    │
    ▼
[5] Apresentar ao {{NOME_OPERADOR}} — sumário + lista priorizada + recomendação binária
    APROVADO / APROVADO COM RESSALVAS / REPROVADO
```

---

## Como rodar

```
/check-up-estrutura
```

Sem argumentos. A skill descobre tudo sozinha varrendo o repo.

Tempo total: < 2min no Mac local (12 categorias rodam em paralelo via background `&` quando possível).

Output:
- Relatório markdown salvo em `squad/output/auditorias/YYYY-MM-DD-checkup-estrutura.md` (timestamp na primeira linha)
- Sumário no chat com contagem por severidade + top 5 findings críticos + veredicto

---

## Categorias de check (14)

Cada categoria é independente. Ordem alfabética A–M2. Severidade quando falha (`CRITICAL` > `HIGH` > `MEDIUM` > `LOW` > `INFO`).

---

### A) Skills com `## Fluxo` (Regra #13)

**Critério:** Toda skill em `.claude/commands/*.md` (excluindo backups `.preFix*`/`.bak`) deve ter um cabeçalho de fluxo: `## Fluxo`, `## 🔄 Fluxo` ou `## Fluxograma`.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
for f in .claude/commands/*.md; do
  case "$f" in
    *.preFix*|*.bak|*MAPA.md) continue ;;
  esac
  if ! grep -qE '^## Fluxo|^## 🔄 Fluxo|^## Fluxograma' "$f"; then
    echo "MISS: $f"
  fi
done
```

**Pass:** 0 misses.
**Severidade quando falha:** HIGH.
**Exemplo de finding:** `HIGH | A | .claude/commands/escrever-copy.md sem '## Fluxo' (Regra #13)`.

---

### B) Pastas com MAPA.md (Regra #10)

**Critério:** Toda pasta em `squad/`, `squads/`, `Segundo Cérebro/` deve ter `MAPA.md` (ou `.gitkeep` se for pasta vazia intencional). Excluir `.git`, `node_modules`, `.claude`.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
find squad squads "Segundo Cérebro" -type d \
  -not -path '*/.*' \
  -not -path '*/node_modules*' \
  | while read d; do
    if [ ! -f "$d/MAPA.md" ] && [ ! -f "$d/.gitkeep" ]; then
      echo "MISS: $d"
    fi
  done
```

**Pass:** 0 misses.
**Severidade quando falha:** MEDIUM.
**Exemplo de finding:** `MEDIUM | B | squads/midia/agentes — sem MAPA.md (Regra #10)`.

---

### C) Squads completos

**Critério:** Cada `squads/{sq}/` deve ter `memoria.md`, `aprendizados.md`, `tarefas.md`, `MAPA.md`. (Squads "a criar" sem agente real podem ter só MAPA + .gitkeep — esses caem em INFO.)

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
for sq in squads/*/; do
  [ -d "$sq" ] || continue
  for arq in memoria.md aprendizados.md tarefas.md MAPA.md; do
    if [ ! -f "${sq}${arq}" ]; then
      echo "MISS: ${sq}${arq}"
    fi
  done
done
```

**Pass:** 0 misses (`memoria.md`, `aprendizados.md`, `tarefas.md`, `MAPA.md`).
**Severidade quando falha:**
- HIGH se faltar `memoria.md` ou `aprendizados.md` ou `tarefas.md`
- MEDIUM se faltar só `MAPA.md`
- INFO se squad é "a criar" (sem `agentes/` ou `agentes/` vazia)
**Exemplo:** `HIGH | C | squads/radar/memoria.md ausente`.

---

### D) Agentes completos

**Critério:** Cada `squads/{sq}/agentes/{ag}/` deve ter `memoria.md`, `aprendizados.md`, `MAPA.md`.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
find squads -type d -path '*/agentes/*' -mindepth 3 -maxdepth 3 | while read ag; do
  for arq in memoria.md aprendizados.md MAPA.md; do
    if [ ! -f "${ag}/${arq}" ]; then
      echo "MISS: ${ag}/${arq}"
    fi
  done
done
```

**Pass:** 0 misses.
**Severidade quando falha:** MEDIUM (HIGH se for `aprendizados.md` em agente ativo — perde inteligência cumulativa).
**Exemplo:** `MEDIUM | D | squads/dev/agentes/paginas-dev/memoria.md ausente (research #152 detectou em 2026-05-07)`.

---

### E) Regras AGENTS.md sem duplicidade numérica

**Critério:** Não pode existir duas `## REGRA INVIOLÁVEL #N` com o mesmo número.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
DUPS=$(grep -E '^## REGRA INVIOLÁVEL #' AGENTS.md \
  | grep -oE '#[0-9]+' \
  | sort | uniq -d)
if [ -n "$DUPS" ]; then
  echo "DUPLICATED: $DUPS"
fi
```

**Pass:** saída vazia.
**Severidade quando falha:** HIGH.
**Exemplo:** `HIGH | E | AGENTS.md tem duas REGRA INVIOLÁVEL #13 (research #152, 2026-05-07)`.

---

### F) Quadro de squads consistente entre docs

**Critério:** Squads listados em `CLAUDE.md`, `MEMORY.md`, `AGENTS.md`, `Segundo Cérebro/MAPA.md` devem existir em `squads/`. E squads existentes em `squads/` devem aparecer pelo menos em `MEMORY.md`.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
# Lista de squads reais
EXISTING=$(ls -d squads/*/ 2>/dev/null | xargs -n1 basename | sort -u)
echo "EXISTING: $EXISTING"
# Lista mencionada em MEMORY.md (procurar squad-X ou squads/X)
MENTIONED=$(grep -hoE 'squad-[a-z]+|squads/[a-z]+' MEMORY.md CLAUDE.md AGENTS.md 2>/dev/null \
  | sed -E 's|squads/||; s|squad-||' | sort -u)
echo "MENTIONED: $MENTIONED"
# Diff manual: cada existente deveria estar mencionado; cada mencionado deveria existir
```

**Pass:** intersecção completa (zero squad existente sem menção, zero menção sem squad).
**Severidade quando falha:** MEDIUM.
**Exemplo:** `MEDIUM | F | MEMORY.md lista 'financeiro' como "a criar" mas squads/financeiro/ existe com agente ativo (research #152)`.

---

### G) Memórias persistentes válidas (auto-memory)

**Critério:** Cada `*.md` em `~/.claude/projects/-Users-{{USERNAME_MAC}}-Documents-Projetos-IA-{{NOME_OPERADOR}}-Squad-Empresa-{{NOME_OPERADOR}}/memory/` (exceto `MEMORY.md`):
- Tem frontmatter (linhas 1-N entre `---`) com `name`, `description`, `type` — OU formato livre claro com `# nome` no topo
- Está indexada em `MEMORY.md` (linha `[arquivo.md](arquivo.md)`)

**Comando:**
```bash
MEMDIR="$HOME/.claude/projects/-Users-{{USERNAME_MAC}}-Documents-Projetos-IA-{{NOME_OPERADOR}}-Squad-Empresa-{{NOME_OPERADOR}}/memory"
[ -d "$MEMDIR" ] || { echo "MEMDIR ausente: $MEMDIR"; exit 0; }
INDEX="$MEMDIR/MEMORY.md"
for f in "$MEMDIR"/*.md; do
  base=$(basename "$f")
  [ "$base" = "MEMORY.md" ] && continue
  # 1) tem header (frontmatter ou H1)?
  head -1 "$f" | grep -qE '^(---|# )' || echo "NO_HEADER: $base"
  # 2) está indexado em MEMORY.md?
  grep -q "$base" "$INDEX" || echo "NOT_INDEXED: $base"
done
```

**Pass:** 0 `NO_HEADER`, 0 `NOT_INDEXED`.
**Severidade quando falha:** MEDIUM (perde discoverability).
**Exemplo:** `MEDIUM | G | feedback_xpto.md não está em MEMORY.md (não vai carregar no auto-memory)`.

---

### H) Backups Regra #18 preservados

**Critério:** Listar arquivos `*.preFix*`, `*.preMigracao`, `*.bloqueado`, `*.bak` em `Páginas Astro {{NOME_OPERADOR}}/` e em `.claude/commands/`. Confirmar que existem (não foram apagados sem autorização — Regra #18 proíbe destruição).

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}" 2>/dev/null \
  && find . -type f \( -name '*.preFix*' -o -name '*.preMigracao' -o -name '*.bloqueado' -o -name '*.bak' \) \
       -not -path '*/node_modules/*' \
       2>/dev/null
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}/.claude/commands"
ls *.preFix* *.preMigracao *.bloqueado *.bak 2>/dev/null
```

**Pass:** lista impressa (zero ou mais — não importa o número, importa que existam quando deveriam).
**Severidade:** INFO (lista pra log) + MEDIUM se a contagem ficar **menor que** o último relatório (sinal de remoção). Como esta é a primeira run, sempre INFO. Em runs futuras, comparar com último relatório arquivado.
**Exemplo:** `INFO | H | 6 backups Regra #18 preservados em Páginas Astro {{NOME_OPERADOR}}/`.

⚠️ **Caveat:** este check faz só listagem. Diff entre runs (detectar deleção) NÃO está implementado nesta versão — adicionar depois quando tivermos baseline arquivado.

---

### I) Páginas em produção HTTP 200

**Critério:** Cada URL canônica de produção em `https://sites.{{DOMINIO}}/*` retorna HTTP 200. Lista das 10 páginas críticas (sincronizada com `squad/output/paginas/MAPA.md`).

**Comando:**
```bash
URLS=(
  "https://sites.{{DOMINIO}}/"
  "https://sites.{{DOMINIO}}/squad-time-ia"
  "https://sites.{{DOMINIO}}/reverso"
  "https://sites.{{DOMINIO}}/consultoria"
  "https://sites.{{DOMINIO}}/mentoria"
  "https://sites.{{DOMINIO}}/mentoria-precos"
  "https://sites.{{DOMINIO}}/clickup8x"
  "https://sites.{{DOMINIO}}/oferta-irresistivel-ensinio"
  "https://sites.{{DOMINIO}}/inscricao-aula-gui-avila-ensinio"
  "https://sites.{{DOMINIO}}/automacoes"
)
for u in "${URLS[@]}"; do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 "$u")
  echo "$CODE $u"
done
```

**Pass:** todas as 10 retornam `200`.
**Severidade quando falha:** HIGH (página fora do ar).
**Exemplo:** `HIGH | I | https://sites.{{DOMINIO}}/mentoria retornou 500 (página fora do ar)`.

---

### J) Padrões obrigatórios em todas as 10 páginas

**Critério:** Para cada URL produção do check (I), o HTML servido deve ter:
- `GTM-NN36ZRZ` count >= 2 (head script + noscript iframe — Regra #19 #147)
- `googletagmanager.com/gtm.js` count >= 1
- `googletagmanager.com/ns.html` count >= 1
- `/images/favicon-gui.ico` count >= 1 (favicon canônico — #149)
- `/_astro/` count > 0 (sinal de Astro nativo, não snapshot estático)

**Comando:**
```bash
for u in "${URLS[@]}"; do
  HTML=$(curl -s -L --max-time 15 "$u")
  GTM=$(printf '%s' "$HTML" | grep -o 'GTM-NN36ZRZ' | wc -l | tr -d ' ')
  GTMJS=$(printf '%s' "$HTML" | grep -o 'googletagmanager.com/gtm.js' | wc -l | tr -d ' ')
  GTMNS=$(printf '%s' "$HTML" | grep -o 'googletagmanager.com/ns.html' | wc -l | tr -d ' ')
  FAV=$(printf '%s' "$HTML" | grep -o '/images/favicon-gui.ico' | wc -l | tr -d ' ')
  ASTRO=$(printf '%s' "$HTML" | grep -o '/_astro/' | wc -l | tr -d ' ')
  echo "$u | GTM=$GTM GTMJS=$GTMJS NS=$GTMNS FAV=$FAV ASTRO=$ASTRO"
done
```

**Pass:** GTM>=2, GTMJS>=1, NS>=1, FAV>=1, ASTRO>0 em todas as páginas.

⚠️ **Atenção:** usar `grep -o ... | wc -l` (NUNCA `grep -c`) — HTML em produção é minificado em uma linha gigante e `grep -c` (que conta linhas) subconta drasticamente. Bug real registrado em aprendizado #147 (07/05/2026).

**Severidade quando falha:**
- HIGH se faltar GTM ou favicon
- MEDIUM se faltar `/_astro/` (provável snapshot estático fora do padrão)
**Exemplo:** `HIGH | J | https://sites.{{DOMINIO}}/automacoes GTM=0 (falta tag de medição — Regra #147)`.

---

### K) Sliders canônicos (Regra #19 #146)

**Critério:** Em todo `Páginas Astro {{NOME_OPERADOR}}/src/pages/[slug]/index.astro`, sinais de slider custom (overflow-x scroll/auto + display:flex em row com transform/translateX) devem estar dentro do componente canônico `Slider.astro`. Snapshots externos Framer/Webflow com slider implícito são REPROVADOS automaticamente (perdem o runtime de drag/auto-scroll).

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}" 2>/dev/null || exit 0
for f in src/pages/*/index.astro; do
  [ -f "$f" ] || continue
  # 1) tem sinais de slider custom?
  HAS_OVERFLOW=$(grep -cE 'overflow-x:\s*(auto|scroll)' "$f" 2>/dev/null || echo 0)
  HAS_TRANSLATE=$(grep -cE 'translateX|transform:\s*matrix' "$f" 2>/dev/null || echo 0)
  # 2) tem import do Slider canônico?
  HAS_CANON=$(grep -cE "from\s+['\"].*Slider\.astro['\"]|<Slider\b|data-gui-slider" "$f" 2>/dev/null || echo 0)
  if [ "$HAS_OVERFLOW" -gt 0 ] || [ "$HAS_TRANSLATE" -gt 0 ]; then
    if [ "$HAS_CANON" -eq 0 ]; then
      echo "SUSPECT: $f (overflow=$HAS_OVERFLOW translate=$HAS_TRANSLATE canon=$HAS_CANON)"
    fi
  fi
done
```

**Pass:** 0 SUSPECT.
**Severidade quando falha:** HIGH.
**Exemplo:** `HIGH | K | src/pages/automacoes/index.astro tem overflow-x:auto sem importar Slider.astro (snapshot Framer perdeu runtime — Regra #146)`.

⚠️ **Caveat:** detecção é heurística (markup-only). Confirmar com Playwright (`scripts/test-slider-drag.mjs`) antes de marcar como problema definitivo. Esta categoria sinaliza candidatos a inspeção.

---

### L) Secrets / segurança

**Critério:**
- `git ls-files` NÃO retorna `.env*` (exceto `.env.example`).
- `git log -p --all -G "sk-(ant|proj|sq|or)-[a-zA-Z0-9_-]{20,}"` retorna vazio (zero secret real no histórico).
- `mcp/.env.local` (App Reverso) NÃO está em `git ls-files`.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
# 1) .env tracked?
git ls-files | grep -E '\.env(\.|$)' | grep -v '\.example$'
# 2) padrão de chave de API no histórico?
git log -p --all -G 'sk-(ant|proj|sq|or)-[a-zA-Z0-9_-]{20,}' --max-count=3 2>/dev/null | head -20
# 3) mcp/.env.local específico?
git ls-files | grep -E '^mcp/\.env\.local$'
```

**Pass:** todas as três queries retornam saída vazia.
**Severidade quando falha:** CRITICAL.
**Exemplo:** `CRITICAL | L | .env.local em git ls-files — ROTAR TODAS as keys + git filter-repo (Regra secrets-em-env-local)`.

---

### M) Sincronia squad ↔ `.claude/agents/`

**Critério:**
Todo agente em `squads/{sq}/agentes/{ag}/` deve ter entry correspondente em `.claude/agents/{ag}.md`. E todo `.claude/agents/{ag}.md` (exceto `jade`) deve ter pasta `squads/{sq}/agentes/{ag}/` correspondente.

**Comando:**
```bash
cd "~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
# Pasta de agentes em squads/
SQUAD_AGENTS=$(ls -d squads/*/agentes/*/ 2>/dev/null | xargs -n1 basename | sort -u)
# Cadastros em .claude/agents/
CC_AGENTS=$(ls .claude/agents/*.md 2>/dev/null | xargs -n1 basename | sed 's/\.md$//' | sort -u)
# Agentes em squads/ SEM cadastro .claude/agents/ (HIGH)
echo "=== Faltando .claude/agents/ ==="
comm -23 <(echo "$SQUAD_AGENTS") <(echo "$CC_AGENTS")
# Cadastros .claude/agents/ ÓRFÃOS (sem pasta squad — exceto jade) (MEDIUM)
echo "=== Cadastros órfãos ==="
comm -13 <(echo "$SQUAD_AGENTS") <(echo "$CC_AGENTS") | grep -v "^jade$"
# Validação básica de frontmatter (name + description + model presentes)
echo "=== Frontmatter inválido ==="
for f in .claude/agents/*.md; do
  if ! python3 -c "import re,sys; c=open('$f').read(); m=re.match(r'^---\n(.*?)\n---\n', c, re.DOTALL); fm=m.group(1) if m else ''; sys.exit(0 if all(k in fm for k in ['name:','description:','model:']) else 1)" 2>/dev/null; then
    echo "$f"
  fi
done
```

**Pass:** seções "Faltando" e "Cadastros órfãos" e "Frontmatter inválido" todas vazias.
**Severidades:**
- HIGH: agente em `squads/` sem cadastro em `.claude/agents/` (Jade vai cair em `general-purpose`).
- MEDIUM: cadastro `.claude/agents/{nome}.md` sem pasta squad correspondente (órfão — `jade` é exceção legítima por ser orquestrador, não tem pasta dedicada).
- HIGH: frontmatter inválido (faltando `name:`, `description:` ou `model:`) — Claude Code não vai carregar.

**Exemplo:**
- `HIGH | M | agente "midia-editor" em squads/midia/agentes/ sem cadastro .claude/agents/midia-editor.md — Jade vai despachar como general-purpose (Tarefa #155)`
- `MEDIUM | M | .claude/agents/legacy.md sem pasta squads/*/agentes/legacy/ — remover ou criar pasta`

---

### M2) Sincronia documento canônico ↔ páginas vivas (Tarefa #158)

**Critério:**
Toda decisão arquitetural em `Segundo Cérebro/04-decisoes/*.md` deve ser referenciada em pelo menos 1 página viva sob `Páginas Astro {{NOME_OPERADOR}}/src/pages/`. E toda página que mencionar uma decisão canônica deve apontar para um arquivo válido em `Segundo Cérebro/04-decisoes/`.

Por quê: source of truth canônica desacoplada de páginas vivas vira "doc fantasma" — fica desatualizada porque ninguém vê. Esta categoria detecta a desincronia.

**Comando:**
```bash
SQUAD_ROOT="~/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
ASTRO_ROOT="~/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}"

# 1) Decisões canônicas em 04-decisoes/ sem referência em src/pages/
echo "=== Decisões canônicas sem referência em página viva ==="
for d in "$SQUAD_ROOT/Segundo Cérebro/04-decisoes/"*.md; do
  base=$(basename "$d" .md)
  # Pula README e MAPA
  case "$base" in README|MAPA) continue ;; esac
  # Procura o nome do arquivo (sem .md) em qualquer .astro de src/pages
  if ! grep -rq --include="*.astro" "$base" "$ASTRO_ROOT/src/pages/" 2>/dev/null; then
    echo "MEDIUM | M2 | $base.md sem referência em src/pages/ — fonte da verdade isolada"
  fi
done

# 2) Páginas mencionando "04-decisoes/" com path inválido
echo "=== Páginas referenciando decisão inexistente ==="
grep -rEho --include="*.astro" "04-decisoes/[a-zA-Z0-9_.-]+\.md" "$ASTRO_ROOT/src/pages/" 2>/dev/null   | sort -u   | while read ref; do
      file_part=$(echo "$ref" | sed 's|^04-decisoes/||')
      if [ ! -f "$SQUAD_ROOT/Segundo Cérebro/04-decisoes/$file_part" ]; then
        echo "MEDIUM | M2 | página referencia $ref mas arquivo não existe em Segundo Cérebro/04-decisoes/"
      fi
    done
```

**Pass:** ambas as seções vazias (toda decisão tem ao menos 1 página citando, toda citação aponta pra arquivo real).
**Severidade:** MEDIUM (não bloqueia produção, mas indica fonte da verdade desincronizada — risco de doc fantasma).

**Exemplo:**
- `MEDIUM | M2 | 2026-05-07-arquitetura-squad-por-dominio.md sem referência em src/pages/ — fonte da verdade isolada`
- `MEDIUM | M2 | página /squad-time-ia referencia 04-decisoes/decisao-antiga.md mas arquivo não existe — citação quebrada`

**Quando atualizar a página viva:**
Se a decisão canônica mudar, atualizar manualmente as páginas que a citam (Astro 6 não suporta import direto de `.md` com path com espaço/acento).

---

## Output canônico

Salvar em `squad/output/auditorias/YYYY-MM-DD-checkup-estrutura.md` (com timestamp na header).

```markdown
# Check-up Estrutura — YYYY-MM-DD HH:MM

## Veredicto: APROVADO / APROVADO COM RESSALVAS / REPROVADO

Regra de veredicto:
- REPROVADO se >=1 CRITICAL ou >=3 HIGH
- APROVADO COM RESSALVAS se 1-2 HIGH ou >=1 MEDIUM
- APROVADO se só LOW/INFO ou nada

## Sumário
- 13 categorias auditadas
- X findings totais
- Y CRITICAL, Z HIGH, W MEDIUM, V LOW, U INFO
- Tempo total: Ns

## Findings por severidade

### 🔴 CRITICAL (Y)
- [L] descrição path:line — ação sugerida

### 🟠 HIGH (Z)
- [A] descrição path:line — ação sugerida
- [E] descrição path:line — ação sugerida

### 🟡 MEDIUM (W)
- [B] descrição path:line — ação sugerida

### 🟢 LOW / INFO (V+U)
- [H] descrição path:line — sem ação

## Detalhe por categoria

### A) Skills com ## Fluxo
- Status: PASS / FAIL (Nfindings)
- Comando rodado: ...
- Saída: ...

[... idem B até L ...]

## Comandos rodados (transparência)

```bash
# Categoria A
for f in .claude/commands/*.md; do ...

# Categoria B
find squad squads "Segundo Cérebro" -type d ...

# ... etc
```

## Próximas ações sugeridas (priorizadas)

1. [CRITICAL] resolver L imediatamente (rotar key + remover do git)
2. [HIGH] aplicar fix em E (renumerar segunda REGRA #13 → #20)
3. [MEDIUM] criar memoria.md em squads/dev/agentes/paginas-dev/

## Caveats / limitações desta run

- Categoria H (backups #18) faz só listagem; diff entre runs não implementado nesta versão.
- Categoria K (sliders) é heurística (markup); confirmar com Playwright.
- (qualquer outra categoria que não rodou totalmente — ex: dev server offline)
```

Sumário no chat (entregue ao {{NOME_OPERADOR}} após salvar o relatório):

```
Check-up estrutura — APROVADO COM RESSALVAS

12 categorias / X findings:
🔴 0 CRITICAL  🟠 2 HIGH  🟡 3 MEDIUM  🟢 5 INFO

Top findings:
1. [HIGH] AGENTS.md tem duas REGRA INVIOLÁVEL #13
2. [HIGH] /automacoes GTM=0 em produção
3. [MEDIUM] squads/dev/agentes/paginas-dev/memoria.md ausente

Relatório completo: squad/output/auditorias/2026-05-07-checkup-estrutura.md

Quer que eu disparare correção de algum item agora?
```

---

## Cron / agendamento futuro

Esta skill é desenhada pra rodar diariamente via cron (a configurar separadamente quando o setup permitir). Por enquanto: manual via `/check-up-estrutura` quando o {{NOME_OPERADOR}} pedir, antes de demos importantes (aulas, lançamentos), e depois de qualquer mudança estrutural grande (novo squad, novo agente, nova regra inviolável).

Quando o cron for configurado, ele:
1. Roda `/check-up-estrutura` toda madrugada (ex: 04:00)
2. Salva relatório do dia
3. Se veredicto = REPROVADO: notifica o {{NOME_OPERADOR}} via canal definido (Telegram/email)
4. Se veredicto = APROVADO: log silencioso

Cron vai ser configurado pela skill `/agendar-checkup-estrutura` (a criar) ou via setup manual de launchd/cron-tab no Mac do {{NOME_OPERADOR}}. Não escopo desta skill.

---

## Como adicionar nova categoria de check

Toda vez que aparecer um padrão novo de erro estrutural (ex: feedback do {{NOME_OPERADOR}} sobre uma classe específica de bug), seguir Regra #19 e adicionar uma categoria nesta skill:

1. Editar este arquivo `.claude/commands/check-up-estrutura.md` **via Bash/Python** (Regra #8 proíbe Edit em `.claude/`).
2. Adicionar nova letra (M, N, O, ...) na lista "Categorias de check (12)" — atualizar o título de "12" para o novo total.
3. Adicionar bloco completo: nome, critério, comando, pass, severidade, exemplo.
4. Atualizar o **ASCII fluxograma** acima (lista das categorias dentro do `[2]`).
5. Atualizar o output canônico se a nova categoria precisar de seção dedicada.
6. Validar a skill rodando `/check-up-estrutura` uma vez no Mac local antes de marcar entregue.

⚠️ **Regra de ouro:** `/check-up-estrutura` só cresce. Nunca tirar categoria — se uma virou irrelevante, marca como `desativada` mas mantém o histórico (auditoria de retrofit precisa do registro).

---

## Restrições

- **Nondestrutivo:** zero categoria escreve, deleta, ou modifica arquivos. Só lê, conta, classifica.
- **Sem dependência de aprovação humana** pra rodar — skill autônoma.
- **Findings sempre com `path:line`** quando aplicável (clicável no VSCode).
- **Performance:** as 12 categorias devem rodar em < 2min total no Mac local. Categorias com curl externo (I, J) podem rodar em background `&` e fazer `wait` no fim.
- **Edição desta skill SÓ via Bash/Python** (Regra #8). Nunca via Edit.

---

## Após a auditoria

1. Salvar relatório em `squad/output/auditorias/YYYY-MM-DD-checkup-estrutura.md`.
2. Atualizar `squad/output/auditorias/MAPA.md` com entrada nova (data + veredicto + N findings).
3. Apresentar sumário ao {{NOME_OPERADOR}} (chat) — não sair perguntando "quer atacar X?". Em vez disso, afirmar próxima ação: "Próximo passo: vou disparar correção do CRITICAL [L]. Me avisa se quiser desviar."
4. Para cada finding aprovado pelo {{NOME_OPERADOR}} pra correção: dispatchar a skill apropriada (ex: HIGH na categoria E → editar AGENTS.md; MEDIUM na categoria D → criar `memoria.md`).
5. Registrar conclusão em `squads/dev/tarefas.md` (skill rodou data X, N findings, veredicto).
