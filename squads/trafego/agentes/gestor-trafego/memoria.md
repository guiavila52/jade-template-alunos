# Memória — agente trafego (squad-trafego)

## Estado atual

- Squad-trafego em construção. Agente trafego responsável por criativos Meta Ads + Google Ads + relatórios + otimizações.
- Foco macro 08/05/2026 (Onda 2): pegar conteúdo orgânico que está performando bem e impulsionar via Meta Ads. Squad inteiro fazendo tráfego pago pra time/empresa.

## Cadeia de despacho — orgânico → pago

```
Gui dispara /impulsionar-organico <URL ou path>
        ↓
Jade detecta input → roteia
        ↓
trafego (análise) — métricas + hooks que funcionaram → analise-organico.md
        ↓
copywriter — 3-5 variações de copy pra ad → copies-variantes.md
        ↓
trafego (config) — público + lance + orçamento + KPI → config-campanha.json
        ↓
Jade apresenta ao Gui → aprovação
        ↓
trafego sobe via Meta Ads API → campanha_id
        ↓
/relatar-trafego (semanal) acompanha
        ↓
/otimizar-campanha (sob demanda) ajusta
```

## KPIs canônicos do squad

| KPI | Definição | Meta padrão |
|---|---|---|
| CPM | Custo por mil impressões | ≤ R$30 |
| CPC | Custo por clique | ≤ R$2 |
| CTR | Cliques / impressões | ≥ 1.5% |
| CPL | Custo por lead | ≤ R$15 |
| ROAS | Receita / investimento | ≥ 2x |

## Skills relacionadas

- `/criar-criativo` — criativo do zero (sem orgânico de referência)
- `/impulsionar-organico` — orgânico bom → campanha Meta Ads
- `/relatar-trafego` — relatório semanal (manual ou cron seg 7h)
- `/otimizar-campanha` — heurísticas pause/scale/iterar
- `/criar-carrossel` + `/criar-carrossel-de-video` — origem de criativo orgânico (Onda 1)

## Princípios invioláveis

- Métricas públicas: NUNCA copy expõe faturamento das empresas (memória `feedback_metricas_publicas_gui.md`). Usar usuários, alunos, criadores.
- Vocabulário aproxima lead: banidas qualificação/avaliação/screening/triagem/fit (memória `feedback_vocabulario_aproxima_lead.md`).
- Cormorant Garamond NUNCA em dígito no criativo visual (Regra #188 absoluta).
- Aprovação do Gui antes de subir QUALQUER campanha.
- Nunca pausar campanha com ROAS ≥ 2x.
- Nunca dobrar orçamento de uma vez (scaleia 20%/dia max — fadiga).

## Memórias relevantes (ler ao despachar)

- `~/.claude/projects/-Users-{{operador_slug}}-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/memory/project_foco_carrossel_youtube_e_meta_ads.md` — foco macro
- `~/.claude/.../memory/feedback_metricas_publicas_gui.md` — banido faturamento
- `~/.claude/.../memory/feedback_vocabulario_aproxima_lead.md` — banidas qualif/avaliação/screening
- `~/.claude/.../memory/feedback_propagacao_correcoes.md` — Regra #19

## Vars Meta Ads / Google Ads

Em `app/.env.local`:
- `META_ADS_ACCESS_TOKEN`, `META_ADS_ACCOUNT_ID`
- `META_APP_ID`, `META_APP_SECRET`
- `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_REFRESH_TOKEN`
- `GA4_PROPERTY_ID`, `GOOGLE_SERVICE_ACCOUNT_JSON`

## Última atualização

2026-05-08 ~13:15 UTC — Onda 2 da rotina autônoma (Meta Ads / orgânico→pago)
