# Skill: /disparar-newsletter

Envia newsletter aprovada via {{Plataforma}} → Resend → base. Pipeline canônico consolidado após jornada v6→v20 (12-13/05/2026).

## Input

```
/disparar-newsletter [path-da-newsletter]
```

Exemplo:
- `/disparar-newsletter workspace/output/newsletter/2026-05-11-tema.md`

---

## Pipeline canônico (10 passos OBRIGATÓRIOS — sem skip)

### Passo 1: /escrever-newsletter
Markdown body + frontmatter (title/preheader/email_subject).

**Output:** `workspace/output/newsletter/YYYY-MM-DD-slug.md`

---

### Passo 2: /renderizar-newsletter-html
HTML preview fiel local que ESPELHA o que {{Plataforma}} vai renderizar.

**Output:** `workspace/output/newsletter/{slug}-PREVIEW-FIEL.html`

**Regras:**
- Template idêntico ao do {{Plataforma}} (after bugs corrigidos 12/05)
- Bullets semânticos `<ul><li>`
- Font-family inline em CADA elemento
- Avatar via placeholder CID (real vem no Passo 7)
- Inline CSS (não `<style>` tag)

---

### Passo 3: /revisar-newsletter (copy revisor APROVA)
Revisor de copy valida conteúdo, tom, clareza, Light Copy.

**Critérios:** 31 itens de checklist em `.claude/commands/revisar-newsletter.md`

**Output obrigatório:**
- APROVADO 31/31 → prosseguir
- REPROVADO X/31 → bloqueia até correção

---

### Passo 4: /revisar-newsletter-visual (HTML/design revisor APROVA)
**Regra Inviolável #30:** Newsletter NUNCA vai pra PATCH sem aprovação visual explícita.

**Critérios:** 30+ itens em `.claude/commands/revisar-newsletter-visual.md`
- Logo visível
- Bullets renderizados como `<ul><li>`
- Avatar circular sem distorção
- Hyperlinks azul + underline
- Assinatura canônica 4 linhas
- Compatibilidade email (<100KB, inline CSS, tableado)
- Font-family inline em cada elemento
- Capitalização title/preheader/email_subject

**Output obrigatório:**
- APROVADO 30/30 → prosseguir
- REPROVADO X/30 → **BLOQUEIA PATCH** até correção

**Caso histórico:** Newsletter v5 12/05/2026 disparada com 6 bugs visuais porque PATCH foi feito após revisão de COPY sem revisão VISUAL/HTML/FRONTEND. Regra #30 blinda esse caminho.

---

### Passo 5: Validar curl HTTP 200 em todos assets

ANTES de qualquer PATCH/POST com body que contenha imagem/vídeo referenciado por URL pública, **VALIDAR via curl** que cada URL retorna HTTP 200.

```python
import re, urllib.request, sys

# Ler body_email limpo (cortado no marker INTERNO)
with open(path_newsletter, 'r', encoding='utf-8') as f:
    raw = f.read()
body_email = raw.split('<!-- INTERNO', 1)[0]

# Extrair URLs de imagens
urls = []
urls += re.findall(r'!\[.*?\]\((https?://[^\)]+)\)', body_email)
urls += re.findall(r'<img[^>]+src="(https?://[^"]+)"', body_email)

for url in urls:
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise Exception(f"status {resp.status}")
        print(f"✅ {url}")
    except Exception as e:
        print(f"❌ BLOQUEIO Regra asset-url: {url} indisponível ({e})")
        print("Resolver: deploy do projeto de assets ANTES do PATCH OU remover imagem do body")
        sys.exit(1)
```

**Anti-padrão:** PATCH com URL `sites.{{DOMINIO}}/...` sabendo que `vercel --prod` ainda não rodou.

**Caso histórico:** Newsletter v5 12/05 — foto perfil 404 no preview porque deploy sites-astro pendente.

---

### Passo 6: PATCH no {{Plataforma}}

**Regras obrigatórias:**

#### 6.1. Cortar marker INTERNO antes de enviar

```python
# 1. Ler arquivo completo
with open(path_newsletter, 'r', encoding='utf-8') as f:
    raw = f.read()

# 2. Cortar no marker
body_email = raw.split('<!-- INTERNO', 1)[0].strip()

# 3. Remover frontmatter YAML (split em `---` × 3, pegar parte 3)
parts = body_email.split('---', 2)
if len(parts) >= 3:
    body_clean = parts[2].strip()
else:
    body_clean = body_email

# 4. Validar que notas internas NÃO vazaram
assert 'Notas pro revisor' not in body_clean
assert 'Histórico de revisão' not in body_clean
assert 'Ajustes v' not in body_clean
```

