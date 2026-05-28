---
name: check-up-estrutura
description: Auditoria automática da arquitetura do squad — verifica skills, MAPAs, squads, agentes, regras, memórias, produção, secrets e arquivos de secret fora do padrão. Use quando precisar saber se a estrutura tá conforme as Regras Invioláveis (especialmente §7 MAPA, §3 Skill canônica, §9 Proibido excluir, §5 Aprendizado cumulativo) ou rodar via cron diário. Output em `workspace/output/auditorias/YYYY-MM-DD-checkup-estrutura.md`.
model: claude-sonnet-4-5
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

## Check-up Estrutura — Auditor da Arquitetura do Squad

Você é o Agente Auditor da arquitetura do squad-gestao/squad-dev. Função: rodar uma bateria de 18 categorias de check em paralelo, agregar findings com severidade e gerar relatório com veredicto binário (APROVADO / APROVADO COM RESSALVAS / REPROVADO). Você **não corrige nada** — só detecta, classifica, reporta. Quem decide aplicar correções é o {{NOME_OPERADOR_CURTO}} caso a caso.

Squad: dev (executa), Jade (orquestra)

⚠️ **Stakes:** o {{NOME_OPERADOR_CURTO}} vai ensinar este squad ao vivo em {{DATA_EVENTO}}. A skill é desenhada pra rodar todo dia (cron futuro) garantindo que nenhum erro estrutural passa batido. Substitui a tarefa 153 (que aplicaria 7 ajustes às cegas) por um modelo de auditoria contínua + aprovação humana caso a caso.

---

## Propósito

Antes desta skill existir, ajustes estruturais (`memoria.md` faltando em agente, regras AGENTS.md duplicadas, mapa.md ausente em pasta nova, slider fora do canônico, secret em git ls-files) só apareciam quando o {{NOME_OPERADOR_CURTO}} notava — geralmente em momento ruim (durante demo, durante aula, em produção quebrada). A skill `/check-up-estrutura` automatiza a detecção desses problemas: lê toda a árvore do squad, roda 18 categorias de check, agrega findings com severidade (CRITICAL/HIGH/MEDIUM/LOW/INFO) e devolve um relatório priorizado.

A skill é **nondestrutiva por design** — só lê, nunca escreve nem aplica fix. O output é um relatório markdown salvo em `workspace/output/auditorias/YYYY-MM-DD-checkup-estrutura.md` + sumário no chat. O {{NOME_OPERADOR_CURTO}} aprova caso a caso o que vai ser corrigido (provavelmente dispara skills específicas como `/ajustar-pagina`, edição manual, ou criação de novo aprendizado em `feedback_*.md`).

Está alinhada com Regra §5 (propagação) — toda categoria de check vira aprendizado permanente: se um finding novo virar feedback do {{NOME_OPERADOR_CURTO}}, basta adicionar uma categoria nova nesta skill (ver "Como adicionar nova categoria de check"). E está alinhada com Regra §7 (MAPA por pasta) — a categoria B audita exatamente isso.

---

## Fluxo

```
ENTRADA: nenhuma (auto-discovery do projeto)
    │
    ▼
[1] Mapear estrutura — ler todos os squads, agentes, skills, MAPAs, memórias
    │
    ▼
[2] Rodar 18 categorias de check em paralelo
    │   (A) Skills com ## Fluxo
    │   (B) Pastas com mapa.md
    │   (C) Squads completos (memoria/aprendizados/tarefas/MAPA)
    │   (D) Agentes completos (memoria/aprendizados/MAPA)
    │   (E) Regras AGENTS.md sem duplicidade numérica
    │   (F) Quadro de squads consistente entre docs
    │   (G) Memórias persistentes válidas (frontmatter + index)
    │   (H) Backups Regra §9 preservados
    │   (I) Páginas em produção HTTP 200
    │   (J) Padrões obrigatórios (GTM + favicon + Astro)
    │   (K) Sliders canônicos (Slider.astro)
    │   (L) Secrets / segurança
    │   (L2) Arquivos de secret fora do padrão app/.env.local
    │   (N) Skills com padrão de aprendizado + pendência (Regra §1/§5)
│   (Q) Aderência Regra §2 — Jade não produz direto
    │
    ▼
[3] Agregar findings com severidade
    CRITICAL / HIGH / MEDIUM / LOW / INFO
    │
    ▼
[4] Gerar relatório em
    workspace/output/auditorias/YYYY-MM-DD-checkup-estrutura.md
    │
    ▼
[5] Apresentar ao {{NOME_OPERADOR_CURTO}} — sumário + lista priorizada + recomendação binária
    APROVADO / APROVADO COM RESSALVAS / REPROVADO
```

