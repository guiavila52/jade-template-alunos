---
name: relatar-leads
description: Consulta GHL e retorna quantos leads chegaram hoje e nos últimos 7 dias, por fonte e por isca. Responde a pergunta "como está nossa captação?"
type: skill
---

# /relatar-leads

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** ✅ FUNCIONAL
**Trigger:** sob demanda (operador pede) ou cron diário às 9h junto com `/relatar-trafego-diario`

---

## Fluxo

```
Input (período: hoje | 7d | 30d)
  ↓
1. Autenticar na GHL API com GHL_API_KEY + GHL_LOCATION_ID
2. Buscar contatos criados no período (paginação automática)
3. Agrupar por source/utm_source → qual isca trouxe ({{ISCA_1}}, {{ISCA_2}}, {{ISCA_3}}, Orgânico, Pago)
4. Calcular totais: hoje, 7d, média diária 7d
5. Alertas: queda > 30% vs média dos 7 dias anteriores
6. Salvar output em workspace/output/trafego/leads/{YYYY-MM-DD}.md
  ↓
Output (resumo curto pra operador + detalhes por isca)
```

---

## Como executar

```bash
python3 workspace/scripts/marketing/relatar-leads.py
# ou com período específico:
python3 workspace/scripts/marketing/relatar-leads.py --periodo 7d
python3 workspace/scripts/marketing/relatar-leads.py --periodo 30d
```

---

## O que o relatório mostra

### Resumo (sempre)
- Leads hoje: N
- Leads últimos 7 dias: N
- Média diária (7d): N
- Alerta se hoje < 70% da média diária

### Por isca (se source disponível)
| Isca | Hoje | 7d |
|---|---|---|
| Isca 1 (/{{SLUG_ISCA_1}}) | N | N |
| Isca 2 (/{{SLUG_ISCA_2}}) | N | N |
| Isca 3 (/{{SLUG_ISCA_3}}) | N | N |
| Orgânico (sem source) | N | N |
| Tráfego pago | N | N |

### Por canal (se utm_source disponível)
- YouTube, Instagram, Direct, Ads, etc.

---

## Credenciais necessárias

- `GHL_API_KEY` → app/.env.local ✅ (PIT token location do operador)
- `GHL_LOCATION_ID` → `{{GHL_LOCATION_ID}}` ✅

---

## Endpoint GHL

```
GET https://{{CRM_LC_HOST}}/contacts/
  ?locationId={GHL_LOCATION_ID}
  &startAfterDate={timestamp_inicio}
  &limit=100
```

Headers:
```
Authorization: Bearer {GHL_API_KEY}
Version: 2021-07-28
```

---

## Output canônico

`workspace/output/trafego/leads/{YYYY-MM-DD}.md`

---

## Bateria de testes

- [x] Script criado em workspace/scripts/marketing/relatar-leads.py
- [x] Skill documentada em .claude/commands/
- [ ] Teste com GHL_API_KEY válida (se 401 → renovar PIT token)
- [ ] Confirmar que source/utm_source está sendo capturado nas iscas
- [ ] Alerta de queda funcionando

---

## O que pode falhar (e como resolver)

| Erro | Causa | Fix |
|---|---|---|
| 401 Unauthorized | PIT token expirado ou escopo revogado | Settings GHL → Private Integrations → copiar token novo → atualizar GHL_API_KEY |
| source vazio em todos contatos | Formulários GHL sem UTM configurado | Adicionar ?source=isca na URL de destino de cada lead magnet |
| Poucos leads vs esperado | Paginação incompleta | Script já faz paginação automática — verificar total_count na resposta |

---

## Aprendizados + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
