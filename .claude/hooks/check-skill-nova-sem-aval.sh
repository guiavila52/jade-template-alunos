#!/bin/bash
# Hook: check-skill-nova-sem-aval.sh
# Trigger: PreToolUse (Write em .claude/commands/*.md)
# Bloqueia criação de skill nova sem aval explícito do {{NOME_OPERADOR_CURTO}}.
# Regra Inviolável §13 (AGENTS.md): "Skill nova exige aval explícito do {{NOME_OPERADOR_CURTO}} antes de criar."
# Bypass legítimo: export JADE_CONTEXT='skill-aprovada-pelo-gui=true' antes do Write.
#
# Input: JSON via stdin com tool_name e tool_input.file_path

set -e
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

case "$TOOL_NAME" in
  Write)
    case "$FILE_PATH" in
      */.claude/commands/*.md)
        if [ -f "$FILE_PATH" ]; then
          exit 0
        fi
        if [ "$JADE_CONTEXT" = "skill-aprovada-pelo-gui=true" ]; then
          exit 0
        fi
        cat <<MSG >&2
ALERTA REGRA INVIOLÁVEL §13 — Skill nova detectada sem aval explícito do {{NOME_OPERADOR_CURTO}}.

Arquivo: $FILE_PATH

Antes de criar skill nova, Jade DEVE propor pro {{NOME_OPERADOR_CURTO}} e aguardar OK explícito.
Bypass legítimo (após aval do {{NOME_OPERADOR_CURTO}}): export JADE_CONTEXT='skill-aprovada-pelo-gui=true'

Ver AGENTS.md §13 + memória feedback_skills.md.
MSG
        exit 2
        ;;
    esac
    ;;
esac

exit 0