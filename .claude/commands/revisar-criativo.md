---
name: revisar-criativo
description: Valida copy de criativo Meta Ads (headline, primary, description, CTA) antes do disparo — squad-trafego -> revisor-criativo.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /revisor-criativo

Skill de validação INDEPENDENTE de **Copy de criativo Meta Ads (headline, primary text, description, CTA button) — texto, NÃO visual (visual = @revisar-visual)** antes da publicação/disparo. Despachada pelo agente `@revisor-criativo` (squad-trafego).

## Quando invocar

- Imediatamente após **/criar-criativo + /impulsionar-organico** produzir/atualizar output
- Antes de qualquer publicação/disparo
- Sempre que houver mudança no conteúdo (mesmo correção pontual)

## Inputs

- `path` (obrigatório): path do output a revisar
- `briefing_id` (opcional): ID do briefing original

## Antes de validar — leitura obrigatória

Ver agente `.claude/agents/revisor-criativo.md` (leitura obrigatória + checklist).

## Checklist obrigatória

### Comum (todas revisões)
1. Acentuação portuguesa perfeita
2. Light Copy (sem 3 Ps)
3. CTA único e claro
4. Tom alinhado com tom-de-voz + exemplos-copy-gui
5. Sem métricas privadas
6. Hiperlinks padrão `{{DOMINIO}}/[slug]`
7. Variáveis de personalização preservadas

### Específico do formato (Copy de criativo Meta Ads (headline, primary text, description, CTA button) — texto, NÃO visual (visual = @revisar-visual))
8. Headline curta (40 chars max — Meta Ads padrão)
9. Primary text com gancho na 1ª linha (3-5 linhas no total)
10. Description (30 chars max — visível em alguns placements)
11. CTA button apropriado (Saiba Mais / Cadastrar / Comprar)
12. Promessa clara da oferta (sem vagueza)
13. Sem métricas privadas exageradas
14. Compliance Meta (sem 'YOU' direto, sem antes/depois extremo)

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
[ Jade despacha /revisor-criativo path=X ]
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

Ao final de cada revisão (especialmente REPROVAÇÃO), registrar em `squads/trafego/agentes/revisor-criativo/aprendizados.md`:
- Padrão de erro recorrente que deve virar item de checklist
- Falsos positivos da própria skill que precisam ser ajustados
- Novas armadilhas (palavras sem acento, expressões fora de tom, etc)

## Pendências registradas

Toda execução desta skill registra entrada em `workspace/memory/pendencias.md` com status (revisão em curso / aprovada / reprovada).

## Bateria de testes (Regra Inviolável #24)

Esta skill É a bateria de testes do formato — última linha antes da publicação.