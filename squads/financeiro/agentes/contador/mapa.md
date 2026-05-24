# MAPA — contador

**Propósito:** Agente de contabilidade técnica e planejamento fiscal do {{NOME_OPERADOR}} (2 CNPJs: {{LMS}} + {{EMPRESA_HOLDING}}).

**Status:** ⚪ ESQUELETO — estrutura criada em 11/05/2026, sem implementação funcional ainda.

**Última atualização:** 2026-05-11

---

## Função

`@contador` é responsável pela contabilidade técnica, planejamento fiscal e decisões tributárias das empresas do Gui. Diferente de `@analista-financeiro` (que OPERA — emite NF, consulta extrato, classifica transações), `@contador` ANALISA e DECIDE sobre:

- DRE mensal (Demonstrativo de Resultado do Exercício)
- Regime tributário (Simples Nacional vs Lucro Presumido)
- Projeção fiscal trimestral (impostos a pagar)
- Análise de viabilidade de investimentos
- Classificação contábil de transações complexas
- Planejamento de IR PJ
- Análise de parcelas do {{BANCO_PJ}} (classificação como despesa vs passivo)

---

## Integrações

- **{{PLATAFORMA_NF}}** (NFs emitidas — receita)
- **{{BANCO_PJ}} PJ** (extrato — movimentações)
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

- `/analisar-resultados` — ⚪ ESQUELETO (análise contábil/fiscal estruturada por período)

---

## Memórias correlatas

- `project_banco_inter.md` — Data de abertura da conta PJ (19/08/2024 — limite histórico)
- `project_{{plataforma_nf}}.md` — Sistema de NF ({{PLATAFORMA_NF}}), conta {{EMPRESA_HOLDING_ID}}, duas empresas
- `project_empresas_cnpj.md` — Estrutura empresarial: {{LMS}} + {{EMPRESA_HOLDING}} (Projeto {{NOME_OPERADOR}} + {{EMPRESA_NEGOCIO}})

---

## Conteúdo

| Arquivo | Função |
|---|---|
| `mapa.md` | este arquivo |
| `memoria.md` | memória do agente (estado, projetos ativos, contexto) |
| `aprendizados.md` | lições registradas após aprovação/rejeição |

---

## Próximos passos

1. Implementar `/analisar-resultados` funcional (integração {{PLATAFORMA_NF}} + {{BANCO_PJ}})
2. Criar dashboard de DRE em Supabase + app/
3. Criar skill `/relatar-financeiro` (relatório mensal/trimestral automático)
