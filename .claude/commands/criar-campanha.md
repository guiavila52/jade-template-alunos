---
name: criar-campanha
description: Cria estrutura completa de campanha Meta Ads — campanha + ad set + targeting. Nasce pausada. Aguarda criativo para ativar.
type: skill
---

# /criar-campanha

**Status:** 🟢 MADURA
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local`, passar como `meta_access_token` em TODOS os calls.
**Conta:** `{{META_ADS_ACCOUNT}}`

Antes de executar, ler:
1. `segundo-cerebro/01-identidade/icp.md`
2. `segundo-cerebro/02-negocios/produtos-servicos.md`
3. `segundo-cerebro/03-operacao/meta-ads-historico.md`

## Inputs obrigatórios (perguntar ao operador)

1. **Produto:** qual produto ({{PRODUTO_PRINCIPAL}}, {{PRODUTO_ENTRADA}}, Mentoria, Consultoria, Lead Magnet)
2. **Objetivo:** LEADS, OUTCOME_SALES, OUTCOME_TRAFFIC, ou OUTCOME_AWARENESS
3. **Orçamento diário:** valor em R$
4. **Público-alvo:** descrição em linguagem natural
5. **Link de destino:** URL da landing page

## Mapeamento de objetivos

| Descrição | Objetivo Meta | Optimization goal |
|---|---|---|
| Leads | LEAD_GENERATION | LEAD_GENERATION |
| Vendas | OUTCOME_SALES | OFFSITE_CONVERSIONS |
| Cliques | OUTCOME_TRAFFIC | LINK_CLICKS |
| Awareness | OUTCOME_AWARENESS | THRUPLAY |

## Fluxo

### 1. Pesquisar interesses

`mcp__meta-ads__search_interests`:
- `query`: [keyword do público]
- `meta_access_token`: [token]
- `page_size`: 10

Fazer 3-5 buscas com keywords diferentes.
Selecionar 3-8 interesses mais relevantes com audiência >500k.

### 2. Estimar público

`mcp__meta-ads__estimate_audience_size`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `targeting`: {
    "age_min": 25, "age_max": 55,
    "geo_locations": {"countries": ["BR"]},
    "interests": [{"id": "[id]"}, ...]
  }

Público ideal: 500k a 5M. Menor: ampliar. Maior: restringir.

### 3. Criar campanha

`mcp__meta-ads__create_campaign`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `name`: "[Produto] — [Objetivo] — [YYYY-MM-DD]"
- `objective`: [objetivo Meta]
- `status`: `PAUSED`
- `campaign_budget_optimization`: true
- `daily_budget`: [valor em centavos, ex: 5000 = R$50]

Salvar `campaign_id`.

### 4. Criar ad set

`mcp__meta-ads__create_ad_set`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `campaign_id`: [campaign_id]
- `name`: "[Produto] — [Público] — [YYYY-MM-DD]"
- `optimization_goal`: [optimization_goal]
- `billing_event`: `IMPRESSIONS`
- `status`: `PAUSED`
- `targeting`: {
    "age_min": [idade_min], "age_max": [idade_max],
    "geo_locations": {"countries": ["BR"]},
    "interests": [lista de interesses selecionados]
  }

Salvar `ad_set_id`.

### 5. Output

`workspace/output/trafego/campanhas/YYYY-MM-DD-[slug].md`:
```
# Campanha criada — [Produto] — YYYY-MM-DD

## IDs
- Campaign ID: [id]
- Ad Set ID: [id]
- Conta: {{META_ADS_ACCOUNT}}

## Configuração
- Objetivo: [objetivo]
- Orçamento: R$ [valor]/dia
- Público estimado: [N] pessoas
- Interesses: [lista]
- Link destino: [URL]

## Próximo passo
/publicar-criativo — informar Ad Set ID: [ad_set_id]

## Status
⏸️ PAUSED — aguardando criativo + aprovação do operador
```

Reportar ao operador: campaign_id, ad_set_id, tamanho do público, próximo passo.
