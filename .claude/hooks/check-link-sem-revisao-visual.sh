#!/usr/bin/env bash
# Regra §4 — Revisão visual real obrigatória
# Bloqueia Jade de enviar URL (localhost:, vercel.app, {{DOMINIO}}) pro operador
# sem arquivo REVISAO-APROVADO recente (≤30min) em workspace/output/screenshots-revisao/
#
# Triggered: PreToolUse Bash — detecta echo/printf com padrão URL em comando

set -uo pipefail

INPUT=$(cat 2>/dev/null || true)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")
BYPASS="${JADE_CONTEXT:-}"

# Bypasses legítimos
[[ "$BYPASS" == "rotina-autonoma" ]] && exit 0
[[ "$BYPASS" == "desenvolvendo-revisor" ]] && exit 0
[[ "$BYPASS" == "operador-autorizou-url-sem-revisor" ]] && exit 0

# Só age em Bash
[[ "$TOOL" != "Bash" ]] && exit 0

# Detecta se o comando vai outputar URL de dev/staging pro operador
URL_PATTERN='localhost:[0-9]|vercel\.app|sites\.{{DOMINIO}}'
OUTPUT_CMD_PATTERN='echo|printf|cat'

HAS_URL=0
HAS_OUTPUT=0

echo "$COMMAND" | grep -qE "$URL_PATTERN" && HAS_URL=1
echo "$COMMAND" | grep -qE "$OUTPUT_CMD_PATTERN" && HAS_OUTPUT=1

# Também bloqueia se for vercel --prod sem revisão (complementa check-revisao-visual-antes-publicar.sh)
echo "$COMMAND" | grep -qE 'vercel.*--prod' && HAS_URL=1 && HAS_OUTPUT=1

if [[ "$HAS_URL" -eq 1 ]] && [[ "$HAS_OUTPUT" -eq 1 ]]; then
  PROJ="${CLAUDE_PROJECT_DIR:-${BASE:-$CLAUDE_PROJECT_DIR}}"
  RECENT=$(find "$PROJ/workspace/output/screenshots-revisao" -type f -name "*REVISAO-APROVADO*" -mmin -30 2>/dev/null | head -1)

  if [[ -z "$RECENT" ]]; then
    echo "BLOQUEADO — §4: URL sem REVISAO-APROVADO recente." >&2
    echo "" >&2
    echo "Jade estava prestes a enviar URL pro operador sem revisão visual do designer-revisor." >&2
    echo "" >&2
    echo "Nenhum REVISAO-APROVADO nos últimos 30min em workspace/output/screenshots-revisao/" >&2
    echo "" >&2
    echo "Fluxo correto:" >&2
    echo "  1. Screenshot headless (Playwright headless:true) — desktop 1280px + mobile 390px" >&2
    echo "  2. Despachar agent designer-revisor para inspeção visual completa" >&2
    echo "  3. Aguardar REVISAO-APROVADO explícito" >&2
    echo "  4. Só então enviar URL pro operador" >&2
    echo "" >&2
    echo "Incidente origem: 17/05/2026 — página com 5 bugs enviada sem revisão." >&2
    echo "" >&2
    echo "Bypass (emergência real): export JADE_CONTEXT=operador-autorizou-url-sem-revisor" >&2
    exit 2
  fi
fi

exit 0
