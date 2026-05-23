#!/usr/bin/env bash
# check-mcp-clickup-deprecated.sh
# Hook PreToolUse — bloqueia qualquer chamada a tools mcp__claude_ai_ClickUp__*
# MCP descontinuado em 2026-05-14 pra uso em skills canônicas.
# Substitutos: skills REST via curl. Ver segundo-cerebro/03-operacao/clickup-historico.md

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
  mcp__claude_ai_ClickUp__*)
    cat >&2 <<MSG
[BLOCK] MCP do ClickUp descontinuado em 2026-05-14 pra uso em skills canônicas.

Tool bloqueada: ${tool_name}

Use as skills REST (curl direto em api.clickup.com):
  - /criar-pendencia       — cria task na lista Tasks Jade COO (901327194775)
  - /listar-pendencias     — lista tasks da lista Tasks Jade COO
  - /comentar-pendencia    — adiciona comentário em task Jade COO
  - /fechar-pendencia      — encerra task Jade COO com sumário
  - /{{plataforma_conteudo}}-add-task      — cria task na lista Tasks App {{Plataforma_Conteudo}} (901327200673)
  - /{{plataforma_conteudo}}-tasks         — consulta lista Tasks App {{Plataforma_Conteudo}}
  - /clickup-task-done     — encerra task na lista {{Plataforma_Conteudo}} dev (901327190242)
  - /sincronizar-clickup   — sync estado entregas → ClickUp
  - /{{SKILL_SUPORTE}}       — skill de suporte

Setup: token em app/.env.local var CLICKUP_API_TOKEN (sem "Bearer" no header).
Ver: segundo-cerebro/03-operacao/clickup-historico.md
MSG
    exit 2
    ;;
esac

exit 0
