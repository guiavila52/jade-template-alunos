---
name: revisar-semana
description: Performance review dominical do squad — pontua cada agente em quality, velocidade, proatividade e aderencia.
type: skill
---

# /revisar-semana — Performance Review do Squad

> Rodar todo domingo. COO avalia cada agente. Resultado: promoção, manutenção, rebaixamento ou desativação.

Execute sem pedir confirmação:

## 1. Leia o contexto

Em paralelo:
- `workspace/memoria-coo/niveis-agentes.md` — estado atual dos agentes
- `workspace/shared/TEAM.md` — registro do squad
- `workspace/memory/pendencias.md` — pendências da semana
- `workspace/shared/lessons/` — lições registradas por agente na semana

## 2. Avalie cada agente ativo

Para cada agente, pontue de 1-5 nos seguintes critérios:

| Critério | Pergunta |
|----------|----------|
| **Quality Score** | Output precisou de retrabalho? Teve erros? Manteve o tom do {{OPERADOR}}? |
| **Velocidade** | Entregou quando pedido? Respondeu rápido? |
| **Proatividade** | Sugeriu melhorias? Antecipou problemas? Trouxe insights? |
| **Aderência** | Seguiu guardrails? Respeitou o nível? Manteve contexto? |
| **Custo-Benefício** | Valor entregue justifica o uso de tokens? |

## 3. Tome uma decisão por agente

- 🏆 **Promover** — critério da tabela atingido + desempenho consistente
- 📊 **Manter** — desempenho ok, sem critério de promoção ainda
- 📉 **Rebaixar** — dois erros graves ou duas entregas com retrabalho
- ❌ **Desativar** — agente sem uso há 4+ semanas ou custo não justificado

## 4. Registre

1. Atualize `workspace/memoria-coo/niveis-agentes.md` com novos níveis e data
2. Atualize `workspace/shared/TEAM.md` com os níveis revisados
3. Adicione entrada em `workspace/shared/lessons/coo-lessons.md` com o resumo da semana
4. Adicione entry em `workspace/memory/diario/[data].md` se houver decisões importantes

## 5. Entregue o relatório

Formato:

```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
PERFORMANCE REVIEW — [data]
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

[agente] → [decisão] | Quality: X | Vel: X | Pró: X | Ad: X | C/B: X
Motivo: [1 frase]

...

⚡ DESTAQUE DA SEMANA
[agente que mais entregou ou insight mais importante]

🔴 ATENÇÃO
[agente com problema ou pendência crítica]
```

## Regras

- Não inflar pontuação por falta de dados — agente sem uso = sem histórico = manter em L1
- Promoção sempre exige critério atingido + confirmação do {{OPERADOR}}
- Desativação exige confirmação do {{OPERADOR}} antes de remover do TEAM.md
- Se a semana foi de estruturação (sem entregas reais), documentar isso e manter todos os níveis


## Fluxo

```
[ Domingo — /revisar-semana ]
        ↓
[ 1. Ler contexto em paralelo ] → @jade
   - workspace/memoria-coo/niveis-agentes.md
   - workspace/shared/TEAM.md
   - workspace/memory/pendencias.md
   - workspace/shared/lessons/ (lições da semana)
        ↓
[ 2. Avaliar cada agente ativo ] → @jade
   pontuar 1-5: Quality / Velocidade
   / Proatividade / Aderência / Custo-Benefício
        ↓
[ 3. Decisão por agente ] → @jade
   ┌──────────────────────────────────────┐
   ↓ 🏆 Promover (critério + consistência — exige OK {{OPERADOR}})
   ↓ 📊 Manter
   ↓ 📉 Rebaixar (2 erros graves ou 2 retrabalhos)
   ↓ ❌ Desativar (4+ semanas sem uso — exige OK {{OPERADOR}})
        ↓
[ 4. Registrar ] → @jade
   - niveis-agentes.md (novos níveis + data)
   - TEAM.md (níveis revisados)
   - coo-lessons.md (resumo da semana)
   - diario/[data].md (se houve decisão importante)
        ↓
[ 5. Entregar relatório ao {{OPERADOR}} ] → @jade
   formato com destaque + atenção
        ↓
   ⟶ FIM
```

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{OPERADOR}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente
