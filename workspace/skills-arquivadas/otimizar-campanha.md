---
name: otimizar-campanha
description: Analisa campanha Meta Ads em curso e sugere ajustes (pause/scale/iterar criativo/mudar público/ajustar lance). Roda APÓS /relatar-trafego identificar problema. Output: lista priorizada de 3-5 ações com justificativa + impacto estimado. Squad-trafego implementa após Gui aprovar.
model: claude-sonnet-4-5
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

## Quando usar

`/relatar-trafego` apontou alerta numa campanha. Ou Gui pergunta "o que fazer com a campanha X?".

```
/otimizar-campanha <campaign_id ou nome>
```

## Heurísticas de otimização — matriz de decisão

| Sintoma | Diagnóstico provável | Ação |
|---|---|---|
| CTR baixo + CPM alto | Criativo cansado / público errado | **Trocar criativo** (despachar /criar-criativo ou /impulsionar-organico) |
| CTR ok + CPL alto | Público amplo demais | **Refinar público** (custom audience, lookalike menor) |
| CTR ok + CPL ok + ROAS baixo | Oferta fraca / preço errado | **Revisar oferta** (despachar estrategista) |
| Frequency >=4 | Saturação de público | **Refresh público** OU **expand budget** se ROAS ok |
| 0 conversões 7d + ROAS 0 | Campanha quebrada | **Pausar** + investigar pixel + tracking |
| ROAS >= 3x estável | Campanha vencedora | **Scale** 20% por dia (não dobrar — fadiga) |
| Custo subiu 20% sem motivo | Concorrência aumentou OU criativo cansando | **A/B novo criativo** + monitor 3 dias |

## Output canônico

```markdown
# Otimização campanha [nome] — YYYY-MM-DD

## Sintoma identificado

[do /relatar-trafego ou pergunta direta]

## Diagnóstico

[1-2 frases — qual heurística aplicada]

## Ações priorizadas

### 1. [ação] — IMPACTO ESTIMADO: [alto/médio/baixo]

[justificativa + como executar + tempo estimado]

### 2. ...

### 3. ...

## NÃO fazer

[o que evitar pra não piorar]

## Validação após implementar

[como medir se funcionou — quantos dias, qual KPI]
```

Salvar em `workspace/output/trafego/otimizacoes/YYYY-MM-DD-[campaign-id].md`.

## Restrições

- **NUNCA** mexer em campanha sem aprovação explícita do Gui
- **NUNCA** pausar campanha que está dando ROAS ≥ 2x (mesmo que tenha "alerta" qualquer)
- **NUNCA** dobrar orçamento de uma vez (scaleia 20%/dia max)
- Edição da skill via Bash/Python (Regra #8)

## Fluxo

```
[ /relatar-trafego apontou alerta OU Gui pediu otimização ]
        ↓
[ otimizar-campanha (squad-trafego) ]
   fetch dados detalhados da campanha (últimos 14 dias)
        ↓
[ Aplicar matriz de decisão ]
   identifica heurística que casa com sintoma
        ↓
[ Listar 3-5 ações priorizadas com impacto estimado ]
        ↓
[ Gerar markdown estruturado ]
        ↓
[ Salvar em workspace/output/trafego/otimizacoes/ ]
        ↓
[ Apresentar ao Gui ]
   sumário + ações + decisão pedida
        ↓
   ⟶ Gui aprova ações específicas
        ↓
[ trafego implementa ações aprovadas ]
        ↓
[ Validar após N dias ]
   KPI mudou? aprende heurística (Regra #19)
```

## Captura de aprendizado (Regra #19)

Quando heurística da matriz acerta/erra, registrar em `squads/trafego/agentes/gestor-trafego/aprendizados.md`. Se erra repetidamente, adicionar nova heurística.

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro Gui testar — testa antes.
