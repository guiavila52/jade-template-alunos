---
name: adicionar-novo-video-na-lista-para-gravar
description: Captura conteúdo bruto (texto livre, link YouTube ou documento) e cria ideia de vídeo no {{PLATAFORMA_NEWSLETTER}} com título, ângulo, hook e roteiro estruturado — status pronto_para_gravar + urgent.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-6 -->

# /adicionar-novo-video-na-lista-para-gravar

Captura conteúdo em qualquer formato, extrai ideia e gera roteiro estruturado, depois cria tudo no **{{PLATAFORMA_NEWSLETTER}}** silenciosamente. {{NOME_OPERADOR_CURTO}} só vê: confirmação rápida → URL do card.

## Passo 1 — Receber conteúdo

Skill ativa e aguarda input do {{NOME_OPERADOR_CURTO}}. Três tipos aceitos:

| Tipo | Exemplo |
|---|---|
| Texto livre | "Quero gravar sobre como montar squad de agentes em 7 dias" |
| Link YouTube | `https://youtube.com/watch?v=...` (referência, inspiração, concorrente) |
| Documento | Caminho de PDF, DOCX, MD — ou conteúdo colado diretamente |

**Se {{NOME_OPERADOR_CURTO}} não mandou conteúdo ainda:** perguntar "Manda o conteúdo — pode ser texto, link YouTube ou caminho de documento."

## Passo 2 — Processar por tipo (silencioso)

Todo o processamento técnico roda em silêncio. {{NOME_OPERADOR_CURTO}} não vê erros de diff, tolerância, retry ou detalhes de transcrição. Se algo falhar de forma irrecuperável, reportar em 1 linha simples.

**Texto livre:** usar diretamente como contexto.

**Link YouTube:**
```bash
# 1. Metadata
yt-dlp --print "%(title)s|%(duration)s|%(id)s" URL

# 2. Legendas (tenta pt-BR primeiro, fallback EN)
yt-dlp --write-auto-sub --sub-lang "pt-orig,pt,pt-BR,en" \
  --sub-format vtt --skip-download \
  -o "/tmp/transcribe-%(id)s.%(ext)s" URL

# Se 429, aguardar 4s e tentar só --sub-lang "en"
```

**Parser VTT — regras críticas:**
- Rolling captions: manter só linhas com tag `<HH:MM:SS.mmm>`, remover restante
- Dedup: apenas consecutivos idênticos (NÃO set global — texto do final do vídeo pode coincidir com texto anterior)
- Agrupar em parágrafos de 30–60s com flush forçado no último cue
- Verificação de completude: usar END timestamp do último parágrafo (não o START) vs duração total
- Tolerância = max(15s, 2% da duração). Se diff > tolerância: retry 1x silencioso (limpar VTT e rebaixar). Se retry falhar, usar o que tem e prosseguir.

**Limpeza Claude (auto-sub):**
- Modelo: `claude-haiku-4-5-20251001`, lotes de 10, 4 paralelos
- Corrigir só termos técnicos errados, typos, nomes próprios. Não reformular.
- API key em `app/.env.local` → `ANTHROPIC_API_KEY`

**Salvar transcrição:**
`workspace/output/transcricoes/YYYY-MM-DD-{slug}.md`

**Documento:** Read tool (PDF → `anthropic-skills:pdf`, DOCX → `anthropic-skills:docx`, MD → Read direto)

## Passo 3 — Derivar campos + roteiro

Com o conteúdo processado, extrair/gerar:

- **`titulo`** — título do NOSSO vídeo sobre o tema. Tom {{NOME_OPERADOR}}: direto, sem clickbait vazio. Não copiar título do vídeo de referência.
- **`angulo`** — 1-2 frases: diferencial, por que agora, pra quem
- **`magnetic_hook`** — 1 frase que para o scroll nos primeiros 3 segundos
- **`formato`** — default `youtube-longo`. Se {{NOME_OPERADOR_CURTO}} mencionou "short/vertical/reels/60s" → `youtube-vertical`
- **`roteiro`** — estrutura completa (ver abaixo)

### Formato do roteiro

