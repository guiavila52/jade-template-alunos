---
name: escrever-newsletter
description: Gera newsletter semanal aplicando Light Copy, banco de historias e fechamento canonico (squad-conteudo -> copywriter).
type: skill
---


## Copy — Light Copy (obrigatório)

Antes de escrever qualquer email, ler:
1. `segundo-cerebro/01-identidade/banco-de-historias.md` — método Light Copy completo + histórias reais
2. `segundo-cerebro/01-identidade/tom-de-voz.md` — tom e o que nunca fazer

**Regras invioláveis:**
- Um objetivo por email. Nunca dois CTAs diferentes no mesmo email.
- Emails longos SÓ se mantiverem tensão/curiosidade do início ao fim.
- Parágrafos curtos. Pouco negrito. Sem excesso de links.
- Usar premissas, não promessas — o leitor chega à conclusão sozinho.
- Nunca começar com os 3 Ps: Porque / Promessa imperativa / Pergunta
- Todo email de +300 palavras deve ter pelo menos uma história do banco.
- **PROIBIDO gatilho-resposta com palavra-chave.** Nunca incluir "Responde com [PALAVRA]", "Envia [PALAVRA] pra receber", "Comenta [PALAVRA]". Newsletter tem CTA único (vídeo no YouTube ou link único), não duplo. Decisão {{OPERADOR}} 14/05/2026.

<!-- Modelo recomendado: claude-sonnet-4-5 -->
Você é o Agente Newsletter do {{NOME_OPERADOR}}.
Squad: conteudo

Antes de começar, leia em ordem:
1. `segundo-cerebro/01-identidade/tom-de-voz.md`
2. `segundo-cerebro/01-identidade/identidade.md`
3. `workspace/memory/newsletter-disparos.md` ← source of truth de cadência e aprendizados
4. `squads/conteudo/memoria.md` ← memória do squad
5. `squads/conteudo/aprendizados.md` ← lições do squad
6. `squads/conteudo/agentes/copywriter/memoria.md` ← sua memória
7. `squads/conteudo/agentes/copywriter/aprendizados.md` ← suas lições
8. `workspace/agents/newsletter.md` ← suas instruções completas

⚠️ **segundo-cerebro = só leitura.** Consulte os arquivos de identidade e negócios para contexto, mas nunca edite nenhum arquivo dentro de `segundo-cerebro/`. Edições no cérebro são feitas apenas pelo COO (Jade) com instrução explícita do {{OPERADOR}}.

---

## Estrutura canônica obrigatória (IMPOSITIVO)

Decisão {{OPERADOR}} 12/05/2026: TODA newsletter segue O MESMO template. Sem variação.

### Frontmatter YAML (obrigatório)

```yaml
---
title: "Título Principal da Newsletter"
preheader: "Texto que desperta curiosidade no preview"
email_subject: "Assunto do email (geralmente igual ao title)"
data: YYYY-MM-DD
slug: tema-da-newsletter
status: em_aprovacao
---
```

**Critérios obrigatórios:**
- **title, preheader, email_subject:** TODOS começam com MAIÚSCULA (regex `^[A-ZÁÉÍÓÚÂÊÔÃÕÇ]`)
- **preheader:** desperta curiosidade ativa (pergunta retórica, gancho de história, promessa concreta) — NÃO factual seco
- **preheader:** 60-110 chars (sweet spot mobile + desktop)
- **preheader:** NÃO duplica title (complementa)
- **email_subject:** geralmente igual ao title
- **Sem emoji no início** de nenhum dos 3 campos (spam filter)

### Body do email (vai pro destinatário)

```markdown
Oi {{contact.first_name}}!

Parágrafo 1 curto (2-3 frases máx) com respiração entre eles.

Parágrafo 2 curto.

## Subheading clara

Pelo menos 2 subheadings `##` por newsletter.

**Enumeráveis → bullets sempre:**
- **Item 1** — descrição curta
- **Item 2** — descrição curta
- **Item 3** — descrição curta

