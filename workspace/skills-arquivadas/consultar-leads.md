# Skill: /consultar-leads

Consulta leads do CRM {{CRM}} ({{CRM}}) via API. Use quando o Gui perguntar sobre leads, contatos, oportunidades ou pipeline.

## Input

```
/consultar-leads [filtro]
```

Exemplos:
- `/consultar-leads esta semana` — leads dos últimos 7 dias
- `/consultar-leads hoje` — leads de hoje
- `/consultar-leads 30 dias` — últimos 30 dias
- `/consultar-leads tag:mentoria` — leads com tag específica
- `/consultar-leads pipeline:reverso` — leads de pipeline específico
- `/consultar-leads email:{{EMAIL_OPERADOR}}` — busca por email
- `/consultar-leads telefone:+5511...` — busca por telefone

Sem filtro: últimos 7 dias.

## O que fazer

### 1. Carregar credenciais

```bash
source "{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}/app/.env.local"
```

Vars necessárias:
- `{{CRM}}_API_KEY` — Bearer token
- `{{CRM}}_LOCATION_ID` — identificador da location

### 2. Executar consulta via Python (com confiabilidade — Regra #22)

Script temporário `/tmp/consultar_leads.py`:

```python
import os, sys, json, requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("{{CRM}}_API_KEY")
LOCATION_ID = os.environ.get("{{CRM}}_LOCATION_ID")
BASE_URL = "https://services.leadconnectorhq.com"
TIMEOUT = 15  # Regra #22

if not API_KEY or not LOCATION_ID:
    print(json.dumps({"erro": "{{CRM}}_API_KEY ou {{CRM}}_LOCATION_ID não setados em app/.env.local"}))
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Accept": "application/json",
}

filtro = sys.argv[1] if len(sys.argv) > 1 else "7 dias"

def parse_periodo(f):
    f = f.lower().strip()
    hoje = datetime.now()
    if "hoje" in f:
        return hoje.replace(hour=0, minute=0, second=0), hoje
    if "semana" in f or "7 dias" in f or "7d" in f:
        return hoje - timedelta(days=7), hoje
    if "30 dias" in f or "30d" in f or "mês" in f or "mes" in f:
        return hoje - timedelta(days=30), hoje
    if "90 dias" in f or "trimestre" in f:
        return hoje - timedelta(days=90), hoje
    # Padrão: 7 dias
    return hoje - timedelta(days=7), hoje

def buscar_contatos(query=None, limit=100):
    """GET /contacts/ — lista contatos da location."""
    url = f"{BASE_URL}/contacts/"
    params = {"locationId": LOCATION_ID, "limit": limit}
    if query:
        params["query"] = query
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
        return {"erro": r.status_code, "body": r.text[:300]}
    except requests.Timeout:
        return {"erro": "timeout", "msg": f"{{CRM}} não respondeu em {TIMEOUT}s"}
    except Exception as e:
        return {"erro": "exception", "msg": str(e)}

def buscar_por_email(email):
    url = f"{BASE_URL}/contacts/search/duplicate"
    params = {"locationId": LOCATION_ID, "email": email}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {"erro": r.status_code}
    except Exception as e:
        return {"erro": str(e)}

# Roteamento por tipo de filtro
if filtro.startswith("email:"):
    email = filtro.split(":", 1)[1].strip()
    resultado = buscar_por_email(email)
elif filtro.startswith("telefone:"):
    tel = filtro.split(":", 1)[1].strip()
    resultado = buscar_contatos(query=tel)
elif filtro.startswith("tag:"):
    tag = filtro.split(":", 1)[1].strip()
    # {{CRM}} filtra tag via query
    resultado = buscar_contatos(query=tag)
elif filtro.startswith("pipeline:"):
    # Pipeline → opportunities endpoint
    pipeline_name = filtro.split(":", 1)[1].strip()
    resultado = {"info": f"Pipeline '{pipeline_name}' — requer endpoint /opportunities/ (a implementar quando demandado)"}
else:
    inicio, fim = parse_periodo(filtro)
    # {{CRM}} não filtra por data via query direto; pegar últimos 100 e filtrar local
    bruto = buscar_contatos(limit=100)
    if "contacts" in bruto:
        filtrados = []
        for c in bruto["contacts"]:
            criado = c.get("dateAdded")
            if criado:
                try:
                    dt = datetime.fromisoformat(criado.replace("Z", "+00:00"))
                    if inicio.timestamp() <= dt.timestamp() <= fim.timestamp() + 86400:
                        filtrados.append(c)
                except Exception:
                    pass
        resultado = {
            "total_no_periodo": len(filtrados),
            "periodo": f"{inicio.strftime('%Y-%m-%d')} a {fim.strftime('%Y-%m-%d')}",
            "contatos": filtrados[:20],
        }
    else:
        resultado = bruto

print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))
```

**Executar:**
```bash
source "{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}/app/.env.local" && \
python3 /tmp/consultar_leads.py "[FILTRO]"
```

### 3. Interpretar o resultado

**Contato {{CRM}} — campos importantes:**
- `firstName`, `lastName` — nome
- `email` — email
- `phone` — telefone
- `tags` — array de tags
- `dateAdded` — quando entrou
- `source` — origem (form, manual, API)
- `customFields` — campos customizados (UTM, score, etc)

### 4. Responder ao Gui

Formato resposta:
- "Período: X a Y"
- "Total: N leads"
- Top 5 com nome + email + tags + origem
- Se relevante: agrupado por tag, source ou pipeline


## Fluxo

```
[ Gui pede: /consultar-leads [filtro] ]
        ↓
[ 1. Carrega {{CRM}}_API_KEY + {{CRM}}_LOCATION_ID de app/.env.local ]
        ↓
[ 2. Parse filtro ]
        ├─ "hoje" | "semana" | "30 dias" | "90 dias" → período
        ├─ "tag:X" → segmento por tag
        ├─ "email:X" | "telefone:X" → busca específica
        └─ "pipeline:X" → roadmap futuro
        ↓
[ 3. Chama endpoint apropriado {{CRM}} API v2 ]
        ├─ GET /contacts/?locationId=... (default)
        └─ GET /contacts/search/duplicate (email/telefone)
        ↓
[ 4. Filtra resultado local ]
        ├─ Por dateAdded se busca por período
        └─ Por tag se busca por tag
        ↓
[ 5. Responde Gui formato canônico ]
        ├─ Período + total
        ├─ Top 5: nome + email + tags + source
        └─ Se relevante: agrupar por tag/source/pipeline
```

## Regras

- **Timeout 15s obrigatório** (Regra Inviolável #22)
- **Secret SÓ em `app/.env.local`** (Regra Inviolável #21)
- **Nunca exibir API key no output**
- Se API down → mensagem clara "{{CRM}} não respondeu — tentar novamente em alguns minutos"
- Se 401/403 → "{{CRM}}_API_KEY inválida ou expirada — Gui renovar no painel {{CRM}}"

## Próximas evoluções

- Endpoint `/opportunities/` para consultar pipeline + valor
- Cache local 5min pra reduzir consumo de quota da API
- Integração com `/disparar-newsletter` (Onda 10.4) — segmentar destinatários por filtro {{CRM}}
