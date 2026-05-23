# Memória — Squad Financeiro

Última atualização: 12/05/2026

## Contexto do squad

Responsável por: extrato bancário, emissão de NF, rotinas financeiras, integrações fiscais.

## Ferramentas

- **{{BANCO_PJ}}:** conta PJ — extrato disponível via API (token já configurado no Dashboard app)
- **App Dashboard:** `/Users/guiavila/Documents/Projetos IA Gui Ávila/` — já tem integração com {{BANCO_PJ}}
- **Sistema de NF:** {{PLATAFORMA_NF}} (app.{{PLATAFORMA_NF_URL}}) — conta {{EMPRESA_HOLDING_ID}}, duas empresas ({{EMPRESA1}} + {{EMPRESA2}}), API integrada

## Skills operacionais

### `/consultar-nf` (12/05/2026 — 🟢 MADURA)

Consulta NF via API {{PLATAFORMA_NF}} com busca por:
- **Email** — busca parcial case insensitive
- **CNPJ** — busca exata com normalização de pontuação
- **CPF** — busca exata com normalização de pontuação
- **Nome** — busca parcial case insensitive
- **Período** — data range customizado (padrão: 60 dias, max: 89 dias)

**Características:**
- Paginação automática (max 50 páginas)
- Retry automático em códigos 120 (3x/30s) e 996 (2x/65s)
- Timeout 30s obrigatório por requisição
- Stderr capturado, stdout limpo (JSON formatado)
- Exit code preciso (0 = sucesso, 1 = erro)

**Teste real executado (12/05/2026):**
- Cliente: TSM FAé Treinamentos LTDA (CNPJ 00.000.000/0000-00, email cliente_exemplo@gmail.com)
- Resultado: ✅ 100% funcional — rate limit tratado, paginação OK, filtros OK
- NF não encontrada (possível: emitida pra outro email/CPF, ou período > 60 dias)

**Limitação conhecida:**
- Busca pontual de 1 NF urgente é mais rápida no painel web {{PLATAFORMA_NF}} (~30s vs. minutos com rate limits)
- Skill é ideal pra automação em lote (relatórios mensais, cross-reference {{BANCO_PJ}})

**Doc completa:**
- Script: `scripts/financeiro/consultar-nf.py`
- Skill: `.claude/commands/consultar-nf.md`
- Histórico {{PLATAFORMA_NF}}: `segundo-cerebro/03-operacao/{{plataforma_nf}}-historico.md`

## Decisão pendente

**Como o squad acessa o extrato:** direto via API do {{BANCO_PJ}}, ou consultando o Dashboard app que já tem a integração?
→ Discutir com Gui antes de implementar.

## Contexto do {{BANCO_PJ}}

- Conta PJ aberta em 19/08/2024 — limite histórico do extrato
- Token de API já gerado e configurado no Dashboard app
- Novo token pode ser gerado direto no app do Inter se necessário
