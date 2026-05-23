# Regras de Negócio — Emissão de Nota Fiscal

> Documento de referência do squad-financeiro. Atualizado em 06/05/2026.

---

## Regra principal

**Tudo que entra no {{BANCO_PJ}} precisa de NF — com exceção das saídas da {{LMS}}.**

---

## Fluxo automático ({{LMS}} → {{PLATAFORMA_NF}})

1. Cliente compra pela plataforma {{LMS}} (guiavila ou {{produto_slug}})
2. **15 dias após a data da compra**, a {{LMS}} envia os dados automaticamente para o {{PLATAFORMA_NF}}
3. {{PLATAFORMA_NF}} emite a NFS-e automaticamente para o cliente
4. Nenhuma ação manual é necessária

**Plataformas com esse fluxo:**
- {{LMS}} Gui Ávila (`guiavila`)
- {{LMS}} {{EMPRESA_NEGOCIO}} (`{{produto_slug}}`)

---

## O que NÃO precisa de NF manual

- Saques da {{LMS}} que caem no {{BANCO_PJ}} — a NF já foi emitida para o cliente no momento da compra (15 dias depois)
- Essas entradas no Inter vêm identificadas como transferências da {{LMS}} (guiavila ou {{produto_slug}})

---

## O que PRECISA de NF manual

Toda entrada no {{BANCO_PJ}} que **não seja** saque de plataforma {{LMS}}:
- Pagamentos diretos de mentoria
- Consultorias avulsas
- Qualquer transferência/PIX de cliente sem venda pela plataforma
- Outros serviços prestados diretamente

**Ferramenta:** {{PLATAFORMA_NF}} (app.{{PLATAFORMA_NF_URL}}) — conta {{EMPRESA_HOLDING_ID}}

---

## Pendência de automação (urgente)

Hoje a emissão de NF manual é feita pelo {{SUPORTE}}. O objetivo é automatizar:
- Agente financeiro monitora entradas no {{BANCO_PJ}} via API
- Identifica se é saque da {{LMS}} (sem ação) ou entrada direta (emite NF via API do {{PLATAFORMA_NF}})
- Notifica o {{SUPORTE}}/Gui apenas para confirmar dados quando necessário

**Pré-requisito:** API do {{PLATAFORMA_NF}} + API do {{BANCO_PJ}} conectadas ao squad-financeiro.

---

## Caso especial — NF para CNPJ

Quando cliente compra pela {{LMS}} com CPF mas quer NF para CNPJ da empresa:
- A NF automática foi emitida para o CPF
- É necessário cancelar a NF original e emitir nova para o CNPJ
- Fazer manualmente no {{PLATAFORMA_NF}} por enquanto
- Caso: {{CONTADORA}} — TSM FAé Treinamentos LTDA — CNPJ 00.000.000/0000-00 — cliente_exemplo@gmail.com