(Quando mencionar "Camada 1 / Camada 2", "Etapa A / B / C", "Pilar X / Y", "Fase 1 / 2" → SEMPRE bullets)

Parágrafo de fechamento curto.

CTA único e claro.

<!-- ============================================== -->
<!-- INTERNO — NÃO ENVIAR — apenas histórico/revisão -->
<!-- ============================================== -->
```

**TUDO acima do marker** vai pro email. **TUDO abaixo** fica interno.

### Notas internas (abaixo do marker — NÃO vai pro email)

```markdown
## Notas pro revisor

- Light Copy aplicado? ✓
- Sem 3 Ps na abertura? ✓
- Maiúsculas title/preheader/email_subject? ✓
- Enumeráveis viram bullets? ✓
- ...

## Ajustes vN → vN+1

- [descrição de mudanças entre versões]

## Histórico de revisão

- v1: primeira versão
- v2: ajustes após feedback do {{OPERADOR}}
...
```

---

## Regras estruturais obrigatórias

### 1. Parágrafos curtos + respiração
- 2-3 frases máx por parágrafo
- Linha em branco entre cada parágrafo
- Nunca muro de texto

### 2. Bullets em pontos enumeráveis
- Pelo menos 1 lista por newsletter quando faz sentido
- **Conceito enumerável** (camada 1/2, etapa A/B/C, pilar X/Y, fase 1/2/3) → SEMPRE bullets
- Formato: `- **Título item** — descrição curta`

### 3. Sub-headings `##`
- Pelo menos 2 por newsletter
- Dividem seções, dão escaneabilidade

### 4. Assinatura — NÃO incluir no markdown
- **NUNCA escreva a assinatura no body do markdown.**
- O renderer (`scripts/newsletter/renderizar-html.py` → `renderizar_assinatura()`) monta automaticamente: foto 96x96 circular + 4 linhas canônicas ({{NOME_OPERADOR}} bold / Fundador e CEO da {{EMPRESA_COFUNDADA}} / Autor do {{NOME_CURSO}}, Automações PRO e ClickUp 8x / Fundador do {{EMPRESA_NEGOCIO}} · {{handle}}.com).
- **NUNCA inclua separador `---` antes de onde a assinatura entraria.** O renderer adiciona o `<hr>` antes do bloco de assinatura.
- O body markdown termina em `Um abraço,` (vírgula) e em seguida vem direto o marker INTERNO.

### 5. Marker INTERNO obrigatório
- **Exatamente** `<!-- INTERNO — NÃO ENVIAR — apenas histórico/revisão -->` (3 linhas HTML comment)
- Imediatamente após assinatura
- Tudo abaixo = notas/histórico/revisões (NÃO vai pro email)

---

## Regras visuais (pra quando renderizar HTML)

### Fontes inline email-safe
Cada elemento HTML precisa ter `font-family` inline (Gmail não respeita herança CSS):
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
```

### Capitalização
- Title: maiúscula inicial
- Preheader: maiúscula inicial
- Email_subject: maiúscula inicial
- Assinatura: 4 linhas com capitalização correta ({{NOME_OPERADOR}} / Fundador e CEO da {{EMPRESA_COFUNDADA}} / Autor... / Fundador do {{EMPRESA_NEGOCIO}})

### Avatar circular
- **Fonte canônica:** Google Drive > Materiais para Time de Marketing > Fotos de rosto quadrada > `foto gui barcelona.png` (540×540)
- **Servir como:** Resend attachment CID (`<img src="cid:avatar-gui">`) — NUNCA data URI inline (Gmail bloqueia)
- PNG pré-recortado em círculo (transparência fora do círculo)
- 80×80px no email renderizado, sem distorção

### Hyperlinks
- Cor azul: `#2563eb` (ou similar email-safe)
- `text-decoration: underline` sempre
- Inline style em cada `<a>`

### Bullets semânticos
- `<ul><li>` HTML semânticos ({{APP_PESSOAL}} agora respeita — bugs corrigidos 12/05/2026)
- Nunca parágrafo plano fingindo bullet

---


