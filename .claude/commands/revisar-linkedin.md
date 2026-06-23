---
name: revisar-linkedin
description: Valida post LinkedIn (200-1500 chars, lista vertical, primeira linha forte) antes da publicacao — squad-conteudo.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /revisor-linkedin

Skill de validação INDEPENDENTE de **Post LinkedIn (200-1500 caracteres, formato lista vertical curta, primeira linha forte)** antes da publicação/disparo. Despachada pelo agente `@revisor-linkedin` (squad-conteudo).

## Quando invocar

- Imediatamente após **/escrever-linkedin** produzir/atualizar output
- Antes de qualquer publicação/disparo
- Sempre que houver mudança no conteúdo (mesmo correção pontual)

## Inputs

- `path` (obrigatório): path do output a revisar
- `briefing_id` (opcional): ID do briefing original

## Antes de validar — leitura obrigatória

Ver agente `.claude/agents/revisor-linkedin.md` (leitura obrigatória + checklist).

## Checklist obrigatória

### Comum (todas revisões)
1. Acentuação portuguesa perfeita
2. Light Copy (sem 3 Ps)
3. CTA único e claro
4. Tom alinhado com tom-de-voz + exemplos-copy
5. Sem métricas privadas
6. Hiperlinks padrão `{{DOMINIO}}/[slug]`
7. Variáveis de personalização preservadas

### Específico do formato (Post LinkedIn (200-1500 caracteres, formato lista vertical curta, primeira linha forte))
8. Primeira linha forte (gancho que faz parar de rolar)
9. Parágrafos MUITO curtos (1-2 linhas cada — LinkedIn móvel)
10. Total entre 200-1500 chars (ideal 1300 pra reach orgânico)
11. Sem hashtags exageradas (máx 3 no fim)
12. Sem links externos no body (mata reach)
13. CTA pra comentário (gera engagement)
14. Pode usar emoji pontual (1-2, não exagerar)

## Output canônico

```markdown
# Revisão — {slug} — {data} — {VEREDICTO}

**Path:** {path}
**Veredicto:** ✅ APROVADO | ❌ REPROVADO | 🟡 APROVADO COM RESSALVAS

## Checklist (N itens)
(✓/✗ por item com linha + nota)

## Findings (se aplicável)
{gaps específicos com linha + ação}
```

## Severidade

- **REPROVADO** se: itens críticos (acentuação, 3 Ps, métricas privadas, formato fundamental) falham
- **APROVADO COM RESSALVAS** se: itens secundários falham parcialmente
- **APROVADO** se: 100% dos itens OK

## Fluxo

```
[ Jade despacha /revisor-linkedin path=X ]
        ↓
[ Revisor lê tom-de-voz + exemplos + ICP + memórias + aprendizados ]
        ↓
[ Aplica checklist completo ]
        ↓
   ┌──────────────────┬───────────────────────────────┐
   ↓ (100% OK)        ↓ (1+ REPROVADO)               ↓ (1+ ressalva)
   ✅ APROVADO         ❌ REPROVADO + findings        🟡 RESSALVAS
   Jade libera         Jade despacha produtor         Jade decide
                       pra corrigir + re-revisar
   └──────────────────┴───────────────────────────────┘
```

## Regra de aprendizado (Regra Inviolável #19)

Ao final de cada revisão (especialmente REPROVAÇÃO), registrar em `squads/conteudo/agentes/revisor-linkedin/aprendizados.md`:
- Padrão de erro recorrente que deve virar item de checklist
- Falsos positivos da própria skill que precisam ser ajustados
- Novas armadilhas (palavras sem acento, expressões fora de tom, etc)

## Pendências registradas

Toda execução desta skill registra entrada em `workspace/memory/pendencias.md` com status (revisão em curso / aprovada / reprovada).

## Bateria de testes (Regra Inviolável #24)

Esta skill É a bateria de testes do formato — última linha antes da publicação.