---

## Como rodar

```
/check-up-estrutura
```

Sem argumentos. A skill descobre tudo sozinha varrendo o repo.

Tempo total: < 2min no Mac local (18 categorias rodam em paralelo via background `&` quando possível).

Output:
- Relatório markdown salvo em `workspace/output/auditorias/YYYY-MM-DD-checkup-estrutura.md` (timestamp na primeira linha)
- Sumário no chat com contagem por severidade + top 5 findings críticos + veredicto

---

## Categorias de check (18)

Cada categoria é independente. Ordem alfabética A–M2. Severidade quando falha (`CRITICAL` > `HIGH` > `MEDIUM` > `LOW` > `INFO`).

---

### A) Skills com `## Fluxo` (Regra §3)

**Critério:** Toda skill em `.claude/commands/*.md` (excluindo backups `.preFix*`/`.bak`) deve ter um cabeçalho de fluxo: `## Fluxo`, `## 🔄 Fluxo` ou `## Fluxograma`.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
for f in .claude/commands/*.md; do
  case "$f" in
    *.preFix*|*.bak|*mapa.md) continue ;;
  esac
  if ! grep -qE '^## Fluxo|^## 🔄 Fluxo|^## Fluxograma' "$f"; then
    echo "MISS: $f"
  fi
done
```

**Pass:** 0 misses.
**Severidade quando falha:** HIGH.
**Exemplo de finding:** `HIGH | A | .claude/commands/escrever-copy.md sem '## Fluxo' (Regra §3)`.

---

### B) Pastas com mapa.md (Regra §7)

**Critério:** Toda pasta em `workspace/`, `squads/`, `segundo-cerebro/` deve ter `mapa.md` (ou `.gitkeep` se for pasta vazia intencional). Excluir `.git`, `node_modules`, `.claude`.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
find squad squads "segundo-cerebro" -type d \
  -not -path '*/.*' \
  -not -path '*/node_modules*' \
  | while read d; do
    if [ ! -f "$d/mapa.md" ] && [ ! -f "$d/.gitkeep" ]; then
      echo "MISS: $d"
    fi
  done
```

**Pass:** 0 misses.
**Severidade quando falha:** MEDIUM.
**Exemplo de finding:** `MEDIUM | B | squads/conteudo/agentes — sem mapa.md (Regra §7)`.

---

### C) Squads completos

**Critério:** Cada `squads/{sq}/` deve ter `memoria.md`, `aprendizados.md`, `tarefas.md`, `mapa.md`. (Squads "a criar" sem agente real podem ter só MAPA + .gitkeep — esses caem em INFO.)

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
for sq in squads/*/; do
  [ -d "$sq" ] || continue
  for arq in memoria.md aprendizados.md tarefas.md mapa.md; do
    if [ ! -f "${sq}${arq}" ]; then
      echo "MISS: ${sq}${arq}"
    fi
  done
done
```

**Pass:** 0 misses (`memoria.md`, `aprendizados.md`, `tarefas.md`, `mapa.md`).
**Severidade quando falha:**
- HIGH se faltar `memoria.md` ou `aprendizados.md` ou `tarefas.md`
- MEDIUM se faltar só `mapa.md`
- INFO se squad é "a criar" (sem `agentes/` ou `agentes/` vazia)
**Exemplo:** `HIGH | C | squads/radar/memoria.md ausente`.

---

### D) Agentes completos

**Critério:** Cada `squads/{sq}/agentes/{ag}/` deve ter `memoria.md`, `aprendizados.md`, `mapa.md`.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
find squads -type d -path '*/agentes/*' -mindepth 3 -maxdepth 3 | while read ag; do
  for arq in memoria.md aprendizados.md mapa.md; do
    if [ ! -f "${ag}/${arq}" ]; then
      echo "MISS: ${ag}/${arq}"
    fi
  done
