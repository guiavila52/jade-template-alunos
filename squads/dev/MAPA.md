# MAPA — squads/dev/

> Última atualização: 2026-05-06 (skill `/transcrever-video` + `scripts/`)

## Propósito

Squad responsável por desenvolvimento técnico — páginas Astro, MCP Gimmick, integrações,
infraestrutura de código do squad de agentes.

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `memoria.md` | Estado/contexto do squad-dev. |
| `tarefas.md` | Log oficial de tarefas (status: em andamento, entregue, aprovado, rejeitado). |
| `aprendizados.md` | Lições do squad. Inclui rejeição /consultoria e 5 [BASICO] derivados. |
| `proposta-revisor-visual.md` | Proposta T7 — upgrade do revisor com Playwright headless. Pendente de aprovação. |
| `MAPA.md` | Este arquivo. |
| `agentes/` | Pasta dos agentes worker (cada um com sua memória/aprendizados). |
| `scripts/` | Scripts utilitários reusados por skills (ex: `transcribe_video.py` para `/transcrever-video`). |

## Agentes do squad

- **paginas-dev** (`agentes/codar-pagina/`) — gera componentes Astro a partir de copy aprovada.
  - skill: `/codar-pagina`
- (próximos: gimmick, mcp, infra-code)

## Skills relacionadas

- `/codar-pagina` · `/revisar-codigo-pagina` · `/publicar-pagina` · `/criar-pagina` · `/migrar-pagina` · `/transcrever-video`

## Referências externas

- `Páginas Astro {{NOME_OPERADOR}}/DESIGN-SYSTEM.md` — fonte única visual
- `Páginas Astro {{NOME_OPERADOR}}/MAPA.md` — estrutura do projeto Astro
- `squad/processos/pipeline-paginas.md` — pipeline ponta-a-ponta
