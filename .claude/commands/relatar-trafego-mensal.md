---
name: relatar-trafego-mensal
description: Análise mensal estratégica Meta Ads — MoM, funil completo, realocação de orçamento. Cron dia 1 de cada mês 8h.
type: skill
---

# /relatar-trafego-mensal

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** 🟢 MADURA
**Cron:** `0 8 1 * *`
**Input opcional:** `[YYYY-MM]` (default: mês anterior)

**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local` e passar como `meta_access_token` em TODOS os calls MCP.
**Conta:** `{{META_ADS_ACCOUNT}}`

## Fluxo

### 1. Definir período

Mês atual: `{"since": "YYYY-MM-01", "until": "YYYY-MM-[último_dia]"}`
Mês anterior (MoM): idem para o mês anterior

### 2. Insights mensais por campanha

`mcp__meta-ads__list_insights`:
- `object_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `date_range`: período atual
- `level`: `campaign`
- `compact`: false
- `page_size`: 50

### 3. Insights mês anterior (MoM)

Mesma call com período anterior.

### 4. Insights por anúncio (ranking de criativos)

`mcp__meta-ads__list_insights` com `level`: `ad`, período atual.

### 5. Calcular métricas

| Métrica | Fórmula |
|---|---|
| ROAS | action_values[purchase] / spend |
| CAC | spend / compradores únicos |
| CPL | spend / leads |
| Variação MoM | (atual - anterior) / anterior × 100 |

### 6. Ranking de criativos

Top 3 winners (maior CTR/ROAS, >1000 impressões)
Bottom 3 losers (menor CTR, >1000 impressões)
Em fadiga (frequency > 3 no período)

### 7. Output

`workspace/output/trafego/mensais/YYYY-MM.md`:

```
# Análise mensal — MMMM/YYYY

## Resumo executivo
[3-5 frases]

## Métricas macro
| Métrica | Mês atual | Mês anterior | Δ MoM |
|---|---|---|---|
| Gasto | R$ | R$ | % |
| Leads | | | % |
| CPL | R$ | R$ | % |
| Conversões | | | % |
| ROAS | | | pts |

## Top 3 criativos do mês
1. [Nome] — CTR X%, CPL R$Y

## Bottom 3 (renovar)
1. [Nome] — CTR X%, motivo

## Funil do mês
Impressões → Cliques (CTR%) → Leads (Conv%) → Vendas (Conv%)
Gargalo: [identificado]

## Decisões recomendadas
[3-5 ações]
```
