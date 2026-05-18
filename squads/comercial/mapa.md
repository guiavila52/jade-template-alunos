# MAPA — squad-comercial

**Propósito:** Funil comercial — qualifica leads, fecha vendas, onboarding e retenção.

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@sdr` | `agentes/sdr/` | Qualificação inicial de lead via WhatsApp | `/qualificar-lead` |
| `@closer` | `agentes/closer/` | Fechamento de venda (agendamento, recuperação, follow-up) | `/fechar-venda` |
| `@customer-success` | `agentes/customer-success/` | Experiência primeiros 7 dias do aluno comprado | (sem skill macro ainda) |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
