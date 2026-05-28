---
name: renderizar-newsletter-html
description: Renderiza newsletter em HTML fragment deterministico a partir de config JSON seguindo template canonico v5.
type: skill
---

# Skill: Renderizar Newsletter HTML

**Papel:** Desenvolvedor de newsletters
**Output:** HTML fragment determinístico (body {{PLATAFORMA_EMAIL}})
**Squad:** conteudo
**Maturidade:** 🟢 MADURA — template canônico v5 codificado + regression test passa ({{DATA_EVENTO}})


## Fluxo

```
Input (config JSON: saudação, corpo_secoes[], assinatura_padrao)
  ↓
1. Parser: converter markdown inline ([texto](url), **bold**) → HTML inline canônico
2. Montar corpo: iterar corpo_secoes[] → gerar <p>, <h2>, <ul><li>, video_embed, CTA
3. Injetar assinatura canônica (foto circular + 4 linhas literais)
4. Aplicar estilos inline em CADA elemento (font-family, colors, spacing)
5. Regression test (diff vs v5 baseline) — exit 1 se regressão
6. Salvar HTML fragment em workspace/output/newsletter/YYYY-MM-DD-slug.html
  ↓
Output (HTML fragment determinístico pronto pra PATCH {{PLATAFORMA_EMAIL}})
```

## Propósito

Renderiza newsletter em HTML fragment a partir de config JSON, seguindo **template canônico v5** (newsletter `62bec9ff-1abd-4190-be01-f79f64a5b9fc`, aprovada por {{NOME_OPERADOR_CURTO}} em 13/05/2026).

Produção é **100% determinística** — assinatura/header/footer fixos, corpo via placeholders. Diff zero contra v5 baseline garantido por regression test.

## Source of truth

| Artefato | Path |
|---|---|
| HTML baseline (v5 aprovada) | `workspace/output/newsletter/2026-05-13-cadc4df0-v5.html` |
| Template canônico (anatomia + zonas) | `scripts/newsletter/template-canonico-v5.html` |
| Script render determinístico | `scripts/newsletter/renderizar-html.py` |
| Config exemplo v5 (regression fixture) | `workspace/output/newsletter/cadc4df0-config.json` |
| **Regression test (rodar antes de qualquer alteração)** | `scripts/newsletter/regression-test-v5.py` |
| Memória canônica | `project_newsletter_template_canonico_v5.md` |

## Quando usar

- Após copywriter entregar markdown aprovado (ou config JSON pronta)
- Para regerar newsletter com correções no corpo
- Antes de PATCH na {{PLATAFORMA_EMAIL}} (body)

## Comando canônico

**REGRA INVIOLÁVEL: sempre gerar 2 arquivos. Sempre abrir `-edit.html` pro {{NOME_OPERADOR_CURTO}}. Nunca apresentar markdown.**

```bash
# 1. Preview para Playwright/QA (input do /revisar-newsletter-visual)
python3 scripts/newsletter/renderizar-html.py \
  --input config.json \
  --output workspace/output/newsletter/YYYY-MM-DD-slug-preview.html

# 2. Editable para {{NOME_OPERADOR_CURTO}} validar (layout 600px centrado + copy button + editável)
python3 scripts/newsletter/renderizar-html.py \
  --input config.json \
  --output workspace/output/newsletter/YYYY-MM-DD-slug-edit.html \
  --editable

# Abrir para {{NOME_OPERADOR_CURTO}} (OBRIGATÓRIO antes de apresentar qualquer resultado)
open workspace/output/newsletter/YYYY-MM-DD-slug-edit.html
```

## Regression test (OBRIGATÓRIO antes de qualquer mudança no script ou template)

```bash
python3 scripts/newsletter/regression-test-v5.py
```

Exit 0 = template íntegro. Exit 1 = REGRESSÃO (diff vs v5 baseline) — investigar antes de prosseguir. Sem PASS verde, NUNCA mexer no script de render.

