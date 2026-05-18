# MAPA — squad-copy

**Propósito:** Produção e revisão de copy — páginas, anúncios, emails curtos, headlines.

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@copywriter` | `agentes/copywriter/` | Escreve qualquer copy (LP, anúncio, newsletter, LinkedIn, roteiro) | `/escrever-copy`, `/escrever-pagina`, `/escrever-newsletter`, `/escrever-linkedin`, `/escrever-roteiro` |
| `@revisor-copy` | `agentes/revisor-copy/` | Revisor independente de copy curta | `/revisar-copy` |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
