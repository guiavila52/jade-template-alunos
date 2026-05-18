# MAPA — squads/trafego/agentes/entregabilidade/

> Agente especialista em email deliverability + sender reputation + ESP best practices.

## Propósito

Garantir que emails do squad (newsletter, campanhas, transacionais) chegam na inbox — não no spam, não com bounce, não com complaint.

## Estado atual (11/05/2026)

Agente RECÉM-CRIADO. Estrutura canônica em construção. Skills correlatas ainda NÃO criadas.

## Arquivos

| Arquivo | Propósito |
|---|---|
| `memoria.md` | Contexto operacional + integrações conhecidas + KPIs |
| `aprendizados.md` | Lições do agente (vai crescendo) |
| `mapa.md` | Este arquivo |

## Skills correlatas (a criar — Onda futura)

- `/auditar-entregabilidade-email` — auditoria periódica config GHL/Mailgun
- `/relatar-saude-lista` — bounce rate, complaint rate, engagement decay
- `/configurar-warmup` — guia warmup novo domínio

## Como invocar (futuro)

Despachar via `subagent_type: entregabilidade` quando o agent estiver registrado em `.claude/agents/entregabilidade.md`.

## Última atualização
11/05/2026 — criação da estrutura
