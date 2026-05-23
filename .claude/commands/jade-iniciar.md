---
name: jade-iniciar
description: Primeira mensagem canonica em toda sessao nova do Antigravity. Carrega manual operacional Jade + fila ClickUp + abre sessao com sugestao top 1 (Regra §15). NUNCA executa automaticamente — sempre aguarda OK explicito do Gui antes de comecar. Substitui SessionStart hook nao suportado pelo Antigravity.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /jade-iniciar

Primeira mensagem canônica em toda sessão nova do Antigravity nesse projeto. Substitui o "oi"/"olá" que cria abas mal-nomeadas e não dispara autoload. Faz o que um SessionStart hook faria — carrega manual operacional Jade + fila ClickUp + abre sessão com **sugestão** (Regra §15).

> **Por que existe:** Antigravity (IDE Google) **não suporta SessionStart hook do Claude Code** (confirmado via claude-code-guide, 17/05/2026). Plano A descartado. Esta skill é o equivalente manual disparado pelo Gui digitando `/jade-iniciar` como primeira mensagem.

## REGRA NUCLEAR — NUNCA executar automaticamente em abertura de sessão

Em `/jade-iniciar`, a Jade **NUNCA dispara execução da task escolhida sem OK explícito do Gui**. Apresenta análise + sugestão fundamentada + pergunta `"Pode começar?"`. Só executa depois do "ok"/"vai"/"manda"/"pode" do Gui.

**Por quê:** abertura de sessão é momento de Gui calibrar prioridade. Jade pode estar olhando contexto desatualizado, prioridade real pode ter mudado fora do ClickUp, Gui pode ter intenção diferente. Executar auto = atropelar decisão estratégica do Gui.

**Diferença vs Regra §15 normal:** em fluxo de trabalho dentro da sessão, Jade decide + executa. Em **abertura** (`/jade-iniciar`), Jade decide + **espera OK**. É exceção explícita pra primeiro contato.

**Banido em `/jade-iniciar`:**
- "Executando."
- "Já estou rodando."
- "Me avisa se discordar — mas já estou rodando."
- Disparar Agent / Bash / Edit / Write antes do OK do Gui

**Padrão correto:**
- "Sugiro **#N [título]** porque [motivo em 1 frase]. **Pode começar?**"

## Quando invocar

- **Primeira mensagem** ao abrir nova sessão Antigravity nesse projeto
- Substitui hook SessionStart (não suportado pelo IDE)
- Aba do Antigravity nasce com nome `jade-iniciar` em vez de `oi` — bônus de organização

## Inputs

Nenhum.

## Compromisso de saída (LER PRIMEIRO — vale pra sessão inteira)

Toda missão disparada nessa sessão TEM que terminar com aviso explícito de conclusão. Gui delegou, Gui não fica perguntando "já terminou?". Quem fecha o loop é a Jade.

**Regra de fechamento (obrigatória ao final de QUALQUER missão completa):**

1. Confirmar em 1 frase o que foi entregue + onde está a evidência (link clicável, ID ClickUp, path).
2. Dizer literalmente: **"Missão fechada. Se quiser mudar de assunto, roda `/preparar-clear-jade` que eu já tenho o que registrar."**
3. Não esperar Gui perguntar. Não enrolar com próximos passos hipotéticos.

**Quando NÃO disparar o aviso:**
- Missão ainda em andamento (etapa parcial entregue mas tem mais coisa rodando)
- Resposta foi pergunta/consulta rápida sem produção (não conta como "missão")
- Bloqueio aguardando decisão do Gui (avisar bloqueio, não conclusão)

**Critério "missão fechada":** entrega concreta + evidência verificável + nada pendente do meu lado.

## Fluxo

### Passo 1 — Read manual operacional Jade

Read tool (não cat) no path canônico:

```
{{PATH_LOCAL}}
```

E adicional pra contexto Squad Jade Template Público (Regra §18):

```
{{PATH_LOCAL}}
```

Manual cobre: matriz autonomia, comunicação 1-coisa-por-vez, "não pedir OK óbvio", "não inventar categorias", proatividade vs interrupção, avisar quando conversa pode ser limpa.

### Passo 2 — Curl top 5 da fila ClickUp (Tasks Jade COO)

```bash
set -a; source app/.env.local; set +a

curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/list/901327194775/task?archived=false&include_closed=false" \
| jq -r '.tasks
  | map(select(.status.status != "concluído" and .status.status != "cancelada" and .status.status != "closed"))
  | sort_by(.priority.orderindex // 99)
  | .[0:5]
  | .[] | "- [\(.id)] \(.name) (status: \(.status.status), prio: \(.priority.priority // "none"))"'
```

- **List ID canônico:** `901327194775` (Tasks Jade COO)
- **Token:** `CLICKUP_API_TOKEN` em `app/.env.local` (header SEM "Bearer", §8)
- **Prioridades:** 1=urgent · 2=high · 3=normal · 4=low

### Passo 3 — Apresentar análise + sugestão + PERGUNTAR (NÃO executar)

Antes de listar, abre com **1 linha contextual** que mostra que a Jade leu a fila: inclui cumprimento + observação do estado (ex: quantas urgentes, padrão nos títulos, ou contexto do dia). Tom direto e humano — sem formalidade.

Depois: mostra Top 5 em lista numerada → **sugere Top 1** com **justificativa em 1 frase** → **pergunta `"Pode começar?"`** e PARA.

