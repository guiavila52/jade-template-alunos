---
name: adicionar-novo-video-na-lista-para-gravar
description: Captura conteúdo bruto (texto livre, link de vídeo ou documento), extrai uma ideia estruturada (título, ângulo, hook, roteiro) e cria como task na sua lista de conteúdo do ClickUp — status pronto pra gravar.
---

# Skill: /adicionar-novo-video-na-lista-para-gravar

Captura conteúdo em qualquer formato, estrutura uma ideia de vídeo/post e registra na **sua lista de conteúdo do ClickUp**. Você só vê: confirmação rápida + link da task.

## Fluxo

1. Receber o input bruto (texto, link de vídeo, ou caminho de documento)
2. Extrair e estruturar: título, ângulo, hook de abertura, roteiro em tópicos
3. Criar a task no ClickUp (lista de conteúdo) via API REST direta
4. Reportar: confirmação + URL da task

## Setup

| Item | Onde |
|---|---|
| Token ClickUp | `app/.env.local` → `CLICKUP_API_TOKEN` (header sem "Bearer") |
| Lista de conteúdo | `app/.env.local` → `CLICKUP_CONTENT_LIST_ID` (sua lista "Conteúdo / Pauta") |

> Não tem a lista ainda? Crie uma lista "Conteúdo" no seu ClickUp e cole o ID em `CLICKUP_CONTENT_LIST_ID`. O ID está na URL da lista.

## Implementação

```bash
set -a; source app/.env.local; set +a

python3 <<'PY'
import os, json, urllib.request

token = os.environ["CLICKUP_API_TOKEN"]
list_id = os.environ.get("CLICKUP_CONTENT_LIST_ID", "")
if not list_id:
    print("CLICKUP_CONTENT_LIST_ID não configurado em app/.env.local"); raise SystemExit(1)

# title/description vêm da estruturação feita pela Jade a partir do input bruto
title = os.environ.get("titulo", "")
description = os.environ.get("roteiro_md", "")   # markdown: ângulo + hook + roteiro em tópicos

payload = {
    "name": title,
    "markdown_description": description,
    "tags": ["conteudo", "pronto-pra-gravar"],
    "priority": 2,
}
req = urllib.request.Request(
    f"https://api.clickup.com/api/v2/list/{list_id}/task",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": token, "Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    body = json.loads(resp.read())
    print(f"Ideia criada: {body['url']}")
PY
```

## Estruturação da ideia (o que a Jade extrai do input)

- **Título** — claro e específico, no tom de quem vai gravar
- **Ângulo** — o gancho central / por que esse conteúdo importa
- **Hook** — a primeira frase falada, pra segurar atenção
- **Roteiro** — tópicos em ordem (abertura → desenvolvimento → fechamento/CTA)

## Critério de aceitação

- Task aparece na lista de conteúdo do ClickUp do operador
- Título acionável + roteiro estruturado no corpo
- Zero dado inventado — só o que veio do input

## Após criar

Reportar ao operador: confirmação curta + link clicável da task. Registrar aprendizado em `squads/conteudo/agentes/{agente}/aprendizados.md` se algo novo surgir.
