# MAPA — squads/infra/agentes/

> Última atualização: 07/05/2026

## Propósito

Agentes do squad-infra. Responsável por DNS, SSL, Vercel, VPS, deploys, secrets e infraestrutura de produção em geral.

## Agentes

| Agente | Pasta | Responsabilidade |
|--------|-------|------------------|
| (nenhum agente formalizado ainda) | — | — |

## Status

Squad existente como domínio, agentes ainda não formalizados em pastas próprias. Operações de infra hoje passam pelo squad-dev (paginas-dev) e por skills compartilhadas (`/publicar-pagina`, `/publicar-gimmick`).

## Backlog

- `dns-vercel/` — gestão de domínios `sites.{{DOMINIO}}`, `ferramentas.{{DOMINIO}}`, `mcp.{{DOMINIO}}`
- `secrets/` — rotação e auditoria de `.env.local`, tokens MCP, chaves API

## Regras

- Manter atualizado quando agente novo for formalizado
- Ver `feedback_secrets_em_env_local.md` (padrão validado no MCP Gimmick)
