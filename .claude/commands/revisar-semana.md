# /revisar-semana — Performance Review do Squad

> Rodar todo domingo. COO avalia cada agente. Resultado: promoção, manutenção, rebaixamento ou desativação.

Execute sem pedir confirmação:

## 1. Leia o contexto

Em paralelo:
- `squad/memoria-coo/niveis-agentes.md` — estado atual dos agentes
- `squad/shared/TEAM.md` — registro do squad
- `squad/memory/pendencias.md` — pendências da semana
- `squad/shared/lessons/` — lições registradas por agente na semana

## 2. Avalie cada agente ativo

Para cada agente, pontue de 1-5 nos seguintes critérios:

| Critério | Pergunta |
|----------|----------|
| **Quality Score** | Output precisou de retrabalho? Teve erros? Manteve o tom do {{NOME_OPERADOR}}? |
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

1. Atualize `squad/memoria-coo/niveis-agentes.md` com novos níveis e data
2. Atualize `squad/shared/TEAM.md` com os níveis revisados
3. Adicione entrada em `squad/shared/lessons/coo-lessons.md` com o resumo da semana
4. Adicione entry em `squad/memory/diario/[data].md` se houver decisões importantes

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
- Promoção sempre exige critério atingido + confirmação do Gui
- Desativação exige confirmação do {{NOME_OPERADOR}} antes de remover do TEAM.md
- Se a semana foi de estruturação (sem entregas reais), documentar isso e manter todos os níveis


## Fluxo

```
[ Domingo — /revisar-semana ]
        ↓
[ 1. Ler contexto em paralelo ] → @jade
   - squad/memoria-coo/niveis-agentes.md
   - squad/shared/TEAM.md
   - squad/memory/pendencias.md
   - squad/shared/lessons/ (lições da semana)
        ↓
[ 2. Avaliar cada agente ativo ] → @jade
   pontuar 1-5: Quality / Velocidade
   / Proatividade / Aderência / Custo-Benefício
        ↓
[ 3. Decisão por agente ] → @jade
   ┌──────────────────────────────────────┐
   ↓ 🏆 Promover (critério + consistência — exige OK {{NOME_OPERADOR}})
   ↓ 📊 Manter
   ↓ 📉 Rebaixar (2 erros graves ou 2 retrabalhos)
   ↓ ❌ Desativar (4+ semanas sem uso — exige OK {{NOME_OPERADOR}})
        ↓
[ 4. Registrar ] → @jade
   - niveis-agentes.md (novos níveis + data)
   - TEAM.md (níveis revisados)
   - coo-lessons.md (resumo da semana)
   - diario/[data].md (se houve decisão importante)
        ↓
[ 5. Entregar relatório ao {{NOME_OPERADOR}} ] → @jade
   formato com destaque + atenção
        ↓
   ⟶ FIM
```
