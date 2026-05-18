# MAPA — squad-trafego

**Propósito:** Tráfego pago e email marketing — criativos Meta Ads, gestão de campanhas, entregabilidade.

## Agentes do squad

| Agente | Pasta | Função | Skill macro |
|---|---|---|---|
| `@gestor-trafego` | `agentes/gestor-trafego/` | Cria criativos Meta Ads, gerencia campanhas | `/criar-criativo`, `/relatar-trafego-diario` |
| `@revisor-criativo` | `agentes/revisor-criativo/` | Revisor independente de criativo Meta Ads | `/revisar-criativo` |
| `@especialista-email` | `agentes/especialista-email/` | Entregabilidade email (SPF/DKIM/DMARC, warmup IP) | (skill dedicada futura) |

## Estrutura

| Arquivo | Função |
|---|---|
| `agentes/{nome}/mapa.md` | índice do agente |
| `agentes/{nome}/aprendizados.md` | lições cumulativas (Regra §5) |

> Definição oficial dos agentes (Claude Code subagent system) vive em `.claude/agents/{nome}.md`.