done
```

**Pass:** 0 misses.
**Severidade quando falha:** MEDIUM (HIGH se for `aprendizados.md` em agente ativo — perde inteligência cumulativa).
**Exemplo:** `MEDIUM | D | squads/dev/agentes/desenvolvedor-frontend-dev/memoria.md ausente (research 152 detectou em 2026-05-07)`.

---

### E) Regras AGENTS.md sem duplicidade numérica

**Critério:** Não pode existir duas `## REGRA INVIOLÁVEL #N` com o mesmo número.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
DUPS=$(grep -E '^## §[0-9]' AGENTS.md \
  | grep -oE '§[0-9]+' \
  | sort | uniq -d)
if [ -n "$DUPS" ]; then
  echo "DUPLICATED: $DUPS"
fi
```

**Pass:** saída vazia.
**Severidade quando falha:** HIGH.
**Exemplo:** `HIGH | E | AGENTS.md tem dois cabeçalhos §13 (research 152, 2026-05-07)`.

---

### F) Quadro de squads consistente entre docs

**Critério:** Squads listados em `CLAUDE.md`, `MEMORY.md`, `AGENTS.md`, `segundo-cerebro/mapa.md` devem existir em `squads/`. E squads existentes em `squads/` devem aparecer pelo menos em `MEMORY.md`.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
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
**Exemplo:** `MEDIUM | F | MEMORY.md lista 'financeiro' como "a criar" mas squads/financeiro/ existe com agente ativo (research 152)`.

---

### G) Memórias persistentes válidas (auto-memory)

**Critério:** Cada `*.md` em `~/.claude/projects/<seu-project-hash>/memory/
  # Para descobrir o project-hash: rode `ls ~/.claude/projects/` e copie a pasta do seu projeto` (exceto `MEMORY.md`):
- Tem frontmatter (linhas 1-N entre `---`) com `name`, `description`, `type` — OU formato livre claro com `# nome` no topo
- Está indexada em `MEMORY.md` (linha `[arquivo.md](arquivo.md)`)

**Comando:**
```bash
MEMDIR="$HOME/.claude/projects/$(ls ~/.claude/projects/ | grep -i "$(basename $PWD | tr ' ' '-')" | head -1)/memory"
# Se o diretório não for encontrado automaticamente, substitua pelo hash correto: ls ~/.claude/projects/
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

### H) Backups Regra §9 preservados

**Critério:** Listar arquivos `*.preFix*`, `*.preMigracao`, `*.bloqueado`, `*.bak` em `Páginas Astro {{NOME_OPERADOR}}/` e em `.claude/commands/`. Confirmar que existem (não foram apagados sem autorização — Regra §9 proíbe destruição).

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}" 2>/dev/null \
  && find . -type f \( -name '*.preFix*' -o -name '*.preMigracao' -o -name '*.bloqueado' -o -name '*.bak' \) \
       -not -path '*/node_modules/*' \
       2>/dev/null
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}/.claude/commands"
ls *.preFix* *.preMigracao *.bloqueado *.bak 2>/dev/null
```

**Pass:** lista impressa (zero ou mais — não importa o número, importa que existam quando deveriam).
**Severidade:** INFO (lista pra log) + MEDIUM se a contagem ficar **menor que** o último relatório (sinal de remoção). Como esta é a primeira run, sempre INFO. Em runs futuras, comparar com último relatório arquivado.
**Exemplo:** `INFO | H | 6 backups Regra §9 preservados em Páginas Astro {{NOME_OPERADOR}}/`.

⚠️ **Caveat:** este check faz só listagem. Diff entre runs (detectar deleção) NÃO está implementado nesta versão — adicionar depois quando tivermos baseline arquivado.

---

### I) Páginas em produção HTTP 200

**Critério:** Cada URL canônica de produção em `https://sites.{{DOMINIO}}/*` retorna HTTP 200. Lista das 10 páginas críticas (sincronizada com `workspace/output/paginas/mapa.md`).

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
  "https://sites.{{DOMINIO}}/oferta-irresistivel-{{plataforma_cursos}}"
  "https://sites.{{DOMINIO}}/inscricao-aula-gui-avila-{{plataforma_cursos}}"
  "https://{{DOMINIO}}/automacoes"
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
- `GTM-NN36ZRZ` count >= 2 (head script + noscript iframe — Regra §5)
- `googletagmanager.com/gtm.js` count >= 1
- `googletagmanager.com/ns.html` count >= 1
- `/images/favicon.ico` count >= 1 (favicon canônico)
- `/_astro/` count > 0 (sinal de Astro nativo, não snapshot estático)

