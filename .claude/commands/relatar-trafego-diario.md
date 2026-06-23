---
name: relatar-trafego-diario
description: Health-check diário do tráfego Meta Ads — métricas, alertas, decisões automáticas. Cron todo dia 9h BRT.
type: skill
---

# /relatar-trafego-diario

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** 🟢 MADURA
**Cron:** `0 9 * * *` (todo dia 09:00 BRT)

## Contexto

Você é o @gestor-trafego. Execute este fluxo completo. Ao final, apresente relatório curto e direto.

**Conta:** `{{META_ADS_ACCOUNT}}`
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local` e passar como `meta_access_token` em TODOS os calls MCP.

---

## Fluxo

### 1. Listar campanhas ativas

Use `mcp__meta-ads__list_campaigns`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token do .env.local]
- `status_filter`: `ACTIVE`
- `page_size`: 25

Se nenhuma campanha ativa → reportar "Sem campanhas ativas" e verificar saldo.

### 2. Puxar métricas de ontem por anúncio

Para cada campanha ativa, use `mcp__meta-ads__list_insights`:
- `object_id`: [campaign_id]
- `meta_access_token`: [token]
- `date_range`: `{"since": "ONTEM", "until": "ONTEM"}` (YYYY-MM-DD)
- `level`: `ad`
- `compact`: true
- `page_size`: 50

Campos relevantes: `ad_id`, `ad_name`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`, `spend`, `frequency`, `actions`, `cost_per_action_type`

### 3. Puxar média 7 dias

Mesma call com `date_range`: `{"since": "7_DIAS_ATRAS", "until": "ONTEM"}` e `level`: `campaign`

Calcular: CPM_7d_média, CTR_7d_média, CPL_7d_média

### 4. Verificar saldo

Use `mcp__meta-ads__read_ad_account`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]

Verificar `balance` e `amount_spent`.

### 5. Detectar alertas

| Condição | Alerta |
|---|---|
| CPM_ontem > CPM_7d × 1.30 | 🔴 CPM ALTO |
| CTR_ontem < CTR_7d × 0.70 | 🔴 CTR BAIXO |
| Anúncio DISAPPROVED | 🔴 CRIATIVO REPROVADO |
| saldo = 0 ou < orçamento diário × 3 | 🟡 SALDO BAIXO |
| frequency > 3.0 | 🟡 FADIGA |

### 6. Decisões automáticas (sem pedir aprovação)

Pausar anúncio se: CTR < 0.3% AND impressions > 5.000 AND cpm > CPM_7d_média

Use `mcp__meta-ads__update_ad`:
- `ad_id`: [id]
- `meta_access_token`: [token]
- `status`: `PAUSED`

### 7. Output

Criar `workspace/output/trafego/diarios/YYYY-MM-DD.md`:

```
# Análise diária — YYYY-MM-DD

## Status
- N campanhas ativas | Y pausadas

## Alertas
[listar ou "✅ Sem alertas"]

## Métricas ontem
| Métrica | Ontem | Média 7d | Δ |
|---|---|---|---|
| Gasto | R$ | R$ | % |
| Impressões | | | % |
| CPM | R$ | R$ | % |
| CTR | % | % | pts |
| CPC | R$ | R$ | % |
| CPL | R$ | R$ | % |

## Saldo da conta
R$ [X] — [N] dias restantes estimados

## Ações automáticas tomadas
[lista ou "Nenhuma"]

## Decisões pra operador aprovar
[lista ou "Nenhuma"]
```
