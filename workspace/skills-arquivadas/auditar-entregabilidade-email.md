# Skill: /auditar-entregabilidade-email

**Agente:** @especialista-email (squad-trafego)  
**Maturidade:** 🔵 EM PROGRESSO  
**Propósito:** Auditoria periódica de email deliverability. Garante que newsletters chegam em inbox (não spam), monitora sender reputation, audita config ESP, analisa bounces/complaints, acompanha warmup de domínios.

---

## Input

- **dominio:** domínio a auditar (default: `empresa.{{DOMINIO}}`)
- **modo:** `full` (auditoria completa 10 áreas) | `quick` (só métricas críticas: spam rate, reputation, bounce rate)
- **frequencia:** `diario` | `semanal` | `mensal` | `on-demand`

**Exemplo:**
```bash
/auditar-entregabilidade-email --dominio=empresa.{{DOMINIO}} --modo=full --frequencia=semanal
```

---

## O que fazer

Auditar 10 áreas de deliverability:

### 1. **Authentication (DNS)**
Validar registros DNS:
- **SPF:** `v=spf1 include:_spf.gohighlevel.com ~all` correto
- **DKIM:** 2048-bit key ativo ({{CRM}} gera automático)
- **DMARC:** `v=DMARC1; p=none; rua=mailto:contato@{dominio}` (Stage 1–2) ou `p=quarantine` (Stage 3)
- **PTR record:** forward/reverse DNS match ({{CRM}}/Mailgun handle automático)
- **TLS:** obrigatório ({{CRM}} default)

**Red flags:**
- SPF missing ou syntax error
- DKIM não configurado ou key expirado
- DMARC `rua=` aponta pra email não-monitorado (reports perdidos)
- DMARC `p=reject` em warmup (muito agressivo)

**Ação:** se authentication falhar, BLOQUEAR envios até corrigir (crítico).

---

### 2. **Sender reputation**
Monitorar via:
- **Google Postmaster Tools:** domain/IP reputation, spam rate, delivery errors, authentication status
  - Acesso: https://gmail.com/postmaster
  - KPI crítico: **spam rate < 0.1%** (se > 0.3% = Gmail throttles)
  - Domain reputation: High/Medium = ok, Low/Bad = investigar
- **Microsoft SNDS:** reputation Outlook/Hotmail
  - Acesso: https://sendersupport.olc.protection.outlook.com/snds/
  - Score: green (> 90%) = ok, yellow (70-90%) = atenção, red (< 70%) = problema
- **GlockApps / Mail-Tester:** inbox placement testing (pago ~$50/mês)
  - Opcional — só se spam rate persistente > 0.5%

**Red flags:**
- Spam rate > 0.3% (crítico — pausar envios)
- Domain reputation Low (investigar: conteúdo? lista? engagement?)
- IP reputation < 50% (shared IP — pode ser outros usuários {{CRM}}; considerar dedicated IP se enviar 50k+/mês)

**Ação:** se spam rate > 0.3%, PAUSAR próximo envio até investigar causa.

---

### 3. **Domain warmup status**
{{CRM}} Dedicated Domain tem 3 stages:
- **Stage 1:** 0–10 dias, 1000 emails/dia limit, reputation 0.1%
- **Stage 2:** 10–30 dias, 2500 emails/dia limit, reputation 1–10%
- **Stage 3:** 30–60 dias, 10k+ emails/dia, reputation 10–100%

**Auditoria:**
- Qual stage atual? (via {{CRM}} dashboard ou tempo desde setup)
- Volume enviado últimos 7 dias vs limite do stage
- Plano de escalação (gradual vs spike perigoso)

**Red flags:**
- Enviar 900 emails de uma vez em Stage 1 (risco soft-throttle)
- Não enviar por 7+ dias consecutivos (quebra consistência de warmup)
- Pular de 100/dia pra 2000/dia sem ramp gradual

