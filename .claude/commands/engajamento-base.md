---
name: engajamento-base
description: Diagnóstico completo de engajamento e temperatura de toda a base de leads no GHL. Mostra quem está quente, morno ou frio. Essencial antes de lançamentos e para planejar aquecimento.
type: skill
---

# /engajamento-base

**Squad:** trafego
**Agente:** @gestor-trafego
**Status:** ✅ MADURA
**Trigger:** sob demanda (antes de lançamentos, quando operador perguntar "como está minha base?")

---

## Propósito

Diferente de `/relatar-leads` (que mostra captação nova), esta skill analisa **toda a base existente** e classifica cada lead por temperatura:

- ⭐ **Cliente** — já comprou algum produto (tag de cliente/aluno)
- 🔥 **Quente** — tag de interesse em mentoria/high ticket OU adicionado nos últimos 30 dias
- 🟡 **Morno** — tem email + WhatsApp, na base entre 30 e 90 dias
- 🔵 **Frio** — sem engajamento recente ou sem dados de contato

---

## Fluxo

```
Input (opcional: filtro por tag, top N leads)
  ↓
1. Autenticar na GHL API com GHL_API_KEY + GHL_LOCATION_ID
2. Buscar TODOS os contatos (paginação automática)
3. Classificar cada contato por temperatura
4. Contar por temperatura + qualidade dos dados (email/phone)
5. Top 20 tags mais frequentes na base
6. Listar leads quentes (até 50 no relatório)
7. Recomendação estratégica: base aquecida / morna / fria
8. Salvar em workspace/output/marketing/engajamento/{YYYY-MM-DD}.md
  ↓
Output: resumo de temperatura + leads quentes + recomendação
```

---

## Como executar

```bash
# Diagnóstico completo
python3 workspace/scripts/marketing/engajamento-base.py

# Filtrar apenas leads com tag específica
python3 workspace/scripts/marketing/engajamento-base.py --filtro mentoria

# Mostrar apenas top 50 leads mais quentes
python3 workspace/scripts/marketing/engajamento-base.py --top 50
```

---

## O que o relatório mostra

### Temperatura da Base
| Temperatura | Qtd | % |
|---|---|---|
| ⭐ Cliente | N | % |
| 🔥 Quente | N | % |
| 🟡 Morno | N | % |
| 🔵 Frio | N | % |

### Qualidade dos Dados
- Com email + WhatsApp (alcançável em todos os canais)
- Sem email (só WhatsApp)
- Sem WhatsApp (só email)

### Tags Mais Frequentes (Top 20)
Mapa de interesses da base — indica quais produtos/temas têm mais tração.

### Leads Quentes (lista com nome, email, WhatsApp, tags, dias na base)
Pronto para ação imediata: sequência de aquecimento, convite para live, oferta de mentoria.

### Recomendação Estratégica
- ✅ Base aquecida → pode abrir inscrições
- ⚠️ Base morna → precisa de live + email antes
- 🚨 Base fria → aquecimento urgente antes de lançamento

---

## Critérios de temperatura

### Tags que sinalizam 🔥 Quente (interesse em mentoria/high ticket)
```
mentoria, mentoria-interesse, mentoria-{{ANO_MES}}, high-ticket,
consultoria, interesse-mentoria, produto-entrada, webinar, aulao, aula-ao-vivo
```

### Tags que sinalizam ⭐ Cliente
```
cliente, aluno, produto-1, produto-2, produto-3,
comprou, pagou, produto-4
```

> Para adicionar tags ao critério: editar o script em `workspace/scripts/marketing/engajamento-base.py`, seções `TAGS_QUENTES` e `TAGS_CLIENTE`.

---

## Credenciais necessárias

- `GHL_API_KEY` → app/.env.local ✅ (PIT token location do operador)
- `GHL_LOCATION_ID` → `{{GHL_LOCATION_ID}}` ✅

---

## Output canônico

`workspace/output/marketing/engajamento/{YYYY-MM-DD}.md`

---

## O que pode falhar (e como resolver)

| Erro | Causa | Fix |
|---|---|---|
| 401 Unauthorized | PIT token expirado | Settings GHL → Private Integrations → renovar token → atualizar GHL_API_KEY |
| Base vazia / 0 contatos | Location ID errado | Confirmar GHL_LOCATION_ID = `{{GHL_LOCATION_ID}}` |
| Todos aparecem como 🔵 Frio | Tags não cadastradas no GHL | Verificar nomes reais das tags em Settings GHL → Tags |
| Paginação incompleta | API retornou cursor vazio | Script já tem fallback por data — verificar total no print final |

---

## Bateria de testes

- [x] Script criado em `workspace/scripts/marketing/engajamento-base.py`
- [x] Skill documentada em `.claude/commands/engajamento-base.md`
- [ ] Teste real com GHL_API_KEY (confirmar total de contatos bate com o painel GHL)
- [ ] Confirmar que tags de interesse estão mapeadas corretamente (TAGS_QUENTES)
- [ ] Confirmar que tags de cliente estão mapeadas (TAGS_CLIENTE)
- [ ] Verificar output salvo em workspace/output/marketing/engajamento/

---

## Integração com outros fluxos

- **Antes de lançamento de mentoria:** rodar `/engajamento-base` → ver temperatura → decidir se precisa mais aquecimento
- **Após live/email:** rodar novamente → comparar temperatura antes/depois
- **Relatório semanal:** pode ser incluso no briefing financeiro de segunda (`/briefing-financeiro-segunda`)

---

## Aprendizados (Regras §1 §5)

- Registrar pendência no ClickUp antes de executar via `/criar-pendencia`
- Ao concluir, fechar via `/fechar-pendencia`
