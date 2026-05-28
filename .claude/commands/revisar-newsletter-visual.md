---
name: revisar-newsletter-visual
description: Revisa HTML renderizado da newsletter (layout, contraste, espacamento, fontes) antes de PATCH no {{PLATAFORMA_NEWSLETTER}} e disparo.
type: skill
---

# /revisar-newsletter-visual — Revisor de HTML/design renderizado


## Fluxo

```
Input (HTML preview FIEL renderizado)
  ↓
1. Playwright headless: renderizar HTML em Chromium (desktop 600px + mobile 375px)
2. Screenshots full-page + blocos específicos
3. Validação visual humana (30+ critérios: layout, tipografia, espaçamento, imagens, assinatura, bullets, links, compatibilidade)
4. Validar URLs de assets (curl -I → HTTP 200)
5. Comparar com markdown source (enumeráveis viraram bullets?)
6. Gerar relatório: APROVADO (30/30 ✅) ou REPROVADO (lista bugs + root cause + correção)
  ↓
Output (REVISAO-APROVADO → libera PATCH {{PLATAFORMA_NEWSLETTER}} | REVISAO-REPROVADO → volta pro renderer)
```

## Propósito
Revisor especialista em HTML de email, frontend e design visual. Garante que o HTML renderizado da newsletter está perfeito ANTES de PATCH no {{PLATAFORMA_NEWSLETTER}}.

**Regra Inviolável #30 (12/05/2026):** Newsletter NUNCA vai pra PATCH sem aprovação visual explícita. Caso histórico: v5 disparada com 6 bugs visuais porque revisão de copy ≠ revisão visual/HTML/frontend.

## Quando rodar
Após `/renderizar-newsletter-html`, ANTES de `/disparar-newsletter`. Bloqueia PATCH no {{PLATAFORMA_NEWSLETTER}} até aprovação explícita.

## Pré-requisitos
- HTML preview em `workspace/output/newsletter/{slug}-preview.html` (gerado por `/renderizar-newsletter-html` **sem** `--editable` — NÃO usar o `-edit.html`)
- Comparação lado a lado com markdown source
- Acesso visual ao HTML renderizado (abrir em navegador)

---

## Checklist obrigatório (30+ critérios — todos APROVADO ou REPROVA)

### Layout e estrutura
- [ ] Logo no topo VISÍVEL em fundo claro (contraste > 4.5:1 WCAG)
- [ ] Sem espaço gigante (>200px) acima do conteúdo
- [ ] Espaçamento entre parágrafos consistente (16-24px, não saltos de 60px)
- [ ] Max-width 600px (padrão email-safe)
- [ ] Email tableado (não Flexbox/Grid — Outlook não renderiza)

