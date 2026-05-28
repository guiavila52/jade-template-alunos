<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /criar-ideia-conteudo

Cria ideia de conteúdo crua no **{{PLATAFORMA_NEWSLETTER}}** (pipeline editorial) **via API REST direta (curl)**. Não usa MCP — funciona em subagent headless e cron.

Análoga à `/criar-pendencia` (ClickUp), mas o destino é o backlog editorial do {{PLATAFORMA_NEWSLETTER}}.

> Histórico/setup completo: `segundo-cerebro/03-operacao/{{plataforma_newsletter}}-historico.md` (seções youtube/vertical schemas, descobertos 16/05/2026).

## Quando invocar

- {{NOME_OPERADOR_CURTO}} passa ideia de conteúdo nova ("quero gravar vídeo sobre X")
- `estrategista-marketing` captura insight de pauta
- `copywriter` durante brainstorm detecta tema secundário que merece peça própria
- `analista-tendencias` detecta tema quente no radar que vira pauta

**Regra §1:** TODA ideia que vira pauta passa pelo {{PLATAFORMA_NEWSLETTER}}. Sem rascunho em MD solto.

## Inputs

| Campo | Tipo | Obrigatório | Default |
|---|---|---|---|
| `titulo` | string | sim | — |
| `formato` | enum | sim | — |
| `angulo` | string (1-2 frases) | sim | — |
| `prioridade` | `urgent`/`high`/`normal`/`low` | sim | `high` |
| `contexto` | markdown longo | recomendado | — |
| `magnetic_hook` | string (só youtube-longo) | opcional | — |
| `cover_text` | string (só youtube-vertical) | opcional | — |

## Formatos válidos + endpoint + campos canônicos

| Valor | Endpoint | Body fields (PATCH top-level) |
|---|---|---|
| `youtube-longo` | `/api/content/youtube` | `idea`, `summary`, `short_summary`, `magnetic_hook`, `script` |
| `youtube-vertical` | `/api/content/vertical` | `script`, `cover_text` (top-level mesmo aparecendo em `vertical_content` no GET) |
| `carrossel` | `/api/content/carrossel` | a descobrir |
| `linkedin` | `/api/content/linkedin` | a descobrir |
| `newsletter` | `/api/content/newsletters` | `body`, `preheader`, `email_subject` |

## Status válidos (enum {{PLATAFORMA_NEWSLETTER}})

`ideia_crua` (default youtube/newsletter) · `proximos` · `escrevendo` · `pronto_para_gravar` (default vertical) · `aprovacao` · `alteracoes` · `configuracao` · `fila_para_publicar` · `publicado` · `enviado` · `geladeira` · `erro`

**Atenção:** vertical default = `pronto_para_gravar` mesmo enviando `proximos` no POST — sistema sobrescreve.

**Matriz canônica de origem → prioridade + status (Regra crítica 16/05/2026):**

| Origem da ideia | Priority | Status default |
|---|---|---|
| **{{NOME_OPERADOR_CURTO}} passou direto pela Jade** ("adiciona na fila", "quero gravar") | `urgent` | `pronto_para_gravar` |
| **`estrategista-marketing` capturou pauta consolidada** | `high` | `proximos` |
| **`copywriter` captou tema secundário em brainstorm** | `high` | `proximos` |
| **`analista-tendencias` capturou raw do radar** | `normal` | `ideia_crua` |
| **Rotina autônoma / bulk import sem triagem** | `low` | `ideia_crua` |

**Razão:** Quando {{NOME_OPERADOR_CURTO}} passa ideia direta pela Jade, é sempre "ideia fresca que quero gravar logo" — vai pro **topo da fila** automaticamente. Status `pronto_para_gravar` é canônico TANTO em `youtube` (validado via PATCH) QUANTO em `vertical` (default do POST). Mover `ideia_crua` ou `proximos` quando {{NOME_OPERADOR_CURTO}} passou direto = falha de processo.

## Setup

Token e base URL em `app/.env.local`:
- `{{PLATAFORMA_NEWSLETTER_API_KEY}}={{CHAVE_API_EXEMPLO}}`
- `CONTENT_API_BASE_URL=https://{{plataforma_newsletter}}.{{DOMINIO}}/api/content`

Carregamento: `set -a; source app/.env.local; set +a`
Header: `Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}`

## Fluxo canônico (REST)

### 1. POST cria card com metadados básicos