**Ação:** se plano de envio não respeita warmup, AJUSTAR cronograma antes de próxima newsletter.

---

### 4. **Bounce rate**
Monitorar via {{CRM}} API `GET /contacts/?query=emailStatus:bounced`:
- **Hard bounce:** email não existe, domínio inválido, mailbox desativado
  - Target: < 2%
  - {{CRM}} remove automático (Suppression List)
- **Soft bounce:** caixa cheia, server timeout, greylisting temporário
  - Target: < 5%
  - {{CRM}} **não remove automático** — precisa cleanup manual

**Auditoria:**
- Hard bounce rate últimos 30 dias
- Soft bounce persistente (3+ bounces consecutivos → tratar como hard)
- Role addresses (`info@`, `admin@`, `noreply@`) na lista (alta taxa bounce/complaint)

**Red flags:**
- Bounce rate > 5% (degrada sender reputation)
- Soft bounces não limpos há 60+ dias

**Ação:** se bounce rate > 5%, rodar `/limpar-lista` (skill futura) antes de próximo envio.

---

### 5. **Complaint rate (spam reports)**
Monitorar via:
- **Google Postmaster Tools:** feedback loop reports
- **{{CRM}} Suppression List:** unsubscribes + complaints ({{CRM}} não separa — precisa inferir)

**Target:** < 0.1% (Gmail bloqueia se > 0.3%)

**Red flags:**
- Complaint rate > 0.1%
- Spike súbito (ex: passou de 0.05% pra 0.2% em 1 envio)

**Causas comuns:**
- Conteúdo não-alinhado com expectativa (comprou curso X, recebe promo produto Y)
- Frequência alta demais (2–3x/semana sem segmentação)
- Lista comprada ou não-opt-in (Gui não tem isso — base é opt-in)

**Ação:** se complaint rate > 0.1%, PAUSAR próximo envio + investigar conteúdo/lista.

---

### 6. **Engagement rate**
Monitorar via {{CRM}} API `GET /campaigns/{id}/stats`:
- **Open rate:** benchmark info-produto 20–30% (Apple MPP infla artificially — menos confiável)
- **Click rate:** benchmark 3–7%
- **Reply rate:** > 1% = excelente engagement (newsletter conversacional)
- **Unsub rate:** < 0.5% = saudável, 0.5–1% = ok, > 1% = problema

**Red flags:**
- Open rate < 15% consistente (problema subject line ou lista desengajada)
- Click rate < 2% (conteúdo não relevante ou CTA fraco)
- Unsub rate > 1% (frequência alta ou conteúdo off)

**Ação:** se engagement baixo, despachar pra @copywriter (newsletter) pra ajustar ângulo.

---

### 7. **List hygiene**
Auditar limpeza da lista:
- **Disengaged contacts:** não abriram últimos 180 dias
  - Ação: segment "Re-engagement" → 1 email final → se não abrir, remover
- **Duplicates:** mesmo email 2+ vezes ({{CRM}} deveria prevenir, mas validar)
- **Invalid syntax:** emails malformados (`foo@`, `bar@.com`)
- **Disposable domains:** `tempmail.com`, `10minutemail.com`, etc (bounce alto)

**Red flags:**
- > 20% da lista não abriu últimos 180 dias (degrada reputation)
- Syntax errors > 1% (precisa validation pre-import)

**Ação:** rodar `/limpar-lista` mensalmente (skill futura).

---

### 8. **Content quality**
Auditar newsletter atual pra spam triggers:
- **Spam words:** "grátis", "promoção", "clique aqui", "urgente", "parabéns você ganhou", ALL CAPS
- **Formatação:** imagem/texto ratio > 60% (muito image), HTML quebrado, anexos (.exe, .zip)
- **Links:** encurtadores (bit.ly, tinyurl) degradam reputation — usar domínio próprio
- **Preheader:** 90–110 chars otimizado (Gmail mostra ~40 mobile, ~100 desktop)
- **Dark mode:** CSS `prefers-color-scheme: dark` suportado
- **Plain text version:** multipart MIME (HTML + plain) — {{CRM}} não gera automático (workaround: `{{plain_text_version}}`)

