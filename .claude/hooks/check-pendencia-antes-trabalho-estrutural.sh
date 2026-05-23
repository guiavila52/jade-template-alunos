#!/usr/bin/env bash
# PreToolUse hook — Regra §1 (reforço 16/05/2026, Task {{CLICKUP_TASK_ID}})
# BLOQUEANTE: detecta trabalho estrutural (.claude/commands/, squads/, AGENTS.md, etc)
# sem pendência ClickUp registrada e BLOQUEIA com exit 2.
#
# Bypass legítimos (exit 0):
# - JADE_CONTEXT=rotina-autonoma (rotinas Jade conhecidas, ex: /preparar-clear-jade)
# - JADE_CONTEXT=skill-aprovada=* (criação de skill com aval do Gui, Regra §13)
# - Subagent com briefing Jade contendo Task ClickUp ID (detectado via stdin)
# - Arquivos de work state (tarefas.md, aprendizados.md, memory.md)

set -uo pipefail

# Bypass via env var (rotina autônoma ou skill aprovada)
case "${JADE_CONTEXT:-normal}" in
  rotina-autonoma|preparar-clear-jade|silencioso) exit 0 ;;
  skill-aprovada=*) exit 0 ;;
esac

INPUT=$(cat 2>/dev/null || true)
[ -z "$INPUT" ] && exit 0

# Extrair tool_name, file_path, command
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

COMMAND=$(printf '%s' "$INPUT" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))
except Exception:
    print('')" 2>/dev/null)

# Só Write|Edit|Bash
case "$TOOL_NAME" in
  Write|Edit|Bash) ;;
  *) exit 0 ;;
esac

# BLOQUEIO ESPECIAL pendencias.md: só se FILE_PATH contém (não COMMAND genérico)
# Motivo: evitar falso positivo quando "pendencias.md" aparece em string de comentário
if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
  case "$FILE_PATH" in
    *pendencias.md*)
      cat >&2 <<'ERREOF'
BLOQUEIO FATAL (Regra §1) — pendencias.md descontinuado desde 2026-05-14.

Pendências SÓ via ClickUp list 901327194775 usando skills canônicas:
- /criar-pendencia
- /listar-pendencias
- /comentar-pendencia
- /fechar-pendencia

Sem fallback pra arquivo MD. Hook bloqueante check-pendencia-md-banido.sh ativo.

Ver memória: feedback_pendencias_clickup_unico.md
ERREOF
      exit 2
      ;;
  esac
fi

# Bash heredoc criando pendencias.md: detectar padrão "> pendencias.md" ou ">> pendencias.md"
if [ "$TOOL_NAME" = "Bash" ]; then
  LC_CMD=$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]')
  case "$LC_CMD" in
    *\>*pendencias.md*|*\>\>*pendencias.md*|*cat*pendencias.md*)
      cat >&2 <<'ERREOF'
BLOQUEIO FATAL (Regra §1) — pendencias.md descontinuado desde 2026-05-14.

Pendências SÓ via ClickUp list 901327194775 usando skills canônicas.

Ver memória: feedback_pendencias_clickup_unico.md
ERREOF
      exit 2
      ;;
  esac
fi

# Path/comando contém sinais de trabalho estrutural?
TARGET="${FILE_PATH}${COMMAND}"
LC=$(printf '%s' "$TARGET" | tr '[:upper:]' '[:lower:]')

# Paths estruturais que disparam o bloqueio
STRUCTURAL=0
for pat in ".claude/commands/" ".claude/agents/" ".claude/hooks/" "squads/" "/agents.md" "/claude.md" "/memory.md" "/agents_md" "regra inviolável" "regra inviolavel"; do
  case "$LC" in
    *"$pat"*) STRUCTURAL=1; break ;;
  esac
done

# Comandos git/mv/cp/rm em paths estruturais
if [ "$TOOL_NAME" = "Bash" ]; then
  for git_pat in "git mv" "git rm" "mv .claude" "cp .claude" "rm .claude" "mv squads" "cp squads" "rm squads"; do
    case "$LC" in
      *"$git_pat"*) STRUCTURAL=1; break ;;
    esac
  done
fi

# Exceções: work state (são justamente o que Jade DEVE atualizar)
case "$LC" in
  *tarefas.md*|*aprendizados.md*|*memory.md*|*progress.md*) exit 0 ;;
esac

[ "$STRUCTURAL" -eq 0 ] && exit 0

# Bypass legítimo: detectar briefing Jade com Task ClickUp ID no stdin
# Heurística: presença de "Task ClickUp: 86ah" ou "**Task ClickUp:** 86ah" no INPUT
if printf '%s' "$INPUT" | grep -qiE 'task clickup.*86ah[a-z0-9]+'; then
  exit 0
fi

# Se chegou aqui: trabalho estrutural sem pendência detectada → BLOQUEIA
cat >&2 <<'ERREOF'
BLOQUEIO FATAL (Regra §1) — trabalho estrutural sem pendência ClickUp registrada.

Detectado: trabalho em .claude/commands/, .claude/agents/, .claude/hooks/, squads/, 
AGENTS.md, CLAUDE.md ou paths estruturais.

ANTES de prosseguir:
1. Registre pendência no ClickUp list 901327194775 via /criar-pendencia
2. Execute o trabalho com referência explícita à Task ID no briefing
3. Ou use bypass legítimo: JADE_CONTEXT=rotina-autonoma (se aplicável)

Bypass legítimos:
- JADE_CONTEXT=rotina-autonoma (rotinas Jade conhecidas)
- JADE_CONTEXT=skill-aprovada={id} (skill nova com aval Gui, Regra §13)
- Briefing de subagent contendo "Task ClickUp: 86ah..." (detectado via stdin)

Ver memória: feedback_registrar_pendencia_antes_de_executar.md
ERREOF
exit 2
