# MAPA — squad-radar

**Propósito:** Monitorar concorrentes e detectar tendências do nicho.

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@analista-mercado` | `agentes/analista-mercado/` | Monitor de concorrentes do nicho | `/monitorar-concorrentes` |
| `@analista-tendencias` | `agentes/analista-tendencias/` | Varredura de Reddit, Twitter/X, YouTube atrás de tendências | `/varrer-tendencias` |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
