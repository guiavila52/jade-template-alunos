# Mapa — Squads

**Propósito:** Diretório de todos os squads funcionais do time de agentes.

**Última atualização:** configure após clonar

## Squads ativos

| Squad | Propósito | Agentes principais |
|-------|-----------|-------------------|
| gestao | Orquestração geral | COO (Jade) |
| conteudo | Produção de conteúdo | estrategista, copywriter, designer, editor |
| copy | Copy de vendas | copywriter, revisor-copy |
| dev | Desenvolvimento web | desenvolvedor-frontend, designer-revisor, devops |
| trafego | Tráfego pago | gestor-trafego, especialista-email, revisor-criativo |
| financeiro | Financeiro | analista-financeiro, contador |
| comercial | Comercial | sdr, closer, customer-success |
| radar | Pesquisa e análise | analista-mercado, analista-tendencias |
| infra | Infraestrutura | (sem agentes próprios — operado via workspace/infra) |

## Como funciona

- Cada squad tem pasta própria com: `mapa.md`, `aprendizados.md`, `memoria.md`, `tarefas.md`, `agentes/`
- Agentes do squad têm sub-pasta em `agentes/{nome}/` com: `mapa.md`, `aprendizados.md`, `memoria.md`
- Skills canônicas em `.claude/commands/` são o ponto de entrada de cada fluxo de produção
- Agentes invocáveis em `.claude/agents/` — chamados via Agent tool da Jade