```bash
set -a; source app/.env.local; set +a

case "$formato" in
  youtube-longo)     ENDPOINT="${CONTENT_API_BASE_URL}/youtube" ;;
  youtube-vertical)  ENDPOINT="${CONTENT_API_BASE_URL}/vertical" ;;
  carrossel)         ENDPOINT="${CONTENT_API_BASE_URL}/carrossel" ;;
  linkedin)          ENDPOINT="${CONTENT_API_BASE_URL}/linkedin" ;;
  newsletter)        ENDPOINT="${CONTENT_API_BASE_URL}/newsletters" ;;
  *) echo "ERRO: formato inválido: $formato"; exit 1 ;;
esac

PAYLOAD_FILE=$(mktemp)
jq -n \
  --arg title "$titulo" \
  --arg status "${status:-pronto_para_gravar}" \
  --arg origin_type "squad" \
  --arg origin_label "Squad de agentes" \
  --arg priority "$prioridade" \
  '{title: $title, status: $status, origin_type: $origin_type, origin_label: $origin_label, priority: $priority}' > "$PAYLOAD_FILE"

RESP_FILE=$(mktemp)
HTTP=$(curl -s -o "$RESP_FILE" -w "%{http_code}" -X POST \
  -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" \
  -H "Content-Type: application/json" \
  --data-binary "@$PAYLOAD_FILE" \
  "$ENDPOINT")

[ "$HTTP" != "200" ] && [ "$HTTP" != "201" ] && { echo "ERRO POST HTTP $HTTP"; cat "$RESP_FILE"; exit 1; }

ID=$(jq -r '.data.id // .id' < "$RESP_FILE")
echo "Card criado: $ID"
rm -f "$PAYLOAD_FILE" "$RESP_FILE"
```

### 2. PATCH adiciona o conteúdo por formato

**SEMPRE usar `--rawfile` no jq pra evitar dois bugs:**
- `$X` no shell expande pra variável vazia (ex: `R$5.000` → `R.000`)
- Caracteres especiais quebram escape

```bash
ANGULO_FILE=$(mktemp)
cat > "$ANGULO_FILE" <<MD
$angulo

$contexto
MD

case "$formato" in
  youtube-longo)
    PAYLOAD_FILE=$(mktemp)
    jq -n \
      --rawfile idea "$ANGULO_FILE" \
      --arg hook "$magnetic_hook" \
      '{idea: $idea, summary: $idea, magnetic_hook: $hook}' > "$PAYLOAD_FILE"
    ;;
  youtube-vertical)
    PAYLOAD_FILE=$(mktemp)
    jq -n --rawfile script "$ANGULO_FILE" '{script: $script}' > "$PAYLOAD_FILE"
    # cover_text via PATCH top-level retornou 400 em testes — preencher no painel
    ;;
  newsletter)
    PAYLOAD_FILE=$(mktemp)
    jq -n --rawfile body "$ANGULO_FILE" '{body: $body}' > "$PAYLOAD_FILE"
    ;;
esac

HTTP=$(curl -s -o /tmp/patch.json -w "%{http_code}" -X PATCH \
  -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" \
  -H "Content-Type: application/json" \
  --data-binary "@$PAYLOAD_FILE" \
  "${ENDPOINT}/${ID}")

[ "$HTTP" != "200" ] && { echo "ERRO PATCH HTTP $HTTP"; cat /tmp/patch.json; exit 1; }

rm -f "$ANGULO_FILE" "$PAYLOAD_FILE"
```

### 3. Validar via GET pós-PATCH

```bash
curl -s -H "Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}" "${ENDPOINT}/${ID}" \
  | jq '{title: .data.title, status: .data.status, priority: .data.priority}'

echo "URL admin: https://{{plataforma_newsletter}}.{{DOMINIO}}/{{SLUG_OPERADOR}}/conteudos/${ID}"
```

## Output

```markdown
Ideia criada no {{PLATAFORMA_NEWSLETTER}}

- ID: {id}
- URL admin: https://{{plataforma_newsletter}}.{{DOMINIO}}/{{SLUG_OPERADOR}}/conteudos/{id}
- Formato: {formato}
- Status: {status}
- Prioridade: {prioridade}
```

## Critério de aceitação

- POST retornou 201 + ID válido
- PATCH retornou 200 + GET confirma conteúdo persistido (`length > 0` no campo principal)
- `priority` persistiu (não null) — usar enum inglês: `urgent`/`high`/`normal`/`low`
- Card visível em `https://{{plataforma_newsletter}}.{{DOMINIO}}/{{SLUG_OPERADOR}}/conteudos/{id}`

## Pegadinhas conhecidas

1. **`$` no shell** — `R$5.000` vira `R.000` se não usar `--rawfile` ou `printf '%s'` pra escapar
2. **PATCH retorna 200 silencioso** — engole campo desconhecido, SEMPRE validar via GET
3. **Vertical sobrescreve status** — POST com `ideia_crua` salva como `pronto_para_gravar`
4. **`general_idea` no vertical não persiste via PATCH top-level** — usar `script` (vertical_content)
5. **`cover_text` no vertical retorna 400 via PATCH top-level** — preencher manualmente no painel ou descobrir endpoint específico
6. **admin_url retorna null em youtube/vertical** — montar manualmente: `https://{{plataforma_newsletter}}.{{DOMINIO}}/{{SLUG_OPERADOR}}/conteudos/{id}`

## Aprendizado + retrofit (Regra §5)

- Descobriu campo novo de algum formato → atualizar tabela "Formatos válidos" desta skill
- Endpoint retornou erro novo → adicionar à seção "Pegadinhas conhecidas"
- Formato novo (curtas, stories) → adicionar enum + endpoint + campos