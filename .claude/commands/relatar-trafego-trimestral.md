---
name: relatar-trafego-trimestral
description: Gera analise estrategica trimestral + decisao continuar/pivotar canais + identificacao do gargalo principal do funil.
type: skill
---

# /relatar-trafego-trimestral

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** ⚪ ESQUELETO
**Cron:** `0 9 1 1,4,7,10 *` (1 de jan/abr/jul/out 09:00 BRT)


## Fluxo

```
Input (Trimestre anterior fechado)
  ↓
1. Fetch dados Meta Marketing API (campanhas, métricas, eventos)
2. Calcular métricas macro (ROI, CPM, CTR, CAC, ROAS)
3. Comparação temporal (YoY / MoM / vs 7d média)
4. Análise de tendências e gargalos
5. Gerar análise trimestral + continuar/pivotar
6. Detectar alertas e decisões automáticas (se aplicável)
7. Salvar output em workspace/output/trafego/trimestrais/{YYYY-QX}.md
  ↓
Output (relatório estratégico + decisões pra {{OPERADOR}})
```

## Input

Opcional: `[YYYY-QX]` (default: trimestre anterior fechado).

## O que fazer

Análise estratégica trimestral — decisão de continuar/pivotar canais + comparação ano anterior + identificação de gargalo principal.

### Métricas analisadas
1. Tendências de 3 meses (ROAS + CPL + CAC evolução)
2. Decisão continuar/pivotar canais (canal X tá pagando? não? matar)
3. Análise estratégica de funil — gargalo principal: tráfego? landing? oferta?
4. Comparação YoY (mesmo trimestre ano anterior)
5. Eficiência por persona/avatar
6. Benchmarks de mercado/concorrência (squad-radar consulta CPM/CPL benchmarks)

### Decisões executivas pra {{OPERADOR}}
- Apostar mais em X canal?
- Matar Y canal?
- Investir em canal novo (TikTok? LinkedIn? Pinterest?)
- Reestruturar funil
- Mudar oferta principal

## Output

`workspace/output/trafego/trimestrais/{YYYY-QX}.md` — formato canônico ver `segundo-cerebro/03-operacao/processo-gestor-trafego.md`.

## Dependências

- Meta Ads token ✅
- Histórico mínimo de 12 meses
- `/relatar-trafego-mensal` 🟢 maduro

## Bateria de testes #24

**Pós-implementação:**
- [ ] YoY comparison funcionando
- [ ] Cross-reference com radar pra benchmarks
- [ ] Output salvo + cron configurado

## Bloqueio atual

Esqueleto. A implementar pós-3 meses de dados acumulados.

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{OPERADOR}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
