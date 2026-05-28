---
name: listar-pendencias
description: Lista pendencias abertas da lista canonica Tasks Jade COO no ClickUp via API REST direta (Python urllib) com filtros por status, prioridade e tags.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /listar-pendencias

Lista pendências abertas da lista canônica "Tasks Jade COO" do ClickUp **via API REST direta (Python urllib)**. **Não usa MCP** — funciona em subagent headless, cron e ambientes sem allowlist.

> Histórico/setup completo: `segundo-cerebro/03-operacao/clickup-historico.md`.
> Migração MCP → REST: 2026-05-14.
> Migração bash+jq → Python urllib: 2026-05-17 (proteção contra parse error em payload com backticks/unicode).

## Quando invocar

- {{NOME_OPERADOR_CURTO}} pergunta "o que tá pendente?"
- Jade está fazendo priorização autônoma (rotina /varrer-squads)
- Início de sessão: snapshot do que está em curso
- Antes de despachar nova tarefa pra confirmar que não duplica

## Inputs (todos opcionais)

| Campo | Tipo | Default |
|---|---|---|
| `statuses` | array (ex: `["fila para fazer", "em progresso"]`) | abertas (não `concluído`) |
| `priorities` | array (ex: `["urgent", "high"]`) | todas |
| `tags` | array (ex: `["{{TAG_EVENTO}}"]`) | todas |
| `include_closed` | boolean | `false` |
| `limit` | número | sem limite (paginação automática) |

## IDs canônicos

- **List ID:** `{{CLICKUP_LIST_ID}}`
- **Workspace:** `{{CLICKUP_WORKSPACE_ID}}`
- **Statuses válidos:** `fila para fazer` (open) · `em progresso` · `aprovação` · `alterações` · `concluído` (closed)
- **Prioridades ClickUp:** 1=urgent · 2=high · 3=normal · 4=low

## Setup

Token em `app/.env.local` na var `CLICKUP_API_TOKEN` (gitignored, §8).
Carregamento via `set -a; source app/.env.local; set +a`.
Header HTTP: `Authorization: $CLICKUP_API_TOKEN` (ClickUp **não** usa "Bearer").

## Fluxo (REST via Python urllib)

```bash
set -a; source app/.env.local; set +a

python3 <<'PY'
import os, json, urllib.request, urllib.error
from collections import defaultdict

token = os.environ["CLICKUP_API_TOKEN"]
list_id = "{{CLICKUP_LIST_ID}}"

# Inputs (substituir pelas vars bash ou argumentos)
include_closed = os.environ.get("include_closed", "false").lower() == "true"
filter_statuses = os.environ.get("filter_statuses", "")  # comma-separated
filter_priorities = os.environ.get("filter_priorities", "")  # comma-separated
filter_tags = os.environ.get("filter_tags", "")  # comma-separated

# Paginação
all_tasks = []
page = 0

while True:
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task?archived=false&include_closed={str(include_closed).lower()}&page={page}&subtasks=true&order_by=created&reverse=true"
    
    req = urllib.request.Request(
        url,
        headers={"Authorization": token}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tasks = data.get("tasks", [])
            all_tasks.extend(tasks)
            
            if len(tasks) < 100:
                break
            page += 1
    except urllib.error.HTTPError as e:
        print(f"ERRO HTTP {e.code}: {e.read().decode('utf-8')}")
        exit(1)

# Filtragem client-side
filtered_tasks = all_tasks

if filter_statuses:
    statuses_list = [s.strip() for s in filter_statuses.split(",")]
    filtered_tasks = [t for t in filtered_tasks if t.get("status", {}).get("status") in statuses_list]

if filter_priorities:
    priorities_map = {"urgent": "1", "high": "2", "normal": "3", "low": "4"}
    priority_orderindexes = [priorities_map.get(p.strip(), "") for p in filter_priorities.split(",")]
    filtered_tasks = [t for t in filtered_tasks if str(t.get("priority", {}).get("orderindex", "")) in priority_orderindexes]

if filter_tags:
    tags_list = [t.strip() for t in filter_tags.split(",")]
    filtered_tasks = [t for t in filtered_tasks if any(tag["name"] in tags_list for tag in t.get("tags", []))]

# Ordenar: priority asc (1=urgent primeiro), depois date_created desc
def sort_key(task):
    priority_order = int(task.get("priority", {}).get("orderindex", 9))
    date_created = int(task.get("date_created", 0))
    return (priority_order, -date_created)

filtered_tasks.sort(key=sort_key)

# Output markdown tabela
print("| ID | Título | Prio | Status | Tags |")
print("|---|---|---|---|---|")

prio_counts = defaultdict(int)

for task in filtered_tasks:
    task_id = task["id"]
    name = task["name"]
    priority = task.get("priority", {}).get("priority", "—")
    status = task.get("status", {}).get("status", "—")
    tags = ", ".join([tag["name"] for tag in task.get("tags", [])])
    
    print(f"| {task_id} | {name} | {priority} | {status} | {tags} |")
    
    if priority != "—":
        prio_counts[priority.lower()] += 1

# Resumo
total = len(filtered_tasks)
urgent = prio_counts.get("urgent", 0)
high = prio_counts.get("high", 0)
normal = prio_counts.get("normal", 0)
low = prio_counts.get("low", 0)

print(f"
**Resumo:** {total} abertas ({urgent} urgent · {high} high · {normal} normal · {low} low)")
print(f"**URL lista:** https://app.clickup.com/{{CLICKUP_WORKSPACE_ID}}/v/l/li/{list_id}")
PY
```

