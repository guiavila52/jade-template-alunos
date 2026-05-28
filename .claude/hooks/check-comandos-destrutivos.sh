#!/bin/bash
# Hook PreToolUse — Destructive Command Guard (DCG)
# Bloqueia comandos destrutivos antes de executar.
# Regra §16 (segurança first) + §9 (proibido excluir) + §12 (proibido bypass)

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)

# Só intercepta Bash
[[ "$TOOL_NAME" != "Bash" ]] && exit 0

CMD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Bypass autorizado pra contextos legítimos
if [[ "$JADE_CONTEXT" == "rotina-autonoma" ]] || [[ "$DCG_BYPASS" == "true" ]]; then
  exit 0
fi

BLOCK=0
REASON=""

# Pattern 1: rm -rf em path crítico (/, /usr, /home, $HOME, raiz do projeto)
if echo "$CMD" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\s+(/|/usr|/etc|/var|/home|\$HOME|~/?\s|\.\s|\.$|\./?\s|\./?\$)' ; then
  BLOCK=1; REASON="rm -rf em path crítico (raiz, /usr, /home, ~, .)"
fi

# Pattern 2: rm -rf .git/ (mata histórico git)
if echo "$CMD" | grep -qE 'rm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+\.git/?' ; then
  BLOCK=1; REASON="rm -rf .git/ (destrói histórico git)"
fi

# Pattern 3: git push --force / -f em main/master
if echo "$CMD" | grep -qE 'git\s+push\s+(.*\s)?(-f|--force|--force-with-lease).*(main|master|production|prod)' ; then
  BLOCK=1; REASON="git push --force em main/master/prod (sobrescreve histórico público)"
fi

# Pattern 4: git reset --hard em commits pushados
if echo "$CMD" | grep -qE 'git\s+reset\s+--hard\s+(origin/|upstream/|HEAD~[0-9]|[a-f0-9]{7,})' ; then
  # Permite reset pra HEAD ou tag local (recovery legítimo), bloqueia em refs remotas
  if echo "$CMD" | grep -qE 'git\s+reset\s+--hard\s+(origin|upstream)/' ; then
    BLOCK=1; REASON="git reset --hard em ref remota (pode perder trabalho)"
  fi
fi

# Pattern 5: --no-verify em git commit/push (pula hooks bloqueantes)
if echo "$CMD" | grep -qE 'git\s+(commit|push|merge|rebase)\s+.*--no-verify' ; then
  BLOCK=1; REASON="--no-verify em git (pula hooks de segurança — Regra §12)"
fi

# Pattern 6: SQL destrutivo (DROP DATABASE, DROP TABLE em prod)
if echo "$CMD" | grep -qiE '(drop\s+(database|schema|table)|truncate\s+table)' ; then
  BLOCK=1; REASON="SQL destrutivo (DROP/TRUNCATE) — confirme manualmente"
fi

# Pattern 7: fork bomb / shell injection conhecidos
if echo "$CMD" | grep -qE ':\(\)\{[^}]*:\|:&[^}]*\};:' ; then
  BLOCK=1; REASON="fork bomb"
fi

# Pattern 8: chmod -R 777 (permission insegura)
if echo "$CMD" | grep -qE 'chmod\s+-R\s+777' ; then
  BLOCK=1; REASON="chmod -R 777 (permission insegura — abre tudo)"
fi

# Pattern 9: curl | sh / wget | bash (executa código não-auditado)
if echo "$CMD" | grep -qE '(curl|wget)\s+[^|;]+\|\s*(sh|bash)' ; then
  BLOCK=1; REASON="curl|sh ou wget|bash (executa código remoto sem auditar)"
fi

# Pattern 10: git push --force em qualquer branch (mais permissivo que pattern 3)
if echo "$CMD" | grep -qE 'git\s+push\s+.*(--force|^|\s)-f(\s|$)' && ! echo "$CMD" | grep -qE '\-\-force\-with\-lease' ; then
  # --force-with-lease é mais seguro, permite
  BLOCK=1; REASON="git push --force sem --force-with-lease (use --force-with-lease pra segurança)"
fi

if [ "$BLOCK" = "1" ]; then
  cat <<EOF
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "DCG BLOQUEOU: $REASON. Se a operação é legítima, exporte JADE_CONTEXT=rotina-autonoma OU DCG_BYPASS=true e tente de novo. Comando bloqueado: $CMD"}}
EOF
  exit 2
fi

exit 0