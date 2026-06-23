---
name: auditar-campanha
description: Diagnóstico profundo de campanha rodando — ranking de anúncios, gargalo do funil, ações priorizadas. Usar antes de escalar.
type: skill
---

# /auditar-campanha

**Status:** 🟢 MADURA
**Input:** `[campaign_id]` ou `todas`
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local`, passar como `meta_access_token`.
**Conta:** `{{META_ADS_ACCOUNT}}`

## Fluxo

### 1. Definir escopo

Se `campaign_id`: auditar essa campanha.
Se `todas`: `mcp__meta-ads__list_campaigns` com `status_filter: ACTIVE`.

### 2. Insights por anúncio (últimos 7 dias)

`mcp__meta-ads__list_insights`:
- `object_id`: [campaign_id]
- `meta_access_token`: [token]
- `date_range`: `last_7d`
- `level`: `ad`
- `compact`: false

Campos: impressions, clicks, ctr, cpm, cpc, spend, frequency, actions, cost_per_action_type

### 3. Insights por ad set

Mesma call com `level`: `adset`.

### 4. Ranquear anúncios

- **Winners (top 25%):** maior CTR E menor CPL, com >2.000 impressões
- **Average (50%):** dentro de 1 desvio padrão das médias
- **Losers (bottom 25%):** menor CTR E maior CPL, com >2.000 impressões
- **Fadiga:** frequency > 3.0 com impressões > 5.000

### 5. Diagnosticar gargalo

```
CPL alto / ROAS baixo?
├── CTR < 1%?
│   ├── Frequency > 3? → FADIGA → trocar criativo
│   └── Frequency < 2 + CTR baixo → CRIATIVO RUIM → /criar-criativo
├── CTR ok + CPL alto?
│   └── LANDING PAGE → acionar @desenvolvedor-frontend + @copywriter
├── CPM > R$30?
│   └── PÚBLICO PEQUENO → ampliar targeting
└── Leads ok + vendas baixas?
    └── OFERTA ou COMERCIAL → acionar @sdr + @copywriter
```

### 6. 3-5 ações priorizadas

Para cada ação: o que fazer, por quê (dado), como executar, quem aprova.

### 7. Output

`workspace/output/trafego/auditorias/YYYY-MM-DD-[campanha].md`:
```
# Auditoria — [Campanha] — YYYY-MM-DD

## Situação geral
[funcionando / com problema / crítica]

## Ranking de anúncios
| Anúncio | CTR | CPM | CPL | Impressões | Freq | Status |
|---|---|---|---|---|---|---|
| [nome] | % | R$ | R$ | N | X | ✅/❌ |

## Gargalo identificado
[diagnóstico]

## 5 ações recomendadas
1. [AUTOMÁTICO/GUI] Ação — justificativa com dado
```
