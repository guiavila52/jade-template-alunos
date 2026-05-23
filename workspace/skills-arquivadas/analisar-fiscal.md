# /analisar-fiscal

**Squad:** financeiro
**Agente:** @contador
**Status:** ⚪ ESQUELETO

## Input

- Empresa: `{{empresa_cofundada}}` ou `{{empresa_holding}}` (default: ambas)
- Período: `mes` | `trimestre` | `ano` | `YYYY-MM` (default: mês corrente)
- Foco: `regime` | `dre` | `optimizacao` | `obrigacoes` (default: visão geral)

## O que fazer

Análise contábil estratégica — não operacional. Operacional (emitir NF, classificar extrato, conferir pagamento) é responsabilidade do @analista-financeiro.

Fluxo:
1. Carregar dados financeiros do período (extratos {{BANCO_PJ}} via @analista-financeiro)
2. Consultar histórico fiscal (regime atual, faturamento últimos 12m)
3. Aplicar lente conforme foco:
   - **regime:** simular Simples vs Presumido vs Real com faturamento real
   - **dre:** consolidar receita, custo, despesa, lucro líquido
   - **optimizacao:** identificar oportunidades legais (pró-labore vs DL, deduções, planejamento)
   - **obrigacoes:** checklist DEFIS, DCTF, ECF, SPED por empresa
4. Output: relatório markdown em `workspace/output/financeiro/YYYY-MM-analise-fiscal-[empresa].md`

## Fluxo de execução

1. Validar input (empresa válida, período coerente)
2. Carregar dados (extratos + histórico de regime)
3. Aplicar análise
4. Gerar relatório
5. Registrar conclusões importantes em `segundo-cerebro/04-decisoes/YYYY-MM-DD-fiscal-[tema].md`

## Regras

- NUNCA dar conselho sem fonte oficial citada (CTN, LC 123/06, IN RFB, etc)
- SEMPRE preservar decisões fiscais em segundo-cerebro
- Distinguir {{LMS}} (CNPJ próprio) de {{EMPRESA_HOLDING}} (engloba Gui Ávila + {{EMPRESA_NEGOCIO}})
- Se dúvida que envolve risco fiscal real → recomendar consulta com contador humano

## Bateria de testes #24

**Pré-implementação (esqueleto atual):**
- [x] Arquivo criado em .claude/commands/
- [x] Estrutura mínima (input, fluxo, regras, bateria)
- [x] Agente @contador existe em .claude/agents/

**Pós-implementação funcional:**
- [ ] Integração com extratos {{BANCO_PJ}} (via @analista-financeiro)
- [ ] Simulador de regime tributário funcional
- [ ] DRE consolidado por empresa
- [ ] Output relatório padronizado
- [ ] Conclusões importantes salvas em segundo-cerebro

## Bloqueio atual

Esqueleto. Sem demanda imediata — aguarda fechamento fiscal 2026 (próxima janela natural) ou pedido explícito do Gui.
