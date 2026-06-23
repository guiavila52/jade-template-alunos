---
name: relatar-trafego-anual
description: Análise estratégica anual Meta Ads — ROI do ano, lições, plano ano seguinte, budget allocation. Cron 1 jan 10h.
type: skill
---

# /relatar-trafego-anual

**Status:** 🟢 MADURA
**Cron:** `0 10 1 1 *`
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local`, passar como `meta_access_token`.
**Conta:** `{{META_ADS_ACCOUNT}}`

## Fluxo

### 1. Insights do ano completo

`mcp__meta-ads__list_insights`:
- `date_range`: `{"since": "YYYY-01-01", "until": "YYYY-12-31"}`
- `level`: `campaign`
- `meta_access_token`: [token]

### 2. Insights ano anterior (YoY)

Mesma call com ano anterior.

### 3. Top criativos do ano

`list_insights` com `level`: `ad`, período anual.
Top 5 winners + 5 piores.

### 4. Sazonalidade

Ler relatórios de `workspace/output/trafego/mensais/` para identificar:
- Meses com melhor CPL
- Meses com pior CPM

### 5. Análise por produto

Para cada produto: gasto, leads, CPL, ROAS, decisão: manter/escalar/pivotar

### 6. Output

`workspace/output/trafego/anuais/YYYY.md`:
- Resumo executivo (10 frases)
- ROI macro YoY
- LTV/CAC do ano
- Top 5 criativos (lições)
- Sazonalidade (calendário)
- Budget allocation ano seguinte
- Metas: CPL, ROAS, leads, vendas