**Red flags:**
- Subject all-caps ("NEWSLETTER SEMANAL")
- 3+ spam words no body
- Só imagem, zero texto (spam filters)

**Ação:** se spam score < 8/10 (Mail-Tester), revisar conteúdo antes de enviar.

---

### 9. **Reply configuration**
Auditar {{CRM}} Reply Settings:
- **Reply Address:** `contato@{dominio}` (alinhado com From address)
- **Forwarding Address:** `{{EMAIL_OPERADOR}}` (Gui recebe replies no Gmail)
- **DMARC reports:** `rua=` configurado + monitorado

**Red flags:**
- Reply Address vazio (replies caem no {{CRM}} Conversations — Gui não vê)
- Forwarding não configurado (feedback/oportunidades perdidos)
- DMARC reports não lidos (não detecta problemas authentication)

**Ação:** configurar Reply + Forwarding se missing (5 min fix, impacto alto).

---

### 10. **Compliance (CAN-SPAM / LGPD)**
Validar conformidade legal:
- **Footer obrigatório:**
  - Endereço físico da empresa (ou caixa postal)
  - Link unsubscribe visível (não texto pequeno escondido)
  - Nome da empresa
  - {{CRM}} adiciona automático (não pode desabilitar — compliance built-in)
- **One-click unsubscribe:** RFC 8058 / List-Unsubscribe header ({{CRM}} implementa automático)
- **LGPD:** opt-in explícito (Gui tem — leads de produtos), right to deletion ({{CRM}} permite export + delete)

**Red flags:**
- Footer missing ({{CRM}} deveria adicionar — se não aparece, template custom quebrado)
- Unsubscribe link quebrado (404)
- Não oferece opt-out claro

**Ação:** se compliance falhar, BLOQUEAR envios até corrigir (risco legal).

---

## Fluxo

```
┌─────────────────────────────────────────────┐
│ 1. Recebe dominio + modo + frequencia        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 2. Coleta dados:                            │
│    - DNS records (SPF/DKIM/DMARC via dig)   │
│    - Google Postmaster Tools (manual/API)   │
│    - {{CRM}} API (bounces, campaigns stats)     │
│    - Microsoft SNDS (manual)                │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 3. Audita 10 áreas (modo full) ou 3         │
│    (modo quick: spam rate, reputation,      │
│    bounce rate)                             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 4. Classifica severidade:                   │
│    - CRÍTICO: spam rate > 0.3%, auth fail   │
│    - ALTO: bounce > 5%, reputation Low      │
│    - MÉDIO: engagement baixo, list hygiene  │
│    - BAIXO: sugestões de polish             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 5. Gera recomendações priorizadas:          │
│    - PAUSAR envios (se CRÍTICO)             │
│    - Ajustar warmup (se volume perigoso)    │
│    - Limpar lista (se bounce/disengaged)    │
│    - Otimizar conteúdo (se engagement low)  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 6. Salva relatório markdown:                │
│    workspace/output/auditorias/                 │
│    entregabilidade-{dominio}-{timestamp}.md │
└─────────────────────────────────────────────┘
```

---

## Regras

### Regra Inviolável #22 (Confiabilidade)
- Timeout 10s por query DNS (se DNS não responde, anota MÉDIO "DNS timeout")
- Captura stderr de comandos externos (`dig`, `curl`)
- Graceful degradation: se Google Postmaster Tools API falhar, continua outras 9 áreas

### Quando bloquear envios
- **CRÍTICO >= 1:**
  - Spam rate > 0.3%
  - Authentication fail (SPF/DKIM/DMARC broken)
  - Complaint rate > 0.3%
  - Bounce rate > 10%
