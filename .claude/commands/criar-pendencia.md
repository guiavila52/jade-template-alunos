---
name: criar-pendencia
description: Cria nova task na lista canonica Tasks Jade COO do ClickUp via API REST direta (Python urllib). Single source of truth de pendencias do squad.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /criar-pendencia

Cria nova task na lista canônica "Tasks Jade COO" do ClickUp **via API REST direta (Python urllib)**. **Não usa MCP** — funciona em subagent headless e cron sem modal de autorização.

> Histórico/setup completo: `segundo-cerebro/03-operacao/clickup-historico.md`.
> Migração MCP → REST: 2026-05-14.
> Migração bash+jq → Python urllib: 2026-05-17 (proteção contra parse error em payload com backticks/unicode).

## Quando invocar

- {{NOME_OPERADOR_CURTO}} passa uma demanda nova ("preciso que vc faça X")
- Jade detecta uma onda atacável que ainda não está registrada
- Subagent reporta um achado/blocker que precisa virar pendência rastreável
- Aprendizado em produção exigiu retrofit que ainda não foi feito

**Regra §1 (AGENTS.md):** TODA demanda do {{NOME_OPERADOR_CURTO}} (mesmo "pequena") vira pendência ANTES de executar. Sem exceção.

## Inputs

| Campo | Tipo | Obrigatório | Default |
|---|---|---|---|
| `title` | string | sim | — |
| `description` (markdown) | string | sim | — |
| `priority` | `urgent`/`high`/`normal`/`low` | sim | `normal` |
| `tags` | array de strings | recomendado | `[]` |
| `due_date` | YYYY-MM-DD | opcional | — |
| `status` | string | opcional | `fila para fazer` |

## IDs canônicos (NÃO inventar)

- **Workspace ID:** `{{CLICKUP_WORKSPACE_ID}}` (Empresa {{NOME_OPERADOR}})
- **List ID:** `{{CLICKUP_LIST_ID}}` (Tasks Jade COO) — **single source of truth**
- **NÃO CONFUNDIR com:** `{{CLICKUP_LIST_ID_2}}` ({{PLATAFORMA_NEWSLETTER}} backlog — sessão {{PLATAFORMA_NEWSLETTER}} paralela, NÃO usar daqui)

## Mapeamento de prioridade (texto → int ClickUp)

| Texto | ClickUp int |
|---|---|
| urgent | 1 |
| high | 2 |
| normal | 3 |
| low | 4 |

## Tags canônicas (catálogo evolutivo)

- `{{TAG_EVENTO}}` — caminho crítico {{PRODUTO_ENTRADA}}
- `aprovacao-gui` — pendente input/decisão {{NOME_OPERADOR_CURTO}}
- `skill-faltante` — skill a criar/refinar
- `arquitetura` — mudança estrutural
- `financeiro`, `nf`, `trafego`, `meta-ads`, `{{plataforma_newsletter}}`, `paginas`, `astro`, `migracao`, `seguranca`, `infra`, `dns`
- `onda-N` — quando faz parte de onda macro (ex: `onda-9`, `onda-mestra`)

## Setup

Token em `app/.env.local` na var `CLICKUP_API_TOKEN` (gitignored, §8).
Carregamento: `set -a; source app/.env.local; set +a`.
Header: `Authorization: $CLICKUP_API_TOKEN` (sem Bearer).

## Fluxo (REST via Python urllib)

```bash
set -a; source app/.env.local; set +a

python3 <<'PY'
import os, json, urllib.request, urllib.error
from datetime import datetime

token = os.environ["CLICKUP_API_TOKEN"]
list_id = "{{CLICKUP_LIST_ID}}"

# Inputs (substituir pelas vars bash ou argumentos)
title = os.environ.get("title", "")
description = os.environ.get("description", "")
priority_text = os.environ.get("priority", "normal")
tags_str = os.environ.get("tags", "")  # comma-separated ou vazio
due_date = os.environ.get("due_date", "")
status = os.environ.get("status", "fila para fazer")

# Validação mínima
if not title or not description:
    print("ERRO: title e description são obrigatórios")
    exit(1)

# Mapear prioridade texto -> int
prio_map = {"urgent": 1, "high": 2, "normal": 3, "low": 4}
priority_int = prio_map.get(priority_text, 3)

# Tags (split)
tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

# Payload base
payload = {
    "name": title,
    "markdown_description": description,
    "priority": priority_int,
    "tags": tags,
    "status": status
}

# Due date opcional (ms epoch)
if due_date:
    try:
        dt = datetime.strptime(due_date, "%Y-%m-%d")
        due_ms = int(dt.timestamp() * 1000)
        payload["due_date"] = due_ms
        payload["due_date_time"] = False
    except:
        pass

# POST
req = urllib.request.Request(
    f"https://api.clickup.com/api/v2/list/{list_id}/task",
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
        task_id = body["id"]
        task_url = body["url"]
        print(f"Task criada: {task_id} — {task_url}")
except urllib.error.HTTPError as e:
    print(f"ERRO HTTP {e.code}: {e.read().decode('utf-8')}")
    exit(1)
except Exception as e:
    print(f"ERRO: {e}")
    exit(1)
PY
```

## Output

```markdown
Pendência criada

- ID: {task_id}
- URL: {task_url}
- Prio: {priority}
- Tags: {tags}
- Status: {status}
```

## Critério de aceitação

- Task aparece em `GET /list/{{CLICKUP_LIST_ID}}/task?archived=false`
- Title curto e acionável (verbo no início se for ação)
- Description tem contexto suficiente pra outro agente executar sem voltar pro {{NOME_OPERADOR_CURTO}}
- Priority refletindo realidade (não tudo urgent)
- Tags úteis pra filtragem futura
- Sem jq/bash no caminho de payload (proteção contra parse error com backticks/unicode)

## Tratamento de erros

- HTTP 401 → token inválido → reportar {{NOME_OPERADOR_CURTO}} pra rotacionar
- HTTP 400 → payload inválido (status name não existe na lista, prioridade fora 1-4): mostrar body do erro
- HTTP 429 → rate limit → esperar 60s + retry uma vez

## Anexar print (Regra §1 + memória `feedback_anexar_print_em_task_clickup.md`)

Se a demanda **veio de um print/screenshot do {{NOME_OPERADOR_CURTO}}**, anexar via REST:

```bash
TS=$(date +"%Y-%m-%d-%H%M%S")
mkdir -p "workspace/output/screenshots-gui"
cp "<path-do-print>" "workspace/output/screenshots-gui/${TS}-<tema>.png"

curl -s -X POST \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -F "attachment=@workspace/output/screenshots-gui/${TS}-<tema>.png" \
  "https://api.clickup.com/api/v2/task/${TASK_ID}/attachment"
```

## Aprendizado + pendência (Regra §5)

- Se erro REST durante criação: registrar em `squads/gestao/aprendizados.md` + memória `feedback_clickup_api_nao_mcp.md`
- Se feedback do {{NOME_OPERADOR_CURTO}} apontou skill faltando: criar pendência cascata (criar/ajustar a skill, com aval {{NOME_OPERADOR_CURTO}} §13)