### Tipografia e texto
- [ ] Bullets renderizam como `<ul><li>` com marker visível (não vira parágrafo plano)
- [ ] Tipografia legível mobile (font-size ≥16px body, line-height ≥1.5)
- [ ] Cores texto AAA contraste (corpo #1a1a1a em #ffffff = passa WCAG)
- [ ] Caracteres Unicode/acentuação corretos (UTF-8)
- [ ] Sem placeholders ou `{{...}}` remanescentes (exceto `{{contact.first_name}}` intencional)
- [ ] **Font-family inline em CADA elemento** (Gmail não respeita herança CSS):
  ```css
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  ```
- [ ] Parágrafos curtos (2-3 frases) com respiração (linha em branco entre)
- [ ] Sub-headings `<h2>` visíveis, pelo menos 2 por newsletter
- [ ] Hierarquia tipográfica clara (h2 > p > li)

### Capitalização (Regra Inviolável)
- [ ] **Title** começa com MAIÚSCULA (validar via GET {{PLATAFORMA_NEWSLETTER}} após PATCH)
- [ ] **Preheader** começa com MAIÚSCULA (validar via GET)
- [ ] **Email_subject** começa com MAIÚSCULA (validar via GET)
- [ ] Regex obrigatório: `^[A-ZÁÉÍÓÚÂÊÔÃÕÇ]`
- [ ] **Assinatura canônica 4 linhas** com capitalização correta:
  ```
  {{NOME_OPERADOR}} — fundador e CEO da {{PLATAFORMA_CURSOS}}
  Autor do {{PRODUTO_PRINCIPAL}}, Automações PRO e ClickUp 8x
  Fundador do {{PRODUTO_PARCERIA}}
  Site: {{DOMINIO}}
  ```

### Imagens e assets
- [ ] Imagens com aspect-ratio preservado (object-fit: cover, dimensão FIXA px)
- [ ] **Avatar circular:**
  - PNG pré-recortado em círculo (transparência fora)
  - Fonte canônica: Google Drive > Materiais para Time de Marketing > Fotos de rosto quadrada > `foto gui barcelona.png` (540×540)
  - Servido via **Resend attachment CID** (`<img src="cid:avatar-gui">`)
  - NUNCA data URI inline (Gmail bloqueia)
  - 80×80px renderizado, sem distorção
  - `border-radius: 50%`, `width=height` fixo
- [ ] Todas imagens com `alt` explícito (acessibilidade + clientes que bloqueiam imagens)
- [ ] **Todas URLs de assets HTTP 200** (validar via `curl -I` antes de PATCH):
  ```bash
  for url in $(grep -oP '(src|href)="https?://[^"]+' preview.html | cut -d'"' -f2); do
    curl -I "$url" 2>&1 | grep -q "200" || echo "BLOQUEIO: $url indisponível"
  done
  ```

### Assinatura canônica
- [ ] Assinatura completa (foto 80px circular esquerda + 4 linhas direita)
- [ ] Foto perfil visível e circular (não quadrada, não distorcida)
- [ ] Texto LITERAL (sem variação):
  ```
  {{NOME_OPERADOR}} — fundador e CEO da {{PLATAFORMA_CURSOS}}
  Autor do {{PRODUTO_PRINCIPAL}}, Automações PRO e ClickUp 8x
  Fundador do {{PRODUTO_PARCERIA}}
  Site: {{DOMINIO}}
  ```
- [ ] Hyperlink ativo em `{{DOMINIO}}`
- [ ] Separador `---` (visual divider) ANTES da assinatura
- [ ] Mobile: foto centralizada em cima, texto abaixo (responsivo)

### Links e interatividade
- [ ] Hyperlinks com cor azul (`#2563eb` ou similar) + `text-decoration: underline` inline
- [ ] Hyperlink ativo em palavras-chave ({{PLATAFORMA_CURSOS}}, {{DOMINIO}}, produtos)
- [ ] Todos links testados (curl -I retorna 200/301/302)
- [ ] Sem links quebrados (`href="#"` ou `href="javascript:void(0)"`)

### Compatibilidade email
- [ ] **Inline CSS** (não `<style>` tag — Gmail strip out)
- [ ] Render testado em modo escuro (Gmail dark mode pode inverter cores)
- [ ] Tamanho HTML <100KB (Gmail clipa em 102KB)
- [ ] **Preheader não duplica title** (complementa, não repete)
- [ ] Preheader desperta curiosidade (não factual seco)
- [ ] Sem `overflow: hidden` em avatares (Gmail strippa — usar PNG pré-recortado)
- [ ] Sem Flexbox/Grid (Outlook não renderiza — usar `<table>` tableado)

### Enumeráveis → bullets (Regra 12/05)
- [ ] Conceitos enumeráveis (Camada 1/2, Etapa A/B/C, Pilar X/Y, Fase 1/2/3) renderizam como `<ul><li>`
- [ ] NUNCA parágrafo plano fingindo bullet
- [ ] Marker visível (•) em cada item

### Marker INTERNO (Regra Inviolável)
- [ ] Marker `<!-- INTERNO — NÃO ENVIAR — apenas histórico/revisão -->` presente EXATAMENTE após assinatura
- [ ] Notas internas (revisões, histórico, ajustes) ABAIXO do marker
- [ ] Body limpo (NÃO vaza notas pro email final)

---

## Output obrigatório

### Se APROVADO:
```
APROVADO — Newsletter visual pronta para PATCH

Checklist completo: 30/30 ✅

Destaques:
- Logo: ✅ visível, contraste OK
- Espaçamento: ✅ consistente
- Bullets: ✅ renderizam como <ul><li> semânticos
- Imagens: ✅ aspect-ratio preservado
- Avatar: ✅ circular PNG pré-recortado, CID attachment, sem distorção
- Hyperlinks: ✅ azul #2563eb + underline inline
- Assinatura: ✅ canônica completa (4 linhas literais + foto circular)
- Capitalização: ✅ title/preheader/email_subject maiúsculas
- Compatibilidade: ✅ tableado, inline CSS, <100KB
- Font-family: ✅ inline em cada elemento
- Assets: ✅ todas URLs HTTP 200 validadas
- Enumeráveis: ✅ bullets em conceitos listados
- Marker INTERNO: ✅ presente e correto

Liberado para PATCH no {{PLATAFORMA_NEWSLETTER}}.
```

### Se REPROVADO:
```
REPROVADO — BLOQUEIA PATCH no {{PLATAFORMA_NEWSLETTER}}

Bugs encontrados (N/30):
1. [Bug] — [root cause] — [linha do markdown que origina] — [correção necessária]
2. [Bug] — [root cause] — [linha do markdown que origina] — [correção necessária]
...

Próximos passos:
1. Corrigir markdown source OU template HTML
2. Re-rodar /renderizar-newsletter-html
3. Re-submeter para /revisar-newsletter-visual
4. Só APROVAR quando 30/30 ✅
```

---

## Validação pré-disparo (após PATCH, antes de agendar)

**Após PATCH no {{PLATAFORMA_NEWSLETTER}}, antes de disparar:**
1. GET no {{PLATAFORMA_NEWSLETTER}} pra conferir `data.newsletter_content.preheader`, `data.newsletter_content.email_subject`, `data.title`
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

## Email teste obrigatório (Regra Inviolável #30)

ANTES de disparar pra base:
1. Enviar email teste pra `{{EMAIL_OPERADOR}}` via Resend
2. Usar attachment CID pro avatar (`<img src="cid:avatar-gui">`)
3. {{NOME_OPERADOR_CURTO}} abre no **Gmail real** (não preview do painel)
4. Valida:
   - Avatar circular visível (não bloqueado)
   - Bullets renderizados
   - Hyperlinks azul + underline
   - Assinatura completa
   - Sem buracos/distorções
5. {{NOME_OPERADOR_CURTO}} dá **GO explícito** pra disparar pra base

**Sem GO do {{NOME_OPERADOR_CURTO}} no Gmail real = NÃO disparar.**

---

## Cross-reference

- `/escrever-newsletter` — produz markdown source
- `/revisar-newsletter` — revisa copy/conteúdo
- `/renderizar-newsletter-html` — gera preview HTML fiel
- `/disparar-newsletter` — PATCH no {{PLATAFORMA_NEWSLETTER}} (bloqueado sem aprovação visual)
- Memória: `feedback_newsletter_template_padrao_assinatura.md`
- Memória: `feedback_newsletter_skill_consolidada_v20.md`
- AGENTS.md Regra Inviolável #30 (revisão visual obrigatória)

---

## Caso histórico

Newsletter v5 12/05/2026 disparada com **6 bugs visuais**:
1. Logo invisível (contraste baixo)
2. Buracos entre parágrafos (60px+)
3. Bullets viraram parágrafos planos
4. Imagem avatar distorcida (não circular)
5. Hyperlinks sem cor azul nem underline
6. Assinatura incompleta

**Root cause:** PATCH no {{PLATAFORMA_NEWSLETTER}} foi feito após revisão de COPY sem revisão VISUAL/HTML/FRONTEND.

**Solução:** Regra Inviolável #30 + esta skill blindam esse caminho. Nenhuma newsletter vai pra PATCH sem aprovação visual explícita de revisor frontend independente.

---

## Aprendizados consolidados jornada v6→v20 (12-13/05/2026)

### Bugs {{PLATAFORMA_NEWSLETTER}} corrigidos (commits 6ef59c9 + 2f9c581)
- Sanitizer removia `<ul>/<li>` → corrigido
- Parser convertia `<ul>` em `-` → corrigido
- Template wrappava em `<p>` adicional → corrigido
- CSS template usava `!important` → mitigado
- Parser convertia `
` em `<br>` entre tags → corrigido (splitMixedBlock)
- Painel admin ≠ email real → corrigido (iframe srcDoc)
- `<table>` aninhada em `<p>` → corrigido
- Avatar `<img>` distorcido → mitigado por wrapper

### Aprendizados visuais aplicados
- Fontes inline em CADA elemento
- Avatar PNG pré-recortado + CID attachment (não data URI)
- Capitalização title/preheader/email_subject obrigatória
- Assinatura canônica 4 linhas literais
- Bullets semânticos `<ul><li>` ({{PLATAFORMA_NEWSLETTER}} agora respeita)
- Hyperlinks azul + underline inline
- Compatibilidade: tableado, inline CSS, <100KB

### Regras estruturais
- Regra #30: revisão visual obrigatória antes PATCH
- Regra #33: Jade não aprova, só revisor independente
- Regra #35: comentário antes de mudar status ClickUp
- Hook bloqueante: check-newsletter-revisao-visual.sh


---

## Revisão visual REAL com Playwright screenshot (OBRIGATÓRIO)

**Regra Inviolável adicionada 13/05/2026:** Auto-checklist do agent NÃO substitui revisão visual REAL.

### Caso histórico que motivou esta seção

Newsletter `cadc4df0-21e2-4b0b-84d8-adb517ab1275` (13/05/2026) chegou pro {{NOME_OPERADOR_CURTO}} com 4 problemas:
1. Buraco branco excessivo no topo
2. Buraco branco excessivo no fim
3. Sem bloco vídeo embed (newsletter era de transcrição YouTube)
4. **Auto-checklist do subagent passou sem detectar NADA**

Root cause: revisor era TEÓRICO (lia HTML como texto), não VISUAL (renderizava pra ver). Checklist mental = falsa segurança.

---

## Protocolo obrigatório ANTES de aprovar HTML

### 1. Renderizar HTML no headless Chromium (Playwright)

```javascript
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const htmlContent = fs.readFileSync('workspace/output/newsletter/{slug}-preview.html', 'utf-8');
  
  // Desktop 600px (email-safe width)
  const pageDesktop = await browser.newPage({ viewport: { width: 600, height: 800 } });
  await pageDesktop.setContent(htmlContent, { waitUntil: 'networkidle' });
  await pageDesktop.screenshot({ 
    path: 'workspace/output/newsletter/screenshots/{slug}-desktop-600.png', 
    fullPage: true 
  });
  
  // Mobile 375px (iPhone SE)
  const pageMobile = await browser.newPage({ viewport: { width: 375, height: 667 } });
  await pageMobile.setContent(htmlContent, { waitUntil: 'networkidle' });
  await pageMobile.screenshot({ 
    path: 'workspace/output/newsletter/screenshots/{slug}-mobile-375.png', 
    fullPage: true 
  });
  
  await browser.close();
  console.log('Screenshots salvos em workspace/output/newsletter/screenshots/');
})();
```

**Salvar script em:** `scripts/newsletter/screenshot-preview.mjs`

---

### 2. Validação visual obrigatória (olho humano nos screenshots)

Abrir screenshots gerados e validar VISUALMENTE:

#### Espaçamento (crítico)
- [ ] Sem buraco branco > 60px no TOPO do conteúdo (após logo se houver)
- [ ] Sem buraco branco > 60px no FIM do conteúdo (antes da assinatura)
- [ ] Espaçamento entre parágrafos consistente (16-24px, não saltos de 60px+)

#### Bloco vídeo (se newsletter é de vídeo)
- [ ] **Bloco vídeo embed presente** (thumbnail YouTube + botão CTA)
- [ ] Thumbnail carrega visualmente (não quebrado)
- [ ] Botão CTA com estilo correto:
  - `border-radius: 8px`
  - `padding: 14px 32px` (visual robusto, não apertado)
  - `background-color: #1a1a1a` (fundo escuro)
  - `color: #ffffff` (texto branco)
  - `font-weight: 600` (negrito médio)

#### Bullets e tipografia
- [ ] Bullets renderizam como `<ul><li>` com marker visível (•)
- [ ] NUNCA parágrafo plano fingindo bullet
- [ ] Sub-headings `<h2>` visíveis e hierárquicas
- [ ] Font-size body ≥ 16px (legível mobile)

#### Assinatura
- [ ] Avatar circular presente e dimensionado corretamente (80×80px, não distorcido)
- [ ] 4 linhas texto literais presentes e corretas
- [ ] Hyperlink `{{DOMINIO}}` azul + underline

#### Compatibilidade
- [ ] Max-width 600px respeitado (não vaza lateral em desktop)
- [ ] Mobile 375px sem scroll horizontal (responsive OK)

---

### 3. REPROVAR se qualquer item falhar

**Output de reprovação obrigatório:**

```
REPROVADO — BLOQUEIA PATCH no {{PLATAFORMA_NEWSLETTER}}

Bugs encontrados (N/30):
1. Buraco branco 120px no topo — `<body>` tem `padding-top: 100px` — corrigir pra máximo 32px
2. Bloco vídeo ausente — newsletter é de transcrição YouTube — adicionar `::video-embed::` no markdown
3. [outros bugs...]

Screenshots evidência:
- workspace/output/newsletter/screenshots/{slug}-desktop-600.png (linha 1: ver buraco branco topo)
- workspace/output/newsletter/screenshots/{slug}-mobile-375.png (linha 2: bloco vídeo ausente)

Próximos passos:
1. Corrigir markdown source OU template renderizador
2. Re-rodar /renderizar-newsletter-html
3. Re-submeter para /revisar-newsletter-visual
4. Só APROVAR quando validação visual passar 100%
```

**NUNCA aprovar sem ter gerado + validado screenshots REAIS.**

---

### 4. Salvar screenshots como evidência obrigatória

Diretório canônico:

```
workspace/output/newsletter/screenshots/
  ├── {slug}-desktop-600.png
  └── {slug}-mobile-375.png
```

Retention: manter últimas 10 newsletters (limpeza manual periódica).

**Propósito:** rastreabilidade. Se {{NOME_OPERADOR_CURTO}} reportar bug visual em produção, comparar com screenshot pré-PATCH pra identificar se regressão foi introduzida no PATCH ou já estava no preview.

---

## Diferença crítica: auto-checklist vs revisão visual REAL

| Auto-checklist (insuficiente)                     | Revisão visual REAL (obrigatória)                  |
|---------------------------------------------------|----------------------------------------------------|
| Agent lê HTML como texto                          | Playwright renderiza HTML como navegador           |
| Busca padrões de código (grep `<ul>`, `padding`) | Mede dimensões visuais reais (bounding box, gaps)  |
| Assume que markup correto = visual correto        | Valida que visual renderizado = esperado           |
| **Falso positivo frequente**                      | **Detecta bugs visuais reais**                     |

**Lição do caso histórico 13/05/2026:** Newsletter `cadc4df0` tinha markup HTML correto (sem erro de sintaxe), mas padding excessivo + falta de bloco vídeo. Auto-checklist passou batido porque não RENDERIZOU.

---

## Cross-reference

- `/renderizar-newsletter-html` — gera HTML preview ANTES desta skill
- `/escrever-newsletter` — produz markdown source
- `/disparar-newsletter` — PATCH no {{PLATAFORMA_NEWSLETTER}} (bloqueado sem aprovação visual)
- Memória: `feedback_newsletter_video_embed_e_revisao_visual_real.md` (criada 13/05/2026)
- Memória: `feedback_smoke_test_funcional_revisor.md` (princípio geral: markup ≠ comportamento)

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{NOME_OPERADOR_CURTO}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente