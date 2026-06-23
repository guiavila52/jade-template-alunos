#!/usr/bin/env bash
# PreToolUse hook — Regra §1 (implementado 09/06/2026)
# BLOQUEANTE: exige task ClickUp ativa (/tmp/jade-tarefa-ativa.txt) antes de
# qualquer Write, Edit ou Bash substantivo.
#
# Arquivo de controle: /tmp/jade-tarefa-ativa.txt
# - Criado por: /criar-pendencia (ao criar task)
# - Limpo por:  /fechar-pendencia (ao concluir task)
#
# Bypasses legítimos:
# - JADE_CONTEXT=rotina-autonoma
# - JADE_CONTEXT=skill-aprovada=*
# - JADE_CONTEXT=operador-autorizou-push-template
# - Bash com chamada a api.clickup.com (criação de task)
# - Operações read-only (grep, ls, cat, find, git status/log/diff/show)
# - Escrita em /tmp/ ou workspace/output/ ou workspace/memory/

set -uo pipefail

TAREFA_FILE="/tmp/jade-tarefa-ativa.txt"

# Bypass via env var
case "${JADE_CONTEXT:-normal}" in
  rotina-autonoma|preparar-clear-jade|silencioso|operador-autorizou-push-template) exit 0 ;;
  skill-aprovada=*) exit 0 ;;
esac

INPUT=$(cat 2>/dev/null || true)
[ -z "$INPUT" ] && exit 0

TOOL_NAME=$(printf '%s' "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_name',''))
except: print('')
" 2>/dev/null)

# Só age em Write, Edit, Bash
case "$TOOL_NAME" in
  Write|Edit|Bash) ;;
  *) exit 0 ;;
esac

FILE_PATH=$(printf '%s' "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))
except: print('')
" 2>/dev/null)

COMMAND=$(printf '%s' "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_input',{}).get('command',''))
except: print('')
" 2>/dev/null)

# ─── WRITE / EDIT: verificar path ───────────────────────────────────────────
if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
  # Exempt: /tmp/, workspace/output/, workspace/memory/, app/.env, /tmp/jade-*
  case "$FILE_PATH" in
    /tmp/*|*/workspace/output/*|*/workspace/memory/*|*/app/.env*|*.env.local) exit 0 ;;
  esac
  # Bloquear se não há task ativa
  if [ ! -f "$TAREFA_FILE" ] || [ ! -s "$TAREFA_FILE" ]; then
    TASK_INFO=$(cat "$TAREFA_FILE" 2>/dev/null || echo "(nenhuma)")
    cat >&2 <<ERREOF
BLOQUEIO FATAL (Regra §1) — nenhuma task ClickUp ativa.

Você está tentando escrever em: $FILE_PATH

ANTES de executar qualquer trabalho:
1. Crie a task no ClickUp via /criar-pendencia
2. A task fica registrada em /tmp/jade-tarefa-ativa.txt
3. Ao concluir, use /fechar-pendencia para marcar como done

Task ativa atual: $TASK_INFO

Bypass legítimo: JADE_CONTEXT=rotina-autonoma (apenas para rotinas conhecidas)
ERREOF
    exit 2
  fi
fi

# ─── BASH: verificar se é substantivo ───────────────────────────────────────
if [ "$TOOL_NAME" = "Bash" ]; then
  CMD_LC=$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]')

  # Sempre permitir: chamadas ClickUp (criar task), git reads, exploração
  case "$CMD_LC" in
    *api.clickup.com*) exit 0 ;;
    *"git status"*|*"git log"*|*"git diff"*|*"git show"*|*"git branch"*|*"git remote"*) exit 0 ;;
    *"grep "*|*"ls "*|*"ls\n"*|"ls"|*"cat "*|*"find "*|*"head "*|*"tail "*|*"wc "*) exit 0 ;;
    *"echo "*|"echo"|*"pwd"*|*"which "*|*"whoami"*|*"date"*) exit 0 ;;
    *"source app/.env"*|*"set -a"*) exit 0 ;;
    */tmp/venv*|*"python3 -m venv"*|*"pip install"*|*"pip3 install"*) exit 0 ;;
    *"python3 -c"*) exit 0 ;;
    *"wc -l"*|*"sed -n"*) exit 0 ;;
  esac

  # Comandos substantivos: chamadas a APIs externas, scripts, curl não-ClickUp, etc.
  SUBSTANTIVO=0
  for pat in \
    "curl " \
    "python3 " \
    "/tmp/venv/bin/python" \
    "vercel" \
    "npm " \
    "git commit" \
    "git push" \
    "git add" \
    "git mv" \
    "git rm" \
    "brew " \
    "nohup" \
    "bash " \
    "sh "; do
    case "$CMD_LC" in
      *"$pat"*) SUBSTANTIVO=1; break ;;
    esac
  done

  [ "$SUBSTANTIVO" -eq 0 ] && exit 0

  # É substantivo — verificar task ativa
  if [ ! -f "$TAREFA_FILE" ] || [ ! -s "$TAREFA_FILE" ]; then
    TASK_INFO=$(cat "$TAREFA_FILE" 2>/dev/null || echo "(nenhuma)")
    cat >&2 <<ERREOF
BLOQUEIO FATAL (Regra §1) — nenhuma task ClickUp ativa.

Você está tentando executar um comando substantivo sem task registrada.

ANTES de executar:
1. Crie a task via /criar-pendencia — descreva o que vai fazer e por quê
2. A task ID fica salva em /tmp/jade-tarefa-ativa.txt automaticamente
3. Ao concluir, use /fechar-pendencia

Task ativa atual: $TASK_INFO

Bypass: JADE_CONTEXT=rotina-autonoma
ERREOF
    exit 2
  fi
fi

exit 0
