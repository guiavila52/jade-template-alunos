---
name: relatar-trafego-anual
description: Gera analise estrategica anual do trafego pago + plano ano seguinte + budget allocation + roadmap (cron 1jan 10h).
type: skill
---

# /relatar-trafego-anual

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** ⚪ ESQUELETO
**Cron:** `0 10 1 1 *` (1 de janeiro 10:00 BRT)


## Fluxo

```
Input (Ano anterior fechado)
  ↓
1. Fetch dados Meta Marketing API (campanhas, métricas, eventos)
2. Calcular métricas macro (ROI, CPM, CTR, CAC, ROAS)
3. Comparação temporal (YoY / MoM / vs 7d média)
4. Análise de tendências e gargalos
5. Gerar análise estratégica anual + plano ano seguinte
6. Detectar alertas e decisões automáticas (se aplicável)
7. Salvar output em workspace/output/trafego/anuais/{YYYY}.md
  ↓
Output (relatório estratégico + decisões pra Gui)
```

## Input

Opcional: `[YYYY]` (default: ano anterior fechado).

## O que fazer

Análise estratégica anual + plano ano seguinte + budget allocation + metas + roadmap canais novos.

### Métricas analisadas
1. ROI macro do ano (todos os canais consolidados)
2. Evolução vs ano anterior (YoY)
3. LTV/CAC do ano (lifetime value vs custo de aquisição)
4. Lições do ano: o que funcionou? o que falhou?
5. Tendências detectadas (sazonalidade real do negócio {{NOME_OPERADOR}})
6. Budget allocation pro ano seguinte
7. Roadmap de canais novos a testar

### Decisões estratégicas pra Gui
- Budget total ano seguinte
- Distribuição por canal/produto
- Metas anuais (CPL, ROAS, leads, vendas)
- Pessoas a contratar (squad-trafego precisa expansão humana?)
- Pivot estratégico se necessário

## Output

`workspace/output/trafego/anuais/{YYYY}.md` — plano estratégico anual completo + formato canônico ver `segundo-cerebro/03-operacao/processo-gestor-trafego.md`.

## Dependências

- 12 meses de dados via Marketing API
- `/relatar-trafego-trimestral` 🟢 maduro
- Cross-reference com financeiro (LTV requer dados de vendas)

## Bateria de testes #24

**Pós-implementação:**
- [ ] YoY funcionando
- [ ] LTV/CAC calculados
- [ ] Roadmap canais novos com benchmarks de mercado (via squad-radar)
- [ ] Output salvo + cron configurado

## Bloqueio atual

Esqueleto. A implementar pós-12 meses de dados acumulados + outras 3 cadências (diária/mensal/trimestral) 🟢 maduras.

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do Gui, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