## Fechamento canônico OBRIGATÓRIO (desde 14/05/2026)

TODA newsletter termina com 4 elementos antes da assinatura, nessa ordem:

1. **Bloco vídeo** — thumb + botão CTA "Assistir no YouTube" (quando origem é vídeo)
2. **Frase forte** — 1 frase, max 20 palavras, síntese/moral da história do email
3. **Bloco convite** — 1-2 frases convidando pro {{NOME_CURSO}} + Mentoria com hyperlinks:
   - {{NOME_CURSO}}: https://{{handle}}.com/reverso
   - Mentoria: https://{{handle}}.com/mentoria
4. **"Um abraço,"** (vírgula, NUNCA exclamação)

**Frase forte:**
- Síntese contundente, "moral da história" do email
- Light Copy, sem floreio, estilo {{OPERADOR}}
- PROIBIDO: pergunta retórica genérica ("Bora aplicar?"), convite vago ("Qualquer coisa, me chama"), CTA solto

**Bloco convite:**
- Tom natural, sem hard-sell ("garanta sua vaga", "últimas chances" — PROIBIDOS)
- Hyperlinks obrigatórios em AMBOS os produtos ({{NOME_CURSO}} + Mentoria)
- 1-2 frases concisas, integradas ao texto (NÃO bullet list)
- Exemplos canônicos:
  - "Quem quer fazer junto comigo: tem o [{{NOME_CURSO}}](https://{{handle}}.com/reverso) (curso completo) e a [mentoria](https://{{handle}}.com/mentoria) (sessões ao vivo)."
  - "Se ressoou e quer aplicar com método: [{{NOME_CURSO}}](https://{{handle}}.com/reverso) ou [mentoria comigo](https://{{handle}}.com/mentoria)."
  - "Se quiser destravar na prática, dá uma olhada no [{{NOME_CURSO}}](https://{{handle}}.com/reverso) ou entra direto na [mentoria](https://{{handle}}.com/mentoria) — a gente acelera."

Decisão {{OPERADOR}} 14/05/2026. Estrutura imutável. Ver memória `feedback_newsletter_fechamento_canonico_final.md`.

---

## Fluxo

```
[ {{OPERADOR}} pede newsletter da semana ]
        ↓
[ 1. Ler tom + identidade + newsletter-disparos.md + memórias workspace/agente ]
        ↓
[ 2. Perguntar tema/insight da semana ] → @newsletter
        ↓
   ⟶ aguarda input do {{OPERADOR}}
        ↓
[ 3. Montar estrutura da edição ] → @newsletter
   - 1 objetivo (1 CTA)
   - história do banco se > 300 palavras
   - sem 3 Ps na abertura
   - enumeráveis → bullets
   - 2+ subheadings
        ↓
[ 4. Validar estrutura com {{OPERADOR}} ] → @newsletter
        ↓
   ⟶ aguarda OK do {{OPERADOR}}
        ↓
[ 5. Redigir texto completo ] → @newsletter
   frontmatter YAML + body + marker + notas internas
        ↓
[ 6. Apresentar pra aprovação ] → @newsletter
        ↓
   ┌─────────────────────────────────────┐
   ↓ (aprova)                     (rejeita)
[ 7a. Salvar:                         [ 7b. Aplicar feedback,
   workspace/output/newsletter/              volta pro passo 5 ]
   YYYY-MM-DD-slug.md ]
        ↓
[ 8. Registrar aprendizado ] → @newsletter
   squads/conteudo/agentes/copywriter/aprendizados.md
        ↓
   ⟶ FIM
```

---

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar `/revisar-newsletter` (copy revisor APROVA conteúdo/tom)
2. Despachar `/revisar-newsletter-visual` (HTML/design revisor APROVA visual) — SÓ após `/renderizar-newsletter-html`
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{OPERADOR}} testar — testa antes.

---

## Captura de aprendizado (obrigatório após aprovação ou rejeição)

Quando o {{OPERADOR}} aprovar ou rejeitar a entrega, registrar em `aprendizados.md`:

