#!/bin/bash
# Hook PreToolUse — Regra §16: Segurança first
# Alerta antes de instalar dependências (supply chain) ou modificar config MCP
# Contexto: AGENTS.md §16, Task ClickUp interna
#
# ESCOPO: package.json, requirements.txt, .mcp.json, ~/.claude.json
#         + comandos Bash com npm install, pip install, pip3 install, brew install
# NÃO cobre .claude/ paths — cobertos por check-edit-em-claude-paths.sh e check-bash-em-claude-paths.sh

set -e
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")
CMD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

# Bypass legítimos
BYPASS_TOKENS=("security-checklist-ok" "fase-0-hardening=true" "rotina-autonoma")
for tok in "${BYPASS_TOKENS[@]}"; do
  if [[ "${JADE_CONTEXT:-}" == *"$tok"* ]]; then
    exit 0
  fi
done

CRITICAL_ZONE=0
REASON=""

# Verifica paths críticos em Write/Edit
if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  case "$FILE_PATH" in
    */package.json)           CRITICAL_ZONE=1; REASON="package.json (supply chain — Regra §16 item 5)" ;;
    */requirements.txt)       CRITICAL_ZONE=1; REASON="requirements.txt (supply chain — Regra §16 item 5)" ;;
    */.mcp.json)              CRITICAL_ZONE=1; REASON=".mcp.json (MCP config — Regra §16 item 6)" ;;
    ~/.claude.json)           CRITICAL_ZONE=1; REASON="~/.claude.json (config global Claude — Regra §16 item 4)" ;;
    ~/.claude/mcp.json)       CRITICAL_ZONE=1; REASON="~/.claude/mcp.json (MCP config global — Regra §16 item 6)" ;;
  esac
fi

# Verifica comandos Bash com instalação de dependências
if [[ "$TOOL_NAME" == "Bash" ]]; then
  case "$CMD" in
    *"npm install"*|*"npm add"*|*"npm i "*|*"yarn add"*|*"pnpm add"*)
      CRITICAL_ZONE=1; REASON="instalação npm/yarn/pnpm (supply chain — Regra §16 item 5)" ;;
    *"pip install"*|*"pip3 install"*)
      CRITICAL_ZONE=1; REASON="instalação pip/pip3 (supply chain — Regra §16 item 5)" ;;
    *"brew install"*)
      CRITICAL_ZONE=1; REASON="instalação brew (supply chain — Regra §16 item 5)" ;;
  esac
fi

if [[ "$CRITICAL_ZONE" -eq 0 ]]; then
  exit 0
fi

cat >&2 <<MSG
⚠️  CHECKLIST DE SEGURANÇA (§16) — Ação em zona crítica detectada.

Zona: $REASON
Tool: $TOOL_NAME

Antes de prosseguir, confirme mentalmente os 7 itens (AGENTS.md §16):

1. Lethal trifecta: combina dados privados + untrusted content + comunicação externa?
2. Hook bypass: subagent pode furar PreToolUse do parent (issue #45427)?
3. Secret leak: arquivo/log pode vazar token ou key?
4. Self-modification: modifica .claude/settings.json ou hooks?
5. Supply chain: está instalando dependência nova? (auditada contra Shai-Hulud?)
6. MCP novo: está habilitando MCP server? (auditado via mcp-scan?)
7. Plugin novo: review hooks.json + skills antes de instalar?

BYPASS após confirmar checklist:
  export JADE_CONTEXT=security-checklist-ok
  (inclua no mesmo comando: JADE_CONTEXT=security-checklist-ok <seu-comando>)

Ver AGENTS.md §16 + Task ClickUp interna.
MSG
exit 2
