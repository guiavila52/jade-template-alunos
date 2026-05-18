---
name: relatar-trafego-diario
description: Gera health-check diario do trafego pago + alertas (CPM, CTR, criativos rejeitados, saldo) — cron todo dia 9h BRT.
type: skill
---

# /relatar-trafego-diario

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** ⚪ ESQUELETO (a implementar com Meta Marketing API)
**Cron:** `0 9 * * *` (todo dia 09:00 BRT)


## Fluxo

```
Input (Hoje (cron 9h))
  ↓
1. Fetch dados Meta Marketing API (campanhas, métricas, eventos)
2. Calcular métricas macro (ROI, CPM, CTR, CAC, ROAS)
3. Comparação temporal (YoY / MoM / vs 7d média)
4. Análise de tendências e gargalos
5. Gerar health-check diário + alertas
6. Detectar alertas e decisões automáticas (se aplicável)
7. Salvar output em workspace/output/trafego/diarios/{YYYY-MM-DD}.md
  ↓
Output (relatório estratégico + decisões pra {{OPERADOR}})
```

## Input

Sem argumentos (rota cron).

## O que fazer

Análise diária do tráfego pago — health-check + alertas.

### Métricas analisadas
1. Status das campanhas ativas (rodando? pausadas? aprovação?)
2. Orçamento gasto vs planejado (hoje vs 7d média)
3. CPM ontem vs média 7 dias (alerta se > 30% acima)
4. CTR ontem vs média 7 dias (alerta se > 30% abaixo)
5. Criativos rejeitados pela Meta (alerta imediato)
6. Saldo da conta de ads (alerta se < 3 dias de orçamento)
7. Eventos webhook Meta (suspensão de conta, mudança de status)

### Decisões automáticas (Jade decide, executa)
- Pausar criativo com CTR < 0.3% após >5k impressões + CPM acima da média
- Notificar {{OPERADOR}} se conta de ads suspensa
- Notificar {{OPERADOR}} se saldo < 3 dias

### Decisões pra {{OPERADOR}} aprovar
- Mudar orçamento > 30%
- Criar criativo novo
- Mudar público estrutural

## Output

`workspace/output/trafego/diarios/{YYYY-MM-DD}.md` — formato canônico ver `segundo-cerebro/03-operacao/processo-gestor-trafego.md` (seção "ANÁLISE DIÁRIA").

## Dependências

- Meta Ads token funcional ✅ (validado 11/05/2026)
- Conta de ads `act_1321128045938616` acessível ✅
- MCP Meta Ads {{mcp_provider}} OU integração direta via Marketing API

## Bateria de testes #24

**Pré-implementação (esqueleto atual):**
- [x] Arquivo criado em .claude/commands/
- [x] Estrutura mínima + agente alvo
- [x] Documentado em processo-gestor-trafego.md

**Pós-implementação funcional:**
- [ ] Integração Marketing API funcionando
- [ ] Output salvo em path canônico
- [ ] Alertas funcionando
- [ ] Decisões automáticas executando (com idempotência)
- [ ] Cron `/schedule` configurado

## Bloqueio atual

Esqueleto. A implementar pós-validação ponta-a-ponta do MCP Meta Ads {{mcp_provider}} v1.1.0.

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{OPERADOR}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
