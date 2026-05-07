# MAPA — squad-jade

**Propósito:** Camada de orquestração estratégica do squad. Jade COO + agentes que operam em nível alto (estratégia, decisões, governança), não em produção direta. Os outros squads produzem; este pensa antes e coordena.

**Última atualização:** 2026-05-06 (Tarefa #124 — `@estrategista` migrado de squad-conteudo pra cá)

## Agentes do squad

| Agente | Pasta | Função | Skill principal |
|---|---|---|---|
| `@jade` | (skill `/jade` em `.claude/commands/jade.md`) | COO — orquestradora, prioriza, despacha, blinda processos | `/jade` |
| `@estrategista` 🆕 | `agentes/estrategista/` | Define posicionamento, ângulo, narrativa e métricas ANTES da copy. Atende todos os squads (não só conteudo). Entrou em 06/05/2026 — antes morava em squad-conteudo. | `/escrever-estrategia` (revisado por `/revisar-estrategia`) |

## Conteúdo

| Arquivo | Função |
|---|---|
| `agentes/` (subpasta) | agentes do squad — ver MAPA.md interno de cada um |
| `aprendizados.md` | lições registradas pela camada de orquestração |
| `memoria.md` | memória de orquestração (estado, contexto cruzado entre squads) |

## Histórico
- 2026-05-06: Tarefa #124 — `@estrategista` migrado de `squad-conteudo` pra `squad-jade`. Decisão Gui + Jade: estratégia é peer da Jade, não produção. Atende todos os squads.
