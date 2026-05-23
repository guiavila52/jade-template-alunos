# Sistema segundo-cerebro — Bruno Okamoto

> Referência extraída dos vídeos do Bruno Okamoto. Fonte para inspirar o squad do Gui.

---

## O que é

Workspace compartilhado entre dois agentes:
- **Claude Code** (local no Mac do Bruno) — agente interativo
- **Amora** (agente autônomo no VPS) — roda 24/7, faz commits automáticos

Canal de sincronia: Git. Push/pull a cada 30 minutos via cron.

```
Bruno (Mac) ↔ GitHub (okjpg/repo-amora-cos) ↔ Amora (VPS)
                git push/pull a cada 30min (cron)
```

Ambos os agentes leem e escrevem no mesmo repositório. O git é o canal de sincronia.

---

## Arquivos raiz

| Arquivo | Quem lê | Função |
|---|---|---|
| CLAUDE.md | Claude Code (local) | Boot manual do agente local |
| SOUL.md | Amora (VPS) | Identidade e personalidade |
| AGENTS.md | Amora (VPS) | Regras de sessão e boot sequence |
| USER.md | Ambos | Perfil do Bruno |
| TOOLS.md | Ambos | Integrações e credenciais |
| mapa.md | Ambos | Navegação — onde encontrar o que |
| PROPAGATION.md | Ambos | Protocolo único de propagação de dados |
| MEMORY.md | Ambos | Índice de memória de longo prazo |
| HEARTBEAT.md | Amora (VPS) | Checklist de heartbeat dos crons |
| IDENTITY.md | Amora (VPS) | Nome, emoji, modelo |

---

## Estrutura de pastas

```
amora-cos/
├── memory/            → Cérebro: contexto, projetos, sessões, integrações, tracking
├── skills/            → Skills categorizadas (ver skills/_registry.md)
├── content/           → Produção ativa de conteúdo por plataforma
├── areas/conteudo/    → Referência: voz, análises, estratégia, microprogramas
├── projects/          → Projetos ativos com PRD.md
├── reports/           → Reports gerados por crons e skills
├── scripts/           → Automação (youtube, content, metrics, utils)
├── docs/              → Documentação técnica
├── team-sync/         → Briefings e reports da equipe
└── archive/           → Organizado por trimestre (2026-Q1/, etc.)
```

---

## Regras do sistema

1. **Tudo vira registro** — decisão, pendência, ideia = arquivo. Nada fica só no chat.
2. **Propagar sempre** — seguir PROPAGATION.md quando qualquer dado mudar.
3. **Nunca sobrescrever** — se arquivo existe (Amora escreve) → edições, não substitui.

---

## Output da skill /rotina

Quando Bruno roda `/rotina`, a Amora:
1. Conecta no Supabase e puxa métricas do negócio em tempo real
2. Puxa agenda do Google Calendar do dia
3. Puxa emails classificados por urgência de ação
4. Gera cockpit no formato:

```
═══════════════════════════════════
ROTINA — [dia da semana], [data]
═══════════════════════════════════

📅 AGENDA
[horário] [evento]
[horário] livre (Xh)

📧 EMAILS
🔴 AÇÃO
→ [remetente] - "[assunto]" - [contexto/o que fazer]

📊 MÉTRICAS
[dados do negócio em tempo real]
```

---

## Memória de sessão

A Amora mantém registro de:
- O que foi feito hoje
- O que foi feito ontem
- O que foi feito nos últimos 7 dias
- Decisões recentes
- Alertas ativos

Isso alimenta o briefing do `=== SEGUNDO CÉREBRO - [data] ===` que aparece no início de cada sessão.
