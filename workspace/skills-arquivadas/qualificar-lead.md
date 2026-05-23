# /qualificar-lead

**Squad:** comercial  
**Agente:** @sdr  
**Status:** ⚪ ESQUELETO (pendente integração API {{LMS_AI}})

---

## Input

- Lead info (nome, telefone, origem, interesse)
- OU consulta direta ao {{LMS_AI}} (quando integração estiver pronta)

---

## O que fazer

Qualificar lead inicial via PROXY para o sistema {{LMS_AI}} (que já atende no WhatsApp como SDR).

Fluxo ideal:
1. Receber lead novo (via {{CRM}}, formulário, campanha, orgânico)
2. Consultar {{LMS_AI}} (histórico, mensagens trocadas, interesse declarado)
3. Avaliar fit:
   - Interesse claro no produto/serviço?
   - Fit com ICP (perfil ideal)?
   - Urgência / momento certo?
   - Capacidade de investimento (se aplicável)?
4. Qualificado → encaminhar pro @closer com contexto completo
5. Não qualificado → marcar no CRM e descartar educadamente

---

## Fluxo de execução

1. Validar input (lead tem dados mínimos?)
2. Consultar API {{LMS_AI}} (histórico de conversas WhatsApp)
3. Avaliar critérios de qualificação
4. Output: status (qualificado / não qualificado) + contexto pro closer

---

## Regras

- NUNCA inventar informação do lead — só usar dados reais da conversa WhatsApp
- SEMPRE registrar no CRM ({{CRM}}) o status da qualificação
- Se dúvida sobre fit, preferir passar pro closer (melhor excesso que falta)

---

## Bateria de testes #24

**Pré-implementação (esqueleto atual):**
- [ ] Arquivo criado em .claude/commands/
- [ ] Estrutura mínima presente (input, output, fluxo, regras, bateria)

**Pós-implementação funcional:**
- [ ] Integração API {{LMS_AI}} funcionando
- [ ] Lead qualificado é encaminhado pro closer com contexto
- [ ] Lead não qualificado é marcado no CRM
- [ ] Erro de API é capturado e retorna graceful degradation
- [ ] Timeout configurado (max 10s por consulta)

---

## Bloqueio atual

Aguardando {{NOME_PARCEIRO_PLATAFORMA}} (CPO {{LMS}}) retornar com documentação da API do {{LMS_AI}}.

Sem essa integração, skill permanece esqueleto.
