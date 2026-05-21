---
name: revisar-copy
description: Valida copy generica curta (bio, headline, oneliner, anuncio) antes da publicacao — squad-copy -> revisor-copy.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /revisor-copy

Skill de validação INDEPENDENTE de **Copy genérica curta (bio, headline, oneliner, descrição, anúncio curto)** antes da publicação/disparo. Despachada pelo agente `@revisor-copy` (squad-copy).

## Quando invocar

- Imediatamente após **/escrever-copy** produzir/atualizar output
- Antes de qualquer publicação/disparo
- Sempre que houver mudança no conteúdo (mesmo correção pontual)

## Inputs

- `path` (obrigatório): path do output a revisar
- `briefing_id` (opcional): ID do briefing original

## Antes de validar — leitura obrigatória

Ver agente `.claude/agents/revisor-copy.md` (leitura obrigatória + checklist).

## Checklist obrigatória

### Comum (todas revisões)
1. Acentuação portuguesa perfeita
2. Light Copy (sem 3 Ps)
3. CTA único e claro
4. Tom alinhado com tom-de-voz + exemplos-copy-gui
5. Sem métricas privadas
6. Hiperlinks padrão `{{DOMINIO}}/[slug]`
7. Variáveis de personalização preservadas

### Específico do formato (Copy genérica curta (bio, headline, oneliner, descrição, anúncio curto))
8. Objetivo único e claro (1 ação)
9. Sem 3 Ps na abertura (Porque, Promessa, Pergunta)
10. Palavras-armadilha de tom checadas (`feedback_vocabulario_aproxima_lead.md`)
11. Sem métricas privadas (R\$, MRR) — `feedback_metricas_publicas_gui.md`
12. Sem promessas vagas — `feedback_vagueza_calibrada_copy.md`
13. Tom alinhado com `exemplos-copy-{{nome_operador}}.md` e `tom-de-voz.md`

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
[ Jade despacha /revisor-copy path=X ]
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

Ao final de cada revisão (especialmente REPROVAÇÃO), registrar em `squads/copy/agentes/revisor-copy/aprendizados.md`:
- Padrão de erro recorrente que deve virar item de checklist
- Falsos positivos da própria skill que precisam ser ajustados
- Novas armadilhas (palavras sem acento, expressões fora de tom, etc)

## Pendências registradas

Toda execução desta skill registra entrada em `workspace/memory/pendencias.md` com status (revisão em curso / aprovada / reprovada).

## Bateria de testes (Regra Inviolável #24)

Esta skill É a bateria de testes do formato — última linha antes da publicação.
