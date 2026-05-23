# /fechar-venda

**Squad:** comercial  
**Agente:** @closer  
**Status:** ⚪ ESQUELETO

---

## Input

- Lead qualificado (dados + contexto do @sdr)
- Produto/serviço de interesse

---

## O que fazer

Fechar venda de lead qualificado pelo @sdr.

Fluxo ideal:
1. Receber lead qualificado com contexto completo do SDR
2. Avaliar melhor abordagem (call síncrona vs assíncrona, urgência, ticket médio)
3. Apresentar oferta adequada ao momento/interesse do lead
4. Responder objeções comuns (preço, timing, dúvida)
5. Fechar venda → registrar no {{LMS}} + liberar acesso
6. OU agendar follow-up (se não for o momento)

---

## Fluxo de execução

1. Validar input (lead tem contexto completo do SDR?)
2. Avaliar estratégia de fechamento (sync vs async, urgência)
3. Apresentar oferta
4. Capturar objeções e responder
5. Fechar OU agendar follow-up
6. Registrar venda no {{LMS}} (se fechou)
7. Atualizar CRM ({{CRM}})

---

## Regras

- NUNCA pressionar venda se lead não estiver pronto — melhor follow-up que queimar lead
- SEMPRE registrar venda no sistema ({{LMS}} + {{CRM}})
- Se follow-up, agendar próximo contato (não deixar esfriar)

---

## Bateria de testes #24

**Pré-implementação (esqueleto atual):**
- [ ] Arquivo criado em .claude/commands/
- [ ] Estrutura mínima presente (input, output, fluxo, regras, bateria)

**Pós-implementação funcional:**
- [ ] Venda fechada é registrada no {{LMS}}
- [ ] Aluno recebe acesso automaticamente
- [ ] CRM ({{CRM}}) é atualizado com status da venda
- [ ] Follow-up é agendado se venda não fechar
- [ ] Erros de API são capturados com graceful degradation
- [ ] Timeout configurado (max 15s por operação)

---

## Próximos passos

1. Definir fluxo de fechamento (call sync vs async, scripts, objeções comuns)
2. Integrar com {{LMS}} (transações) e {{CRM}} (pipeline)
3. Implementar skill funcional
4. Testar fluxo completo SDR → closer → venda
