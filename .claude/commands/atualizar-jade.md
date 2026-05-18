<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /atualizar-jade — Atualiza framework do squad preservando identidade do aluno

Aplica updates do upstream (`{{github_user}}/squad-template`) preservando dados pessoais do aluno. Inspirado em `shadcn-ui add`, `next codemod`, `rails app:update`.

## Quando invocar

- Aluno quer puxar últimas atualizações do squad (novas skills, agentes melhorados, hooks novos)
- Após semanas sem atualizar
- Quando ver no LinkedIn/YouTube/Newsletter do {{OPERADOR}} que tem nova feature no squad

## Conceito-chave: framework vs persona

Two-track architecture protege customização do aluno:

### Framework (ATUALIZAR — sobrescreve do upstream)
- `.claude/commands/*.md` (skills)
- `.claude/agents/*.md` (agentes)
- `.claude/hooks/*.sh` (hooks bloqueantes)
- `.claude/settings.json` (config harness)
- `AGENTS.md` (regras invioláveis)
- `CLAUDE.md` (orquestrador)
- `squads/*/agentes/*/agente.md` (instructions dos agentes)
- `squads/*/agentes/*/mapa.md`
- `workspace/scripts/` (scripts utilitários)
- `workspace/integracoes/*.md` (docs históricas de integrações)
- `.gitignore`, `.gitleaks.toml`, `.pre-commit-config.yaml`, `.secrets.baseline`

### Persona (PRESERVAR — nunca toca)
- `IDENTIDADE.md` (operador, empresas, funil — único arquivo com dados pessoais)
- `MEMORY.md` (memória pessoal)
- `segundo-cerebro/` (knowledge atemporal do aluno)
- `workspace/memory/` (work state local)
- `workspace/output/` (artefatos do aluno)
- `squads/*/aprendizados.md` (aprendizados acumulados)
- `squads/*/tarefas.md` (fila local)
- `squads/*/agentes/*/aprendizados.md`
- `app/.env.local` (secrets)

## Pré-flight (sempre)

```bash
# 1. CWD correto
[[ -f CLAUDE.md && -f AGENTS.md && -f IDENTIDADE.md ]] || { echo "❌ Não está na raiz do squad"; exit 1; }

# 2. Git status limpo
if [[ -n "$(git status --short)" ]]; then
  echo "❌ Há mudanças não-commitadas. Commit ou stash antes de atualizar."
  git status --short
  exit 1
fi

# 3. Branch main (não rodar em branch de feature)
[[ "$(git branch --show-current)" == "main" ]] || {
  echo "⚠️  Você está em '$(git branch --show-current)'. Mudar pra main? (s/n)"
  read -r r; [[ "$r" == "s" ]] && git checkout main || exit 1
}

# 4. Backup automático
ts=$(date +%Y%m%d-%H%M%S)
git tag "pre-atualizar-jade-$ts" -m "Backup antes de /atualizar-jade em $ts"
echo "✅ Backup tag: pre-atualizar-jade-$ts (rollback: git reset --hard pre-atualizar-jade-$ts)"
```

## Fluxo

```
[ pre-flight ] → [ fetch upstream ] → [ diff + changelog ]
                                              │
                                              ▼
                  [ aluno aprova mudanças ]
                                              │
                                              ▼
                  [ aplica patches em framework (whitelist) ]
                                              │
                                              ▼
                  [ valida persona files intocada (blacklist) ]
                                              │
                                              ▼
                  [ smoke tests (hooks + JSON valid + skill list) ]
                                              │
                                              ▼
                  [ commit "chore: /atualizar-jade vX.Y" ]
```

## Implementação

### 1. Configurar upstream remote (1ª vez)

```bash
git remote get-url upstream 2>/dev/null || \
  git remote add upstream https://github.com/{{github_user}}/squad-template.git

git fetch upstream main
```

### 2. Gerar changelog do que vai mudar

