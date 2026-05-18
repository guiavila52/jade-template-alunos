# Aprendizados — @especialista-email (squad-trafego)

> Lições acumuladas do agente. Cresce conforme cada entrega + correção do {{OPERADOR}}.

## 2026-05-11 — Onda zero (criação da estrutura)

**Contexto:** agente recém-criado. Spec definida via pesquisa profunda email GHL 11/05/2026 (relatório `workspace/output/auditorias/2026-05-11-email-ghl-deep-research.md`).

**Lições iniciais (extraídas da pesquisa):**

1. **Lembrança ≠ enforcement** — config correta no GHL não garante deliverability. Precisa MONITORAMENTO ativo (Postmaster Tools).
2. **Warmup tem 3 stages fixos no GHL** — não acelera manualmente. Stage 1: ~10 dias, Stage 2: ~30 dias, Stage 3: full.
3. **GHL API v2 NÃO suporta POST email campaigns** — disparo via UI ou Workflow trigger.
4. **Reply destino vazio = cai em Conversations** — decisão de produto: monitorar pelo app GHL vs forward externo.
5. **Dedicated domain > Shared IP** — branding + reputation isolada.

## Próximos aprendizados serão registrados aqui conforme:
- Métricas reais do primeiro disparo de newsletter chegarem
- Correções do {{OPERADOR}} sobre processo
- Descobertas de comportamento ESP (GHL/Mailgun)