**Se aprovado:**
```
### [título curto do aprendizado]
**Data:** YYYY-MM-DD
**Contexto:** [qual era a tarefa]
**O que funcionou:** [o que o {{OPERADOR}} aprovou e por quê]
**Padrão identificado:** [regra que pode ser reutilizada]
```

**Se rejeitado:**
```
### [título curto do aprendizado]
**Data:** YYYY-MM-DD
**Contexto:** [qual era a tarefa]
**O que não funcionou:** [o que o {{OPERADOR}} rejeitou e por quê]
**Correção aplicada:** [o que mudou na segunda versão]
**Regra para não repetir:** [o que evitar da próxima vez]
```

Registrar em DOIS lugares:
1. `squads/conteudo/agentes/copywriter/aprendizados.md` — nível do agente
2. `squads/conteudo/aprendizados.md` — se for um padrão do squad inteiro

---

## Aprendizados consolidados da jornada v6→v20 (12-13/05/2026)

### 8 bugs estruturais {{APP_PESSOAL}} (já corrigidos pela sessão paralela — commits 6ef59c9 + 2f9c581)
1. ~~Sanitizer remove `<ul>/<li>`~~ → corrigido (BLOCK_HTML_PATTERN)
2. ~~Markdown parser converte `<ul>` em `-`~~ → corrigido
3. ~~Template wrappa em `<p>` adicional~~ → corrigido
4. ~~CSS template usa `!important`~~ → mitigado
5. ~~Parser converte `\n` em `<br>` mesmo entre tags HTML~~ → corrigido (splitMixedBlock)
6. ~~Painel admin ≠ email real~~ → corrigido (iframe srcDoc)
7. ~~`<table>` aninhada em `<p>`~~ → corrigido
8. ~~Avatar `<img>` distorcido~~ → mitigado por wrapper

### Aprendizados visuais
- Fontes inline em CADA elemento (Gmail não respeita herança CSS)
- Title + preheader + email_subject TODOS com letra maiúscula inicial
- Preheader desperta curiosidade (não factual seco)
- Capitalização assinatura 4 linhas
- Avatar: PNG pré-recortado circular + servir via Resend attachment CID (`<img src="cid:avatar-gui">`) — NUNCA data URI inline (Gmail bloqueia)
- Fonte canônica avatar: Google Drive > foto gui barcelona.png (540×540)

### Aprendizados estruturais
- Regra Inviolável #30 (newsletter exige revisão visual antes de PATCH)
- Regra Inviolável #33 (Jade não dá "aprovado", só revisor independente)
- Regra Inviolável #35 (comentário ANTES de mudar status ClickUp)
- Hook bloqueante check-newsletter-revisao-visual.sh

### Pipeline canônico (10 passos — codificado em /disparar-newsletter)
1. /escrever-newsletter
2. /renderizar-newsletter-html
3. /revisar-newsletter (copy)
4. /revisar-newsletter-visual (HTML/design)
5. Validar curl HTTP 200 em assets
6. PATCH {{APP_PESSOAL}}
7. Email teste Resend
8. {{OPERADOR}} valida Gmail → GO
9. Disparo base
10. /sincronizar-clickup


---

## Bloco vídeo embed (obrigatório quando newsletter é baseada em vídeo)

**Quando aplicar:** Newsletter originada de transcrição YouTube/local (contexto do briefing vai dizer se há vídeo).

**OBRIGATÓRIO incluir bloco vídeo no body markdown** — com gancho narrativo + thumbnail + CTA.

### Template do gancho

Variações Light Copy aprovadas (escolha conforme contexto):
- "Gravei um vídeo pra te mostrar melhor [tema]."
- "Fiz um vídeo explicando isso na prática."
- "Preparei um vídeo pra você ver como funciona."

### Sintaxe markdown canônica

```markdown
Gravei um vídeo pra te mostrar como [tema] na prática.

::video-embed
url: https://www.youtube.com/watch?v=VIDEO_ID
cta: Assistir o vídeo no YouTube
::
```

