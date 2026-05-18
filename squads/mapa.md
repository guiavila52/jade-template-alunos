# MAPA — squads

**Propósito:** Arquitetura de squads do {{NOME_OPERADOR}} — cada subpasta é um squad especializado coordenado pela Jade (COO).

**Última atualização:** 2026-05-16 (Onda 2 housekeeping — agentes fantasmas removidos, tabela legacy eliminada)

## Conteúdo

| Squad | Função | Path |
|---|---|---|
| `gestao/` | Camada de orquestração estratégica — Jade COO + estrategista-marketing. NÃO produz, ORQUESTRA. | `squads/gestao/` |
| `conteudo/` | Newsletter + carrossel + vídeo | `squads/conteudo/` |
| `copy/` | Copywriting + landing pages | `squads/copy/` |
| `dev/` | Front-end + QA + revisão visual | `squads/dev/` |
| `trafego/` | Criativos + Meta Ads + email | `squads/trafego/` |
| `financeiro/` | Análise financeira + fiscal | `squads/financeiro/` |
| `comercial/` | SDR + closer + CS | `squads/comercial/` |
| `radar/` | Pesquisa de mercado + tendências | `squads/radar/` |

## Agentes

Cada squad tem seus agentes documentados em `squads/{squad}/mapa.md`. Agentes invocáveis via Agent tool estão registrados em `.claude/agents/{nome}.md`.

## Histórico

- **2026-05-16:** Onda 2 housekeeping — 11 pastas fantasmas (arquiteto-curricular, carrossel, estrategista, newsletter, social-media, paginas, bug-hunter, paginas-dev, revisor-visual, financeiro, trafego) removidas; aprendizados consolidados nos agentes novos equivalentes.
- **2026-05-07:** Tarefa #155 — agentes registrados em `.claude/agents/` pra dispatch nativo.
- **2026-05-06:** Estrutura inicial squads/.
