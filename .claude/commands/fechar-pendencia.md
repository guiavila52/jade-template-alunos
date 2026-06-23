---
name: fechar-pendencia
description: Marca task como concluida na lista Tasks Jade COO do ClickUp via API REST direta (Python urllib) e adiciona comentario final com sumario do que foi entregue.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /fechar-pendencia

Marca task como `concluído` na lista "Tasks Jade COO" do ClickUp + adiciona comentário final com sumário do que foi entregue. **Via API REST direta (Python urllib)**, sem MCP.

> Histórico/setup completo: `segundo-cerebro/03-operacao/clickup-historico.md`.
> Migração MCP → REST: 2026-05-14.
> Migração bash+jq → Python urllib: 2026-05-17 (proteção contra parse error em payload com backticks/unicode).

## Quando invocar

- Subagent entregou o escopo COMPLETO da pendência (todas as fases)
- {{NOME_OPERADOR_CURTO}} aprovou o output final
- Pendência virou obsoleta (mudança estratégica, deduplicação)

**NÃO usar:** se entrega for parcial (use `/comentar-pendencia`).
**NÃO usar:** se {{NOME_OPERADOR_CURTO}} ainda precisa aprovar (use `/comentar-pendencia` notificando "aguarda aprovação {{NOME_OPERADOR_CURTO}}").

## Inputs

| Campo | Tipo | Obrigatório |
|---|---|---|
| `task_id` | string | sim |
| `sumario` | string (markdown) — o que foi entregue + como validar | sim |
| `status` | string — default `concluído` | opcional |

## IDs canônicos

- **List ID:** `{{CLICKUP_LIST_ID}}`
- **Status válido pra fechar:** `concluído` (type: closed na list "Tasks Jade COO")
- Status disponíveis: `fila para fazer` · `em progresso` · `aprovação` · `alterações` · `concluído`

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
sumario = os.environ.get("sumario", "")
status = os.environ.get("status", "concluído")

# Validação
if not task_id or not sumario:
    print("ERRO: task_id e sumario são obrigatórios")
    exit(1)

if not task_id.replace("_", "").isalnum():
    print("ERRO: task_id inválido")
    exit(1)

# Buscar metadata da task
try:
    req_meta = urllib.request.Request(
        f"https://api.clickup.com/api/v2/task/{task_id}",
        headers={"Authorization": token}
    )
    with urllib.request.urlopen(req_meta) as resp:
        meta = json.loads(resp.read().decode("utf-8"))
        list_of_task = meta.get("list", {}).get("id")
        task_name = meta.get("name", "")
        
        if list_of_task != "{{CLICKUP_LIST_ID}}":
            print(f"AVISO: task {task_id} pertence à lista {list_of_task} (não Tasks Jade COO). Confirme antes.")
except urllib.error.HTTPError as e:
    if e.code == 404:
        print(f"ERRO: task {task_id} não encontrada")
        exit(1)
    print(f"ERRO HTTP {e.code}: {e.read().decode('utf-8')}")
    exit(1)

# Timestamp BRT (UTC-3 fixo, sem horário de verão desde 2019)
ts = datetime.now(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d %H:%M BRT")

# Comentário final estruturado
final_comment = f"## ENTREGUE — {ts}

{sumario}"

# POST comentário
comment_payload = {
    "comment_text": final_comment,
    "notify_all": False
}

req_comment = urllib.request.Request(
    f"https://api.clickup.com/api/v2/task/{task_id}/comment",
    data=json.dumps(comment_payload).encode("utf-8"),
    headers={
        "Authorization": token,
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req_comment) as resp:
        pass  # Comentário criado
except urllib.error.HTTPError as e:
    print(f"AVISO: erro ao criar comentário final HTTP {e.code}: {e.read().decode('utf-8')}")

# PUT status -> concluído
status_payload = {"status": status}

req_status = urllib.request.Request(
    f"https://api.clickup.com/api/v2/task/{task_id}",
    data=json.dumps(status_payload).encode("utf-8"),
    headers={
        "Authorization": token,
        "Content-Type": "application/json"
    },
    method="PUT"
)

try:
    with urllib.request.urlopen(req_status) as resp:
        print(f"Pendência fechada: {task_id} ({task_name}) — https://app.clickup.com/t/{task_id}")
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    print(f"ERRO HTTP {e.code}: {body}")
    exit(1)
PY
```

## Estrutura do comentário final (sumario)

```markdown
**Resumo:** {o que foi entregue em 1-2 linhas}

**Outputs:**
- {arquivo/URL/memória}
- ...

**Validação:**
- {como {{NOME_OPERADOR_CURTO}} pode verificar — preview, build, link, etc}

**Aprendizados (Regra §5):**
- Memória: {path}
- Squad/agente: {path}
- Retrofit aplicado: {sim/não, onde}
```

## Output

```markdown
Pendência fechada

- Task: {task_id} ({task_name})
- Status: concluído
- Comentário final: registrado
- URL: https://app.clickup.com/t/{task_id}
```

## Critério de aceitação

- Task aparece com status `concluído` (type closed) no ClickUp
- Comentário final tem estrutura: o que foi entregue + onde validar + aprendizados
- Aprendizados em 3 camadas registrados ANTES de fechar (Regra §5):
  - Memória persistente atualizada
  - `squads/{squad}/aprendizados.md` atualizado (se aplicável)
  - Agente responsável atualizou `squads/{squad}/agentes/{ag}/aprendizados.md`
- Sem jq/bash no caminho de payload (proteção contra parse error)

## Tratamento de erros

- HTTP 401 → token inválido → reportar {{NOME_OPERADOR_CURTO}}
- HTTP 400 com `Status not found` → status name digitado errado (lembrar: `concluído` com acento)
- HTTP 404 → task_id inexistente

## Anti-padrão

NÃO fechar pendência só porque "achou que estava feito". Confirmar:
1. Output existe no path declarado
2. Validação real foi executada (build/teste/preview)
3. Triple-check (§6) se for deploy
4. Bateria de testes (§6) se for skill/feature

## Aprendizado + pendência (Regra §5)

- Se {{NOME_OPERADOR_CURTO}} reabrir um task fechado: criar pendência de retrofit + atualizar aprendizado "fechamento prematuro"
- Se HTTP 400 por status: memória `feedback_clickup_api_nao_mcp.md` (status names com acento)