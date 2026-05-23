---
name: preparar-clear-jade
description: Rotina de preparação pra /clear no Squad Empresa {{NOME_OPERADOR}}. Sincroniza ClickUp, salva memórias persistentes, registra estado git/prod, decisões em aberto. Project-level, sobrescreve user-level.
type: skill
---

# Skill: /preparar-clear-jade (project-level, Squad Empresa {{NOME_OPERADOR}})

Execute agora a rotina de preparação para limpar o contexto. Faça tudo em sequência sem esperar confirmação do usuário em cada passo.

⚠️ Esta é a versão **project-level** do squad-empresa. Sobrescreve a user-level genérica. Reflete arquitetura pós-refactor 2026-05-14: pendências no ClickUp, aprendizados só em agente-level, paths via symlink `workspace/ → workspace/`.

📎 Versão deste projeto da família `/preparar-clear-{projeto}`. Sister: `/preparar-clear-{{plataforma_conteudo}}` (projeto {{Plataforma_Conteudo}}).

---


## Fluxo

```
Sessão atual pronta pra /clear
  ↓
1. Sincronizar ClickUp (comentários + status de tasks executadas)
2. Log narrativo da sessão (jade/aprendizados.md ou agente-level)
3. Salvar memórias persistentes (auto-memory consolidada)
4. Registrar aprendizados (feedback_* / agente-level / AGENTS.md se lei)
5. Atualizar PROGRESS.md (ou deletar se tarefa 100%)
6. Log rotina autônoma (se aplicável)
7. Dashboard Jade (metricas appended)
  ↓
Output (resposta padronizada + "Pode rodar /clear agora")
```

## Passo 1 — Sincronizar ClickUp

Pendências vivem no **ClickUp** list `901327194775` ("Tasks Jade COO"). Arquivo `workspace/memory/pendencias.md` é ponteiro de 15 linhas — não atualizar manualmente.

Ação:
1. Pra CADA entrega significativa da sessão, identificar task ClickUp correspondente
2. Adicionar comentário detalhado (Regra §1 + §35: comentário ANTES de mudar status) descrevendo o que foi entregue
3. Mudar status: `em progresso` → `aprovação` (espera Gui) OU `concluído` (se task auto-fechável)
4. Tasks novas surgidas na conversa: criar via `/criar-pendencia` ou diretamente via MCP ClickUp

Skill canônica: `/sincronizar-clickup` (se existir e funcional) ou MCP `clickup_create_task_comment` + `clickup_update_task` direto.

---

## Passo 2 — Log narrativo da sessão

Registrar narrativa da sessão em `squads/gestao/agentes/jade/aprendizados.md` (agente-level — Jade COO). Aprendizados específicos de outros agentes vão em `squads/{squad}/agentes/{agente}/aprendizados.md`.

**Não criar `squads/{squad}/aprendizados.md` denso** — regra fixada em 2026-05-14: aprendizados só em agente-level.