**Anti-padrão:** push do markdown bruto inteiro — vaza notas internas (caso v5 12/05: 60 linhas de metadata vazaram pro painel).

#### 6.2. PATCH com body top-level (NÃO nested)

```python
import requests, os

GIMMICK_API_URL = "https://{{DOMINIO_APP}}.{{DOMINIO}}/api/content/newsletters"
CONTENT_API_KEY = os.environ.get("CONTENT_SQUAD_API_KEY")

headers = {
    "Authorization": f"Bearer {CONTENT_API_KEY}",
    "Content-Type": "application/json"
}

# Extrair frontmatter
import yaml
frontmatter = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}

payload = {
    "title": frontmatter.get("title", "Newsletter Gui Ávila"),
    "body": body_clean,  # Top-level (funciona)
    "newsletter_content": {
        "preheader": frontmatter.get("preheader", ""),
        "email_subject": frontmatter.get("email_subject", frontmatter.get("title", ""))
    }
}

# PATCH (se já existe) ou POST (se nova)
if {{plataforma}}_id:
    r = requests.patch(f"{GIMMICK_API_URL}/{{{plataforma}}_id}", headers=headers, json=payload, timeout=15)
else:
    r = requests.post(GIMMICK_API_URL, headers=headers, json=payload, timeout=15)

if r.status_code not in [200, 201]:
    print(f"❌ {{Plataforma}} retornou {r.status_code}: {r.text[:500]}")
    sys.exit(1)

data = r.json()
newsletter_id = data.get("data", {}).get("id") or data.get("id")
```

**Bug conhecido:** `{ "newsletter_content": { "body": ... } }` (nested) = silently ignored — bug GIMMICK-005. Sempre usar `body` top-level.

#### 6.3. Validar via GET subsequente que body persistiu

```python
# GET pra confirmar que PATCH funcionou
r_get = requests.get(f"{GIMMICK_API_URL}/{newsletter_id}", headers=headers, timeout=10)
if r_get.status_code == 200:
    persisted = r_get.json()
    if len(persisted.get("data", {}).get("body", "")) < 1000:
        print(f"❌ ALERTA: body persistiu com apenas {len(persisted['data']['body'])} chars — esperado ~2500+")
        print("Possível causa: nested body bug. Re-PATCH com body top-level.")
        sys.exit(1)
    print(f"✅ Body persistiu: {len(persisted['data']['body'])} chars")
```

**Não confiar em `ok: true` do PATCH** — validar GET.

---

### Passo 7: Email teste pra {{EMAIL_OPERADOR}} via Resend com attachment CID do avatar

**Regra Inviolável #30:** ANTES de disparar pra base, Gui precisa validar visual no **Gmail real** (não preview do painel).

```python
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")

# Baixar avatar canônico do Drive
# Fonte: Google Drive > Materiais para Time de Marketing > Fotos de rosto quadrada > foto gui barcelona.png (540×540)
avatar_path = "/path/to/foto-gui-barcelona.png"

# Renderizar HTML com CID
html_body = render_newsletter_html(body_clean)  # Template canônico
html_body = html_body.replace('{{AVATAR_URL}}', 'cid:avatar-gui')

# Enviar com attachment
r = resend.Emails.send({
    "from": "contato@empresa.{{DOMINIO}}",
    "to": "{{EMAIL_OPERADOR}}",
    "subject": f"[TESTE] {frontmatter.get('email_subject', 'Newsletter')}",
    "html": html_body,
    "attachments": [{
        "filename": "avatar-gui.png",
        "content": open(avatar_path, 'rb').read(),
        "content_id": "avatar-gui"  # CID attachment
    }]
})

print(f"✅ Email teste enviado pra {{EMAIL_OPERADOR}} — ID: {r.get('id')}")
```

**Por que CID attachment e não data URI inline:**
- Gmail bloqueia data URI (`data:image/png;base64,...`)
- CID attachment (`<img src="cid:avatar-gui">`) renderiza corretamente

**Por que PNG pré-recortado circular:**
- `overflow: hidden` + `border-radius: 50%` não funciona no Gmail (strippa CSS)
- PNG já vem com transparência fora do círculo → renderiza circular em qualquer cliente

---

### Passo 8: Gui valida visual no Gmail real → GO

**Checklist do Gui (visual):**
- [ ] Avatar circular visível (não bloqueado, não distorcido)
- [ ] Bullets renderizados (não vira parágrafo plano)
- [ ] Hyperlinks azul + underline
- [ ] Assinatura completa (4 linhas + foto)
- [ ] Sem buracos entre parágrafos
- [ ] Sem distorções de imagem
- [ ] Capitalização title/preheader/subject correta

