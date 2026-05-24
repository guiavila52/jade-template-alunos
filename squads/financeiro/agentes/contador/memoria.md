# Memória — @contador

**Função:** Contabilidade técnica e planejamento fiscal do {{NOME_OPERADOR}} (2 CNPJs: {{LMS}} + {{EMPRESA_HOLDING}}).

**Status:** ⚪ ESQUELETO — criado em 11/05/2026, sem histórico operacional ainda.

**Última atualização:** 2026-05-11

---

## Responsabilidades

`@contador` é o agente de contabilidade técnica e decisões fiscais. Diferente de `@analista-financeiro` (operacional — emite NF, consulta extrato, classifica transações), `@contador` analisa e decide sobre:

- **DRE mensal** — Demonstrativo de Resultado do Exercício (receita, despesas, lucro líquido, margem)
- **Regime tributário** — análise comparativa Simples Nacional vs Lucro Presumido
- **Projeção fiscal trimestral** — impostos estimados a pagar nos próximos 3 meses
- **Planejamento de IR PJ** — decisões tributárias anuais
- **Classificação contábil** — transações complexas que exigem decisão técnica (ex: parcelas {{BANCO_PJ}} = despesa ou passivo?)
- **Análise de viabilidade** — investimentos, contratações, expansão

---

## Integrações

### {{PLATAFORMA_NF}} (NFs emitidas)
- **Função:** receita das empresas ({{LMS}} + {{EMPRESA_HOLDING}})
- **API Key:** `{{PLATAFORMA_NF}}_API_KEY` em `app/.env.local`
- **Conta:** {{EMPRESA_HOLDING_ID}}
- **Duas empresas emissoras:** {{operador_slug}} + {{produto_slug}}

### {{BANCO_PJ}} PJ (extrato)
- **Função:** movimentações financeiras (entradas, saídas, saldos)
- **Data de abertura:** 19/08/2024 — limite histórico do extrato
- **Conta:** {{EMPRESA_HOLDING}}

### Supabase (dashboard de finanças — a integrar)
- **Função:** armazenar DRE, fluxo de caixa, projeções fiscais
- **Local:** `app/` ({{Plataforma_Conteudo}})

---

## KPIs canônicos

| KPI | Descrição | Uso |
|---|---|---|
| **DRE mensal** | Receita, despesas, lucro líquido, margem | Interno + decisões estratégicas |
| **Fluxo de caixa** | Entradas vs saídas por mês | Interno + planejamento |
| **MRR** | Monthly Recurring Revenue | Interno — NUNCA expor publicamente |
| **Regime tributário** | Comparativo Simples vs Lucro Presumido | Decisão trimestral |
| **Projeção fiscal trimestral** | Impostos estimados a pagar | Planejamento de caixa |

---

## Memórias correlatas

- `project_banco_inter.md` — Data de abertura da conta PJ (19/08/2024 — limite histórico)
- `project_{{plataforma_nf}}.md` — Sistema de NF ({{PLATAFORMA_NF}}), conta {{EMPRESA_HOLDING_ID}}, duas empresas
- `project_empresas_cnpj.md` — Estrutura empresarial: {{LMS}} + {{EMPRESA_HOLDING}} (Projeto {{NOME_OPERADOR}} + {{EMPRESA_NEGOCIO}})
- `feedback_metricas_publicas_gui.md` — PROIBIDO expor faturamento (R$, MRR, lucro) em copy pública. Usar usuários ativos, alunos, criadores, cases.

---

## Projetos ativos

Nenhum projeto ativo no momento (agente criado em 11/05/2026, ainda sem histórico operacional).

---

## Histórico de sessões

| Data | Evento |
|---|---|
| 11/05/2026 | Agente criado (Onda B2) — estrutura esqueleto + skill `/analisar-resultados` |

---

## Próximos passos

1. Implementar `/analisar-resultados` funcional (integração {{PLATAFORMA_NF}} + {{BANCO_PJ}})
2. Criar dashboard de DRE em Supabase + app/
3. Criar skill `/relatar-financeiro` (relatório mensal/trimestral automático)
4. Primeira análise fiscal manual com Gui para calibrar output esperado

## Contabilidade externa — Contabilizei

**Empresa:** Contabilizei (https://www.contabilizei.com.br)
**CNPJ atendido:** {{CNPJ_PRINCIPAL}} ({{EMPRESA_HOLDING}})
**Modelo:** Contabilidade digital com mensalidade fixa

**Princípio operacional:**
- @contador faz análise estratégica + cross-reference com Contabilizei
- @contador NÃO substitui contabilidade oficial — complementa
- Decisões fiscais estruturais (mudança de regime, distribuição grande de lucros, etc): SEMPRE consultar Contabilizei antes

**Doc histórica completa:** `segundo-cerebro/03-operacao/contabilizei-historico.md`

**A confirmar:** Contabilizei tem API pública? Verificar em https://www.contabilizei.com.br/api ou painel cliente.