Conteúdo do log:
- Tarefas executadas (#número ClickUp) com agente responsável + status final
- Decisões técnicas autonomas tomadas + raciocínio
- Bloqueios encontrados + workaround aplicado

---

## Passo 3 — Salvar memórias persistentes (auto-memory)

Verifique o que surgiu nesta sessão que vale guardar em `~/.claude/projects/-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/memory/`:

| Tipo | Arquivo | Conteúdo |
|---|---|---|
| Feedback recorrente do Gui | `feedback_*.md` | Correções, preferências, aprovações de abordagem |
| Decisão de produto / arquitetura | `project_*.md` | Mudanças no posicionamento, squad, integrações |
| Info nova sobre Gui | `user_*.md` | Cargo, contexto pessoal, preferências fixas |
| Pointer externo | `reference_*.md` | URL canônica, conta externa, doc-fonte |

**Regra (refactor 2026-05-14):** consolidar em arquivo de tema existente em vez de criar novo. 14 arquivos consolidados — mais arquivos = MEMORY.md infla e estoura o limite oficial Anthropic (25 KB).

Tema novo só com aval explícito do Gui.

Para CADA memória nova ou atualizada:
1. Escrever o conteúdo no arquivo correto (frontmatter `name/description/type` válido)
2. Verificar se entrada em `MEMORY.md` (índice) existe — se não, adicionar 1 linha
3. Confirmar `MEMORY.md` < 25 KB pós-update

---

## Passo 4 — Aprendizados (Regra Inviolável §5 — Aprendizado cumulativo)

Varre a sessão atrás de correções que viraram aprendizados. Registra na camada certa:

### Cross-squad (afeta múltiplos agentes/Jade)
Local: `~/.claude/.../memory/feedback_*.md` consolidado por tema (Passo 3).

Exemplos:
- "Não inventar categorias intermediárias visuais sem combinar" → `feedback_jade_comportamento.md`
- "Subagent BG tem timeout interno" → `feedback_subagent_bg_timeout.md` (ou consolidar em tema existente)

### Agente-level (específico de UM agente)
Local: `squads/{squad}/agentes/{agente}/aprendizados.md`

Exemplos:
- Correção da copy do `@copywriter` que precisa virar regra → `squads/copy/agentes/copywriter/aprendizados.md`
- Bug do `@desenvolvedor-frontend` que não pode acontecer de novo → `squads/dev/agentes/desenvolvedor-frontend/aprendizados.md`

### Lei inviolável (aprendizado virou regra)
Local: `AGENTS.md` regra numerada (§1-§13)

Promover pra AGENTS.md quando:
- Reincidência (Gui pediu 2+ vezes a mesma correção)
- OU Gui pediu explicitamente promoção

**Não usar mais `squads/{squad}/aprendizados.md`** — eliminado em 2026-05-14.

Template de aprendizado:
```markdown
### YYYY-MM-DD — [título curto]

**Contexto:** [qual foi a tarefa]
**O que aconteceu:** [erro/correção/descoberta]
**Padrão identificado:** [regra reutilizável]
**Como evitar/repetir:** [ação concreta]
**Memória correlata:** [link se houver]
```

---

## Passo 5 — PROGRESS.md

- Se PROGRESS.md existe e a sessão tem continuidade: atualizar com estado atual + próxima ação exata (comando específico, arquivo específico) + bloqueios pendentes do Gui
- Se a tarefa fechou 100% E não tem follow-up: deletar PROGRESS.md
- Se não existe: pular

---

## Passo 6 — Log rotina autônoma (se aplicável)

Se a sessão foi disparada por `/rotina-gui-ausente` E ainda EM CURSO (não declarou Caqui):
- Atualizar `workspace/output/rotinas-autonomas/{YYYY-MM-DD-HHMM}-rotina-autonoma.md` (path real: `workspace/output/rotinas-autonomas/`)
- Conteúdo: status parcial, bloqueios, próximo passo pra retomar

Se NÃO é rotina autônoma OU já declarou Caqui: pular este passo.

---

## Passo 7 — Auto-verificação final (gate da paz ✌️)

Antes de mandar a resposta padronizada (Passo 9), executar bateria de verificação real. SÓ se TODOS os checks passarem é que a resposta inclui a frase "tá tudo em paz ✌️". Se algum falhar, NÃO mandar a frase — listar o que ficou pendente e pedir pro Gui resolver antes de `/clear`.

**Bateria obrigatória (rodar em sequência):**

```bash
cd "/Users/guiavila/Documents/Projetos IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"

# 1. Git working tree limpo (sem arquivos modificados não-commitados; untracked OK)
MODIFIED=$(git status --short 2>/dev/null | grep -E '^( M| D| A|MM|AM|AD|UU)' | wc -l | tr -d ' ')

# 2. Pelo menos 1 commit hoje (indica trabalho registrado)
COMMITS_HOJE=$(git log --since=midnight --oneline 2>/dev/null | wc -l | tr -d ' ')

# 3. ClickUp acessível (token válido) + lista de tasks responde HTTP 200
set -a; source app/.env.local; set +a
CLICKUP_OK=$(curl -s -o /dev/null -w "%{http_code}"   -H "Authorization: $CLICKUP_API_TOKEN"   "https://api.clickup.com/api/v2/list/901327194775/task?archived=false&include_closed=false&page=0")

# 4. Memória persistente acessível (auto-memory MEMORY.md existe)
MEMORY_INDEX="$HOME/.claude/projects/-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/MEMORY.md"
MEMORY_OK=$([ -f "$MEMORY_INDEX" ] && echo "1" || echo "0")

# 5. Pelo menos 1 aprendizado/memória tocado nas últimas 6h
RECENT_LEARN=$(find squads -name "aprendizados.md" -mmin -360 2>/dev/null | wc -l | tr -d ' ')
RECENT_MEM=$(find "$HOME/.claude/projects/-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/memory" -name "*.md" -mmin -360 2>/dev/null | wc -l | tr -d ' ')

echo "MODIFIED=$MODIFIED COMMITS_HOJE=$COMMITS_HOJE CLICKUP=$CLICKUP_OK MEMORY=$MEMORY_OK RECENT_LEARN=$RECENT_LEARN RECENT_MEM=$RECENT_MEM"
```

**Critério de paz ✌️ (TODOS têm que ser verdade):**
- `MODIFIED == 0` (working tree sem mudanças não-commitadas)
- `COMMITS_HOJE >= 1` (alguma coisa foi commitada hoje)
- `CLICKUP_OK == 200` (token válido + API responde)
- `MEMORY_OK == 1` (índice auto-memory existe)
- `RECENT_LEARN + RECENT_MEM >= 1` (sessão tocou pelo menos 1 aprendizado/memória)

Se TODOS verdadeiros → resposta do Passo 9 inclui "**tá tudo em paz ✌️**".
Se QUALQUER falhar → listar exatamente qual check falhou + pedir ação ao Gui antes de `/clear`. **NÃO escrever a frase de paz com o emoji ✌️ sem rodar a bateria.**

**Anti-fake:** o emoji ✌️ é a senha. Só usar se a bateria rodou de verdade e passou. Inventar/escrever sem rodar = quebra de confiança = falha de processo (Regra §5).

---

## Passo 8 — Atualizar dashboard de performance da Jade

Atualiza `workspace/output/metricas/jade-performance.md` (path real: `workspace/output/metricas/`) com métricas desta sessão:
- Duração estimada (timestamp inicial → agora)
- Tool uses estimados
- Subagents despachados (lista)
- Tabela acumulada (append, não sobrescreve)

Não é trabalho de subagent — Jade faz direto via Bash/Python. Hook §11 não se aplica (é `workspace/output/`).

---

## Passo 9 — Resposta padronizada (condicional ao Passo 7)

Após executar os passos acima, responda com:

```
Pronto pra limpar.

**ClickUp:** [N tasks atualizadas, N comentários adicionados]
**Log Jade:** [aprendizados de orquestração registrados em squads/gestao/agentes/jade/aprendizados.md]
**Memórias:** [arquivos criados/atualizados em auto-memory, ou "nenhuma novidade"]
**Aprendizados de agente:** [Squad: X. Agentes: Y. Cross-squad em auto-memory: Z. Promovidas pra AGENTS.md: W]
**PROGRESS.md:** [atualizado / removido / não havia]
**Rotina autônoma:** [parcial registrada / declarou Caqui / N/A]
**Dashboard Jade:** [métricas appended]

Pode rodar /clear agora.
```

---

## Princípios invioláveis durante o /preparar-clear

- **Não despachar agents** — Jade faz tudo direto. Skill é meta-trabalho de organização, não produção criativa.
- **Ler antes de escrever** — todo arquivo de aprendizado/memória antes de editar
- **Não duplicar memórias** — consolidar em arquivo de tema existente
- **Não inventar aprendizados** — só registrar o que REALMENTE aconteceu na sessão
- **Atualizar MEMORY.md index** pra cada memória nova
- **Não usar squad-level aprendizados** — eliminado no refactor 2026-05-14
