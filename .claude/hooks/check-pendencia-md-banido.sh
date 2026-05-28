#!/bin/bash
# Hook PreToolUse — BLOQUEIA criação/escrita em qualquer pendencias.md
# Regra: arquivo descontinuado em 2026-05-14. Pendências SÓ no ClickUp via /criar-pendencia.
# Ver AGENTS.md §1 + MEMORY.md feedback_pendencias_clickup_unico.md.

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)

# Detecta file_path em Write/Edit/NotebookEdit
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Detecta comando em Bash (BASH_COMMAND é reservado do bash, usar CMD)
CMD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

BLOCK=0
REASON=""

# Caso 1: Write/Edit/NotebookEdit em pendencias.md
if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "NotebookEdit" ]]; then
  case "$FILE_PATH" in
    *pendencias.md)
      BLOCK=1
      REASON="$TOOL_NAME em arquivo pendencias.md ($FILE_PATH)"
      ;;
  esac
fi

# Caso 2: Bash tentando criar/escrever pendencias.md
if [[ "$TOOL_NAME" == "Bash" ]]; then
  # Padrões a bloquear:
  #   redirect      :  > pendencias.md  ou  >> pendencias.md
  #   tee           :  tee ... pendencias.md
  #   touch         :  touch ... pendencias.md
  #   cp/mv destino :  cp/mv ... pendencias.md
  # Detecta qualquer string que termine em "pendencias.md" combinada com operador de escrita.
  if echo "$CMD" | grep -qE '>[[:space:]]*[^|&;]*pendencias\.md|>>[[:space:]]*[^|&;]*pendencias\.md|tee[[:space:]]+[^|]*pendencias\.md|touch[[:space:]]+[^|&;]*pendencias\.md|cp[[:space:]]+[^|]+pendencias\.md|mv[[:space:]]+[^|]+pendencias\.md'; then
    BLOCK=1
    REASON="Bash tentando criar/escrever pendencias.md"
  fi
fi

if [[ "$BLOCK" -eq 1 ]]; then
  echo "❌ BLOQUEADO — Arquivo pendencias.md foi descontinuado em 2026-05-14."
  echo ""
  echo "Motivo detectado: $REASON"
  echo ""
  echo "Pendências SÓ no ClickUp via skill canônica:"
  echo "  - /criar-pendencia    — nova"
  echo "  - /listar-pendencias  — ver fila"
  echo "  - /comentar-pendencia — progresso"
  echo "  - /fechar-pendencia   — encerrar"
  echo ""
  echo "Lista canônica: {{CLICKUP_LIST_ID}} (Tasks Jade COO)"
  echo "URL: https://app.clickup.com/{{CLICKUP_WORKSPACE_ID}}/v/l/li/{{CLICKUP_LIST_ID}}"
  echo ""
  echo "Ver AGENTS.md §1 + MEMORY.md feedback_pendencias_clickup_unico.md."
  exit 2
fi

exit 0