**Sem GO explícito do Gui = NÃO disparar pra base.**

---

### Passo 9: Disparo pra base

**Caminho canônico investigado (12/05/2026):**

#### Opção A: Via {{Plataforma}} → {{CRM}} (recomendado)
{{Plataforma}} tem integração com {{CRM}} Email Campaigns. Endpoint de disparo:

```python
# Endpoint ainda em desenvolvimento na sessão {{Plataforma}} paralela
# POST /api/content/newsletters/:id/send
payload_disparo = {
    "segmento": "tag:templates-gratuitos,caixa-ferramentas",
    "filtro_data": "Date Added >= 01/02/2026",  # Últimos 90 dias
    "warmup_stage": 1,  # Limite 1000/dia
    "sender": "contato@empresa.{{DOMINIO}}"
}

r = requests.post(
    f"{GIMMICK_API_URL}/{newsletter_id}/send",
    headers=headers,
    json=payload_disparo,
    timeout=30
)
```

**Status:** Endpoint `/send` pendente implementação (doc em `segundo-cerebro/03-operacao/{{plataforma}}-historico.md`).

#### Opção B: Via Resend direto pra lista CSV (alternativa)
Requer lista de contatos da base exportada do {{CRM}}.

```python
# Exportar contatos {{CRM}}
ghl_contacts = get_ghl_contacts_by_tags(["templates-gratuitos", "caixa-ferramentas"])

# Filtrar últimos 90 dias
import datetime
cutoff = datetime.datetime.now() - datetime.timedelta(days=90)
ghl_contacts_filtered = [c for c in ghl_contacts if parse_date(c['dateAdded']) >= cutoff]

# Disparo em lotes (respeitar warmup Stage 1: 1000/dia)
for batch in chunk_list(ghl_contacts_filtered, 100):  # Lotes de 100
    for contact in batch:
        resend.Emails.send({
            "from": "contato@empresa.{{DOMINIO}}",
            "to": contact['email'],
            "subject": frontmatter.get('email_subject'),
            "html": html_body.replace('{{contact.first_name}}', contact.get('firstName', 'você')),
            "attachments": [{"filename": "avatar-gui.png", "content": avatar_bytes, "content_id": "avatar-gui"}]
        })
    time.sleep(60)  # Pausa entre lotes
```

**Trade-off:**
- {{Plataforma}} → {{CRM}}: centralizado, rastreável no painel, usa warmup automático {{CRM}}
- Resend direto: mais controle, mas sem histórico no {{CRM}}

**Decisão Gui (11/05/2026):** caminho canônico é via {{Plataforma}} → {{CRM}}. Aguardar endpoint `/send`.

**Documentado em:** `segundo-cerebro/03-operacao/disparo-newsletter-base.md` (a criar neste passo).

---

### Passo 10: /sincronizar-clickup pra atualizar status

Após disparo bem-sucedido:

```python
# Atualizar task no ClickUp
# (skill /sincronizar-clickup já existe)
# Marcar status "enviado" + registrar métricas iniciais
```

Atualizar `workspace/memory/newsletter-disparos.md` com entry de histórico:

```markdown
### YYYY-MM-DD — [Título da newsletter]

- Data envio: YYYY-MM-DD HH:MM BRT
- Segmento: tag:X + filtro Date Added >= ...
- Total enviado: N contatos
- Sender: contato@empresa.{{DOMINIO}}
- {{Plataforma}} ID: {id}
- Copy: workspace/output/newsletter/YYYY-MM-DD-slug.md
- Métricas D+1: (aguardar)
- Métricas D+7: (aguardar)
- Aprendizados: (anotar após análise)
```

---

## Regras operacionais

