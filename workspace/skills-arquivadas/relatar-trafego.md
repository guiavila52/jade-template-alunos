---
name: relatar-trafego
description: Relatório semanal de campanhas Meta Ads + Google Ads em curso. ROI/ROAS, CPM, CTR, CPL, ranking criativos, alertas (fadiga, estagnação, CPL fora da meta), recomendações. Output em workspace/output/trafego/relatorios/YYYY-MM-DD-relatorio.md. Roda manual ou via cron semanal (segundas 7h).
model: claude-sonnet-4-5
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

## Quando usar

- Manualmente: `/relatar-trafego`
- Cron semanal: segundas 7h (a configurar via launchd/cron-tab)
- Sob demanda quando Gui pergunta "como tá o tráfego pago?"

## Fontes de dados

| Fonte | Vars `app/.env.local` |
|---|---|
| Meta Ads API | `META_ADS_ACCESS_TOKEN`, `META_ADS_ACCOUNT_ID` |
| Google Ads API | `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_REFRESH_TOKEN` |
| GA4 (atribuição) | `GA4_PROPERTY_ID`, `GOOGLE_SERVICE_ACCOUNT_JSON` |

## KPIs canônicos do squad

| KPI | Definição | Meta padrão |
|---|---|---|
| CPM | Custo por mil impressões | ≤ R$30 |
| CPC | Custo por clique | ≤ R$2 |
| CTR | Cliques / impressões | ≥ 1.5% |
| CPL | Custo por lead | ≤ R$15 |
| ROAS | Receita / investimento | ≥ 2x |

Metas podem ser override por campanha via `config-campanha.json`.

## Estrutura do relatório

```markdown
# Relatório semanal tráfego — YYYY-MM-DD

## Sumário executivo

- N campanhas ativas
- R$ X total investido na semana
- Y leads gerados | Z conversões
- ROAS médio: A.B x

## Por campanha

| ID | Nome | Plataforma | Status | CPM | CTR | CPL | ROAS | Δ vs semana anterior |
|---|---|---|---|---|---|---|---|---|

## Ranking criativos (top 5 + bottom 3)

[ordenar por CTR ou CPL conforme objetivo da campanha]

## Alertas

🔴 [ALERTA TIPO] - [campanha] - [detalhe + ação sugerida]

## Recomendações

1. [ação priorizada]
2. ...

## Próxima ação

[O que fazer na próxima semana]
```

## Detecção de alertas

| Tipo | Critério | Severidade | Ação sugerida |
|---|---|---|---|
| **Fadiga criativa** | CTR cai ≥20% em 3 dias | 🟠 HIGH | Trocar criativo (despachar /criar-criativo) |
| **Campanha estagnada** | 0 conversões em 7 dias | 🔴 CRITICAL | Pausar OU ajustar público |
| **CPL fora da meta** | CPL ≥ 2x meta da campanha | 🟠 HIGH | /otimizar-campanha |
| **ROAS < 1x** | Investindo mais que retornando | 🔴 CRITICAL | Pausar imediatamente |
| **Frequência alta** | Frequency >= 4 | 🟡 MEDIUM | Refresh de público OU criativo |

## Output canônico

```
workspace/output/trafego/relatorios/YYYY-MM-DD-relatorio.md
```

E atualiza `workspace/output/trafego/relatorios/mapa.md` com entrada nova.

## Cron semanal (a configurar)

Quando launchd/cron-tab for setup:
1. Roda toda segunda-feira 7:00 BRT
2. Salva relatório em `workspace/output/trafego/relatorios/`
3. Se houver alerta CRITICAL: notifica Gui via Telegram/email
4. Se tudo OK: log silencioso

## Fluxo

```
[ Trigger: manual /relatar-trafego OU cron segunda 7h ]
        ↓
[ Carregar credenciais (.env.local via dotenv) ]
        ↓
[ Fetch Meta Ads API: campanhas + criativos + métricas (últimos 7 dias) ]
        ↓
[ Fetch Google Ads API: idem ]
        ↓
[ Fetch GA4: atribuição + conversões ]
        ↓
[ Calcular KPIs por campanha + agregados ]
        ↓
[ Detectar alertas (5 tipos) ]
        ↓
[ Ranking criativos (top 5 + bottom 3) ]
        ↓
[ Gerar markdown estruturado ]
        ↓
[ Salvar relatório + atualizar MAPA ]
        ↓
   ⟶ Se CRITICAL: notifica Gui
   ⟶ Apresenta ao Gui (sumário + path)
```

## Restrições

- NUNCA expor valores de faturamento das empresas em copy de relatório (ok dentro do relatório técnico interno, NÃO em copy de marketing)
- Edição da skill via Bash/Python (Regra #8)

## Captura de aprendizado (Regra #19)

`squads/trafego/aprendizados.md` quando alerta novo é detectado pela 1ª vez OU quando heurística falha.

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro Gui testar — testa antes.
