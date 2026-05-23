#!/bin/bash
# Hook PreToolUse — BLOQUEIA Bash com escrita em paths críticos de config Claude Code
# Regra §16 (Segurança first) — estende Regra §11
# Vetor R2: self-modification de settings via Bash.
# Vetores 2026: CVE-2025-59536, CVE-2026-21852, Mini Shai-Hulud (~/.claude.json).
# Pendência mãe: ClickUp 86ahha462

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULT=$(cat | python3 "$DIR/_check-bash-em-claude-paths-detect.py")

if [[ "$RESULT" == "PASS" || -z "$RESULT" ]]; then
  exit 0
fi

if [[ "$RESULT" == BLOCK* ]]; then
  PROTECTED_PATH=$(echo "$RESULT" | cut -d'|' -f2)
  OP_DETECTED=$(echo "$RESULT" | cut -d'|' -f3)
  CMD_B64=$(echo "$RESULT" | cut -d'|' -f4)
  COMMAND_SHOWN=$(echo "$CMD_B64" | base64 -d 2>/dev/null)

  BYPASS_TOKENS=("skill-aprovada=true" "fase-0-hardening=true" "regra-aprovada-gui=true" "rotina-autonoma")
  for tok in "${BYPASS_TOKENS[@]}"; do
    if [[ "$JADE_CONTEXT" == *"$tok"* ]]; then
      echo "check-bash-em-claude-paths.sh: BYPASS via JADE_CONTEXT=$JADE_CONTEXT (path=$PROTECTED_PATH, op=$OP_DETECTED)" >&2
      exit 0
    fi
  done

  cat >&2 <<MSG
HOOK BLOQUEANTE — check-bash-em-claude-paths.sh (Regra §16 / §11 extended)

VETOR: R2 — self-modification de settings via Bash
COMMAND: $COMMAND_SHOWN
PATH PROTEGIDO DETECTADO: $PROTECTED_PATH
OPERACAO DETECTADA: $OP_DETECTED

Bash com escrita em paths críticos de configuração do Claude Code é vetor
documentado de auto-modificação (modelo adicionando Bash(*) em allowedTools
pra bypass próprio hook). Bloqueado por padrão.

BYPASS LEGITIMO:
- export JADE_CONTEXT=skill-aprovada=true   (Regra §13 — skill nova com aval Gui)
- export JADE_CONTEXT=fase-0-hardening=true (durante execução da Fase 0)
- export JADE_CONTEXT=regra-aprovada-gui=true (mudança de regra com aval explícito)
- export JADE_CONTEXT=rotina-autonoma       (rotina autônoma da Jade)

Vetores ativos 2026 (consultar Regra §16 / AGENTS.md):
- CVE-2025-59536, CVE-2026-21852
- Mini Shai-Hulud (worm modifica ~/.claude.json)

Pendencia mae: ClickUp 86ahha462
MSG
  exit 2
fi

exit 0
