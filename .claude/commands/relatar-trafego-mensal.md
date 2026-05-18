---
name: relatar-trafego-mensal
description: Gera analise mensal estrategica do trafego pago + comparacao MoM + decisoes de realocacao de orcamento (cron dia 1 8h).
type: skill
---

# /relatar-trafego-mensal

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** ⚪ ESQUELETO
**Cron:** `0 8 1 * *` (dia 1 de cada mês 08:00 BRT)


## Fluxo

```
Input (Mês anterior fechado)
  ↓
1. Fetch dados Meta Marketing API (campanhas, métricas, eventos)
2. Calcular métricas macro (ROI, CPM, CTR, CAC, ROAS)
3. Comparação temporal (YoY / MoM / vs 7d média)
4. Análise de tendências e gargalos
5. Gerar análise mensal + MoM
6. Detectar alertas e decisões automáticas (se aplicável)
7. Salvar output em workspace/output/trafego/mensais/{YYYY-MM}.md
  ↓
Output (relatório estratégico + decisões pra {{OPERADOR}})
```

## Input

Opcional: `[YYYY-MM]` (default: mês anterior fechado).

## O que fazer

Análise mensal estratégica + comparação MoM + decisões de realocação de orçamento.

### Métricas analisadas
1. ROAS macro do mês (todas as campanhas combinadas)
2. CAC (Custo de Aquisição de Cliente) vs LTV
3. Comparação MoM (mês vs mês anterior)
4. Funil mensal completo: impressão → clique → lead → venda
5. Distribuição de orçamento por canal (Meta vs Google vs YouTube)
6. ROI por produto (Reverso vs Imersão vs Consultoria vs Mentoria)
7. Sazonalidade detectada

### Decisões estruturais
- Realocar orçamento entre canais
- Pausar/manter produto sub-performante
- Investir em testes A/B estruturais
- Identificar oportunidades de escala

## Output

`workspace/output/trafego/mensais/{YYYY-MM}.md` — formato canônico ver `segundo-cerebro/03-operacao/processo-gestor-trafego.md`.

## Dependências

- Meta Ads token ✅
- Histórico mínimo de 60 dias de dados (pra MoM)

## Bateria de testes #24

**Pós-implementação:**
- [ ] Comparação MoM funcionando
- [ ] DRE de tráfego (gasto vs receita atribuída)
- [ ] Output salvo + cron configurado

## Bloqueio atual

Esqueleto. A implementar pós-`/relatar-trafego` semanal estar 🟢 maduro.

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{OPERADOR}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
