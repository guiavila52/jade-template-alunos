#!/usr/bin/env bash
# sessionstart-jade-autoload.sh
# SessionStart hook — injeta contexto Jade obrigatório no início de toda sessão.
#
# O quê:
#  1) Manual operacional Jade (feedback_jade_comportamento.md)
#  2) Top 5 pendências abertas no ClickUp list 901327194775 (Tasks Jade COO)
#     ordenadas por priority (orderindex asc: 1=urgent, 2=high, 3=normal, 4=low)
#  3) Instrução inicial: NÃO pergunte "o que quer atacar"; apresente top 3 + decisão (§15).
#
# Por quê: instrução em CLAUDE.md em markdown é frágil — Claude pode ignorar.
# Hook injeta o conteúdo no stdout como system context — mais forte que markdown.
#
# Importante: SessionStart hooks injetam stdout como contexto. Exit 0 sempre.
# NÃO usar exit 2 (esse é o exit code de bloqueio).
#
# Regra §11: este arquivo NUNCA editado via Edit/Write tool. Só Bash heredoc/sed.
# Regra §16: usa API REST direta (curl) — não MCP (issue: MCP ClickUp não funciona em hook).

set -uo pipefail

MANUAL_PATH="~/.claude/projects/-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/memory/feedback_jade_comportamento.md"
ENV_FILE="~/Documents/Projetos IA Gui Ávila/Squad Empresa Gui Ávila/app/.env.local"
LIST_ID="901327194775"

echo "<jade-autoload>"
echo "## MANUAL OPERACIONAL JADE (autoload obrigatório)"
echo ""

if [ -f "$MANUAL_PATH" ]; then
  cat "$MANUAL_PATH"
else
  echo "[AVISO] Manual operacional não encontrado em $MANUAL_PATH"
fi

echo ""
echo "## FILA CLICKUP ATUAL (top 5 abertos — list Tasks Jade COO, ordenado por prioridade)"
echo ""

# Carrega CLICKUP_API_TOKEN do .env.local (set -a; source) — caminho canônico do squad
TOKEN=""
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  set -a
  source "$ENV_FILE" 2>/dev/null || true
  set +a
  TOKEN="${CLICKUP_API_TOKEN:-}"
fi

if [ -z "$TOKEN" ]; then
  echo "- [AVISO] CLICKUP_API_TOKEN não encontrado em $ENV_FILE — fila não carregada."
elif ! command -v jq >/dev/null 2>&1; then
  echo "- [AVISO] jq não disponível — fila não carregada."
elif ! command -v curl >/dev/null 2>&1; then
  echo "- [AVISO] curl não disponível — fila não carregada."
else
  # Query simples: sem subtasks (combinação subtasks=true + order_by=priority quebra a API
  # e retorna .tasks=null). Ordenação local via jq por priority.orderindex.
  RESPONSE="$(curl -sS --max-time 8 \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.clickup.com/api/v2/list/${LIST_ID}/task?archived=false&include_closed=false" 2>/dev/null || echo '')"

  if [ -z "$RESPONSE" ]; then
    echo "- [AVISO] ClickUp não respondeu (timeout 8s ou erro de rede)."
  else
    COUNT="$(printf '%s' "$RESPONSE" | jq -r '(.tasks // []) | length' 2>/dev/null || echo 0)"
    if [ "$COUNT" = "0" ] || [ -z "$COUNT" ]; then
      ERR_MSG="$(printf '%s' "$RESPONSE" | jq -r '.err // .ECODE // empty' 2>/dev/null || echo '')"
      if [ -n "$ERR_MSG" ]; then
        echo "- [AVISO] ClickUp API erro: $ERR_MSG"
      else
        echo "- (fila vazia)"
      fi
    else
      # Filtra status fechados + ordena por priority.orderindex asc (1=urgent ... 4=low; sem prio → 5)
      printf '%s' "$RESPONSE" | jq -r '
        .tasks
        | map(select(.status.status != "concluído" and .status.status != "cancelada" and .status.status != "closed"))
        | sort_by((.priority.orderindex // "5") | tonumber)
        | .[0:5]
        | .[]
        | "- [\(.id)] \(.name) (status: \(.status.status), prio: \(.priority.priority // "sem"))"
      ' 2>/dev/null || echo "- [AVISO] erro parsing jq do response."
    fi
  fi
fi

echo ""
echo "## INSTRUÇÃO INICIAL (Regra §15 — Jade decide com opinião + justificativa)"
echo ""
echo "Esta é uma sessão nova. Antes da primeira resposta, NÃO pergunte 'o que quer atacar' nem 'qual prefere'."
echo "Apresente os top 3 da fila acima, ESCOLHA UM com justificativa em 1 frase, e diga que está executando."
echo "Padrão correto: 'Vou começar por X porque [motivo]. Executando agora.'"
echo "Banido: listar A/B/C esperando Gui decidir."
echo "</jade-autoload>"

exit 0
