#!/usr/bin/env bash
# Regra Inviolável #37 — Toda produção via skill canônica
# Bloqueia Write/Edit em paths de output + PATCH em APIs de conteúdo
# se nenhuma skill canônica foi invocada na sessão.
#
# Bypass legítimo: JADE_CONTEXT=desenvolvendo-skill
#                  JADE_CONTEXT=rotina-autonoma (autoriza Jade fazer auditoria estrutural)

set -uo pipefail

INPUT=$(cat 2>/dev/null || true)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""' 2>/dev/null || echo "")
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")
BYPASS="${JADE_CONTEXT:-}"

# Bypass legítimo
[[ "$BYPASS" == "desenvolvendo-skill" ]] && exit 0
[[ "$BYPASS" == "rotina-autonoma" ]] && exit 0

# Paths protegidos (produção)
PROD_PATTERNS=(
  "workspace/output/newsletter/"
  "workspace/output/carrosseis/"
  "workspace/output/paginas/"
  "workspace/output/criativos/"
  "workspace/output/copy/"
  "workspace/output/videos-verticais/"
  "src/pages/"
)

# APIs de conteúdo (via curl PATCH)
API_PATTERNS=(
  "{{PLATAFORMA_API_URL}}/api/content/newsletters"
  "{{PLATAFORMA_API_URL}}/api/content/carrosseis"
  "{{PLATAFORMA_API_URL}}/api/content/ideias"
  "rest.gohighlevel.com"
  "services.leadconnectorhq.com"
)

is_protected_path() {
  local target="$1"
  for pat in "${PROD_PATTERNS[@]}"; do
    [[ "$target" == *"$pat"* ]] && return 0
  done
  return 1
}

is_protected_api_call() {
  local cmd="$1"
  for pat in "${API_PATTERNS[@]}"; do
    if echo "$cmd" | grep -qE "(PATCH|POST).*$pat"; then
      return 0
    fi
    if echo "$cmd" | grep -qE "$pat.*-X *(PATCH|POST)"; then
      return 0
    fi
  done
  return 1
}

# Detectar se invocação foi de produção
PRODUCTION_DETECTED=0

if [[ "$TOOL" =~ ^(Write|Edit|NotebookEdit)$ ]] && is_protected_path "$FILE_PATH"; then
  PRODUCTION_DETECTED=1
  CONTEXTO="$TOOL em $FILE_PATH"
elif [[ "$TOOL" == "Bash" ]] && is_protected_api_call "$COMMAND"; then
  PRODUCTION_DETECTED=1
  CONTEXTO="Bash com PATCH/POST em API de conteúdo"
fi

if [[ "$PRODUCTION_DETECTED" -eq 1 ]]; then
  # Verificar se skill canônica foi invocada na sessão (heurística simples:
  # arquivo de marker em /tmp/ é criado pela skill quando ela roda)
  MARKER="/tmp/claude-skill-invoked-$$.flag"
  SKILL_MARKERS_GLOB="/tmp/skill-invoked-*.flag"
  
  # Procurar markers recentes (< 5min)
  RECENT_MARKER=$(find /tmp -maxdepth 1 -name "skill-invoked-*.flag" -mmin -5 2>/dev/null | head -1)
  
  if [[ -z "$RECENT_MARKER" ]]; then
    echo "🚫 BLOQUEADO — Regra Inviolável #37: produção sem skill canônica detectada." >&2
    echo "" >&2
    echo "Operação: $CONTEXTO" >&2
    echo "" >&2
    echo "Nenhuma skill canônica foi invocada nos últimos 5 minutos." >&2
    echo "Toda produção/ação de competência de agente/squad PASSA por skill." >&2
    echo "" >&2
    echo "Como desbloquear:" >&2
    echo "  1. Invoque a skill canônica correspondente:" >&2
    echo "     - Newsletter → /escrever-newsletter + /renderizar-newsletter-html" >&2
    echo "     - Carrossel → /criar-carrossel" >&2
    echo "     - Página → /criar-pagina" >&2
    echo "     - Criativo → /criar-criativo" >&2
    echo "  2. Se não existe skill → criar primeiro em .claude/commands/ + script em scripts/" >&2
    echo "  3. Bypass legítimo (apenas se desenvolvendo skill nova):" >&2
    echo "     export JADE_CONTEXT=desenvolvendo-skill" >&2
    echo "" >&2
    echo "Source: AGENTS.md Regra Inviolável #37 + memória feedback_producao_via_skill_canonica_obrigatoria.md" >&2
    exit 2
  fi
fi

exit 0