## Formato de config JSON

```json
{
  "saudacao": "Oi {{contact.first_name}}!",
  "corpo_secoes": [
    {"tipo": "paragrafo", "texto": "Texto com <a href=\"URL\" style=\"color:#2563eb; text-decoration:underline; font-size:inherit;\">link</a>."},
    {"tipo": "heading2", "texto": "Título da seção"},
    {"tipo": "bullets", "items": [
      "<strong style=\"font-weight:700; color:#1a1a1a;\">Negrito:</strong> texto",
      "Outro bullet"
    ]},
    {"tipo": "video_embed", "youtube_id": "cVm18LNG3mE", "gancho": "Gravei um vídeo curto."},
    {"tipo": "cta_botao_link", "texto": "Cria sua conta aqui", "url": "https://{{DOMINIO}}/clickup"}
  ],
  "assinatura_padrao": true
}
```

## Componentes (tipos suportados)

### 1. Parágrafo
`{"tipo": "paragrafo", "texto": "..."}` — aceita `<a>` e `<strong>` inline com estilos canônicos.

### 2. Heading 2
`{"tipo": "heading2", "texto": "..."}` — 22px / 700 / margin top 32px.

### 3. Bullets
`{"tipo": "bullets", "items": ["...", "..."]}` — `<ul>` + `<li>` com estilos canônicos.

### 4. Vídeo YouTube (Design A)
`{"tipo": "video_embed", "youtube_id": "...", "gancho": "..."}`
- Gancho (parágrafo)
- Capa `maxresdefault.jpg` clicável (600px, border-radius 12px)
- Botão CTA vermelho `#dc2626` "▶ Assistir no YouTube"

### 5. CTA inline
`{"tipo": "cta_botao_link", "texto": "...", "url": "..."}` — link azul `#2563eb` inline.

## Assinatura canônica — IMUTÁVEL

**NUNCA editar.** Mudança aqui = ciclo completo (aprovação {{NOME_OPERADOR_CURTO}} + nova versão template v6 + atualizar baseline + atualizar regression test).

Estrutura (literal):
- Foto perfil 96×96 circular → `https://sites.{{DOMINIO}}/assets-gui/foto-gui-barcelona-circular.png`
  - `border-radius:50%` + `object-fit:cover` + `object-position:center 25%`
