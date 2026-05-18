# MAPA — squad-financeiro

**Propósito:** Operação fiscal/financeira — notas fiscais, classificação de extratos, análise contábil.

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@analista-financeiro` | `agentes/analista-financeiro/` | Operação NF, conferência de pagamentos, extratos
| `@contador` | `agentes/contador/` | Análise fiscal estratégica, DRE, regime tributário | (skill dedicada futura) |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