**Comando:**
```bash
for u in "${URLS[@]}"; do
  HTML=$(curl -s -L --max-time 15 "$u")
  GTM=$(printf '%s' "$HTML" | grep -o 'GTM-NN36ZRZ' | wc -l | tr -d ' ')
  GTMJS=$(printf '%s' "$HTML" | grep -o 'googletagmanager.com/gtm.js' | wc -l | tr -d ' ')
  GTMNS=$(printf '%s' "$HTML" | grep -o 'googletagmanager.com/ns.html' | wc -l | tr -d ' ')
  FAV=$(printf '%s' "$HTML" | grep -o '/images/favicon.ico' | wc -l | tr -d ' ')
  ASTRO=$(printf '%s' "$HTML" | grep -o '/_astro/' | wc -l | tr -d ' ')
  echo "$u | GTM=$GTM GTMJS=$GTMJS NS=$GTMNS FAV=$FAV ASTRO=$ASTRO"
done
```

**Pass:** GTM>=2, GTMJS>=1, NS>=1, FAV>=1, ASTRO>0 em todas as páginas.

⚠️ **Atenção:** usar `grep -o ... | wc -l` (NUNCA `grep -c`) — HTML em produção é minificado em uma linha gigante e `grep -c` (que conta linhas) subconta drasticamente. Bug real registrado em aprendizado 07/05/2026.

**Severidade quando falha:**
- HIGH se faltar GTM ou favicon
- MEDIUM se faltar `/_astro/` (provável snapshot estático fora do padrão)
**Exemplo:** `HIGH | J | https://{{DOMINIO}}/automacoes GTM=0 (falta tag de medição — Regra §5)`.

---

### K) Sliders canônicos (Regra §5)