## Output (markdown renderizado)

```markdown
## Pendências abertas — 17/05/2026

| ID | Título | Prio | Status | Tags |
|---|---|---|---|---|
| {{CLICKUP_TASK_EXEMPLO}} | {{NOME_TASK_EXEMPLO}} | urgent | em progresso | {{TAG_EXEMPLO}} |
| {{CLICKUP_TASK_EXEMPLO_2}} | {{NOME_TASK_EXEMPLO_2}} | high | fila para fazer | skills |
| ... | ... | ... | ... | ... |

**Resumo:** N abertas (X urgent · Y high · Z normal · W low)
**URL lista:** https://app.clickup.com/{{CLICKUP_WORKSPACE_ID}}/v/l/li/{{CLICKUP_LIST_ID}}
```

## Critério de aceitação

- Toda task com link ClickUp clicável (`https://app.clickup.com/t/{id}`)
- Priorização visível (urgent em destaque, ordem decrescente)
- Tags listadas pra filtragem mental
- Contadores no rodapé
- Sem jq/bash no caminho de payload (proteção contra parse error)

## Tratamento de erros

- HTTP 401 → token inválido/expirado → reportar pro {{NOME_OPERADOR_CURTO}} pra rotacionar key
- HTTP 429 → rate limit → esperar 60s + retry uma vez
- HTTP 5xx → ClickUp instável → reportar + tentar novamente em 30s

## Modo Jade autônoma (rotina /varrer-squads ou wakeup)

Quando chamada em rotina autônoma, ao invés de só listar:
1. Listar → priorizar (caminho crítico Imersão → deadline → dependência)
2. Detectar urgents sem assignee
3. Sinalizar pendências bloqueadas por input do {{NOME_OPERADOR_CURTO}} (tag `aprovacao-gui`)
4. Sugerir próximas 3 a atacar autonomamente

## Aprendizado + pendência (Regra §5)

- Se {{NOME_OPERADOR_CURTO}} apontar inconsistência (task no painel mas não veio na lista): registrar em `squads/gestao/aprendizados.md` + criar pendência de fix de filtro
- Se HTTP 401 acontecer: registrar em memória `feedback_clickup_api_nao_mcp.md` + abrir pendência rotacionar token