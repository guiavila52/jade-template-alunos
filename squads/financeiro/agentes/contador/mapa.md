# MAPA — contador

**Propósito:** Agente de contabilidade técnica e planejamento fiscal do {{NOME_OPERADOR}} (2 CNPJs: {{EMPRESA_COFUNDADA}} + {{EMPRESA_HOLDING}}).

**Status:** ⚪ ESQUELETO — estrutura criada em 11/05/2026, sem implementação funcional ainda.

**Última atualização:** 2026-05-11

---

## Função

`@contador` é responsável pela contabilidade técnica, planejamento fiscal e decisões tributárias das empresas do {{OPERADOR}}. Diferente de `@analista-financeiro` (que OPERA — emite NF, consulta extrato, classifica transações), `@contador` ANALISA e DECIDE sobre:

- DRE mensal (Demonstrativo de Resultado do Exercício)
- Regime tributário (Simples Nacional vs Lucro Presumido)
- Projeção fiscal trimestral (impostos a pagar)
- Análise de viabilidade de investimentos
- Classificação contábil de transações complexas
- Planejamento de IR PJ
- Análise de parcelas do Banco Inter (classificação como despesa vs passivo)

---

## Integrações

- **Notazz** (NFs emitidas — receita)
- **Banco Inter PJ** (extrato — movimentações)
- **Supabase** (dashboard de finanças no app/ — a integrar)

---

## KPIs canônicos

- **DRE mensal** — receita, despesas, lucro líquido, margem
- **Fluxo de caixa** — entradas vs saídas por mês
- **MRR** (Monthly Recurring Revenue) — uso INTERNO, nunca exposto publicamente
- **Análise de regime tributário** — comparativo Simples vs Lucro Presumido trimestral
- **Projeção fiscal trimestral** — impostos estimados a pagar nos próximos 3 meses

---

## Skills disponíveis

- — ⚪ ESQUELETO (análise contábil/fiscal estruturada por período)

---

## Memórias correlatas

- `project_banco_inter.md` — Data de abertura da conta PJ (19/08/2024 — limite histórico)
- `project_notazz.md` — Sistema de NF (Notazz), conta {{EMPRESA_HOLDING_UPPER}} (8959), duas empresas
- `project_empresas_cnpj.md` — Estrutura empresarial: {{EMPRESA_COFUNDADA}} + {{EMPRESA_HOLDING}} (Projeto {{NOME_OPERADOR}} + {{EMPRESA_NEGOCIO}})

---

## Conteúdo

| Arquivo | Função |
|---|---|
| `mapa.md` | este arquivo |
| `memoria.md` | memória do agente (estado, projetos ativos, contexto) |
| `aprendizados.md` | lições registradas após aprovação/rejeição |

---

## Próximos passos

1. Implementar funcional (integração Notazz + Banco Inter)
2. Criar dashboard de DRE em Supabase + app/
3. Criar skill `/relatar-financeiro` (relatório mensal/trimestral automático)
