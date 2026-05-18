#!/usr/bin/env bash
# check-baseline-hash-claude.sh
# Hook PreToolUse leve — Item 0.2 Fase 0 Hardening (Regra §16, vetor R1)
# Comportamento:
#   - NUNCA bloqueia (exit 0 sempre, exceto warning em stderr)
#   - Dispara verificação em background se status vazio ou >1h
#   - Mostra warning se última verificação acusou divergência
#
set -uo pipefail

PROJECT_ROOT="$CLAUDE_PROJECT_DIR
SCRIPT="$PROJECT_ROOT/workspace/scripts/seguranca/baseline-hash-claude.sh"
LAST_STATUS="$PROJECT_ROOT/workspace/output/seguranca/last-check-status.txt"
LOG_FILE="$PROJECT_ROOT/workspace/output/seguranca/hash-check.log"

[[ ! -x "$SCRIPT" ]] && exit 0

NEEDS_RUN=0
if [[ ! -s "$LAST_STATUS" ]]; then
  NEEDS_RUN=1
else
  # mtime do arquivo de status — se >3600s atrás, roda de novo
  STAT_EPOCH=$(stat -f '%m' "$LAST_STATUS" 2>/dev/null || echo 0)
  NOW=$(date +%s)
  AGE=$((NOW - STAT_EPOCH))
  [[ $AGE -gt 3600 ]] && NEEDS_RUN=1
fi

if [[ $NEEDS_RUN -eq 1 ]]; then
  # dispara em background, redireciona output, desanexa
  nohup "$SCRIPT" check >>"$LOG_FILE" 2>&1 &
  disown 2>/dev/null || true
fi

# Se última verificação acusou divergência, warning em stderr (não bloqueia)
if [[ -f "$LAST_STATUS" ]]; then
  STATUS=$(cat "$LAST_STATUS" 2>/dev/null | tr -d '[:space:]')
  if [[ "$STATUS" == "1" ]]; then
    echo "" >&2
    echo "⚠️  WARNING SEGURANÇA — baseline hash Claude divergente (Regra §16, vetor R1)" >&2
    echo "   última verificação acusou modificação em arquivo crítico (~/.claude.json, hooks, settings)." >&2
    echo "   rode: $SCRIPT check  pra ver detalhes." >&2
    echo "   se alteração foi legítima: $SCRIPT init  pra refrescar baseline." >&2
    echo "" >&2
  fi
fi

exit 0