```bash
echo "=== Mudanças disponíveis ==="
git log HEAD..upstream/main --oneline | head -20
echo ""
echo "=== Arquivos framework que vão ser atualizados ==="
git diff --name-only HEAD upstream/main -- \
  '.claude/commands/*.md' \
  '.claude/agents/*.md' \
  '.claude/hooks/*.sh' \
  '.claude/settings.json' \
  AGENTS.md \
  CLAUDE.md \
  'squads/*/agentes/*/agente.md' \
  'workspace/scripts/' \
  '.gitignore' \
  '.gitleaks.toml' \
  '.pre-commit-config.yaml'
echo ""
echo "=== Persona preservada (NÃO toca) ==="
echo "  IDENTIDADE.md, MEMORY.md, segundo-cerebro/, workspace/memory/,"
echo "  workspace/output/, squads/*/aprendizados.md, app/.env.local"
echo ""
echo "Confirmar atualização? (s/n)"
read -r r; [[ "$r" == "s" ]] || exit 0
```

### 3. Aplicar updates (cherry-pick por whitelist)

```bash
# Checkout framework files do upstream (sobrescreve local com upstream)
WHITELIST=(
  '.claude/commands/'
  '.claude/agents/'
  '.claude/hooks/'
  '.claude/settings.json'
  'AGENTS.md'
  'CLAUDE.md'
  'squads/*/agentes/*/agente.md'
  'squads/*/agentes/*/mapa.md'
  'workspace/scripts/'
  'workspace/integracoes/'
  '.gitignore'
  '.gitleaks.toml'
  '.pre-commit-config.yaml'
  '.secrets.baseline'
)

for path in "${WHITELIST[@]}"; do
  git checkout upstream/main -- "$path" 2>/dev/null || true
done
```

### 4. Validação pós-update

```bash
# Persona files intocada?
PERSONA=(
  'IDENTIDADE.md'
  'MEMORY.md'
  'segundo-cerebro/'
  'workspace/memory/'
  'workspace/output/'
  'squads/*/aprendizados.md'
  'squads/*/tarefas.md'
)

for f in "${PERSONA[@]}"; do
  if git diff --quiet HEAD -- "$f" 2>/dev/null; then
    echo "  ✅ $f preservada"
  else
    echo "  ⚠️  $f modificada (não deveria) — verificar"
  fi
done

# Smoke tests críticos
echo ""
echo "=== Smoke tests ==="
python3 -c "import json; json.load(open('.claude/settings.json'))" && echo "  ✅ settings.json válido"
for h in .claude/hooks/check-*.sh; do
  bash -n "$h" 2>&1 >/dev/null && echo "  ✅ $(basename $h) sintaxe OK"
done
```

### 5. Commit

```bash
UPSTREAM_SHA=$(git rev-parse --short upstream/main)
git add -A
git commit -m "$(cat <<EOF
chore(jade): /atualizar-jade — sync upstream {{github_user}}/squad-template@$UPSTREAM_SHA

Framework atualizado. Persona preservada.

Mudanças resumo: $(git diff --name-only HEAD~1 HEAD | wc -l) arquivos

Rollback: git reset --hard pre-atualizar-jade-$ts
EOF
)"

echo ""
echo "✅ Jade atualizada. Rollback disponível em tag: pre-atualizar-jade-$ts"
echo ""
echo "Próximo:"
echo "  - Teste 1 skill que você usa muito (ex: /listar-pendencias)"
echo "  - Se algo quebrou: git reset --hard pre-atualizar-jade-$ts"
```

## Restrições

- **Backup automático** sempre (tag git antes)
- **Pre-flight obrigatório** (git status limpo + branch main)
- **Whitelist explícita** — só framework files. Persona NUNCA é tocada.
- **Aprovação aluno** antes de aplicar (mostra changelog)
- **Validação pós** — settings.json + hooks + persona preservada
- **Rollback 1 comando** — `git reset --hard pre-atualizar-jade-TIMESTAMP`
- **Sem força** — sem `--force`, `--no-verify`, ou bypass de gitleaks
- **Não rodar em branch feature** — só main

## Sinais de problema

| Sintoma | Causa provável | Solução |
|---|---|---|
| "Há mudanças não-commitadas" | Aluno tem trabalho em andamento | Commitar ou stash antes |
| "Persona modificada" warning | Upstream tentou tocar persona (bug do template) | Revert do arquivo + report {{OPERADOR}} |
| Hook quebrou (sintaxe) | Atualização introduziu bug | Rollback: `git reset --hard pre-atualizar-jade-TIMESTAMP` |
| Skill não funciona | Path antigo hardcoded | Update do squad parou no meio — rollback + reportar |

## Histórico

- 2026-05-18 — Skill criada. Two-track architecture: framework atualiza, persona preserva.