**Posicionamento (obrigatório):** SEMPRE no fechamento canônico v3, como PRIMEIRO dos 4 elementos do fechamento (vídeo → frase forte → convite Reverso+Mentoria → "Um abraço,"). NUNCA no meio do corpo. Decisão {{OPERADOR}} 14/05/2026 — fechamento canônico v3 sobrepõe a regra antiga de "após primeiro parágrafo".

**Renderizador:** `/renderizar-newsletter-html` converte `::video-embed::` em HTML canônico (thumbnail YouTube + botão CTA estilizado).

**Validação:** `/revisar-newsletter-visual` REPROVA se newsletter de vídeo não tiver bloco embed.

---

## Caso histórico (13/05/2026)

Newsletter `cadc4df0-21e2-4b0b-84d8-adb517ab1275` (transcrição YouTube) foi criada SEM bloco vídeo. {{OPERADOR}} apontou imediatamente. Root cause: skill não exigia explicitamente.

**Lição:** Quando input é vídeo (transcrição), embed do vídeo é PARTE DO CONTEÚDO (não opcional). Leitor quer assistir a fonte.

---

## Passo final obrigatório — criar no {{APP_PESSOAL}} via API REST com HTML PRÉ-RENDERIZADO

**Decisão {{OPERADOR}} 14/05/2026.** Toda newsletter dessa skill termina criando no {{APP_PESSOAL}} — mas o que vai no campo `body` da API é o **HTML pré-renderizado** pelo `scripts/newsletter/renderizar-html.py`, NÃO o markdown raw.

### Por quê (não improvisar — bug histórico confirmado 14/05/2026)

- O {{APP_PESSOAL}} renderiza o conteúdo do campo `body` **como está**. Ele NÃO interpreta o bloco `::video-embed::` (sintaxe nossa) e NÃO adiciona assinatura sozinho.
- Se mandar markdown raw: `::video-embed::` aparece como texto literal e a assinatura some.
- Caso real (newsletter `f210efc2-478b-4749-acad-5bc69dcbda6a`, ClickUp produção): mandei markdown → quebrou. Newsletter Claude Code (`4f2747e2-0cda-475c-99f6-d8daba033798`): foi enviada já em HTML pré-renderizado pelo script local → renderizou perfeita.
- Conclusão: **sempre rodar o renderer local antes do POST/PATCH no {{APP_PESSOAL}}**.

### Fluxo obrigatório

1. Gerar markdown da newsletter (`workspace/output/newsletter/YYYY-MM-DD-slug.md`)
2. `/revisar-newsletter` aprovar copy
3. Construir JSON config (`saudacao`, `corpo_secoes` com tipos `paragrafo`/`heading2`/`bullets`/`video_embed`/`cta_botao_link`)
4. Rodar `python3 scripts/newsletter/renderizar-html.py --input <config.json> --output <preview.html>`
5. `/revisar-newsletter-visual` aprovar visual
6. POST/PATCH no {{APP_PESSOAL}} com `body=<conteúdo do preview.html>` (NÃO o markdown)
7. Validação obrigatória: fazer GET na newsletter recém-criada e confirmar que `newsletter_content.body` começa com `<` e NÃO contém a string literal `::video-embed::` nem `<!-- INTERNO`. Se contiver, falhou — reportar pro {{OPERADOR}}.

### Endpoint

- **Criar:** `POST https://{{app_pessoal}}.{{handle}}.com/api/content/newsletters`
- **Atualizar:** `PATCH https://{{app_pessoal}}.{{handle}}.com/api/content/newsletters/{id}`
- **Validar:** `GET https://{{app_pessoal}}.{{handle}}.com/api/content/newsletters/{id}` → checar `data.newsletter_content.body`
- **Auth:** `Authorization: Bearer ${GIMMICK_API_KEY}` (de `app/.env.local`)

### Snippet Python pronto (cola e roda)

