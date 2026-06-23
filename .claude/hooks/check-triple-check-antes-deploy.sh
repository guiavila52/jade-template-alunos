#!/usr/bin/env bash
# PreToolUse hook — Regra Inviolável #23 (10/05/2026)
# Detecta tentativa de Bash com `vercel --prod` ou `vercel deploy --prod`
# e printa lembrete pra confirmar que triple-check rodou.
# Não bloqueia — é backstop educativo.

set -uo pipefail

# M4 — Suprimir durante rotinas autônomas
case "${JADE_CONTEXT:-normal}" in
  rotina-autonoma|preparar-clear-jade|silencioso) exit 0 ;;
esac

INPUT=$(cat 2>/dev/null || true)
[ -z "$INPUT" ] && exit 0

TOOL_NAME=$(printf '%s' "$INPUT" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); print(d.get('tool_name',''))
except Exception:
    print('')" 2>/dev/null)

COMMAND=$(printf '%s' "$INPUT" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))
except Exception:
    print('')" 2>/dev/null)

[ "$TOOL_NAME" != "Bash" ] && exit 0

LC=$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]')

# Detecta vercel --prod ou variantes
DEPLOY=0
for pat in "vercel --prod" "vercel deploy --prod" "vercel --production" "vercel deploy --production"; do
  case "$LC" in
    *"$pat"*) DEPLOY=1; break ;;
  esac
done

[ "$DEPLOY" -eq 0 ] && exit 0

cat <<'JSONEOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "ALERTA REGRA INVIOLÁVEL #23 — vercel --prod detectado. ANTES de prosseguir, confirme: (1) paginas (revisor copy) APROVOU? (2) paginas-dev (revisor código) APROVOU? (3) bug-hunter (Playwright funcional) APROVOU? Se qualquer ❌: corrige + re-roda os 3. NUNCA deploy sem triple-check completo. Ver memória feedback_triple_check_obrigatorio.md."
  }
}
JSONEOF