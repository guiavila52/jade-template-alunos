# MAPA — squad-conteudo

**Propósito:** Produção de conteúdo orgânico — newsletter, carrossel, vídeos, posts LinkedIn.

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@estrategista-marketing` | `agentes/estrategista-marketing/` | Define posicionamento, ângulo, narrativa antes da copy | `/escrever-estrategia` |
| `@designer-conteudo` | `agentes/designer-conteudo/` | Carrossel Instagram (Light Copy + HTML→PNG) | `/criar-carrossel` |
| `@editor-audiovisual` | `agentes/editor-audiovisual/` | Edição de vídeo YouTube/Reels | `/cortar-youtube` |
| `@revisor-linkedin` | `agentes/revisor-linkedin/` | Revisor independente de post LinkedIn | `/revisar-linkedin` |
| `@revisor-newsletter` | `agentes/revisor-newsletter/` | Revisor independente de newsletter | `/revisar-newsletter` |
| `@revisor-roteiro` | `agentes/revisor-roteiro/` | Revisor independente de roteiro YouTube | `/revisar-roteiro` |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
