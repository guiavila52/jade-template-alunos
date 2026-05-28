---
name: revisar-roteiro
description: Valida roteiro de video YouTube (script falado, marcacoes, hooks de retencao) antes da gravacao — squad-conteudo.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /revisor-roteiro

Skill de validação INDEPENDENTE de **Roteiro de vídeo YouTube (script falado, marcações de cena, hooks de retenção)** antes da publicação/disparo. Despachada pelo agente `@revisor-roteiro` (squad-conteudo).

## Quando invocar

- Imediatamente após **/escrever-roteiro** produzir/atualizar output
- Antes de qualquer publicação/disparo
- Sempre que houver mudança no conteúdo (mesmo correção pontual)

## Inputs

- `path` (obrigatório): path do output a revisar
- `briefing_id` (opcional): ID do briefing original

## Antes de validar — leitura obrigatória

Ver agente `.claude/agents/revisor-roteiro.md` (leitura obrigatória + checklist).

## Checklist obrigatória

### Comum (todas revisões)
1. Acentuação portuguesa perfeita
2. Light Copy (sem 3 Ps)
3. CTA único e claro
4. Tom alinhado com tom-de-voz + exemplos-copy-gui
5. Sem métricas privadas
6. Hiperlinks padrão `{{DOMINIO}}/[slug]`
7. Variáveis de personalização preservadas

### Específico do formato (Roteiro de vídeo YouTube (script falado, marcações de cena, hooks de retenção))
8. Hook nos primeiros 5 segundos (frase que prende atenção imediata)
9. Loop aberto antes de cada quebra (gera curiosidade pra próxima parte)
10. Storytelling com 3 atos (setup → conflito → resolução)
11. Tempo de fala estimado (geralmente 1500-2500 palavras pra vídeo de 8-12min)
12. Marcações [VISUAL: ...] [CORTE] [B-ROLL: ...] presentes
13. CTA único e claro no fim
14. Frase de fechamento conecta com próximo vídeo (série)

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
[ Jade despacha /revisor-roteiro path=X ]
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

Ao final de cada revisão (especialmente REPROVAÇÃO), registrar em `squads/conteudo/agentes/revisor-roteiro/aprendizados.md`:
- Padrão de erro recorrente que deve virar item de checklist
- Falsos positivos da própria skill que precisam ser ajustados
- Novas armadilhas (palavras sem acento, expressões fora de tom, etc)

## Pendências registradas

Toda execução desta skill registra entrada em `workspace/memory/pendencias.md` com status (revisão em curso / aprovada / reprovada).

## Bateria de testes (Regra Inviolável #24)

Esta skill É a bateria de testes do formato — última linha antes da publicação.