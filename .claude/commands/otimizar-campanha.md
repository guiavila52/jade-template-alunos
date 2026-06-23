---
name: otimizar-campanha
description: Executa otimizações automáticas (pausar losers, fadiga) e apresenta ao operador o que precisa de aprovação. Usar após auditar-campanha.
type: skill
---

# /otimizar-campanha

**Status:** 🟢 MADURA
**Input:** `[campaign_id]` ou `todas`
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local`, passar como `meta_access_token`.
**Conta:** `{{META_ADS_ACCOUNT}}`

## Regras de autonomia

**Executar automaticamente (sem pedir):**
- Pausar anúncio: CTR < 0.3% AND impressions > 5.000 AND cpm > CPM_médio da campanha
- Pausar anúncio em fadiga: frequency > 4.0 AND CTR caindo >30% vs semana anterior

**Sempre pedir aprovação do operador:**
- Aumentar orçamento > 20%
- Pausar ad set inteiro
- Pausar campanha inteira
- Mudar targeting

## Fluxo

### 1. Diagnóstico interno

Executar mesma lógica do `/auditar-campanha`:
- `mcp__meta-ads__list_insights` com `level: ad`, `date_range: last_7d`
- `meta_access_token`: [token]
- Calcular CTR_médio, CPM_médio da campanha

### 2. Ações automáticas

Para cada anúncio candidato:

`mcp__meta-ads__update_ad`:
- `ad_id`: [id]
- `meta_access_token`: [token]
- `status`: `PAUSED`

Registrar: "[Nome] pausado — CTR [X]% com [N] impressões"

### 3. Lista de aprovações para operador

```
📋 Aguardando sua aprovação:

1. AUMENTAR ORÇAMENTO — [Campanha]
   De: R$X/dia → Para: R$Y/dia
   Motivo: ROAS [X]x nos últimos 7 dias
   Responda: "aprovar 1"

2. PAUSAR AD SET — [Nome]
   Motivo: [N] dias sem conversão com R$[X] gasto
   Responda: "aprovar 2"
```

### 4. Executar aprovações

Após resposta do operador:

`mcp__meta-ads__update_campaign`:
- `campaign_id`: [id]
- `meta_access_token`: [token]
- `daily_budget`: [novo valor em centavos]

`mcp__meta-ads__update_ad_set`:
- `ad_set_id`: [id]
- `meta_access_token`: [token]
- `status`: `PAUSED`

### 5. Log de otimizações

`workspace/output/trafego/logs-otimizacao/YYYY-MM.md`:
- Ações automáticas tomadas
- Aprovações executadas
- Resultado esperado

## Bateria de testes (Regra §6)

Antes de marcar a entrega desta skill como pronta: bateria de testes externa obrigatória — revisor independente do produtor valida o output real (não checklist do próprio produtor). Jade nunca pede pro operador testar. Falhou na bateria → volta pro produtor com finding específico antes de reportar.
