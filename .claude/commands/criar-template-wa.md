<!-- Modelo recomendado: claude-sonnet-4-5 -->
# /criar-template-wa — Gera template de WhatsApp para aprovação Meta/GHL

## Fluxo

1. Definir tipo (Utility ou Marketing), idioma e variáveis do template
2. Gerar texto no formato correto com mapeamento de variáveis `{{1}}`, `{{2}}`...
3. Mapear variáveis → campos GHL correspondentes
4. Apresentar template formatado ao operador para revisão
5. Instruir criação manual no GHL: Settings → WhatsApp → Templates → + Create Template
6. Aguardar aprovação Meta (Utility: minutos; Marketing: até 24h)

## Quando usar

Criar template de WhatsApp para submeter à aprovação da Meta via GHL.
Skill focada em **Utility** (lembretes, confirmações, avisos que a pessoa pediu pra receber).

---

## Limitação importante — API do GHL

**A API do GHL NÃO permite criar templates via API.** Pesquisa confirmada em 28/05/2026:
- Existe endpoint GET (listar templates existentes), mas não existe POST para criar
- A criação é obrigatoriamente manual via UI do GHL
- Única alternativa para automatizar seria API direta do Meta (WhatsApp Business Cloud), que bypassa o GHL

**Fluxo obrigatório:**
1. Esta skill gera o texto do template no formato correto (com mapeamento de variáveis)
2. operador copia e cria manualmente no GHL: **Settings → WhatsApp → Templates → + Create Template**
3. Meta aprova (Utility: normalmente em minutos; Marketing: até 24h)
4. Aprovado → agendado via GHL Workflows ou Conversations

---

## Contas GHL disponíveis

| Conta | Quando usar |
|---|---|
| **{{NOME_OPERADOR}}** (pessoal) | Comunicações com a base do operador |
| **{{PLATAFORMA_CURSOS}}** | Comunicações com alunos da {{PLATAFORMA_CURSOS}} |

Jade sempre pergunta qual conta antes de gerar o template se não estiver claro.

---

## Categorias suportadas

| Categoria | Quando usar |
|---|---|
| **Utility** | Lembrete de evento, confirmação de compra, aviso de acesso — a pessoa pediu pra receber |
| **Marketing** | Promoção, lançamento, oferta — mais critério, aprovação mais lenta |

---

## Input que Jade coleta antes de despachar

- **Objetivo:** o que o template faz (lembrete 30min antes, confirmação compra, aviso acesso)
- **Categoria:** Utility (default) ou Marketing
- **Evento/contexto:** nome do evento, produto, link de destino
- **Tom:** direto/urgente/empolgado — depende do momento
- **Conta GHL:** {{NOME_OPERADOR}} ou {{PLATAFORMA_CURSOS}}

---

## Regras de copy (obrigatórias)

- Pronome: **você/seu** — nunca tu/teu/ti
- Body: máximo 4 linhas, máximo 1024 chars
- Emojis: máximo 1, só se fizer sentido contextual
- Header: texto curto e claro (até 60 chars) — opcional
- Footer: linha discreta, curta (até 60 chars) — opcional
- Button texto: máximo 20 chars
- Sem gatilhos de spam: "GRÁTIS", "CLIQUE AGORA", "URGENTE" em maiúsculas
- Sem prometer resultados financeiros específicos
- Body Utility deve deixar claro que é algo que a pessoa solicitou: "você pediu", "conforme solicitado", "sua compra foi confirmada"

---

## Variáveis — mapeamento obrigatório no output

O GHL exige, para cada variável usada no body, que você informe:
1. **Campo do CRM** que vai preencher essa variável (ex: `{{contact.first_name}}`)
2. **Exemplo de valor** para a Meta aprovar (ex: "João Pedro")

**Mapeamento padrão:**

| Variável no template | Campo CRM no GHL | Exemplo para Meta |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | João Pedro |
| `{{2}}` | `{{contact.last_name}}` | Silva |
| `{{3}}` | Campo customizado específico | (definir por caso) |

---

## Formato de output canônico

```
NOME DO TEMPLATE: [snake_case_descritivo]
CATEGORIA: Utility | Marketing
IDIOMA: Português (BR)
CONTA GHL: [{{NOME_OPERADOR}} | {{PLATAFORMA_CURSOS}}]

HEADER: [Texto — opcional]
BODY:
[Texto linha 1]
[Texto linha 2 — máx 4 linhas]
FOOTER: [Linha discreta — opcional]
BUTTON: [Texto — máx 20 chars]
URL: [URL de destino]

MAPEAMENTO DE VARIÁVEIS (preencher no GHL ao criar):
  {{1}} → Campo CRM: {{contact.first_name}} | Exemplo: João Pedro
  [{{2}} → Campo CRM: ... | Exemplo: ... — se houver]

---
INSTRUÇÕES PARA CRIAR NO GHL:
Conta: [{{NOME_OPERADOR}} / {{PLATAFORMA_CURSOS}}]
Caminho: Settings → WhatsApp → Templates → + Create Template
Obs: ao inserir {{1}} no body, o GHL abre campo de mapeamento — preencher conforme acima.
```

---

## Exemplo aprovado (com mapeamento)

```
NOME: lembrete_aulao_30min
CATEGORIA: Utility
CONTA GHL: {{PLATAFORMA_CURSOS}}

HEADER: Aulão em 30 minutos
BODY:
Oi, {{1}} — o aulão de Claude Code + time de agentes começa em meia hora (15h).
Você pediu pra receber esse lembrete. Link da sala logo abaixo.
FOOTER: Nos vemos lá
BUTTON: Entrar na sala
URL: https://meet.google.com/xxx-xxxx-xxx

MAPEAMENTO DE VARIÁVEIS:
  {{1}} → Campo CRM: {{contact.first_name}} | Exemplo: João Pedro

---
INSTRUÇÕES: Settings → WhatsApp → Templates → + Create Template (conta {{PLATAFORMA_CURSOS}})
```