```markdown
## Hook (0:00–0:30)
[frase de abertura falada]

## Intro (0:30–1:30)
[por que importa, o que o espectador vai aprender]

## [Seção 1] (~X min)
- Ponto chave com bullet
- Exemplo prático

## [Seção N] (~X min)
- ...

## CTA Principal
[o que pedir]

## Encerramento (30s)
[fechamento + teaser próximo vídeo]
```

Para vídeo de referência YouTube: reinterpretar tópicos no contexto do {{NOME_OPERADOR_CURTO}}, não traduzir. Organizar por progressão lógica (ex: básico → avançado, problema → solução → ação).

Para `youtube-vertical`: script corrido falado de ~60s, sem seções.

**Confirmação antes de criar — breve e visual:**

```
Título: {titulo}
Seções: Hook → {seção 1} → {seção 2} → ... → CTA

OK?
```

Só título + nomes das seções em linha. Sem ângulo, sem hook, sem roteiro completo. Aguardar OK ou ajuste pontual.

## Passo 4 — Criar no {{PLATAFORMA_NEWSLETTER}}

**Setup:**
```bash
set -a; source app/.env.local; set +a
ENDPOINT="${CONTENT_API_BASE_URL}/youtube"  # ou /vertical
```

**POST:**
```bash
jq -n --arg title "$titulo" --arg status "pronto_para_gravar" \
  --arg origin_type "squad" --arg origin_label "Squad de agentes" --arg priority "urgent" \
  '{title:$title,status:$status,origin_type:$origin_type,origin_label:$origin_label,priority:$priority}' \
  | curl -s -o /tmp/{{plataforma_newsletter}}_post.json -w "%{http_code}" -X POST \
    -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" -H "Content-Type: application/json" \
    --data-binary @- "$ENDPOINT"

ID=$(jq -r '.data.id // .id' /tmp/{{plataforma_newsletter}}_post.json)
```

**PATCH (sempre --rawfile para evitar expansão de `$`):**
```bash
# youtube-longo
jq -n --rawfile idea <(printf '%s

---
%s' "$angulo" "$contexto") \
      --rawfile script <(printf '%s' "$roteiro") \
      --arg hook "$magnetic_hook" \
  '{idea:$idea,summary:$idea,script:$script,magnetic_hook:$hook}' \
  | curl -s -o /dev/null -w "%{http_code}" -X PATCH \
    -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" -H "Content-Type: application/json" \
    --data-binary @- "${ENDPOINT}/${ID}"

# youtube-vertical
jq -n --rawfile script <(printf '%s' "$roteiro") '{script:$script}' \
  | curl -s -o /dev/null -w "%{http_code}" -X PATCH \
    -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" -H "Content-Type: application/json" \
    --data-binary @- "${ENDPOINT}/${ID}"
```

**GET validar (silencioso — só verifica, não exibe pro {{NOME_OPERADOR_CURTO}}):**
```bash
curl -s -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" "${ENDPOINT}/${ID}" \
  | jq '{ok: ((.data.idea//""|length) > 0 and (.data.script//""|length) > 0)}'
```

## Passo 5 — Reportar (curto)

```
✅ Adicionado na lista pra gravar

Título: {titulo}
URL: https://{{plataforma_newsletter}}.{{DOMINIO}}/{{HANDLE_OPERADOR}}/conteudos/{id}
```

Nada mais. Sem status, sem prioridade, sem script_len, sem diff. Só título e link.

## Critério de aceitação (interno, não exibir)

- POST 201 + ID válido
- PATCH 200
- GET confirma `idea` e `script` preenchidos (length > 0)

## Pegadinhas (referência interna)

- Diff usa END do último parágrafo, não START — bug antigo causava falso INCOMPLETA
- Dedup consecutivo, não set global — texto do final do vídeo pode coincidir com meio
- `$` no shell → `--rawfile` obrigatório no jq
- PATCH 200 silencioso → sempre validar via GET
- `admin_url` retorna null → montar manualmente com ID
- YouTube 429 no PT → aguardar 4s e tentar só EN

## Aprendizado (Regra §5)

- Bug novo no parser → atualizar seção "Parser VTT — regras críticas"
- Campo novo na API → adicionar ao PATCH
- Formato novo → adicionar enum + endpoint