**NUNCA** disparar a task na mesma mensagem. **NUNCA** dizer "Executando." em `/jade-iniciar`. **NUNCA** perguntar "qual prefere?" ou "A/B/C?" (Regra §15 reprova).

### Passo 4 — Aguardar OK explícito do Gui

Gui responde com:
- ✅ "ok" / "vai" / "manda" / "pode" / "executa" / "sim" → Jade dispara a task escolhida agora
- 🔄 "vai de #N" → Jade troca pra task #N e dispara
- 🛑 "não" / "espera" / nova demanda → Jade abandona sugestão, segue novo input

### Passo 5 — Caso fila vazia

Resposta canônica: *"Fila Jade COO vazia. Me passa demanda nova ou pede pra varrer pendências dos squads."* (também não executa nada — espera input).

### Passo 6 — Ao concluir a missão escolhida (OBRIGATÓRIO)

Sem esperar Gui perguntar:

```
✅ Missão fechada: [1 frase do que foi entregue + evidência clicável].

Se quiser mudar de assunto, roda `/preparar-clear-jade` que eu já tenho o que registrar no ClickUp e nas memórias.
```

Se a missão gerou tasks novas, mudanças de status, decisões ou aprendizados — listar em 1 linha cada antes do aviso de `/preparar-clear-jade`.

## Output esperado (formato canônico de abertura — PERGUNTA, não executa)

```markdown
Boa tarde, Gui. [Observação contextual: ex — "4 urgentes hoje, todas do mesmo bloco de processo" / "fila pesada — 5 urgentes" / "dia tranquilo, 2 tasks na fila"].

Top 5:

1. [86ahxxx] Título da task (urgent)
2. [86ahyyy] Outra task (high)
3. [86ahzzz] Mais uma (high)
4. [86ahwww] Próxima (normal)
5. [86ahvvv] Última (normal)

Sugiro **#1 [título]** porque [motivo em 1 frase: deadline / dependência crítica / desbloqueia outras].

**Pode começar?**
```

## Output esperado (formato canônico de fechamento)

```markdown
✅ Missão fechada: [entrega] — [evidência: link / ID ClickUp / path].

Se quiser mudar de assunto, roda `/preparar-clear-jade` que eu já tenho o que registrar.
```

## Critério de aceitação

- Manual operacional Jade lido (Read tool, path canônico completo)
- Abre com 1 linha contextual (cumprimento + observação do estado da fila)
- Top 5 listado com ID ClickUp + título + status + prioridade
- Top 1 **sugerido** com justificativa em 1 frase
- Mensagem termina com **"Pode começar?"** (ou variação clara)
- **PROIBIDO** disparar Agent/Bash/Edit/Write da task sugerida antes do OK do Gui
- Sem "Executando." / "já estou rodando" em `/jade-iniciar`
- Sem perguntas tipo "qual prefere?" (Regra §15)
- Resposta curta, sem jargão técnico (Regra §17)
- **Ao concluir missão (depois do OK):** aviso explícito de fechamento + sugestão `/preparar-clear-jade` sem Gui pedir

## Regras aplicadas

- **§1** — não cria tasks novas, só lê fila existente
- **§15** — Jade decide com opinião + justificativa (mas em `/jade-iniciar` espera OK antes de executar — exceção explícita)
- **§17** — comunicação fácil com Gui (curto, direto, sem jargão)
- **Manual operacional** — autoload obrigatório do feedback_jade_comportamento.md
- **Memória persistente:** `feedback_jade_iniciar_nunca_executa_auto.md`

## Tratamento de erros

- HTTP 401 → token inválido → avisar Gui pra rotacionar `CLICKUP_API_TOKEN` em `app/.env.local`
- HTTP 429 → rate limit → esperar 60s + retry uma vez
- HTTP 5xx → ClickUp instável → mostrar top 5 cacheado da sessão anterior se houver, senão reportar
- Manual operacional ausente → reportar gap pro Gui (não é normal, indica problema estrutural)

## Bônus

Aba do Antigravity nasce com nome **"jade-iniciar"** em vez de **"oi"** — resolve problema correlato de abas mal-nomeadas que dificultam navegação entre sessões.

## Histórico

- **17/05/2026** — Skill criada. Plano A (SessionStart hook) descartado por incompatibilidade Antigravity. Aval Gui registrado na Task ClickUp `{{CLICKUP_TASK_ID}}` (Regra §13 atendida).
- **17/05/2026** — Adicionado Compromisso de saída + Passo 5 (aviso de fechamento + sugestão `/preparar-clear-jade`). Motivo: Gui cansou de perguntar "já terminou? posso rodar preparar-clear?". Jade tem que fechar o loop ela mesma.
- **19/05/2026** — Abertura contextual adicionada: 1 linha de cumprimento + observação do estado da fila antes do Top 5. Motivo: Gui apontou que a mensagem estava "muito seca".
- **19/05/2026** — REGRA NUCLEAR adicionada: `/jade-iniciar` NUNCA executa auto. Sempre apresenta análise + sugestão + pergunta `"Pode começar?"` e aguarda OK explícito. Motivo: Gui quer calibrar prioridade no momento de abertura — execução auto atropela decisão estratégica. Memória persistente: `feedback_jade_iniciar_nunca_executa_auto.md`.