- **Ação:** não enviar próxima newsletter até corrigir + validar fix.

### Quando ajustar plano
- **ALTO >= 2:**
  - Bounce rate 5–10%
  - Domain reputation Low (não Bad)
  - Warmup stage não respeita limite (ex: 1200 emails em Stage 1)
- **Ação:** ajustar cronograma, limpar lista, ou reduzir volume.

### Quando apenas monitorar
- **MÉDIO/BAIXO:** anota no relatório, não bloqueia envio.

---

## Bateria de testes da skill

Antes de dar commit nesta skill, validar:

```bash
# 1. Testa contra domínio limpo (deve APROVAR)
/auditar-entregabilidade-email --dominio=empresa.{{DOMINIO}} --modo=full

# 2. Testa contra domínio sem DKIM (deve REPROVAR CRÍTICO)
/auditar-entregabilidade-email --dominio=dominio-quebrado-teste.com --modo=full

# 3. Testa modo quick (só 3 áreas)
/auditar-entregabilidade-email --dominio=empresa.{{DOMINIO}} --modo=quick

# 4. Valida que relatório é gerado
ls -lh workspace/output/auditorias/entregabilidade-*.md

# 5. Valida classificação severidade
grep -E "CRÍTICO|ALTO|MÉDIO|BAIXO" workspace/output/auditorias/entregabilidade-*.md
```

**Critérios de sucesso:**
- REPROVAR se spam rate > 0.3%
- REPROVAR se SPF/DKIM missing
- APROVAR se todos KPIs ok
- Relatório tem recomendações priorizadas (não só detecta, propõe fix)
- Tempo execução razoável (< 2 min modo full, < 30s modo quick)

---

## Integrações

### {{CRM}} (ESP principal)
- **App:** "Squad Jade e App {{Plataforma}}" (PIT v2)
- **Dedicated Domain:** `empresa.{{DOMINIO}}` (Stage 1 warmup)
- **API endpoints:**
  - `GET /contacts/?query=emailStatus:bounced` — bounces
  - `GET /contacts/?query=lastEmailOpenedAt<{date}` — disengaged
  - `GET /campaigns/{id}/stats` — open/click/unsub rates
- **Auth:** Bearer token via API Key ({{CRM}} dashboard → Settings → API)

### Google Postmaster Tools
- **Acesso:** https://gmail.com/postmaster
- **Setup:** cadastrar domínio + validar via DNS TXT record `google-site-verification=...`
- **KPIs:** spam rate, domain/IP reputation, delivery errors, authentication status
- **API:** não oficial (manual check via dashboard)
- **Frequência:** monitorar semanalmente (segunda-feira, pós-newsletter)

### Microsoft SNDS
- **Acesso:** https://sendersupport.olc.protection.outlook.com/snds/
- **Setup:** cadastrar IP address (shared IP do {{CRM}} — pegar via suporte ou headers email)
- **KPI:** reputation score (green > 90%, yellow 70–90%, red < 70%)
- **Frequência:** monitorar mensalmente (menos crítico que Gmail)

### Mail-Tester.com (opcional)
- **Acesso:** https://www.mail-tester.com/
- **Free tier:** 3 tests/dia
- **Uso:** enviar email teste pra endereço único gerado → aguardar 30s → buscar score
- **Output:** spam score 0–10 (ideal > 8) + recomendações

### DNS tools
- **dig:** validar SPF/DKIM/DMARC records
- **MXToolbox:** https://mxtoolbox.com/SuperTool.aspx (validação DNS + blacklist check)

---

## Referência

Relatório de pesquisa completo (11/05/2026):
`workspace/output/auditorias/2026-05-11-email-ghl-deep-research.md`

