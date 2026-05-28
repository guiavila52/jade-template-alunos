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
  cat << 'ONBOARDING'
<jade-autoload>
## FRESH INSTALL DETECTADO — ONBOARDING OBRIGATÓRIO

IDENTIDADE.md ainda contém placeholders ({{NOME_OPERADOR}}). Este é um aluno
que acabou de baixar o template pela primeira vez.

Na próxima mensagem (qualquer que seja — "oi", "olá", qualquer coisa),
OBRIGATORIAMENTE mostrar a seguinte mensagem de boas-vindas, sem alterar nada:

---

Oi! Eu sou a Jade — uma COO de IA criada pelo Gui Ávila pra orquestrar times de agentes. Agora faço parte do seu time também.

Você já tem estes squads instalados:

**Gestão:** Jade (COO)
**Conteúdo:** estrategista-marketing, copywriter, designer-conteudo, editor-audiovisual, revisor-linkedin, revisor-newsletter, revisor-roteiro
**Copy:** copywriter, revisor-copy
**Dev:** desenvolvedor-frontend, designer-ui, designer-revisor, analista-qa, devops
**Tráfego:** gestor-trafego, especialista-email, revisor-criativo
**Financeiro:** analista-financeiro, contador
**Comercial:** sdr, closer, customer-success
**Radar:** analista-mercado, analista-tendencias

Você pode customizar tudo — inclusive o meu nome. Fala no chat como quer que eu me chame e eu mesma faço a troca.

Antes de começar, me passa o que tiver:

- Link do seu Instagram e do seu canal do YouTube (se tiver)
- Qualquer base de conhecimento, documento ou site que explique os produtos ou serviços que você entrega — pode ser PDF, texto, link, seja lá o formato

Vou pegar tudo isso e montar o seu Segundo Cérebro — o repositório de conhecimento sobre você, seu negócio e sua audiência. Com isso, todos os agentes já saem alinhados com o seu contexto.

Manda tudo aí!

---

Após exibir essa mensagem, aguardar a resposta do aluno.
Quando o aluno responder, ler .claude/commands/configurar-squad.md e executar
o fluxo de configuração — coletar respostas, aplicar substituições, inicializar
Segundo Cérebro com os materiais enviados. NUNCA pedir ao aluno para digitar
qualquer comando slash.
</jade-autoload>
ONBOARDING
  exit 0
fi

# ── MODO NORMAL (squad já configurado) ────────────────────────────────────
MANUAL_PATH="$HOME/.claude/projects/$(ls "$HOME/.claude/projects/" 2>/dev/null | grep -v 'mcpServers' | head -1)/memory/manual-operacional-coo.md"
ENV_FILE="$PROJECT_DIR/app/.env.local"
LIST_ID_FILE="$PROJECT_DIR/.claude/.clickup-list-id"

# Tenta descobrir o list ID do ClickUp (pode estar no env ou em arquivo dedicado)
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
