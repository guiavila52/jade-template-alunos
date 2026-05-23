---
name: escrever-newsletter
description: Produz e publica a newsletter semanal do {{NOME_OPERADOR}} — compartilhar conhecimento com a base. CTA/pitch é opcional, só adicionado quando Gui pede.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# /escrever-newsletter

## Propósito

Newsletter semanal do {{NOME_OPERADOR}}. Objetivo padrão: **compartilhar conhecimento** com a base.

CTA/Pitch: **OPCIONAL** — Gui pede explicitamente quando quiser. Ex: "adiciona gancho pro Reverso no final." Se não pediu, a newsletter termina em "Um abraço," sem pitch.

---

## Orquestração — quem faz o quê

| Agente / Ferramenta | Papel | Skill |
|---|---|---|
| **Jade** (COO) | Orquestra o fluxo ponta a ponta | — |
| **@copywriter** | Escreve markdown da newsletter | — |
| **@revisor-newsletter** | Revisa copy (revisor independente) | `/revisar-newsletter` |
| **renderizar-html.py** | Converte markdown → HTML email-safe | `/renderizar-newsletter-html` |
| **@designer-revisor** | Revisa HTML visual (revisor independente) | `/revisar-newsletter-visual` |
| **Jade** | Sobe ao {{Plataforma_Conteudo}} via API e valida | — |
| **publicar-ghl.py** | Cria rascunho GHL + envia teste Resend | `scripts/newsletter/publicar-ghl.py` |

> **Regra §2:** Jade orquestra, **nunca** escreve a newsletter.
> **Regra §14:** copywriter produz, revisores copy e visual são agentes separados e independentes.

---

## Fluxo canônico

```
[ Gui pede newsletter ]
        ↓
[ Jade lê: banco-de-historias.md + tom-de-voz.md + newsletter-disparos.md ]
        ↓
[ Jade despacha @copywriter com briefing completo ]
        ↓
[ @copywriter escreve markdown → salva em workspace/output/newsletter/ ]
        ↓
[ Jade despacha @revisor-newsletter ]
        ↓
   REPROVADO? → @copywriter corrige → revisão de novo
        ↓
[ Jade roda renderizar-html.py → gera -preview.html ]
        ↓
[ Jade despacha @designer-revisor com path do HTML ]
        ↓
   REPROVADO? → corrigir markdown → re-renderizar → revisão de novo
        ↓
[ Jade apresenta HTML ao Gui — NUNCA markdown ]
        ↓
   Gui aprova copy? → Jade sobe ao {{Plataforma_Conteudo}} via API → valida GET
        ↓
[ Jade roda publicar-ghl.py → cria rascunho no GHL + envia teste pra {{EMAIL_OPERADOR}} ]
        ↓
[ Gui recebe email teste, confirma OK no chat ]
        ↓
[ Gui agenda manualmente no painel GHL ]
   Gui ajusta copy? → @copywriter corrige → re-renderizar → abrir edit.html → aguardar aprovação
   ⚠️ NÃO rodar publicar-ghl.py durante iteração de copy — só após aprovação final
```

**Regra inviolável (21/05/2026):** Gui **nunca** valida markdown. Toda aprovação acontece em HTML renderizado.

---

## Input

O que Jade precisa antes de despachar @copywriter:

1. **Tema** — insight da semana OU URL de vídeo YouTube
2. **Audiência (obrigatório)** — `minha-base` ({{MARCA_PESSOAL}}) OU `{{EMPRESA_COFUNDADA_SLUG}}`. Se Gui não informar, Jade pergunta antes de prosseguir.
3. **Pitch (opcional)** — Gui diz se quer CTA e pra qual produto (Reverso, Mentoria, outro)

Se o input for URL de vídeo: Jade transcreve com yt-dlp antes de despachar copywriter.

---

## Briefing para @copywriter

Jade despacha com:

- Tema / transcrição completa do vídeo
- **Audiência:** `minha-base` ou `{{EMPRESA_COFUNDADA_SLUG}}` (define variante do PS)
- Pedido de pitch (se houver, com produto e link)
- Regras de conteúdo desta skill
- Path de output canônico: `workspace/output/newsletter/YYYY-MM-DD-{slug}.md`

---

## Regras de conteúdo (copywriter aplica)

### Leitura obrigatória antes de escrever

1. `segundo-cerebro/01-identidade/banco-de-historias.md` — histórias reais + método Light Copy
2. `segundo-cerebro/01-identidade/tom-de-voz.md` — como o Gui fala e o que nunca dizer
3. `workspace/memory/newsletter-disparos.md` — cadência e aprendizados de edições anteriores
4. `squads/conteudo/agentes/copywriter/aprendizados.md` — lições do agente