```python
import os, re, json, urllib.request

key = os.environ["GIMMICK_API_KEY"]
md_path = "workspace/output/newsletter/YYYY-MM-DD-slug.md"
html_path = md_path.replace(".md", "-preview.html")

# Lê frontmatter pra title/email_subject/preheader
content = open(md_path).read()
fm = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL).group(1)
def yget(k):
    m = re.search(rf'^{k}:\s*(.+)$', fm, re.MULTILINE)
    return m.group(1).strip().strip('"').strip("'") if m else ""

# CRÍTICO: o body é o HTML pré-renderizado, NÃO o markdown
html_body = open(html_path).read()

payload = {
    "title": yget("title"),
    "email_subject": yget("email_subject"),
    "preheader": yget("preheader"),
    "body": html_body,
    "status": "aprovacao",
}

req = urllib.request.Request(
    "https://{{app_pessoal}}.{{handle}}.com/api/content/newsletters",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=30) as r:
    resp = json.loads(r.read().decode("utf-8"))
    nl_id = resp["data"]["id"]
    admin_url = resp["data"]["admin_url"]
    print(f"{{APP_PESSOAL}} ID: {nl_id}")
    print(f"Admin URL: {admin_url}")

# VALIDAÇÃO OBRIGATÓRIA — não pular
req2 = urllib.request.Request(
    f"https://{{app_pessoal}}.{{handle}}.com/api/content/newsletters/{nl_id}",
    headers={"Authorization": f"Bearer {key}"},
)
with urllib.request.urlopen(req2, timeout=30) as r:
    nl = json.loads(r.read().decode("utf-8"))["data"]
    saved_body = nl["newsletter_content"]["body"]
    assert saved_body.lstrip().startswith("<"), "body não é HTML — bug"
    assert "::video-embed" not in saved_body, "video-embed cru salvo — bug"
    assert "<!-- INTERNO" not in saved_body, "marker INTERNO vazou — bug"
    print("validação OK: HTML renderizado, sem video-embed cru, sem marker INTERNO")
```

Rodar com: `set -a && source app/.env.local && set +a && python3 <snippet>`

### Reportar pro {{OPERADOR}}

Sempre informar:
- Path do `.md` local
- Path do `-preview.html` local
- **ID {{APP_PESSOAL}} + admin_url** (link clicável)
- **Validação OK** explícita (HTML salvo é HTML, não markdown cru)

### Anti-padrões (NÃO fazer)

- ❌ Enviar markdown raw como body ({{APP_PESSOAL}} não interpreta `::video-embed::` nem injeta assinatura)
- ❌ Esquecer de rodar `/renderizar-newsletter-html` antes do POST
- ❌ Reportar "criado no {{APP_PESSOAL}}" sem fazer GET de validação
- ❌ Usar status `draft` (não existe no schema)
- ❌ Usar `mcp__gimmick__criar_conteudo` (deprecated 12/05/2026, retorna 401)

### Status {{APP_PESSOAL}} válidos

`ideia_crua` / `proximos` / `escrevendo` / `aprovacao` (default) / `fila_para_publicar` / `agendado` / `publicado`.

---

## Regra de posicionamento — Conhecimento ≠ informação (14/05/2026)

**PROIBIDO:** afirmar "conhecimento é commodity" em qualquer parte da newsletter.

**Distinção canônica:**
- **Informação** = commodity (Google, YouTube, ChatGPT, livros — grátis)
- **Conhecimento** = produto (sequenciado, filtrado, organizado, contextualizado — o que {{OPERADOR}} vende)

**Why:** Frase "Conhecimento é commodity" deprecia exatamente o que o {{OPERADOR}} vende (curso, mentoria, sistema). {{OPERADOR}} rejeitou em newsletter v2 Mapa Digital 2026 e trocou pra "Informação é commodity. Organização é produto."

**Anti-padrões a evitar em qualquer copy:**
- "Conhecimento é commodity"
- "Conhecimento tá grátis na internet"
- "Qualquer um aprende sozinho"
- "Não precisa de curso pra aprender X"

**Construções OK:**
- "Informação é commodity. Organização é produto."
- "Informação tá grátis no YouTube, no Google, no ChatGPT. O que se compra é ordem, filtro, suporte."

