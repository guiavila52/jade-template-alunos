# modelos-agentes.md — Referências de Squads de IA

> Modelos de outros criadores/empresas para inspirar a evolução do squad do Gui.

---

## Bruno Okamoto — Sistema Amora

**Fonte:** canal @obrunookamoto no YouTube + mini-curso OpenClaw
**Ferramenta:** OpenClaw + VPS + Claude (agora ChatGPT após ban da Anthropic)

**Arquitetura:**
- COO (Amora, L4-Autônomo) orquestra tudo
- 6 agentes ativos: Amora, Scraper, Content, Planner, Dev, QA
- Níveis L1→L4 (Observer → Advisor → Operator → Autonomous)
- Heartbeat escalonado a cada 15min por agente
- WORKING.md por agente (o que está fazendo agora — sobrescrito a cada task)
- Supabase como banco central (cards, tasks, memórias, atividades)
- Mission Control: dashboard web próprio (Express + React + Supabase + Cloudflare Access)
- 7 Arquivos Sagrados por agente: IDENTITY, SOUL, AGENTS, USER, TOOLS, MEMORY, WORKING
- Shared/: TEAM.md, outputs/, lessons/, context/, templates/, HEARTBEAT.md

**Aprendizados relevantes:**
- COO tem memória privada inacessível aos outros agentes
- Extração obrigatória antes de compactar (lições, decisões, pendências)
- Skills são genéricas — o segundo-cerebro é que é específico por cliente
- Compactar sem extrair = perder 80% do valor

**Custo estimado:** ~$45/mês (setup completo com VPS)

---

## Mateus Dias — Agência de Squads

**Fonte:** mencionado pelo Gui em 05/05/2026 (aula/vídeo)
**Ferramenta:** a confirmar

**Princípio central:**
> "Quanto menos squads, melhor."

Filosofia de simplicidade — resistir à tentação de criar muitos agentes especializados. Foco em poucos, bem calibrados.

**Arquitetura — 7 squads especializados sob 1 estratégico:**

```
estratégia (orquestrador central)
├── audiovisual     → squad-audiovisual-worker (4 agentes)
├── conteúdo        → squad-conteudo-worker    (8 agentes)
├── copy            → squad-copy-worker        (7 agentes)
├── dev             → squad-dev-worker         (8 agentes)
├── infra           → squad-infra-worker
├── pesquisa        → squad-pesquisa-worker    (2 agentes)
└── tráfego         → squad-trafego-worker     (7 agentes)
```

Cada squad tem um **squad-[área]-worker** com N agentes especializados dentro.

**Skills da operação:**

*Conteúdo & Vendas:*
- copywriting, newsletter, cold-email, email-sequence
- short-viral-content, copy-hooks-and-angles
- big-idea-builder, create-story, ad-creative, meta-ads-strategy

*Produto & Tech:*
- landing-page-prd, landing-page-implement, audit-landing
- create-prd, create-plan, site-architecture
- clean-code, deploy-pipeline, seo-audit
- supabase-admin, schema-markup, dns-ssl, env-secrets

---

## Princípios que emergem das referências

- **Menos é mais** (Mateus Dias) — não criar agente para tudo
- **COO como hub** (Bruno) — centralizar orquestração, agentes não falam entre si
- **Skills genéricas, contexto específico** (Bruno) — não duplicar skills, duplicar o segundo-cerebro
- **Extração antes de compactar** (Bruno/AGENTS.md) — memória viva é o ativo real

