# Regras de Negócio — Emissão de Nota Fiscal

> Documento de referência do squad-financeiro. Atualizado em 06/05/2026.

---

## Regra principal

**Tudo que entra no Banco Inter precisa de NF — com exceção das saídas da {{EMPRESA_COFUNDADA}}.**

---

## Fluxo automático ({{EMPRESA_COFUNDADA}} → Notazz)

1. Cliente compra pela plataforma {{EMPRESA_COFUNDADA}} ({{handle}} ou magicaonline)
2. **15 dias após a data da compra**, a {{EMPRESA_COFUNDADA}} envia os dados automaticamente para o Notazz
3. Notazz emite a NFS-e automaticamente para o cliente
4. Nenhuma ação manual é necessária

**Plataformas com esse fluxo:**
- {{EMPRESA_COFUNDADA}} {{NOME_OPERADOR}} (`{{handle}}`)
- {{EMPRESA_COFUNDADA}} {{EMPRESA_NEGOCIO}} (`magicaonline`)

---

## O que NÃO precisa de NF manual

- Saques da {{EMPRESA_COFUNDADA}} que caem no Banco Inter — a NF já foi emitida para o cliente no momento da compra (15 dias depois)
- Essas entradas no Inter vêm identificadas como transferências da {{EMPRESA_COFUNDADA}} ({{handle}} ou magicaonline)

---

## O que PRECISA de NF manual

Toda entrada no Banco Inter que **não seja** saque de plataforma {{EMPRESA_COFUNDADA}}:
- Pagamentos diretos de mentoria
- Consultorias avulsas
- Qualquer transferência/PIX de cliente sem venda pela plataforma
- Outros serviços prestados diretamente

**Ferramenta:** Notazz (app.notazz.com) — conta {{EMPRESA_HOLDING_UPPER}} (8959)

---

## Pendência de automação (urgente)

Hoje a emissão de NF manual é feita pelo {{NOME_SUPORTE}}. O objetivo é automatizar:
- Agente financeiro monitora entradas no Banco Inter via API
- Identifica se é saque da {{EMPRESA_COFUNDADA}} (sem ação) ou entrada direta (emite NF via API do Notazz)
- Notifica o {{NOME_SUPORTE}}/{{OPERADOR}} apenas para confirmar dados quando necessário

**Pré-requisito:** API do Notazz + API do Banco Inter conectadas ao squad-financeiro.

---

## Caso especial — NF para CNPJ

Quando cliente compra pela {{EMPRESA_COFUNDADA}} com CPF mas quer NF para CNPJ da empresa:
- A NF automática foi emitida para o CPF
- É necessário cancelar a NF original e emitir nova para o CNPJ
- Fazer manualmente no Notazz por enquanto
- Caso: {{EXEMPLO_CLIENTE_NOME}} — {{EXEMPLO_CLIENTE_EMPRESA}} Treinamentos LTDA — CNPJ 00.000.000/0000-00 — cliente@exemplo.com