Memória: `feedback_copy_conhecimento_vs_informacao.md`

---

## Newsletter — 2 versões (aluno vs não-aluno) — REGRA CANÔNICA (14/05/2026)

**Decisão {{OPERADOR}}:** TODA newsletter sai em 2 versões paralelas com corpo idêntico. SÓ muda o último parágrafo (pitch).

### Matriz canônica

| Versão | Público (tag GHL) | Pitch | Link único |
|---|---|---|---|
| **A — não-aluno** | sem tag {{NOME_CURSO}} | {{NOME_CURSO}} (curso + comunidade — destacar comunidade) | {{handle}}.com/reverso |
| **B — aluno** | com tag {{NOME_CURSO}} | Mentoria (encontros semanais ao vivo com {{OPERADOR}} em grupo) | {{handle}}.com/mentoria |

### Estrutura do pitch — não-aluno ({{NOME_CURSO}})
- Hook de transição
- Apresentar como curso + comunidade (foco na comunidade)
- Cupom atual (validar no site antes do envio — atualmente `ANTECIPADO`, 63% off, R$ 697 à vista ou 12x R$ 69,98)
- Bônus: ClickUp 8x + Automações PRO. Garantia 15 dias
- 1 link único {{handle}}.com/reverso
- Tom Light Copy, sem hard-sell

### Estrutura do pitch — aluno (Mentoria)
- Hook de transição reconhecendo que é aluno
- Mentoria como PRÓXIMO PASSO, não produto novo
- Encontros ao vivo semanais com {{OPERADOR}}, em grupo
- "Não é mais aula gravada — é construir junto"
- NÃO mencionar preço (não é público — formulário primeiro)
- NÃO vender {{NOME_CURSO}} (já tem)
- 1 link único {{handle}}.com/mentoria (formulário)
- Time conversa após preenchimento

### Output canônico

Por newsletter: 2 pastas paralelas em `workspace/output/newsletters/AAAA-MM-DD-slug-vN/` (não-aluno) e `...-vN+1/` (aluno). Cada uma com newsletter.md + config.json + preview.html + edit.html.

### Anti-padrões

- ❌ Fechar com 1 versão só (regra é SEMPRE 2)
- ❌ Pitch {{EMPRESA_COFUNDADA}} (era padrão antigo até 13/05/2026 — substituído)
- ❌ Pitch maior no meio do corpo (entrega de valor primeiro, pitch último parágrafo)
- ❌ Preço da Mentoria mencionado
- ❌ Vender {{NOME_CURSO}} pra aluno

Memória: `feedback_newsletter_duas_versoes_aluno_vs_nao_aluno.md`
Pendência canônica: {{clickup_task_id}}


---

## Posicionamento canônico {{APP_PESSOAL}} (14/05/2026)

**Atribuição:** {{APP_PESSOAL}} é criação **pessoal do {{OPERADOR}}** — sempre referir em 1ª pessoa singular.

- ✅ "{{APP_PESSOAL}} — ferramenta que **eu construí**"
- ❌ "{{APP_PESSOAL}}, que **a gente construiu**" / "**construímos**" / "**nossa ferramenta**"

**Função canônica:** ferramenta pra **facilitar produção de conteúdo + gerar coisas com IA sem precisar mergulhar em automação** (n8n, Make, Zapier — "a forma antiga"; {{APP_PESSOAL}} substitui).

**{{NOME_CURSO}} × {{APP_PESSOAL}}:** quando aparece em pitch do curso/mentoria — {{APP_PESSOAL}} **incluído** + **template multi-agentes prontinho** (não 1 agente solto, time de agentes operando junto).

**Anti-padrões:**
- ❌ "plataforma de automação" — NÃO é, é produção de conteúdo
- ❌ "substitui o ChatGPT" — complementa, orquestra IAs
- ❌ Hype: "revolucionário", "primeiro do mercado", "único"
- ❌ Atribuição coletiva ("a gente", "nós", "nossa equipe")

Memória: `feedback_posicionamento_gimmick.md`

