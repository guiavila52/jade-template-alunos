# Integração GoHighLevel (GHL)

## Credenciais (app/.env.local)

| Variável | Descrição |
|---|---|
| `GHL_API_KEY` | PIT token da location Gui Ávila (renovar se der 401 em tudo) |
| `GHL_LOCATION_ID` | `CsiBUbUirVZnXWpyDivf` |
| `GHL_{{LMS}}_API_KEY` | PIT token da location {{LMS}} |
| `GHL_{{LMS}}_LOCATION_ID` | — |

**userId Gui Ávila na location:** `NOOTHv2vbo1S52MK00Dm`

## Token PIT — quando renovar

Tokens PIT do GHL são invalidados quando você edita os escopos. Sintoma: 401 em TUDO (inclusive contatos).
Fix: Settings → Private Integrations → editar integração → copiar token novo → atualizar `GHL_API_KEY` no `.env.local`.

**Integração ativa:** "Squad Jade e App {{PLATAFORMA_CONTEUDO}}" — 145/148 escopos habilitados.

## Email Campaigns API

**Endpoint criar campanha:**
```
POST https://services.leadconnectorhq.com/emails/public/v2/locations/{locationId}/campaigns/email-campaign
```

**Headers obrigatórios:**
```
Authorization: Bearer {GHL_API_KEY}
Content-Type: application/json
Version: 2023-02-21
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
```

**Payload mínimo funcional (descoberto 21/05/2026):**
```json
{
  "name": "Título da campanha",
  "subject": "Assunto do email",
  "fromName": "Gui Ávila",
  "fromAddress": "{{EMAIL_OPERADOR}}",
  "editorType": "html",
  "editorContent": "<HTML completo>",
  "timeZone": "America/Sao_Paulo",
  "userId": "NOOTHv2vbo1S52MK00Dm"
}
```

**Notas:**
- Campo é `name` (não `title`) e `editorContent` (não `htmlBody`)
- `editorType: "html"` = HTML livre, sem builder visual
- Campanha criada sempre como `draft` — Gui define destinatários e dispara no painel
- Cloudflare bloqueia User-Agent padrão do Python (`urllib`) — obrigatório User-Agent de browser

## Script canônico

```bash
python3 scripts/newsletter/publicar-ghl.py \
  --html workspace/output/newsletter/YYYY-MM-DD-slug-preview.html \
  --md   workspace/output/newsletter/YYYY-MM-DD-slug.md
```

Retorna URL direta da campanha no painel GHL.

## Outros endpoints úteis

| Endpoint | Descrição |
|---|---|
| `GET /contacts/?locationId=...` | Listar contatos |
| `GET /users/?locationId=...` | Listar usuários da location |
| `GET /emails/public/v2/locations/{id}/campaigns/emails` | Listar campanhas |

## Histórico

- **21/05/2026** — Primeira integração newsletter → GHL via API. Descoberta do payload correto por tentativa/erro (422 → 200). Token invalidado ao editar escopos, renovado durante sessão.