### Frontmatter YAML obrigatório

```yaml
---
title: "Título da newsletter"
preheader: "Texto que aparece no preview do email"
email_subject: "Assunto do email (geralmente igual ao title)"
data: YYYY-MM-DD
slug: tema-da-newsletter
status: em_aprovacao
---
```

**Critérios:**
- `title`, `preheader`, `email_subject`: TODOS começam com **MAIÚSCULA**
- `preheader`: 60–110 chars, desperta curiosidade, **não duplica** o title
- Sem emoji no início de nenhum dos 3 campos

### Estrutura do body

```markdown
Oi {{contact.first_name}}!

Parágrafo curto. Máximo 2-3 frases por parágrafo.

Linha em branco entre cada parágrafo — sempre.

## Subheading clara

Pelo menos 2 subheadings `##` por newsletter.

Conceito enumerável? → SEMPRE bullets:

- **Item 1** — descrição curta
- **Item 2** — descrição curta
- **Item 3** — descrição curta

Parágrafo de fechamento.

[Bloco vídeo — se origem for YouTube]

[Frase forte]

[Pitch/CTA — só se Gui pediu]

Um abraço,

**PS:** Se você quiser saber mais sobre [referência ao tema da newsletter] e ainda receber dois bônus, entra no [Sistema Reverso](https://{{DOMINIO}}/reverso).

<!-- ============================================== -->
<!-- INTERNO — NÃO ENVIAR — apenas histórico/revisão -->
<!-- ============================================== -->

## Notas pro revisor
...
```

### Light Copy — regras invioláveis

- **Nunca** começar com os 3 Ps: Porque / Promessa imperativa / Pergunta
- Premissas, não promessas — leitor chega à conclusão sozinho
- Parágrafos curtos. Pouco negrito. Sem excesso de links
- Emails longos só se mantiverem tensão/curiosidade do início ao fim
- Newsletter de +300 palavras: incluir pelo menos 1 história do banco

### Bloco vídeo embed (obrigatório quando origem é YouTube)

```markdown
Gravei um vídeo pra te mostrar como [tema] na prática.

::video-embed
url: https://www.youtube.com/watch?v=VIDEO_ID
cta: Assistir o vídeo no YouTube
::
```

Posição: **primeiro elemento do fechamento**, antes da frase forte.

### Hiperlinks em palavras-chave (obrigatório quando há CTA de produto/evento)

Distribuir 2-3 hiperlinks em **palavras-chave centrais do tema** ao longo do corpo — não concentrar cliques apenas no CTA final.

- Identificar 2 palavras-chave que resumam o tema e o destino (ex: "aulão ao vivo", "segundo cérebro")
- Linkar essas palavras para a URL de destino principal: `color:#2563eb; text-decoration:underline; font-weight:700;`
- Máximo 2-3 links intermediários. Não transformar cada frase em hyperlink
- Posicionar nos primeiros 2-3 parágrafos — quem lê rápido encontra o link sem chegar ao final

### Frase forte (obrigatória)

1 frase, máximo 20 palavras. Síntese/moral da história.

**Proibido:** pergunta retórica vaga ("Bora aplicar?"), convite genérico ("qualquer coisa me chama").

### CTA/Pitch (OPCIONAL — só quando Gui pedir)

Se Gui pediu pitch, adicionar 1–2 frases antes de "Um abraço,":

- Tom natural, sem hard-sell ("garanta sua vaga", "últimas chances" — proibido)
- 1 link único (nunca dois CTAs primários no mesmo email)
- Links canônicos: `{{DOMINIO}}/reverso` · `{{DOMINIO}}/mentoria`

Se Gui **não** pediu pitch: a newsletter termina direto em "Um abraço,".

### PS — OBRIGATÓRIO em toda newsletter

Sempre após "Um abraço,", antes do marker INTERNO. Variante depende da **audiência**:

**Audiência `minha-base`:**
```
**PS:** Se você quiser saber mais sobre [referência ao tema da newsletter] e ainda receber dois bônus, entra no [Sistema Reverso](https://{{DOMINIO}}/reverso).
```

**Audiência `{{EMPRESA_COFUNDADA_SLUG}}`:**
```
**PS:** Se você quiser [referência ao tema aplicado à {{EMPRESA_COFUNDADA}}], dá uma olhada no que a gente tá construindo lá na [{{EMPRESA_COFUNDADA}}](https://{{DOMINIO}}/{{lms_slug}}).
```

**Regras:**
- **[referência ao tema]** → adaptar pra conectar com o assunto da newsletter
- Tom natural, não hard-sell
- Links canônicos: `minha-base` → `https://{{DOMINIO}}/reverso` · `{{EMPRESA_COFUNDADA_SLUG}}` → `https://{{DOMINIO}}/{{lms_slug}}`
- Nunca remover o PS, mesmo quando não há pitch principal
- Nunca misturar: newsletter pra {{EMPRESA_COFUNDADA}} nunca menciona o Reverso

### Assinatura

**Nunca escrever assinatura no markdown.** O renderer (`renderizar-html.py`) monta automaticamente: foto circular 80×80 + 4 linhas canônicas.

O body termina em `Um abraço,` (vírgula — nunca exclamação) seguido direto pelo marker INTERNO.

### Marker INTERNO obrigatório

Exatamente após "Um abraço,":

```
<!-- ============================================== -->
<!-- INTERNO — NÃO ENVIAR — apenas histórico/revisão -->
<!-- ============================================== -->
```

Tudo abaixo = notas internas (não vai pro email).

---

## Renderização HTML

Após aprovação de copy, Jade roda:

```bash
python3 scripts/newsletter/renderizar-html.py \
  --input workspace/output/newsletter/YYYY-MM-DD-{slug}-config.json \
  --output workspace/output/newsletter/YYYY-MM-DD-{slug}-edit.html \
  --editable
```

O config JSON é gerado por Jade a partir do markdown aprovado. Ver `/renderizar-newsletter-html` para formato do JSON.

---

## Subida ao {{Plataforma_Conteudo}} (após aprovação visual)

```python
# CRÍTICO: body = HTML renderizado, NUNCA markdown raw
payload = {
    "title": ...,
    "email_subject": ...,
    "preheader": ...,
    "body": html_renderizado,
    "status": "aprovacao",
}
# POST para https://{{plataforma_conteudo}}.{{DOMINIO}}/api/content/newsletters
# Auth: Authorization: Bearer ${CONTENT_API_KEY}
```

**Validação obrigatória pós-POST:** GET na newsletter criada → confirmar que `body` começa com `<` e não contém `::video-embed` ou `<!-- INTERNO`.

---

## Publicação no GHL (após {{Plataforma_Conteudo}} aprovado)

```bash
python3 scripts/newsletter/publicar-ghl.py \
  --html workspace/output/newsletter/YYYY-MM-DD-{slug}-preview.html \
  --md workspace/output/newsletter/YYYY-MM-DD-{slug}.md
```

**O que o script faz:**
1. Cria campanha de email no GHL como **rascunho** (não envia ainda)
2. Envia email de teste para `{{EMAIL_OPERADOR}}` via Resend (com banner indicando URL da campanha)
3. Retorna URL do rascunho no painel GHL

**Fluxo após o script:**
- Jade apresenta URL da campanha no GHL
- Gui recebe o email de teste, confere no inbox
- Gui dá **OK no chat** confirmando que o email chegou certo
- Gui acessa o painel GHL e agenda o disparo (newsletter = toda **terça-feira 09:00 BRT**)

⚠️ **REGRA INVIOLÁVEL:** `publicar-ghl.py` roda UMA única vez — quando Gui aprova a copy final.
Durante iteração de copy (ajustes, revisões), Jade renderiza o HTML e abre o `-edit.html` para Gui revisar localmente. NUNCA rodar publicar-ghl.py a cada ajuste de copy.

**Chave Resend:** `RESEND_API_KEY` em `app/.env.local`. Se expirada → Gui regenera em resend.com/api-keys e atualiza o .env.local.

**Chave GHL:** `GHL_API_KEY` em `app/.env.local` (PIT token). Se retornar 401 → Gui regenera em GHL → Private Integrations.

---

## Apresentação ao Gui

- Mostrar **path do preview.html** + abrir no browser (`open`)
- Mostrar **link admin {{Plataforma_Conteudo}}** (após subida)
- **Nunca** mostrar markdown ao Gui

---

## Aprendizado (após aprovação ou rejeição do Gui)

Registrar em 2 lugares:
1. `squads/conteudo/agentes/copywriter/aprendizados.md`
2. `squads/conteudo/aprendizados.md` (se for padrão do squad)

---

## Proibições permanentes

- ❌ Gatilho-resposta: "Responde com X", "Envia Y pra receber Z" — proibido desde 14/05/2026
- ❌ "Conhecimento é commodity" — deprecia o produto do Gui (usar "informação é commodity")
- ❌ Métricas de receita em R$ no body
- ❌ Pitch sem Gui ter pedido
- ❌ Markdown entregue ao Gui sem renderizar
