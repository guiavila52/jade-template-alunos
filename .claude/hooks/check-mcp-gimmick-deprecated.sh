#!/usr/bin/env bash
# check-mcp-plataforma-deprecated.sh
# Hook PreToolUse — bloqueia qualquer chamada a tools mcp__{{plataforma_email}}__* (MCP descontinuado 12/05/2026).
# Substituto canônico: API REST da {{PLATAFORMA_EMAIL}}.
# Ver: segundo-cerebro/03-operacao/plataforma-historico.md

set -euo pipefail

# Lê o payload JSON do stdin (formato PreToolUse do Claude Code).
payload="$(cat 2>/dev/null || true)"

# Extrai o tool_name. jq se disponível; fallback grep.
if command -v jq >/dev/null 2>&1; then
  tool_name="$(printf '%s' "$payload" | jq -r '.tool_name // empty' 2>/dev/null || true)"
else
  tool_name="$(printf '%s' "$payload" | grep -oE '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*"tool_name"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"
fi

case "${tool_name:-}" in
  mcp__{{plataforma_email}}__*)
    cat >&2 <<MSG
[BLOCK] MCP da {{PLATAFORMA_EMAIL}} descontinuado em 12/05/2026 — tools mcp__{{plataforma_email}}__* retornam HTTP 401 e foram desativadas.

Tool bloqueada: ${tool_name}

Substituto canônico: API REST da {{PLATAFORMA_EMAIL}}.
  - Auth: Authorization: Bearer \${{{PLATAFORMA_NEWSLETTER_API_KEY}}}  ({{CHAVE_API_EXEMPLO}})
  - Base: https://{{PLATAFORMA_API_URL}}/api/content
  - Endpoints + exemplos curl: segundo-cerebro/03-operacao/plataforma-historico.md

Use Bash + curl (ou wrapper) em vez de chamar mcp__{{plataforma_email}}__*.
MSG
    exit 2
    ;;
esac

exit 0