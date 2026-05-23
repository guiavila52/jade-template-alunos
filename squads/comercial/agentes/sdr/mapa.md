# Agente SDR — MAPA

**Squad:** comercial  
**Status:** ⚪ ESQUELETO (aguardando integração API {{LMS}} AI)  
**Última atualização:** 11/05/2026

---

## Propósito

Qualificação inicial de lead via WhatsApp. **PROXY para o {{LMS}} AI** (sistema que já atende no WhatsApp como SDR hoje).

---

## Função central

Receber lead novo → qualificar interesse/fit → encaminhar pro `@closer` OU descartar.

---

## KPIs principais

- Leads qualificados / dia
- Taxa de qualificação (% de leads que passam pro closer)
- Tempo médio até qualificação

---

## Integrações

- **{{LMS}} AI** (CRÍTICO) — proxy pra sistema de WhatsApp que já atende. Pendente: doc API do {{PARCEIRO_PLATAFORMA}} (CPO {{LMS}})

---

## Bloqueio atual

Sem doc API do {{LMS}} AI, o agente fica esqueleto.

---

## Arquivos

| Arquivo | O que é |
|---|---|
| `mapa.md` | Este arquivo (estrutura e contexto) |
| `memoria.md` | Contexto operacional do agente |
| `aprendizados.md` | Lições aprendidas |

---

## Próximos passos

1. {{PARCEIRO_PLATAFORMA}} entregar doc API
2. Implementar `/qualificar-lead` funcional
3. Testar fluxo lead → qualificação → closer
4. Promover status → 🔵 EM PROGRESSO
