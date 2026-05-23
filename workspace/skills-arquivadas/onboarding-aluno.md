# /onboarding-aluno

**Squad:** comercial  
**Agente:** @customer-success  
**Status:** ⚪ ESQUELETO

---

## Input

- Aluno novo (ID + produto comprado + data da compra)

---

## O que fazer

Experiência dos primeiros 7 dias do aluno recém-comprado. Garantir sucesso rápido, engajamento e evitar churn precoce.

Fluxo ideal:
1. **Dia 0 (compra):** welcome email + acesso liberado + primeira tarefa clara
2. **Dia 1:** lembrete gentil "já acessou a primeira aula?"
3. **Dia 3:** check-in "como está indo? tem dúvida?"
4. **Dia 7:** NPS + feedback aberto + incentivo pra continuar
5. Marcar aluno como "ativado" ou "em risco" conforme engajamento

---

## Fluxo de execução

1. Validar input (aluno tem ID + produto + data compra?)
2. Disparar welcome flow (email/WhatsApp)
3. Monitorar progresso (acessou primeira aula?)
4. Disparar check-ins dia 3 e 7
5. Coletar NPS dia 7
6. Marcar status no CRM (ativado / em risco)

---

## Regras

- NUNCA ser chato — comunicação gentil, útil, não invasiva
- SEMPRE monitorar engajamento real (não só disparo de email)
- Se aluno não acessar nada em 3 dias → alertar squad CS

---

## Bateria de testes #24

**Pré-implementação (esqueleto atual):**
- [ ] Arquivo criado em .claude/commands/
- [ ] Estrutura mínima presente (input, output, fluxo, regras, bateria)

**Pós-implementação funcional:**
- [ ] Welcome flow é disparado automaticamente após compra
- [ ] Check-ins dia 3 e 7 são disparados corretamente
- [ ] NPS dia 7 é coletado e registrado
- [ ] Aluno em risco (sem engajamento) é detectado e alertado
- [ ] Integrações {{LMS}} + {{CRM}} funcionando
- [ ] Erros capturados com graceful degradation
- [ ] Timeout configurado (max 10s por operação)

---

## Próximos passos

1. Definir jornada ideal primeiros 7 dias (welcome, primeira aula, check-ins)
2. Integrar com {{LMS}} (matrículas, progresso) e {{CRM}} (sequências email)
3. Implementar skill funcional
4. Testar fluxo completo venda → onboarding → aluno ativo
