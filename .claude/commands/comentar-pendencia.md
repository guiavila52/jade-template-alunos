---
name: comentar-pendencia
description: Adiciona comentario em task existente da lista Tasks Jade COO no ClickUp via API REST direta (Python urllib). Registra progresso, blockers, decisoes ou links.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /comentar-pendencia

Adiciona comentário num task existente da lista "Tasks Jade COO" do ClickUp **via API REST direta (Python urllib)**. **Não usa MCP** — funciona em subagent headless e cron.

> Histórico/setup completo: `segundo-cerebro/03-operacao/clickup-historico.md`.
> Migração MCP → REST: 2026-05-14.
> Migração bash+jq → Python urllib: 2026-05-17 (proteção contra parse error em payload com backticks/unicode).

## Quando invocar

- Subagent entregou parte de uma pendência ativa → registrar progresso
- Detectado novo blocker numa pendência em curso
- Gui aprovou/rejeitou parte do output → registrar decisão
- Cross-reference: linkar memória/decisão/aprendizado criado pela pendência
- {{NOME_SUPORTE}}/{{NOME_BACKUP_ADMIN}} mencionaram algo num task — Jade responde via comment

## Inputs

| Campo | Tipo | Obrigatório |
|---|---|---|
| `task_id` | string (ex: `{{CLICKUP_TASK_ID}}`) | sim |
| `comment_text` | string (markdown OK) | sim |
| `notify_all` | boolean | opcional (default `false`) |

## IDs canônicos

- List ID `901327194775` é o esperado. Skill aceita qualquer task_id válido — mas se o task não pertencer a essa lista, a skill **avisa** (proteção contra mexer em listas externas como {{Plataforma_Conteudo}} `901327190242`).

## Setup

Token em `app/.env.local` na var `CLICKUP_API_TOKEN` (gitignored, §8).
Carregamento: `set -a; source app/.env.local; set +a`.
Header: `Authorization: $CLICKUP_API_TOKEN`.

## Fluxo (REST via Python urllib)

```bash
set -a; source app/.env.local; set +a

python3 <<'PY'
import os, json, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

token = os.environ["CLICKUP_API_TOKEN"]

# Inputs
task_id = os.environ.get("task_id", "")
comment_text = os.environ.get("comment_text", "")
notify_all = os.environ.get("notify_all", "false").lower() == "true"
agent = os.environ.get("agent", "jade")

# Validação
if not task_id or not comment_text:
    print("ERRO: task_id e comment_text são obrigatórios")
    exit(1)

# Validar task_id (formato alfanumérico)
if not task_id.replace("_", "").isalnum():
    print("ERRO: task_id inválido")
    exit(1)

# (Opcional) Validar lista canônica
try:
    req_meta = urllib.request.Request(
        f"https://api.clickup.com/api/v2/task/{task_id}",
        headers={"Authorization": token}
    )
    with urllib.request.urlopen(req_meta) as resp:
        meta = json.loads(resp.read().decode("utf-8"))
        list_of_task = meta.get("list", {}).get("id")
        task_name = meta.get("name", "")
        
        if list_of_task != "901327194775":
            print(f"AVISO: task {task_id} pertence à lista {list_of_task} (não Tasks Jade COO). Confirme antes de prosseguir.")
except urllib.error.HTTPError as e:
    if e.code == 404:
        print(f"ERRO: task {task_id} não encontrada")
        exit(1)
    print(f"ERRO HTTP {e.code} ao buscar task: {e.read().decode('utf-8')}")
    exit(1)

# Timestamp BRT (UTC-3 fixo, sem horário de verão desde 2019)
ts = datetime.now(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d %H:%M BRT")
full_text = f"[{ts}] {agent}: {comment_text}"

# POST comment
payload = {
    "comment_text": full_text,
    "notify_all": notify_all
}

req = urllib.request.Request(
    f"https://api.clickup.com/api/v2/task/{task_id}/comment",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": token,
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode("utf-8"))
        comment_id = body.get("id", "")
        print(f"Comentário registrado: {comment_id} em https://app.clickup.com/t/{task_id}")
except urllib.error.HTTPError as e:
    print(f"ERRO HTTP {e.code}: {e.read().decode('utf-8')}")
    exit(1)
PY
```

## Output

```markdown
Comentário registrado

- Task: {task_id} ({task_name})
- Comment ID: {comment_id}
- URL: https://app.clickup.com/t/{task_id}
```

## Critério de aceitação

- Comentário aparece no painel ClickUp
- Tem timestamp + autor (Jade ou subagent)
- Linka outputs externos quando relevante (path arquivo, URL deploy, etc)
- Não polui o task com mensagens triviais ("ok", "feito") — comentário é narrativa de progresso
- Sem jq/bash no caminho de payload (proteção contra parse error)

## Convenções de conteúdo

- **Progresso:** `Fase X concluída. Output em {path}. Próxima: Fase Y.`
- **Blocker:** `BLOQUEADO: {motivo}. Aguarda: {ação} de {responsável}.`
- **Decisão Gui:** `Gui aprovou {output} em {data}. Próximo: {ação}.`
- **Cross-ref:** `Memória criada: {path}. Aprendizado em: {workspace/agente}.`

## Tratamento de erros

- HTTP 401 → token inválido → reportar Gui pra rotacionar
- HTTP 404 → task_id inexistente
- HTTP 429 → rate limit → esperar 60s + retry uma vez

## Aprendizado + pendência (Regra §5)

- Se Gui disser "esse comentário tá confuso/longo demais": registrar em `squads/gestao/aprendizados.md` + ajustar convenção acima
- Se HTTP 401: memória `feedback_clickup_api_nao_mcp.md` + pendência rotacionar token
