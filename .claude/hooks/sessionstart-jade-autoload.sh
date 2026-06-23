#!/usr/bin/env bash
# sessionstart-jade-autoload.sh
# SessionStart hook — injeta contexto Jade no início de toda sessão.
#
# MODO FRESH INSTALL: se IDENTIDADE.md ainda tem {{NOME_OPERADOR}},
# injeta instrução de onboarding para que Claude mostre boas-vindas
# na primeira mensagem do aluno (qualquer que seja).
#
# MODO NORMAL (squad configurado): injeta manual operacional + fila ClickUp.
#
# Regra §11: este arquivo NUNCA editado via Edit/Write tool. Só Bash heredoc/sed.

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
IDENTIDADE_FILE="$PROJECT_DIR/IDENTIDADE.md"

# ── DETECÇÃO DE FRESH INSTALL ──────────────────────────────────────────────
IS_FRESH=false
if grep -q '{{NOME_OPERADOR}}' "$IDENTIDADE_FILE" 2>/dev/null; then
  IS_FRESH=true
fi

# ── MODO FRESH INSTALL ─────────────────────────────────────────────────────
if $IS_FRESH; then
  echo "<jade-autoload>"
  echo "## FRESH INSTALL DETECTADO — ONBOARDING OBRIGATÓRIO"
  echo ""
  echo "Aluno novo (IDENTIDADE.md ainda tem {{NOME_OPERADOR}}). Na PRÓXIMA mensagem"
  echo "(qualquer que seja), exibir a mensagem de boas-vindas abaixo palavra por palavra"
  echo "e seguir as instruções dela. Fonte única curada — não improvisar."
  echo ""
  cat "$PROJECT_DIR/.claude/onboarding-aluno.md" 2>/dev/null || echo "[ERRO] onboarding-aluno.md não encontrado"
  echo ""
  echo "</jade-autoload>"
  exit 0
fi

# ── MODO NORMAL (squad já configurado) ────────────────────────────────────
MANUAL_PATH="$HOME/.claude/projects/$(ls "$HOME/.claude/projects/" 2>/dev/null | grep -v 'mcpServers' | head -1)/memory/manual-operacional-coo.md"
ENV_FILE="$PROJECT_DIR/app/.env.local"

# Tenta descobrir o list ID do ClickUp
LIST_ID=""
if [ -f "$ENV_FILE" ]; then
  set -a; source "$ENV_FILE" 2>/dev/null || true; set +a
  LIST_ID="${CLICKUP_COO_LIST_ID:-${CLICKUP_LIST_ID:-}}"
fi

echo "<jade-autoload>"
echo "## MANUAL OPERACIONAL COO (autoload obrigatório)"
echo ""

if [ -f "$MANUAL_PATH" ]; then
  cat "$MANUAL_PATH"
else
  echo "[AVISO] Manual operacional não encontrado. Path esperado: $MANUAL_PATH"
  echo "Isso é normal em instalações novas — configure via /configurar-squad primeiro."
fi

echo ""
echo "## FILA CLICKUP ATUAL (top 5 abertos, ordenados por prioridade)"
echo ""

TOKEN="${CLICKUP_API_TOKEN:-}"

if [ -z "$TOKEN" ]; then
  echo "- [AVISO] CLICKUP_API_TOKEN não encontrado em $ENV_FILE"
elif [ -z "$LIST_ID" ]; then
  echo "- [AVISO] CLICKUP_LIST_ID não configurado — configure via /configurar-squad"
elif ! command -v curl >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
  echo "- [AVISO] curl ou jq não disponível"
else
  RESPONSE="$(curl -sS --max-time 8 \
    -H "Authorization: $TOKEN" \
    "https://api.clickup.com/api/v2/list/${LIST_ID}/task?archived=false&include_closed=false" 2>/dev/null || echo '')"

  if [ -z "$RESPONSE" ]; then
    echo "- [AVISO] ClickUp não respondeu (timeout ou erro de rede)"
  else
    COUNT="$(printf '%s' "$RESPONSE" | jq -r '(.tasks // []) | length' 2>/dev/null || echo 0)"
    if [ "$COUNT" = "0" ] || [ -z "$COUNT" ]; then
      echo "- (fila vazia ou erro de acesso)"
    else
      printf '%s' "$RESPONSE" | jq -r '
        .tasks
        | map(select(.status.status != "concluído" and .status.status != "cancelada" and .status.status != "closed"))
        | sort_by((.priority.orderindex // "5") | tonumber)
        | .[0:5]
        | .[]
        | "- [\(.id)] \(.name) (status: \(.status.status), prio: \(.priority.priority // "sem"))"
      ' 2>/dev/null || echo "- [AVISO] erro ao processar resposta ClickUp"
    fi
  fi
fi

echo ""
echo "## INSTRUÇÃO INICIAL (Regra §15)"
echo ""
echo "Sessão nova. Apresente top 3 da fila, ESCOLHA UM com justificativa em 1 frase,"
echo "e diga que está executando. Padrão: 'Vou começar por X porque [motivo]. Executando.'"
echo "Banido: listar A/B/C esperando o operador decidir."
echo "</jade-autoload>"

exit 0
