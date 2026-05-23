# Memória — @especialista-email (squad-trafego)

> Contexto operacional permanente.

## Função do agente

Especialista em **email deliverability**. Garante chegada em inbox, monitora reputation, audita config ESP, lida com bounces/complaints, conduz warmup de domínios novos.

**Skill própria:** `/auditar-entregabilidade-email` (criada 11/05/2026, Onda B4)

## Integrações conhecidas

### GoHighLevel (ESP principal)
- App: "Squad Jade e App {{Plataforma_Conteudo}}" (PIT v2)
- Dedicated Domain: `empresa.{{DOMINIO}}` (Stage 1 warmup, 1000/dia)
- Backup: `mail.{{DOMINIO_EMAIL}}` (Stage 2, 2500/dia)
- DNS: SPF + DKIM 2048-bit + DMARC p=none na Hostinger
- SMTP backend: Mailgun (oculto pelo GHL)
- API v2 NÃO suporta POST email campaigns (descoberta 11/05)

### Tools de monitoramento (a configurar)
- Google Postmaster Tools — `empresa.{{DOMINIO}}` PENDENTE cadastro
- Microsoft SNDS — opcional
- GlockApps — opcional (paid)

## KPIs canônicos

- Inbox placement rate (target: > 95%)
- Bounce rate (hard < 2%, soft < 5%)
- Complaint rate (target: < 0.1%)
- Open rate (benchmark info-produto: 25-35%)
- Click rate (benchmark: 3-7%)
- Reply rate (newsletter conversacional: > 1%)
- Unsubscribe rate (target: < 0.5%)

## Limites técnicos (warmup GHL)
- Stage 1: 1000 emails/dia (~10 dias)
- Stage 2: 2500 emails/dia (~30 dias)
- Stage 3: full volume

## Memórias correlatas (do squad inteiro)
- `feedback_metricas_publicas_gui.md` — preço produto OK, faturamento empresa NÃO
- `project_jornada_cliente_reverso.md` — destino do tráfego/leads

## Última atualização
11/05/2026 — criação inicial
