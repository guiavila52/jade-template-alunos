# MAPA — squads/dev/agentes/

> Última atualização: 07/05/2026

## Propósito

Pasta com a memória individual de cada agente worker do squad-dev.
Cada subpasta tem `memoria.md`, `aprendizados.md` e `MAPA.md` próprios.

## Agentes

| Agente | Pasta | Responsabilidade |
|--------|-------|------------------|
| paginas-dev | `paginas-dev/` | Implementa páginas Astro a partir de copy aprovada. Skill: `/codar-pagina`. |
| bug-hunter | `bug-hunter/` | Caça bugs ANTES do deploy via Playwright + console/network. Detecta + reporta (não corrige). Definição em `.claude/agents/bug-hunter.md`. |

## Próximos a criar (backlog)

- `gimmick/` — operação do MCP Gimmick
- `mcp/` — manutenção do MCP server
- `infra-code/` — DNS, SSL, deploy, VPS (compartilhado com squad-infra)
