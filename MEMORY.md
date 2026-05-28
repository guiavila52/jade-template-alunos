# MEMORY.md — GPS do Squad

> Carregado automaticamente a cada sessão. Leia antes de qualquer coisa.
> Última atualização: configure via `/configurar-squad`

## ARQUITETURA CANÔNICA

```
{{NOME_SQUAD}}/
├── AGENTS.md           Regras invioláveis (framework)
├── CLAUDE.md           Orquestrador (framework, sem dados pessoais)
├── IDENTIDADE.md       Persona (operador, empresas, funil) — autoload via @
├── MEMORY.md           Este arquivo
├── README.md           Quickstart
├── segundo-cerebro/    Knowledge atemporal
├── workspace/          Estado/runtime (memory, output, scripts, regras, integracoes)
├── squads/             Squads funcionais
└── .claude/            Commands, agents, hooks, settings.json
```

**Two-track architecture:**
- Framework (atualiza via /atualizar-jade): CLAUDE.md, AGENTS.md, .claude/, squads/*/agentes/*/agente.md
- Persona (preservada): IDENTIDADE.md, MEMORY.md, segundo-cerebro/, workspace/memory/, aprendizados.md

---

## FOCO ATUAL

**Meta:** `{{META_FINANCEIRA}}`
**Caminho:** `{{FUNIL_PRINCIPAL}}`

---

## ESTADO DO NEGÓCIO

| | |
|---|---|
| Baseline atual | `{{BASELINE_FINANCEIRO}}` |
| Gap para meta | `{{GAP_FINANCEIRO}}` |
| Prioridade #1 | `{{PRIORIDADE_1}}` |
| Prioridade #2 | `{{PRIORIDADE_2}}` |
| Prioridade #3 | `{{PRIORIDADE_3}}` |

---

## ARQUITETURA DO SQUAD

{{NOME_AGENTE_COO}} (COO) coordena squads especializados:

| Squad | Agentes ativos | Memória |
|-------|---------------|---------|
| gestao | {{NOME_AGENTE_COO}} (COO) | [`squads/gestao/`](squads/gestao/) |
| conteudo | estrategista, copywriter | [`squads/conteudo/`](squads/conteudo/) |
| copy | copywriter | [`squads/copy/`](squads/copy/) |
| dev | desenvolvedor-frontend | [`squads/dev/`](squads/dev/) |
| trafego | gestor-trafego | [`squads/trafego/`](squads/trafego/) |
| financeiro | analista-financeiro | [`squads/financeiro/`](squads/financeiro/) |

---

## TOPIC FILES

- [`projetos.md`](workspace/memory/projetos.md) — projetos ativos, status, bloqueios
- [`decisoes.md`](workspace/memory/decisoes.md) — decisões permanentes com data e contexto
- [`aprendizados.md`](workspace/memory/aprendizados.md) — lições gerais do squad
- [`pessoas.md`](workspace/memory/pessoas.md) — time, parceiros, como acionar

---

## REGRAS DE ATUALIZAÇÃO

- Atualizar este arquivo sempre que o estado mudar
- Antes de compactar: extrair para topic files, depois atualizar este índice
- Nota diária: criar `workspace/memory/diario/YYYY-MM-DD.md` antes de encerrar sessão