### Secrets
- **SÓ em app/.env.local** (Regra #21)
- Nunca em config versionado
- Carregar via:
  ```bash
  source "/Users/guiavila/Documents/Projetos IA Gui Ávila/Squad Empresa Gui Ávila/app/.env.local"
  ```

### Timeouts (Regra #22: confiabilidade)
- PATCH/POST {{Plataforma}}: 15s
- GET {{Plataforma}}: 10s
- Resend send: 30s
- Validação curl assets: 10s por URL

### Tratamento de erro

#### 401/403 — Credenciais inválidas
```
❌ CONTENT_SQUAD_API_KEY inválida ou expirada.
Próxima ação: validar em app/.env.local + testar curl manual
```

#### 429 — Rate limit
```
⚠️ Rate limit {{Plataforma}} atingido. Aguardando 60s...
```
Retry com backoff exponencial (5s, 15s, 60s).

#### Timeout
```
❌ {{Plataforma}} não respondeu em 15s. Tentar de novo em 5min.
```

#### Body não persistiu após PATCH
```
❌ GET retornou body com apenas X chars (esperado ~2500+).
Possível causa: nested body bug GIMMICK-005.
Correção: re-PATCH com body top-level (não nested em newsletter_content).
```

---

## Validação pré-disparo — maiúsculas (obrigatório)

**Após PATCH, antes de agendar/disparar:**

1. GET no {{Plataforma}} pra conferir `data.newsletter_content.preheader`, `data.newsletter_content.email_subject`, `data.title`
2. Validar regex `^[A-ZÁÉÍÓÚÂÊÔÃÕÇ]` na primeira letra de cada um
3. Se algum minúsculo: **PATCH corretivo automático** capitalizando primeira letra:
   ```json
   {
     "title": "Título Corrigido",
     "newsletter_content": {
       "preheader": "Preheader corrigido",
       "email_subject": "Assunto corrigido"
     }
   }
   ```
4. Re-validar com GET
5. Só então agendar/disparar

---

## Warmup e segmentação

**Plano gradual `empresa.{{DOMINIO}}` (Stage 1):**

| Semana | Volume | Critério |
|---|---|---|
| 1 | ~100 | Top engajados últimos 30d |
| 2 | ~250 | Engajados últimos 60d |
| 3 | ~500 | Engajados últimos 90d |
| 4 | ~1000 | Engajados últimos 180d |
| 5+ | escalar | Conforme Stage avança |

**Segmento recomendado semana 1:**
```
TAGS: ("pegou a caixa de ferramentas"
       OR "add automacao caixa de ferramentas"
       OR "recebeu templates gratuitos")
AND Date Added >= [30 dias atrás]
```

**Fonte:** `workspace/memory/newsletter-disparos.md` + `segundo-cerebro/03-operacao/email-marketing-historico.md`

---

## Aprendizados consolidados jornada v6→v20 (12-13/05/2026)

### 8 bugs estruturais {{Plataforma}} (corrigidos commits 6ef59c9 + 2f9c581)
1. ~~Sanitizer remove `<ul>/<li>`~~ → corrigido (BLOCK_HTML_PATTERN)
2. ~~Markdown parser converte `<ul>` em `-`~~ → corrigido
3. ~~Template wrappa em `<p>` adicional~~ → corrigido
4. ~~CSS template usa `!important`~~ → mitigado
5. ~~Parser converte `\n` em `<br>` mesmo entre tags~~ → corrigido (splitMixedBlock)
6. ~~Painel admin ≠ email real~~ → corrigido (iframe srcDoc)
7. ~~`<table>` aninhada em `<p>`~~ → corrigido
8. ~~Avatar `<img>` distorcido~~ → mitigado por wrapper

### Aprendizados visuais
- Fontes inline em CADA elemento
- Avatar PNG pré-recortado + CID attachment Resend
- Capitalização title/preheader/email_subject obrigatória
- Assinatura canônica 4 linhas literais
- Bullets semânticos `<ul><li>`
- Hyperlinks azul + underline inline

### Aprendizados estruturais
- Regra #30: revisão visual obrigatória antes PATCH
- Regra #33: Jade não aprova, só revisor independente
- Regra #35: comentário antes mudar status ClickUp
- Hook bloqueante: check-newsletter-revisao-visual.sh

### Pipeline canônico
10 passos obrigatórios. Pular qualquer passo = risco de bug em produção.

---

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24
2. Revisor APROVA ou REPROVA + findings
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro Gui testar — testa antes.

---

## Cross-reference

- `/escrever-newsletter` — produz markdown source
- `/renderizar-newsletter-html` — gera HTML preview fiel
- `/revisar-newsletter` — revisa copy
- `/revisar-newsletter-visual` — revisa HTML/design (BLOQUEIA PATCH se reprovado)
- `workspace/memory/newsletter-disparos.md` — histórico + cadência + métricas
- `segundo-cerebro/03-operacao/email-marketing-historico.md` — warmup + compliance
- `segundo-cerebro/03-operacao/{{plataforma}}-historico.md` — API endpoints
- `segundo-cerebro/03-operacao/disparo-newsletter-base.md` — caminho canônico de disparo (a criar)
- Memória: `feedback_newsletter_skill_consolidada_v20.md`
- AGENTS.md Regra #30 (revisão visual obrigatória)

