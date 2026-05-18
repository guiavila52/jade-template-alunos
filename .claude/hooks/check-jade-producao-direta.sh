#!/bin/bash
# Hook: check-jade-producao-direta.sh
# Trigger: PreToolUse (Write|Edit|Bash)
# Bloqueia Jade de produzir conteúdo direto em zonas de produção acima de thresholds.
# Regra Inviolável §2 (AGENTS.md): "Jade orquestra, nunca produz."
# Bypass legítimo:
#   - JADE_CONTEXT='rotina-autonoma'         (rotinas BG fora de horário)
#   - JADE_CONTEXT='despachado-pelo-agent'   (chamada vinda de subagent, não da Jade direta)
#
# Input: JSON via stdin com tool_name e tool_input.

set -e
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")

# Bypass legítimo
case "$JADE_CONTEXT" in
  rotina-autonoma|despachado-pelo-agent|skill-aprovada-pelo-gui=true)
    exit 0
    ;;
esac

# Zonas de produção (paths críticos)
PROD_PATTERNS="workspace/output/|public/|src/pages/|/Downloads/|scripts/"

case "$TOOL_NAME" in
  Write)
    FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")
    CONTENT=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('content',''))" 2>/dev/null || echo "")
    SIZE=${#CONTENT}
    if echo "$FILE_PATH" | grep -qE "$PROD_PATTERNS" && [ "$SIZE" -gt 2048 ]; then
      cat <<MSG >&2
ALERTA REGRA INVIOLÁVEL §2 — Jade orquestra, nunca produz.

Write detectado em zona de produção ($FILE_PATH) com $SIZE bytes (>2KB).

Antes de produzir, despache um Agent com briefing completo. Bypass legítimo:
  - JADE_CONTEXT='rotina-autonoma'
  - JADE_CONTEXT='despachado-pelo-agent'

Ver AGENTS.md §2 + memória feedback_jade_comportamento.md.
MSG
      exit 2
    fi
    ;;
  Edit)
    FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")
    NEW_STR=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('new_string',''))" 2>/dev/null || echo "")
    SIZE=${#NEW_STR}
    if echo "$FILE_PATH" | grep -qE "$PROD_PATTERNS" && [ "$SIZE" -gt 500 ]; then
      cat <<MSG >&2
ALERTA REGRA INVIOLÁVEL §2 — Jade orquestra, nunca produz.

Edit detectado em zona de produção ($FILE_PATH) com new_string de $SIZE chars (>500).

Bypass legítimo: JADE_CONTEXT='rotina-autonoma' ou 'despachado-pelo-agent'.
MSG
      exit 2
    fi
    ;;
  Bash)
    COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")
    if echo "$COMMAND" | grep -qE "(python3?|node) <<|cat >.*\.(py|js|ts|astro)"; then
      LINES=$(echo "$COMMAND" | wc -l | tr -d ' ')
      if [ "$LINES" -gt 30 ]; then
        cat <<MSG >&2
ALERTA REGRA INVIOLÁVEL §2 — Jade orquestra, nunca produz.

Bash heredoc Python/Node detectado com $LINES linhas (>30).

Despache subagent pra produção complexa. Bypass: JADE_CONTEXT='rotina-autonoma' ou 'despachado-pelo-agent'.
MSG
        exit 2
      fi
    fi
    ;;
esac

exit 0
