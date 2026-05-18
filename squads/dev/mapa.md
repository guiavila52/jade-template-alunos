# MAPA — squad-dev

**Propósito:** Desenvolvimento front-end, design UI, revisão visual, QA e infra (DevOps).

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@desenvolvedor-frontend` | `agentes/desenvolvedor-frontend/` | Implementa páginas Astro 6 + Tailwind v4 | `/criar-pagina-nova`, `/ajustar-pagina` |
| `@designer-ui` | `agentes/designer-ui/` | Define DESIGN.md das páginas antes do código | (parte do `/criar-pagina-nova`) |
| `@designer-revisor` | `agentes/designer-revisor/` | Revisão visual REAL via Playwright headless | `/revisar-visual-pagina`, `/revisar-visual` |
| `@analista-qa` | `agentes/analista-qa/` | Bateria de QA funcional antes do deploy | `/executar-bateria-qa` |
| `@devops` | `agentes/devops/` | DNS, SSL, deploys Vercel, monitoramento | (skill dedicada futura) |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
