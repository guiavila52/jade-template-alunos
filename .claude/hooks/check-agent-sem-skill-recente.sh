#!/usr/bin/env bash
# PreToolUse hook — Regra §3 (skill canonica obrigatoria pra producao)
# Bloqueia despacho de agentes de producao sem skill canonica ativa
# Criado: 2026-05-17 (Task ClickUp: 86ahha462)

set -uo pipefail

INPUT=$(cat 2>/dev/null || true)
[ -z "$INPUT" ] && exit 0

SUBAGENT=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('subagent_type', ''))
except Exception:
    print('')
" 2>/dev/null)

AGENTES_PRODUCAO="desenvolvedor-frontend copywriter estrategista designer-revisor designer-conteudo gestor-trafego editor-audiovisual analista-qa especialista-email contador sdr closer customer-success revisor-copy revisor-newsletter revisor-linkedin revisor-roteiro revisor-criativo"

PROD=0
for a in $AGENTES_PRODUCAO; do
  [ "$SUBAGENT" = "$a" ] && PROD=1 && break
done
[ "$PROD" -eq 0 ] && exit 0

case "${SKILL_INTERNAL:-}" in
  true|1|yes) exit 0 ;;
esac
case "${JADE_CONTEXT:-}" in
  rotina-autonoma|research-investigativo|skill-interna) exit 0 ;;
esac

TRANSCRIPT=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('transcript_path', ''))
except Exception:
    print('')
" 2>/dev/null)

if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  if tail -c 100000 "$TRANSCRIPT" 2>/dev/null | grep -q '<command-name>'; then
    exit 0
  fi
fi

cat >&2 <<ERREOF
BLOQUEIO REGRA 3 (skill canonica obrigatoria)

Tentativa de despachar agente de producao '$SUBAGENT' sem skill canonica ativa.

Skills disponiveis:
  /criar-pagina, /escrever-pagina, /codar-pagina, /revisar-visual-pagina,
  /revisar-codigo-pagina, /escrever-copy, /escrever-newsletter,
  /escrever-linkedin, /criar-carrossel, /criar-criativo,
  /publicar-pagina, /feature-checkup-geral

Bypass legitimos:
  export SKILL_INTERNAL=true
  export JADE_CONTEXT=rotina-autonoma
  export JADE_CONTEXT=research-investigativo
ERREOF
exit 2