- 4 linhas (literal — capitalização exata):
  1. **{{NOME_OPERADOR}}**
  2. Fundador e CEO da [{{PLATAFORMA_CURSOS}}](https://{{DOMINIO}}/{{plataforma_cursos}})
  3. Autor do {{PRODUTO_PRINCIPAL}}, Automações PRO e ClickUp 8x
  4. Fundador do {{PRODUTO_PARCERIA}} · [{{DOMINIO}}](https://{{DOMINIO}})
- `<hr>` separador acima do bloco

**Foto — técnica:** URL pública (sites.{{DOMINIO}} Astro deploy). Validada live {{DATA_EVENTO}} (HTTP 200). v5 aprovada visual Gmail. Para envio via Resend direto (sem {{PLATAFORMA_EMAIL}}): usar CID via `/enviar-email` (memória `feedback_email_avatar_via_cid_attachment.md`).

## Estilos canônicos (inline — extraídos de v5)

| Elemento | Estilo |
|---|---|
| Font-family | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` |
| Link | `color:#2563eb; text-decoration:underline; font-size:inherit;` |
| Parágrafo | `margin:0 0 16px; line-height:1.6; font-size:16px; color:#1a1a1a;` |
| H2 | `font-size:22px; line-height:1.3; font-weight:700; margin:32px 0 16px;` |
| `<ul>` | `margin:0 0 16px; padding-left:24px; font-size:16px;` |
| `<li>` | `margin-bottom:8px; line-height:1.6; font-size:16px; color:#1a1a1a;` |
| `<strong>` | `font-weight:700; color:#1a1a1a;` |
| `<hr>` (assinatura) | `border:none; border-top:1px solid #e5e5e5; margin:32px 0;` |

## Output

**Dois arquivos por newsletter (OBRIGATÓRIO):**

| Arquivo | Flag | Quem usa |
|---|---|---|
| `YYYY-MM-DD-slug-preview.html` | sem flag | Playwright / `/revisar-newsletter-visual` |
| `YYYY-MM-DD-slug-edit.html` | `--editable` | Aprovação do {{NOME_OPERADOR_CURTO}} (600px centrado + botão copiar + editável) |

Ambos são **HTML fragment** — sem `<!DOCTYPE>`, sem `<html>`, sem `<body>`. Começa em `<p>` ou `<h2>`. {{PLATAFORMA_EMAIL}} wrappa.

**Abrir para {{NOME_OPERADOR_CURTO}}:** sempre `-edit.html --editable`. Nunca `-preview.html` bruto. Nunca markdown.

## Checklist de qualidade

- [ ] Regression test passa (`regression-test-v5.py` exit 0)
- [ ] Font-family inline em CADA elemento
- [ ] Links `#2563eb` + underline + `font-size:inherit`
- [ ] Espaçamento: 16px entre `<p>`, 32px antes de `<h2>`
- [ ] Assinatura literal (4 linhas exatas, foto URL canônica)
- [ ] Vídeo YouTube Design A (capa + botão vermelho)
- [ ] Fragment puro (sem DOCTYPE/html/body wrapper)
- [ ] `-preview.html` gerado em `workspace/output/newsletter/YYYY-MM-DD-{slug}-preview.html`
- [ ] `-edit.html --editable` gerado em `workspace/output/newsletter/YYYY-MM-DD-{slug}-edit.html`
- [ ] `open workspace/output/newsletter/YYYY-MM-DD-{slug}-edit.html` executado ({{NOME_OPERADOR_CURTO}} valida no browser, nunca vê markdown)

## Próximo passo após render

1. `/revisar-newsletter-visual` (screenshot Playwright real + checklist visual)
2. Após aprovação visual: PATCH na {{PLATAFORMA_EMAIL}} (body) via API REST
3. Disparo apenas via `/disparar-newsletter`

## Regras invioláveis cruzadas

- **Acentuação:** UTF-8 obrigatório em texto pt-BR (memória `feedback_acentuacao_obrigatoria.md`)
- **Title/preheader no frontmatter, NUNCA no body** (memória `feedback_newsletter_title_preheader_no_frontmatter.md`)
- **Marker `<!-- INTERNO — NÃO ENVIAR -->`** separa body do email de notas internas no markdown (memória `feedback_newsletter_separar_body_de_metadata.md`)
- **Revisão visual obrigatória antes de disparar** (AGENTS.md Regra #30 + #38)
- **Produção via skill canônica obrigatória** (AGENTS.md Regra #37 — hook bloqueante runtime)

## Memórias relacionadas

- `project_newsletter_template_canonico_v5.md` — fonte de verdade v5
- `feedback_newsletter_template_padrao_assinatura.md` — padrão imperativo
- `feedback_email_avatar_via_cid_attachment.md` — quando usar CID (Resend direto)
- `feedback_newsletter_revisao_visual_obrigatoria.md`
- `feedback_newsletter_video_embed_e_revisao_visual_real.md`


## Integração com {{PLATAFORMA_EMAIL}} (POST / PATCH)

Após renderizar o HTML, publicar/atualizar na {{PLATAFORMA_EMAIL}} via REST.

**Endpoints:**
- POST `https://{{plataforma_newsletter}}.{{DOMINIO}}/api/content/newsletters` — criar
- PATCH `https://{{plataforma_newsletter}}.{{DOMINIO}}/api/content/newsletters/{id}` — atualizar

**Auth:** `Authorization: Bearer ${{PLATAFORMA_NEWSLETTER_API_KEY}}` (em `app/.env.local`)

**Status válidos (descoberto {{DATA_EVENTO}}):**
- `ideia_crua`
- `proximos`
- `escrevendo`
- `aprovacao` ← padrão pra newsletter pronta esperando OK do {{NOME_OPERADOR_CURTO}}
- `fila_para_publicar`

⚠️ **`draft` NÃO é válido.** Rejeitado com HTTP 400.

**Payload mínimo:**
```json
{
  "title": "...",
  "preheader": "...",
  "slug": "...",
  "body": "<HTML completo do renderer>",
  "status": "aprovacao"
}
```

**Body do payload é HTML completo, não markdown.** O {{PLATAFORMA_NEWSLETTER}} guarda e exibe direto.

## Pipeline canônico ponta-a-ponta

1. Input do {{NOME_OPERADOR_CURTO}} (link YouTube, tema solto, briefing)
2. `/transcrever-video` se for YouTube
3. Despachar copywriter → MD em `workspace/output/newsletter/YYYY-MM-DD-slug.md`
4. Despachar revisor-newsletter (independente) → APROVADO
5. **Converter MD → config JSON** estruturado (etapa obrigatória — script só aceita JSON, não MD)
   - Saudação → `saudacao`
   - Parágrafos → `corpo_secoes[].tipo = "paragrafo"` (com `<a>` e `<strong>` inline OU markdown inline — renderer agora converte ambos)
   - Subheadings `##` → `corpo_secoes[].tipo = "heading2"`
   - Bullets `- ...` → `corpo_secoes[].tipo = "bullets"` com `items[]`
   - Bloco `::video-embed::` (no fechamento canônico v3) → `corpo_secoes[].tipo = "video_embed"` com `youtube_id` e `gancho`
   - `assinatura_padrao: true` SEMPRE (renderer monta a assinatura — NÃO incluir no JSON)
6. Salvar config em `/tmp/newsletter-YYYY-MM-DD-config.json`
7. Renderizar — **2 arquivos obrigatórios**:
   ```bash
   python3 scripts/newsletter/renderizar-html.py \
     --input /tmp/newsletter-YYYY-MM-DD-config.json \
     --output workspace/output/newsletter/YYYY-MM-DD-slug-preview.html
   python3 scripts/newsletter/renderizar-html.py \
     --input /tmp/newsletter-YYYY-MM-DD-config.json \
     --output workspace/output/newsletter/YYYY-MM-DD-slug-edit.html \
     --editable
   open workspace/output/newsletter/YYYY-MM-DD-slug-edit.html
   ```
8. POST {{PLATAFORMA_NEWSLETTER}} (primeira vez) com status `aprovacao` → guardar ID retornado
9. Apresentar URL `https://{{plataforma_newsletter}}.{{DOMINIO}}/{{HANDLE_OPERADOR}}/conteudos/{id}` pro {{NOME_OPERADOR_CURTO}}
10. Se {{NOME_OPERADOR_CURTO}} pedir ajuste → editar config JSON → re-renderizar → PATCH no MESMO ID (não criar novo)

## Parser inline do renderer (correção {{DATA_EVENTO}})

O script `scripts/newsletter/renderizar-html.py` agora converte automaticamente em todos os textos:
- `[texto](url)` → `<a href="url" style="color:#2563eb; text-decoration:underline; font-size:inherit;">texto</a>`
- `**texto**` → `<strong style="font-weight:700; color:#1a1a1a;">texto</strong>`
- `*texto*` → `<em>texto</em>`
- `{{contact.first_name}}` preservado intacto

Antes da correção, links saiam como texto bruto no email (bug detectado por {{NOME_OPERADOR_CURTO}} em {{DATA_EVENTO}} — newsletter Claude Code).

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{NOME_OPERADOR_CURTO}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente