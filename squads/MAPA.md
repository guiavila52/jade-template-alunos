# MAPA — squads

**Propósito:** Arquitetura de squads do {{NOME_OPERADOR}} — cada subpasta é um squad especializado coordenado pela Jade (COO).

**Última atualização:** 2026-05-06 (Tarefa #155 — agentes registrados em `.claude/agents/` pra dispatch nativo)

## Conteúdo

| Arquivo | Função |
|---|---|
| `jade/` (subpasta) 🆕 | Camada de orquestração estratégica — Jade COO + `@estrategista`. NÃO produz, ORQUESTRA. |
| `conteudo/` (subpasta) | newsletter + carrossel |
| `copy/` (subpasta) | copywriter + paginas |
| `dev/` (subpasta) | Gimmick + paginas-dev + MCP |
| `financeiro/` (subpasta) | financeiro |
| `infra/` (subpasta) | DNS, SSL, deploy, VPS |
| `midia/` (subpasta) | audiovisual, YouTube, thumbnails |
| `radar/` (subpasta) | pesquisa de mercado, benchmarking |
| `trafego/` (subpasta) | criativos, Meta Ads |

## Agentes registrados em `.claude/agents/`

A partir da Tarefa #155 (07/05/2026), cada agente do squad tem entry correspondente em `.claude/agents/{nome}.md` (Claude Code v2.x). Isso permite que a Jade (e qualquer agente) despache via `Agent` tool com `subagent_type: "{nome}"` em vez de `general-purpose` — o Claude Code carrega automaticamente as instructions do agente.

| Agente registrado | Squad pai | Pasta canônica | Modelo |
|---|---|---|---|
| `paginas-dev` | dev | `squads/dev/agentes/paginas-dev/` | sonnet-4-5 |
| `paginas` | copy | `squads/copy/agentes/paginas/` | sonnet-4-5 |
| `copywriter` | copy | `squads/copy/agentes/copywriter/` | sonnet-4-5 |
| `estrategista` | jade | `squads/jade/agentes/estrategista/` | opus-4-5 |
| `newsletter` | conteudo | `squads/conteudo/agentes/newsletter/` | sonnet-4-5 |
| `carrossel` | conteudo | `squads/conteudo/agentes/carrossel/` | sonnet-4-5 |
| `trafego` | trafego | `squads/trafego/agentes/trafego/` | sonnet-4-5 |
| `financeiro` | financeiro | `squads/financeiro/agentes/financeiro/` | sonnet-4-5 |
| `jade` | jade (orquestrador) | (sem pasta dedicada — skill `/jade`) | opus-4-5 |
| `bug-hunter` | dev | (sem pasta dedicada — só `.claude/agents/bug-hunter.md`) | sonnet-4-5 |

> Os arquivos `instructions.md` antigos em `squads/{sq}/agentes/{ag}/` permanecem como FONTE HISTÓRICA. Os novos `.claude/agents/{ag}.md` são a versão canônica pra dispatch.

## Histórico
- 2026-05-06: Tarefa #124 — `squad-jade` formalizado como pasta. `@estrategista` migrado de `squad-conteudo` pra `squad-jade` (estratégia é peer da Jade, não produção).
- 2026-05-07: Tarefa #155 — agentes registrados em `.claude/agents/{nome}.md` (9 cadastros). Jade despacha via `subagent_type` específico em vez de `general-purpose`.
- 2026-05-07: Tarefa #175.2 — agente `bug-hunter` cadastrado (caçador de bugs pré-deploy via Playwright). Faz parte do triple-check obrigatório (paginas + paginas-dev + bug-hunter) antes de `vercel --prod`. Não corrige, só detecta e reporta.
