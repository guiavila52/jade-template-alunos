#!/usr/bin/env bash
# PreToolUse hook — Regra Inviolável #21
# Detecta tentativa de Write/Edit em arquivo cujo path indica secret/key/token
# e que NÃO seja o padrão .env.local/.env.example. Imprime lembrete via
# additionalContext JSON pra Jade ver a memória antes do tool rodar.
# Não bloqueia (evita falso-positivo) — é backstop educativo.

set -uo pipefail

# M4 — Hook contextual: suprimir durante rotinas autônomas (Jade já sabe das regras)
# Setar JADE_CONTEXT=rotina-autonoma ou JADE_CONTEXT=preparar-clear-jade antes
# de iniciar a rotina pra economizar ruído de lembretes redundantes.
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

FILE_PATH=$(printf '%s' "$INPUT" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))
except Exception:
    print('')" 2>/dev/null)

case "$TOOL_NAME" in
  Write|Edit) ;;
  *) exit 0 ;;
esac

[ -z "$FILE_PATH" ] && exit 0

# Path padrão .env* libera (caminho oficial do squad)
BASE=$(basename "$FILE_PATH")
case "$BASE" in
  .env|.env.local|.env.example|.env.production|.env.development|.env.test|.env.staging) exit 0 ;;
esac

LC=$(printf '%s' "$FILE_PATH" | tr '[:upper:]' '[:lower:]')
SUSPECT=0
for pat in "/key" "/token" "/secret" "/credential" "api_key" "api-key" "apikey" "/password" ".env." "openrouter" "anthropic_key" "/keys/"; do
  case "$LC" in
    *$pat*) SUSPECT=1; break ;;
  esac
done

[ "$SUSPECT" -eq 0 ] && exit 0

cat <<'JSONEOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "ALERTA SECRET (Regra Inviolavel #21) — path suspeito detectado. ANTES de prosseguir: (1) rode `grep -rn \\"\.env\\" --include=\\".env*\\" .` pra listar .env* existentes; (2) leia `~/.claude/projects/{{PROJECT_PATH_HASH}}/memory/feedback_secrets_em_env_local.md` E `feedback_consultar_protocolo_antes_de_criar_secret.md`; (3) padrao do squad: secret SEMPRE em .env.local + dotenv. Se ja existe .env.local no projeto, USAR esse path — NUNCA inventar caminho novo. Se mesmo assim este path for o correto pra este caso, prossiga; senao, redirecione pro .env.local."
  }
}
JSONEOF