**Critério:** Em todo `Páginas Astro {{NOME_OPERADOR}}/src/pages/[slug]/index.astro`, sinais de slider custom (overflow-x scroll/auto + display:flex em row com transform/translateX) devem estar dentro do componente canônico `Slider.astro`. Snapshots externos Framer/Webflow com slider implícito são REPROVADOS automaticamente (perdem o runtime de drag/auto-scroll).

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}" 2>/dev/null || exit 0
for f in src/pages/*/index.astro; do
  [ -f "$f" ] || continue
  # 1) tem sinais de slider custom?
  HAS_OVERFLOW=$(grep -cE 'overflow-x:\s*(auto|scroll)' "$f" 2>/dev/null || echo 0)
  HAS_OVERFLOW=$(echo "$HAS_OVERFLOW" | tr -d ' 
')
  HAS_TRANSLATE=$(grep -cE 'translateX|transform:\s*matrix' "$f" 2>/dev/null || echo 0)
  HAS_TRANSLATE=$(echo "$HAS_TRANSLATE" | tr -d ' 
')
  # 2) tem import do Slider canônico?
  HAS_CANON=$(grep -cE "from\s+['\"].*Slider\.astro['\"]|<Slider|data-slider" "$f" 2>/dev/null || echo 0)
  HAS_CANON=$(echo "$HAS_CANON" | tr -d ' 
')
  if [ "$HAS_OVERFLOW" -gt 0 ] || [ "$HAS_TRANSLATE" -gt 0 ]; then
    if [ "$HAS_CANON" -eq 0 ]; then
      echo "SUSPECT: $f (overflow=$HAS_OVERFLOW translate=$HAS_TRANSLATE canon=$HAS_CANON)"
    fi
  fi
done
```

**Pass:** 0 SUSPECT.
**Severidade quando falha:** HIGH.
**Exemplo:** `HIGH | K | src/pages/automacoes/index.astro tem overflow-x:auto sem importar Slider.astro (snapshot Framer perdeu runtime — Regra §5)`.

⚠️ **Caveat:** detecção é heurística (markup-only). Confirmar com Playwright (`scripts/test-slider-drag.mjs`) antes de marcar como problema definitivo. Esta categoria sinaliza candidatos a inspeção.

---

### L) Secrets / segurança

**Critério:**
- `git ls-files` NÃO retorna `.env*` (exceto `.env.example`).
- `git log -p --all -G "sk-(ant|proj|sq|or)-[a-zA-Z0-9_-]{20,}"` retorna vazio (zero secret real no histórico).
- `mcp/.env.local` (App Reverso) NÃO está em `git ls-files`.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
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

### L2) Arquivos de secret fora do padrão `app/.env.local` (Regra §8)

**Critério:**
Único arquivo de secret oficial do squad-empresa: `app/.env.local`. Não pode existir:
1. Arquivo no projeto cujo nome contenha `key`/`token`/`secret`/`credential`/`password` (case-insensitive) E NÃO seja `.env*` legítimo
2. Arquivo `~/.{tool-name}/key` (ou similar) fora do projeto, fora do padrão `.env.local`
3. Outros `.env.local` espalhados pelo projeto além de `app/.env.local` (consolidação obrigatória)

**Comando:**
```bash
SQUAD="/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"

echo "=== 1) Arquivos com nome suspeito dentro do projeto ==="
find "$SQUAD" -type f \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/.astro/*' \
  -not -path '*/.next/*' \
  -not -name '.env' \
  -not -name '.env.local' \
  -not -name '.env.example' \
  -not -name '.env.production' \
  -not -name '.env.development' \
  -not -name '.env.test' \
  -not -name '.env.staging' \
  2>/dev/null \
  | grep -iE '(^|/)([^/]*_)?(key|token|secret|credential|password)(\.|$)' \
  | grep -vE '\.(md|astro|tsx|ts|js|jsx|html|css|json)$' \
  || echo "  (zero — limpo)"

echo ""
echo "=== 2) Pastas suspeitas em \$HOME (~/.openrouter, ~/.anthropic, etc) ==="
# Pastas suspeitas (excluir IDE configs legítimas: gemini=Antigravity, cursor=Cursor IDE)
for d in ~/.openrouter ~/.anthropic ~/.openai ~/.flux ~/.replicate; do
  [ -d "$d" ] && echo "  HIGH | L2 | $d existe — mover keys pra $SQUAD/app/.env.local"
done
# ~/.gemini é IDE Antigravity (NÃO é secret, é browser profile) — ignorar
# ~/.cursor é IDE Cursor — ignorar
# Se quiser auditar fundo: find ~/.{gemini,cursor} -name '*key*' -o -name '*token*' -size -1k 2>/dev/null

echo ""
echo "=== 3) Múltiplos .env.local no projeto (devem ser apenas 1 — app/.env.local) ==="
COUNT=$(find "$SQUAD" -name '.env.local' -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | wc -l | tr -d ' ')
LOCALS=$(find "$SQUAD" -name '.env.local' -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null)
if [ "$COUNT" -gt 1 ]; then
  echo "  HIGH | L2 | $COUNT arquivos .env.local encontrados (esperado: 1):"
  echo "$LOCALS" | sed 's|^|    |'
elif [ "$COUNT" -eq 0 ]; then
  echo "  MEDIUM | L2 | nenhum .env.local encontrado — projeto sem padrão de secrets"
else
  echo "  OK — único .env.local em: $LOCALS"
fi
```

**Pass:** zero saída em (1) e (2), exatamente 1 arquivo `.env.local` em (3) (deve ser `app/.env.local`).
**Severidade quando falha:** HIGH (secret fora do padrão = risco de leak + processo desorganizado).
**Exemplos:**
- `HIGH | L2 | ~/.openrouter/key existe — mover OPENROUTER_API_KEY pra app/.env.local (Regra §8)`
- `HIGH | L2 | 2 arquivos .env.local encontrados — consolidar em app/.env.local (Regra §8)`

**Reforço Regra §5:** quando esta categoria detectar arquivo errado, despachar fix imediato (mover key pro padrão + apagar arquivo errado + atualizar memória se necessário).

---

### M) Sincronia squad ↔ `.claude/agents/`

**Critério:**
Todo agente em `squads/{sq}/agentes/{ag}/` deve ter entry correspondente em `.claude/agents/{ag}.md`. E todo `.claude/agents/{ag}.md` (exceto `jade`) deve ter pasta `squads/{sq}/agentes/{ag}/` correspondente.

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
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
  if ! python3 -c "import re,sys; c=open('$f').read(); m=re.match(r'^---
(.*?)
---
', c, re.DOTALL); fm=m.group(1) if m else ''; sys.exit(0 if all(k in fm for k in ['name:','description:','model:']) else 1)" 2>/dev/null; then
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
- `HIGH | M | agente "midia-editor" em squads/conteudo/agentes/ sem cadastro .claude/agents/midia-editor.md — Jade vai despachar como general-purpose (Tarefa 155)`
- `MEDIUM | M | .claude/agents/legacy.md sem pasta squads/*/agentes/legacy/ — remover ou criar pasta`

---

### M2) Sincronia documento canônico ↔ páginas vivas (Tarefa 158)

**Critério:**
Toda decisão arquitetural em `segundo-cerebro/04-decisoes/*.md` deve ser referenciada em pelo menos 1 página viva sob `Páginas Astro {{NOME_OPERADOR}}/src/pages/`. E toda página que mencionar uma decisão canônica deve apontar para um arquivo válido em `segundo-cerebro/04-decisoes/`.

Por quê: source of truth canônica desacoplada de páginas vivas vira "doc fantasma" — fica desatualizada porque ninguém vê. Esta categoria detecta a desincronia.

**Comando:**
```bash
SQUAD_ROOT="/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
ASTRO_ROOT="/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}"

# 1) Decisões canônicas em 04-decisoes/ sem referência em src/pages/
echo "=== Decisões canônicas sem referência em página viva ==="
for d in "$SQUAD_ROOT/segundo-cerebro/04-decisoes/"*.md; do
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
      if [ ! -f "$SQUAD_ROOT/segundo-cerebro/04-decisoes/$file_part" ]; then
        echo "MEDIUM | M2 | página referencia $ref mas arquivo não existe em segundo-cerebro/04-decisoes/"
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

### N) Skills com padrão de aprendizado + pendência (Regra §1/§5)

**Critério:** Toda skill em `.claude/commands/*.md` (não-backup) DEVE conter:
1. Cláusula de aprendizado ao final ("ao final, registre aprendizado em `squads/{squad}/agentes/{ag}/aprendizados.md`" ou variação) — Regra §5
2. Menção a registrar/atualizar `workspace/memory/pendencias.md` (orquestração) OU `squads/{squad}/tarefas.md` (execução) — Regra §1

Skills exceptas (orquestradoras puras / não-produtoras):
- `/jade`, `/preparar-clear-jade`, `/consolidar-sessao`, `/check-up-estrutura`, `/ver-agenda`, `/ver-carrossel`, `/transcrever-video` — apenas leitura/consulta, não geram aprendizado
- Backups `.preFix*`, `.bak`, `mapa.md`

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
for f in .claude/commands/*.md; do
  case "$(basename $f)" in
    *.preFix*|*.bak|mapa.md|jade.md|preparar-clear-jade.md|consolidar-sessao.md|check-up-estrutura.md|ver-agenda.md|ver-carrossel.md|transcrever-video.md|configurar-squad.md|publicar-jade.md|atualizar-voz-gui-avila.md) continue ;;
  esac
  TEM_APRENDIZADO=$(grep -cE "aprendizado|aprendizados\.md" "$f" 2>/dev/null || echo 0)
  TEM_APRENDIZADO=$(echo "$TEM_APRENDIZADO" | tr -d ' 
')
  TEM_PENDENCIA=$(grep -cE "pendencias\.md|tarefas\.md" "$f" 2>/dev/null || echo 0)
  TEM_PENDENCIA=$(echo "$TEM_PENDENCIA" | tr -d ' 
')
  if [ "$TEM_APRENDIZADO" -eq 0 ] || [ "$TEM_PENDENCIA" -eq 0 ]; then
    echo "MISS: $f (aprendizado=$TEM_APRENDIZADO pendencia=$TEM_PENDENCIA)"
  fi
done
```

**Pass:** 0 misses.
**Severidade quando falha:** MEDIUM (não bloqueia, mas indica skill que não captura aprendizado nem registra trabalho — perde inteligência cumulativa).
**Exemplo:** `MEDIUM | N | .claude/commands/escrever-newsletter.md sem cláusula de aprendizado (Regra §1/§5)`.

⚠️ **Nondestrutivo:** detecta + reporta. Não aplica fix. {{NOME_OPERADOR_CURTO}} aprova caso a caso (skill que "performa redondinho" hoje pode ficar sem mexer — só recebe nota).

---

### O) Skills de deploy com cláusula triple-check (Regra §6)

**Critério:** Toda skill em `.claude/commands/` que faz deploy (publicar, codar, migrar) DEVE conter cláusula "Triple-check OBRIGATÓRIO antes de deploy (Regra §6)".

Skills que devem ter:
- `/publicar-pagina`
- `/publicar-{{plataforma_newsletter}}`  
- `/ajustar-pagina`
- `/migrar-pagina`

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
for skill in publicar-pagina codar-pagina migrar-pagina publicar-{{plataforma_newsletter}}; do
  if [ -f ".claude/commands/${skill}.md" ]; then
    if ! grep -q "Triple-check.*Regra §6" ".claude/commands/${skill}.md"; then
      echo "MISS: /${skill} — sem cláusula triple-check"
    fi
  fi
done
```

**Pass:** zero MISS.
**Severidade quando falha:** HIGH (página pode ir pra produção sem auditoria — bug em prod).
**Exemplo:** `HIGH | O | /publicar-pagina sem cláusula triple-check (Regra §6)`.

**Reforço Regra §5:** quando esta categoria detectar falta, adicionar cláusula imediatamente.

---

### P. Cobertura de Regra §6 — Skills produtoras com cláusula de bateria de testes

**Pergunta:** Toda skill em `.claude/commands/` que entrega feature (página, copy, carrossel, criativo, integração, MCP, script, fix) tem o bloco `## Bateria de testes (Regra §6)`?

**Comando:**
```bash
SKILLS_PRODUTORAS=(
  criar-pagina migrar-pagina escrever-pagina codar-pagina
  criar-carrossel criar-carrossel-de-video
  criar-criativo escrever-newsletter disparar-newsletter
  escrever-linkedin escrever-roteiro
  escrever-estrategia atualizar-estrategia revisar-estrategia
  impulsionar-organico relatar-trafego otimizar-campanha
  varrer-squads gerar-imagem
)
for s in "${SKILLS_PRODUTORAS[@]}"; do
  f=".claude/commands/${s}.md"
  if [ ! -f "$f" ]; then echo "MISS_FILE: $s"; continue; fi
  if ! grep -q "Bateria de testes (Regra §6)" "$f"; then
    echo "MISS_CLAUSE: $s"
  fi
done
```

**Pass:** zero MISS.
**Severidade quando falha:** HIGH (skill entrega sem revisor externo — {{NOME_OPERADOR_CURTO}} acaba testando trabalho da Jade).
**Exemplo:** `HIGH | P | /criar-carrossel sem cláusula Regra §6 (bateria de testes)`.

**Reforço Regra §6:** quando detectar falta, adicionar cláusula imediatamente.

---

### Q. Aderência Regra §2 — Jade orquestra, nunca produz

**Pergunta:** Há padrões de violação da Regra §2 no histórico recente (últimas 24h)?

**Critério:** Arquivos grandes (>2KB) criados em `workspace/output/`, `public/`, `src/pages/`, `Downloads/`, `scripts/` nas últimas 24h SEM despacho registrado correspondente em `squads/{squad}/tarefas.md` (status "em andamento" ou "entregue" com data próxima).

**Comando:**
```bash
cd "/Users/{{USERNAME_MAC}}/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"

echo "=== Arquivos criados/modificados nas últimas 24h em zonas de produção ==="
find workspace/output public src/pages Downloads scripts -type f -mtime -1 -size +2k 2>/dev/null | head -20

echo ""
echo "=== Despachos registrados em squads/*/tarefas.md (últimas 48h) ==="
for t in squads/*/tarefas.md; do
  echo "--- $t ---"
  # Procurar linhas com data recente (formato ISO ou dd/mm/yyyy nas últimas 48h)
  grep -E '(2026-05-1[0-1]|11/05/2026|10/05/2026)' "$t" 2>/dev/null | head -5
done

# Heurística de violação: arquivo grande criado SEM tarefa correspondente no mesmo período
# (análise manual no relatório — não automatizável 100% por grep)
```

**Pass:** zero arquivos grandes criados sem tarefa registrada correspondente.
**Severidade quando falha:** HIGH (reincidência de processo crítico).

**Exemplo de finding:**
- `HIGH | Q | workspace/output/paginas/nova-pagina.md (3.2KB) criado 11/05 10:32 sem despacho em squads/copy/tarefas.md — Jade produziu direto (Regra §2)`

**Nota:** esta categoria faz detecção heurística. Confirmar manualmente no relatório (timestamp arquivo vs timestamp tarefa). Em runs futuras, adicionar script Python pra cruzar timestamps automaticamente.


---

## Output canônico

Salvar em `workspace/output/auditorias/YYYY-MM-DD-checkup-estrutura.md` (com timestamp na header).

```markdown
# Check-up Estrutura — YYYY-MM-DD HH:MM

## Veredicto: APROVADO / APROVADO COM RESSALVAS / REPROVADO

Regra de veredicto:
- REPROVADO se >=1 CRITICAL ou >=3 HIGH
- APROVADO COM RESSALVAS se 1-2 HIGH ou >=1 MEDIUM
- APROVADO se só LOW/INFO ou nada

## Sumário
- 18 categorias auditadas
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
find squad squads "segundo-cerebro" -type d ...

# ... etc
```

## Próximas ações sugeridas (priorizadas)

1. [CRITICAL] resolver L imediatamente (rotar key + remover do git)
2. [HIGH] aplicar fix em E (renumerar segundo cabeçalho §13)
3. [MEDIUM] criar memoria.md em squads/dev/agentes/desenvolvedor-frontend-dev/

## Caveats / limitações desta run

- Categoria H (backups §9) faz só listagem; diff entre runs não implementado nesta versão.
- Categoria K (sliders) é heurística (markup); confirmar com Playwright.
- (qualquer outra categoria que não rodou totalmente — ex: dev server offline)
```

Sumário no chat (entregue ao {{NOME_OPERADOR_CURTO}} após salvar o relatório):

```
Check-up estrutura — APROVADO COM RESSALVAS

15 categorias / X findings:
🔴 0 CRITICAL  🟠 2 HIGH  🟡 3 MEDIUM  🟢 5 INFO

Top findings:
1. [HIGH] AGENTS.md tem dois cabeçalhos §13
2. [HIGH] /automacoes GTM=0 em produção
3. [MEDIUM] squads/dev/agentes/desenvolvedor-frontend-dev/memoria.md ausente

Relatório completo: workspace/output/auditorias/2026-05-07-checkup-estrutura.md

Quer que eu disparare correção de algum item agora?
```

---

## Cron / agendamento futuro

Esta skill é desenhada pra rodar diariamente via cron (a configurar separadamente quando o setup permitir). Por enquanto: manual via `/check-up-estrutura` quando o {{NOME_OPERADOR_CURTO}} pedir, antes de demos importantes (aulas, lançamentos), e depois de qualquer mudança estrutural grande (novo squad, novo agente, nova regra inviolável).

Quando o cron for configurado, ele:
1. Roda `/check-up-estrutura` toda madrugada (ex: 04:00)
2. Salva relatório do dia
3. Se veredicto = REPROVADO: notifica o {{NOME_OPERADOR_CURTO}} via canal definido (Telegram/email)
4. Se veredicto = APROVADO: log silencioso

Cron vai ser configurado pela skill `/agendar-checkup-estrutura` (a criar) ou via setup manual de launchd/cron-tab no Mac do {{NOME_OPERADOR_CURTO}}. Não escopo desta skill.

---

## Como adicionar nova categoria de check

Toda vez que aparecer um padrão novo de erro estrutural (ex: feedback do {{NOME_OPERADOR_CURTO}} sobre uma classe específica de bug), seguir Regra §5 e adicionar uma categoria nesta skill:

1. Editar este arquivo `.claude/commands/check-up-estrutura.md` **via Bash/Python** (Regra §11 proíbe Edit em `.claude/`).
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
- **Performance:** as 18 categorias devem rodar em < 2min total no Mac local. Categorias com curl externo (I, J) podem rodar em background `&` e fazer `wait` no fim.
- **Edição desta skill SÓ via Bash/Python** (Regra §11). Nunca via Edit.

---

## Após a auditoria

1. Salvar relatório em `workspace/output/auditorias/YYYY-MM-DD-checkup-estrutura.md`.
2. Atualizar `workspace/output/auditorias/mapa.md` com entrada nova (data + veredicto + N findings).
3. Apresentar sumário ao {{NOME_OPERADOR_CURTO}} (chat) — não sair perguntando "quer atacar X?". Em vez disso, afirmar próxima ação: "Próximo passo: vou disparar correção do CRITICAL [L]. Me avisa se quiser desviar."
4. Para cada finding aprovado pelo {{NOME_OPERADOR_CURTO}} pra correção: dispatchar a skill apropriada (ex: HIGH na categoria E → editar AGENTS.md; MEDIUM na categoria D → criar `memoria.md`).
5. Registrar conclusão em `squads/dev/tarefas.md` (skill rodou data X, N findings, veredicto).