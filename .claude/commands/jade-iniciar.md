---
name: jade-iniciar
description: Primeira mensagem canonica em toda sessao nova do Antigravity. Carrega manual operacional Jade + fila ClickUp + abre sessao com decisao top 1 (Regra §15). Substitui SessionStart hook nao suportado pelo Antigravity.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /jade-iniciar

Primeira mensagem canônica em toda sessão nova do Antigravity nesse projeto. Substitui o "oi"/"olá" que cria abas mal-nomeadas e não dispara autoload. Faz o que um SessionStart hook faria — carrega manual operacional Jade + fila ClickUp + abre sessão com decisão (Regra §15).

> **Por que existe:** Antigravity (IDE Google) **não suporta SessionStart hook do Claude Code** (confirmado via claude-code-guide, 17/05/2026). Plano A descartado. Esta skill é o equivalente manual disparado pelo {{OPERADOR}} digitando `/jade-iniciar` como primeira mensagem.

## Quando invocar

- **Primeira mensagem** ao abrir nova sessão Antigravity nesse projeto
- Substitui hook SessionStart (não suportado pelo IDE)
- Aba do Antigravity nasce com nome `jade-iniciar` em vez de `oi` — bônus de organização

## Inputs

Nenhum.

## Compromisso de saída (LER PRIMEIRO — vale pra sessão inteira)

Toda missão disparada nessa sessão TEM que terminar com aviso explícito de conclusão. {{OPERADOR}} delegou, {{OPERADOR}} não fica perguntando "já terminou?". Quem fecha o loop é a Jade.

**Regra de fechamento (obrigatória ao final de QUALQUER missão completa):**

1. Confirmar em 1 frase o que foi entregue + onde está a evidência (link clicável, ID ClickUp, path).
2. Dizer literalmente: **"Missão fechada. Se quiser mudar de assunto, roda `/preparar-clear-jade` que eu já tenho o que registrar."**
3. Não esperar {{OPERADOR}} perguntar. Não enrolar com próximos passos hipotéticos.

**Quando NÃO disparar o aviso:**
- Missão ainda em andamento (etapa parcial entregue mas tem mais coisa rodando)
- Resposta foi pergunta/consulta rápida sem produção (não conta como "missão")
- Bloqueio aguardando decisão do {{OPERADOR}} (avisar bloqueio, não conclusão)

**Critério "missão fechada":** entrega concreta + evidência verificável + nada pendente do meu lado.

## Fluxo

### Passo 1 — Read manual operacional Jade

Read tool (não cat) no path canônico:

```
$HOME/.claude/projects/-Users-{{handle}}-Documents-Projetos-IA-{{OPERADOR}}--vila-Jade---Time-{{OPERADOR}}--vila/memory/feedback_jade_comportamento.md
```

E adicional pra contexto Squad Jade Template Público (Regra §18):

```
$HOME/.claude/projects/-Users-{{handle}}-Documents-Projetos-IA-{{OPERADOR}}--vila-Jade---Time-{{OPERADOR}}--vila/memory/project_squad_jade_template_publico.md
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

### Passo 3 — Apresentar resposta inicial canônica (Regra §15 + §17)

Mostra Top 5 em lista numerada → **escolhe Top 1** com **justificativa em 1 frase** → diz **"Executando."** OU **"Me avisa se discordar — mas já estou rodando."**

**NUNCA perguntar** "qual prefere?" ou "tu escolhe A/B/C?" — Regra §15 reprova automaticamente.

### Passo 4 — Caso fila vazia

Resposta canônica: *"Fila Jade COO vazia. Me passa demanda nova ou pede pra varrer pendências dos squads."*

### Passo 5 — Ao concluir a missão escolhida (OBRIGATÓRIO)

Sem esperar {{OPERADOR}} perguntar:

```
✅ Missão fechada: [1 frase do que foi entregue + evidência clicável].

Se quiser mudar de assunto, roda `/preparar-clear-jade` que eu já tenho o que registrar no ClickUp e nas memórias.
```

Se a missão gerou tasks novas, mudanças de status, decisões ou aprendizados — listar em 1 linha cada antes do aviso de `/preparar-clear-jade`.

## Output esperado (formato canônico de abertura)

```markdown
Olhei a fila Jade COO. Top 5:

1. [86ahxxx] Título da task (urgent)
2. [86ahyyy] Outra task (high)
3. [86ahzzz] Mais uma (high)
4. [86ahwww] Próxima (normal)
5. [86ahvvv] Última (normal)

Vou de **#1 [título]** porque [motivo em 1 frase: deadline / dependência crítica / desbloqueia outras]. Executando.
```

## Output esperado (formato canônico de fechamento)

```markdown
✅ Missão fechada: [entrega] — [evidência: link / ID ClickUp / path].

Se quiser mudar de assunto, roda `/preparar-clear-jade` que eu já tenho o que registrar.
```

## Critério de aceitação

- Manual operacional Jade lido (Read tool, path canônico completo)
- Top 5 listado com ID ClickUp + título + status + prioridade
- Top 1 escolhido com justificativa em 1 frase
- "Executando." OU "já estou rodando" no fechamento de abertura
- Sem perguntas tipo "qual prefere?" (Regra §15)
- Resposta curta, sem jargão técnico (Regra §17)
- **Ao concluir missão:** aviso explícito de fechamento + sugestão `/preparar-clear-jade` sem {{OPERADOR}} pedir

## Regras aplicadas

- **§1** — não cria tasks novas, só lê fila existente
- **§15** — Jade decide com opinião + justificativa, nunca joga bola pro {{OPERADOR}}
- **§17** — comunicação fácil com {{OPERADOR}} (curto, direto, sem jargão)
- **Manual operacional** — autoload obrigatório do feedback_jade_comportamento.md

## Tratamento de erros

- HTTP 401 → token inválido → avisar {{OPERADOR}} pra rotacionar `CLICKUP_API_TOKEN` em `app/.env.local`
- HTTP 429 → rate limit → esperar 60s + retry uma vez
- HTTP 5xx → ClickUp instável → mostrar top 5 cacheado da sessão anterior se houver, senão reportar
- Manual operacional ausente → reportar gap pro {{OPERADOR}} (não é normal, indica problema estrutural)

## Bônus

Aba do Antigravity nasce com nome **"jade-iniciar"** em vez de **"oi"** — resolve problema correlato de abas mal-nomeadas que dificultam navegação entre sessões.

## Histórico

- **17/05/2026** — Skill criada. Plano A (SessionStart hook) descartado por incompatibilidade Antigravity. Aval {{OPERADOR}} registrado na Task ClickUp `{{clickup_task_id}}` (Regra §13 atendida).
- **17/05/2026** — Adicionado Compromisso de saída + Passo 5 (aviso de fechamento + sugestão `/preparar-clear-jade`). Motivo: {{OPERADOR}} cansou de perguntar "já terminou? posso rodar preparar-clear?". Jade tem que fechar o loop ela mesma.
