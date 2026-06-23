---
name: relatar-trafego-trimestral
description: Análise estratégica trimestral Meta Ads — continuar/pivotar canais, gargalo do funil, QoQ. Cron dia 1 jan/abr/jul/out 9h.
type: skill
---

# /relatar-trafego-trimestral

**Status:** 🟢 MADURA
**Cron:** `0 9 1 1,4,7,10 *`
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local`, passar como `meta_access_token`.
**Conta:** `{{META_ADS_ACCOUNT}}`

## Fluxo

### 1. Período trimestral

Q1: jan-mar | Q2: abr-jun | Q3: jul-set | Q4: out-dez

### 2. Insights QoQ

`mcp__meta-ads__list_insights` com `level`: `campaign`:
- `date_range` trimestre atual
- `date_range` trimestre anterior
- `meta_access_token`: [token]

### 3. Análise por produto

Agrupar campanhas por produto ({{PRODUTO_PRINCIPAL}}, {{PRODUTO_ENTRADA}}, Mentoria, etc.)
Calcular por grupo: gasto, CPL, ROAS, tendência QoQ

### 4. Decisão: continuar/otimizar/pivotar

- ✅ CONTINUAR — ROAS positivo, tendência boa
- 🟡 OTIMIZAR — resultados mediocres, 1 trimestre de teste
- 🔴 PIVOTAR — 2 trimestres negativos, matar canal

### 5. Diagnóstico do gargalo

```
CTR baixo → criativo ou público
Alto CTR + alto CPL → landing page
Baixo CPL + baixas vendas → oferta ou comercial
Alto spend + zero conversão → targeting errado
```

### 6. Output

`workspace/output/trafego/trimestrais/YYYY-QX.md` com:
- Resumo executivo (5 frases)
- Tabela QoQ por campanha
- Decisões continuar/otimizar/pivotar
- Plano trimestre seguinte
