#!/bin/bash
# Hook PreToolUse — Bloqueia push direto pro repo público {{GITHUB_USER}}/jade
# Regra §18 (Território público — só via /publicar-jade)

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)
[[ "$TOOL_NAME" != "Bash" ]] && exit 0

CMD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Bypass autorizado
[[ "$JADE_CONTEXT" == "publicar-jade" ]] && exit 0
[[ "$PUBLICAR_JADE_VALIDADO" == "true" ]] && exit 0

# Detecção em 2 passos pra capturar ambas ordens de gh api
TARGET_REPO=""
if echo "$CMD" | grep -qE '{{GITHUB_USER}}/(jade|squad-template)'; then
  TARGET_REPO=1
fi

if [[ -z "$TARGET_REPO" ]]; then
  exit 0
fi

# Verificar se é operação de escrita
BLOCK=0
REASON=""

# git push pra remote do repo
if echo "$CMD" | grep -qE 'git\s+push'; then
  BLOCK=1; REASON="git push pra {{GITHUB_USER}}/jade"
fi

# gh api -X (PUT|POST|PATCH|DELETE)
if echo "$CMD" | grep -qE 'gh\s+api.*-X\s+(PUT|POST|PATCH|DELETE)|gh\s+api\s+-X\s+(PUT|POST|PATCH|DELETE)'; then
  BLOCK=1; REASON="gh api write em {{GITHUB_USER}}/jade (PUT/POST/PATCH/DELETE)"
fi

# gh repo edit/rename/delete
if echo "$CMD" | grep -qE 'gh\s+repo\s+(edit|rename|delete|archive|transfer)'; then
  BLOCK=1; REASON="gh repo destructive em {{GITHUB_USER}}/jade"
fi

if [ "$BLOCK" = "1" ]; then
  cat <<EOF
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "BLOQUEADO Regra §18: $REASON detectada. Push/edit direto pro repo público NÃO autorizado. Use a skill /publicar-jade que faz sanitização + 5 validações bloqueantes ANTES. Se rodando a skill, exporte JADE_CONTEXT=publicar-jade. Comando: $CMD"}}
EOF
  exit 2
fi

exit 0
