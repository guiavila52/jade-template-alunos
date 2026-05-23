---
name: impulsionar-organico
description: Pega post orgânico (URL Instagram, path do carrossel local ou URL LinkedIn) e cria campanha Meta Ads pra impulsionar. Trafego analisa engajamento orgânico, copywriter cria 3-5 variações de copy pra ad, trafego configura campanha (público, lance, orçamento), Jade aprova com Gui antes de subir. Output em workspace/output/trafego/YYYY-MM-DD-[slug]/.
model: claude-sonnet-4-5
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

## Quando usar

Post orgânico (carrossel/reels/post) está performando bem (engajamento >5%, salvamentos >50, CTR pra perfil >2%) e Gui quer escalar.

```
/impulsionar-organico <URL ou path>
```

Pra geração de criativo do zero (sem orgânico de referência), usar `/criar-criativo`.

## Memórias relevantes (ler antes)

1. `~/.claude/projects/-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/memory/project_foco_carrossel_youtube_e_meta_ads.md` — foco macro Onda 2
2. `~/.claude/.../memory/feedback_metricas_publicas_gui.md` — copy nunca expõe faturamento
3. `~/.claude/.../memory/feedback_vocabulario_aproxima_lead.md` — banidas: qualificação/avaliação/screening/triagem/fit
4. `~/.claude/.../memory/feedback_propagacao_correcoes.md` — Regra #19

Vars Meta Ads no `app/.env.local`:
- `META_ADS_ACCESS_TOKEN`
- `META_ADS_ACCOUNT_ID`
- `META_APP_ID`, `META_APP_SECRET`

## Detecção de input

```
INPUT?
├─ URL Instagram (instagram.com/p/... ou /reel/...) → fetch via Graph API → métricas + media
├─ Path local de carrossel (workspace/output/carrosseis/[slug]/) → ler MAPA + slides
├─ URL LinkedIn (linkedin.com/posts/...) → fetch via API se token disponível, senão scrape
└─ Outro → ABORTA com erro claro
```

## Schema do briefing — passo a passo entre agentes

| De → Pra | Recebe | Entrega |
|---|---|---|
| **Jade → trafego (análise)** | URL/path + métricas orgânicas | `analise-organico.md` (engajamento, salvamentos, CTR-perfil, comentários relevantes, hooks que funcionaram) |
| **trafego → copywriter** | analise-organico.md + Light Copy framework | `copies-variantes.md` (3-5 variações de copy pra ad — header, body, CTA) |
| **copywriter → trafego (config)** | copies aprovadas | `config-campanha.json` (público, orçamento, lance, KPI alvo, criativo selecionado) |
| **trafego → Jade** | config-campanha.json | aprovação Gui antes de subir |
| **Jade → Gui** | sumário visual | OK / NÃO |
| **trafego (após OK)** | config aprovada | sobe campanha via Meta Ads API + retorna campaign_id |

## Critérios de "orgânico bom" pra impulsionar

| Métrica | Meta mínima |
|---|---|
| Engajamento (likes+comments+saves)/impressions | ≥ 5% |
| Salvamentos | ≥ 50 (carrossel) ou ≥ 20 (reels) |
| CTR pra perfil | ≥ 2% |
| Comentários relevantes (não emoji) | ≥ 10 |
| Tempo desde publicação | 24-72h (não muito quente, não muito frio) |

Se não atender ≥3 critérios: NÃO impulsionar — recomendar /criar-criativo do zero.

## Output canônico

```
workspace/output/trafego/YYYY-MM-DD-[slug]/
├── analise-organico.md       # métricas + hooks que funcionaram
├── copies-variantes.md       # 3-5 variações pra ad
├── config-campanha.json      # público, lance, orçamento, KPIs
├── aprovacao-gui.md          # decisão do Gui
├── campanha-id.txt           # ID da campanha após subir
└── mapa.md                   # Regra #10
```

## Restrições

- Orçamento default: R$50/dia (Gui pode override)
- Público default: lookalike 1% audiência atual
- KPI default: CPM + CTR-perfil
- NUNCA subir campanha sem aprovação explícita do Gui
- NUNCA copy expor faturamento (Regra `feedback_metricas_publicas_gui.md`)
- NUNCA usar palavras banidas (Regra `feedback_vocabulario_aproxima_lead.md`)
- Cormorant Garamond NUNCA em dígito no criativo (Regra #188 — vale pra criativos visuais também)
- Edição da skill via Bash/Python (Regra #8)

## Fluxo

```
[ Gui dispara /impulsionar-organico <URL ou path> ]
        ↓
[ Jade detecta input ]
   │
   ├─ Inválido → ABORTA
   └─ Válido → segue
        ↓
[ trafego (análise) ]
   fetch métricas + content + comentários
   output: analise-organico.md
        ↓
   ⟶ se NÃO atende ≥3 critérios: PARA + recomenda /criar-criativo
        ↓
[ copywriter ]
   recebe analise + Light Copy
   produz: 3-5 variações de copy pra ad
        ↓
[ trafego (config) ]
   recebe copies + analise
   produz: config-campanha.json (público, lance, orçamento, KPI)
        ↓
[ Jade apresenta ao Gui ]
   sumário visual + config + estimativas
        ↓
   ⟶ Gui aprova / rejeita / pede ajuste
        ↓
[ trafego sobe via Meta Ads API ]
   retorna campaign_id
        ↓
[ Atualizar MAPA + aprendizado ] (Regra #10 + #19)
        ↓
   ⟶ FIM (campanha em curso; /relatar-trafego acompanha semanalmente)
```

## Captura de aprendizado (Regra #19)

`squads/trafego/agentes/gestor-trafego/aprendizados.md` + `squads/trafego/aprendizados.md` se for padrão do squad.

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro Gui testar — testa antes.
