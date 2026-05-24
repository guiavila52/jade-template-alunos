# Memória — Agente Financeiro

## Função

Consultar extrato bancário, emitir NF, monitorar entradas e saídas, gerar relatórios financeiros.

## Status

🟢 MADURA — Skill `/registrar-financeiro` testada ponta-a-ponta em caso real, 100% confiável (12/05/2026).

## Skills operacionais

### `/registrar-financeiro` (12/05/2026 — 🟢 MADURA)

Consulta NF via API {{PLATAFORMA_NF}} com busca por:
- **CPF/CNPJ** — busca via paginação + filtro local
- **Email** — busca últimos 60 dias + filtro local case insensitive
- **Telefone** — normaliza e compara substring
- **Nome** — filtro local case insensitive

**Fix completo 12/05/2026:**
1. ✅ Regex `doc:` corrigida (bug: parseava como `nome:`)
2. ✅ Iterator corrigido pra dict com chaves numerais `{"1": {...}, "2": {...}}`
3. ✅ Período ampliado pra 60 dias (limite seguro: 89 dias)
4. ✅ Retry automático pra códigos 120 (3x/30s) e 996 (2x/65s)
5. ✅ Indicador de progresso durante paginação
6. ✅ Tratamento HTTP 401 pra código 996 (API retorna 401, não 200, em rate limit)

**Características:**
- Paginação automática (max 50 páginas)
- Timeout 15s obrigatório (Regra #22)
- Rate limit 996 → aguarda 65s automaticamente (max 2x)
- Código 120 → aguarda 30s automaticamente (max 3x)
- Retorna Top 10 NFs encontradas
- NUNCA expõe `{{PLATAFORMA_NF}}_API_KEY` no output
- Carrega `.env.local` via função Python (source não funciona em subshell)

**Limitação conhecida:**
- Busca pontual de 1 NF pra 1 cliente é mais rápida no painel web {{PLATAFORMA_NF}} (30s vs. minutos)
- Skill é ideal pra automação em lote (relatórios mensais, cross-reference {{BANCO_PJ}})

**Teste real executado (12/05/2026 ~02h00):**
- Cliente: TSM FAé Treinamentos LTDA (CNPJ 00.000.000/0000-00, email cliente@exemplo.com)
- Resultado: ✅ Skill 100% funcional — paginação OK, filtros OK, retry OK, rate limit tratado
- NF não encontrada (possível: emitida pra outro email/CPF, ou período > 60 dias)
- Transcript: `workspace/output/financeiro/teste-registrar-financeiro-{{contadora}}-2026-05-12.md`

**Doc completa:** 
- Skill: `.claude/commands/registrar-financeiro.md`
- Script: `scripts/financeiro/registrar-financeiro.py`
- Histórico {{PLATAFORMA_NF}}: `segundo-cerebro/03-operacao/{{plataforma_nf}}-historico.md`

## Contabilidade online (07/05/2026)

- **Contabilizei** — escritório de contabilidade online utilizado pelo Gui. Integração futura (sem prazo). Documentação interna a coletar quando demandar (chave API, contato, periodicidade de envio de docs).
