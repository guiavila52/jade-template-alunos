#!/bin/bash
# Hook PreToolUse — BLOQUEIA Edit/Write em .claude/* (Regra Inviolável #8)
# Forçar uso de Bash heredoc/sed/python pra essas operações.
# Origem: reincidência 5+ vezes em 11/05/2026 — modal Antigravity ignora bypassPermissions.

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Verifica se tool é Edit/Write E file_path está em .claude/
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "NotebookEdit" ]]; then
  if [[ "$FILE_PATH" == *"/.claude/"* ]]; then
    echo "❌ BLOQUEADO — Regra Inviolável #8: NÃO usar $TOOL_NAME tool em .claude/*"
    echo ""
    echo "Path: $FILE_PATH"
    echo ""
    echo "Antigravity (VSCode extension) tem filtro hard-coded pra Edit/Write em .claude/ que ignora bypassPermissions."
    echo "Modal de permissão aparece toda vez = atrito infinito pro {{OPERADOR}}."
    echo ""
    echo "✅ USE Bash heredoc:"
    echo "   cat > '.claude/commands/skill.md' <<'EOF'"
    echo "   conteúdo aqui"
    echo "   EOF"
    echo ""
    echo "✅ Pra editar arquivo existente:"
    echo "   sed -i '' 's/antigo/novo/g' .claude/commands/skill.md"
    echo "   # OU python3 heredoc com replace"
    echo ""
    echo "✅ Pra rename:"
    echo "   git mv .claude/agents/antigo.md .claude/agents/novo.md"
    echo ""
    echo "Memória completa: feedback_bash_heredoc_em_claude_paths.md"
    exit 2
  fi
fi

exit 0