Tópicos cobertos:
- Práticas "verify before send" no {{CRM}}
- Warmup strategy (3 stages)
- List hygiene (suppression, soft/hard bounce)
- Authentication DNS (SPF/DKIM/DMARC/BIMI)
- Sender reputation (Postmaster Tools, SNDS)
- Compliance (CAN-SPAM, LGPD, one-click unsub)
- Content best practices (spam triggers, dark mode, mobile-first)
- Métricas + analytics (KPIs, benchmarks)
- Erros comuns + landmines
- Boas práticas específicas {{CRM}}

---

## Output canônico

Path: `workspace/output/auditorias/entregabilidade-{dominio}-{YYYY-MM-DD-HHMM}.md`

Estrutura:
```markdown
# Auditoria Entregabilidade — {dominio} — {timestamp}

## Summary
- Modo: full
- Domínio: empresa.{{DOMINIO}}
- Stage warmup: 1 (1000/dia limit)
- Veredicto: APROVADO COM RESSALVAS

---

## 1. Authentication (DNS)
✅ SPF: `v=spf1 include:_spf.gohighlevel.com ~all`
✅ DKIM: 2048-bit key ativo
✅ DMARC: `v=DMARC1; p=none; rua=mailto:contato@empresa.{{DOMINIO}}`
⚠️ [MÉDIO] DMARC reports não monitorados (caem no {{CRM}} Conversations)

## 2. Sender reputation
✅ Google Postmaster Tools: spam rate 0.08% (< 0.1% target)
✅ Domain reputation: High
⚠️ [BAIXO] Microsoft SNDS não cadastrado (Outlook 15% audiência)

## 3. Domain warmup status
⚠️ [ALTO] Stage 1 (1000/dia), mas planeja 900 de uma vez — risco soft-throttle
✅ Sending consistency ok (enviou últimos 7 dias)

## 4. Bounce rate
✅ Hard bounce: 1.2% (< 2% target)
⚠️ [MÉDIO] Soft bounce: 3.8% (alguns persistentes 60+ dias não limpos)

## 5. Complaint rate
✅ Spam reports: 0.05% (< 0.1% target)

## 6. Engagement rate
✅ Open rate: 28% (benchmark 20–30%)
✅ Click rate: 4.2% (benchmark 3–7%)
⚠️ [BAIXO] Reply rate: 0.3% (poderia melhorar com CTA reply)

## 7. List hygiene
⚠️ [MÉDIO] 18% da lista (680 contatos) não abriram últimos 180 dias
✅ Duplicates: 0
✅ Invalid syntax: 0

## 8. Content quality
✅ Spam score: 8.5/10 (Mail-Tester)
✅ No spam trigger words
⚠️ [BAIXO] Preheader não otimizado (padrão {{CRM}} genérico)

## 9. Reply configuration
🔴 [CRÍTICO] Reply Address VAZIO — replies caem no {{CRM}}, Gui não vê
🔴 [CRÍTICO] Forwarding Address VAZIO

## 10. Compliance
✅ Footer CAN-SPAM ok ({{CRM}} automático)
✅ One-click unsubscribe ok (RFC 8058)
✅ LGPD compliant

---

## Recomendações priorizadas

### [CRÍTICO] 1. Configurar Reply + Forwarding (5 min)
{{CRM}} → Settings → Email Services → Reply Settings:
- Reply Address: `contato@empresa.{{DOMINIO}}`
- Forwarding: `{{EMAIL_OPERADOR}}`

### [ALTO] 2. Ajustar plano warmup (30 min)
Semana 1: 100 contatos (engajados 30d)  
Semana 2: 200 contatos (engajados 90d)  
Semana 3: 500 contatos  
Semana 4+: 900 (full list)

### [MÉDIO] 3. Limpar soft bounces + disengaged (45 min)
Rodar `/limpar-lista` antes de próximo envio.

### [BAIXO] 4. Cadastrar Microsoft SNDS (10 min)
Monitorar Outlook reputation.

---

Agente: @especialista-email  
Data: 2026-05-11 15:10
```

---

## Última atualização
11/05/2026 — skill criada (Onda B4)
