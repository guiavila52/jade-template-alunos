# MEMORY.md — GPS do Squad

> Carregado automaticamente a cada sessão. Leia antes de qualquer coisa.
> Última atualização: 18/05/2026 — refactor estrutural mãe (squad/→workspace/ + Segundo Cérebro/→segundo-cerebro/ + DCG hook + IDENTIDADE.md + skill /atualizar-jade)

## 🏛️ ARQUITETURA CANÔNICA (pós-refactor 18/05/2026)

```
Jade - Time {{NOME_OPERADOR}}/
├── AGENTS.md           17 regras invioláveis (framework)
├── CLAUDE.md           orquestrador (framework, sem dados pessoais)
├── IDENTIDADE.md       persona (operador, empresas, funil) — autoload via @
├── MEMORY.md           este arquivo
├── README.md           quickstart
├── segundo-cerebro/    knowledge atemporal (lowercase, sem espaço/acento)
├── workspace/          estado/runtime (memory, output, scripts, regras, integracoes)
├── squads/             squads funcionais (gestao, conteudo, copy, dev, etc)
├── app/                código {{APP_PESSOAL}} (gitignored) + app/docs/ (PRD, business-rules, database, integrations)
├── docs/, scripts/
└── .claude/            commands, agents, hooks, settings.json
```

**Convenção pro aluno:** `workspace/` (singular) = onde a Jade trabalha. `squads/` (plural) = squads funcionais. Igual `app/` vs `apps/`.

**Two-track architecture:**
- Framework (atualiza via /atualizar-jade): CLAUDE.md, AGENTS.md, .claude/, squads/*/agentes/*/agente.md
- Persona (preservada): IDENTIDADE.md, MEMORY.md, segundo-cerebro/, workspace/memory/, workspace/output/, aprendizados.md

**Eliminados pelo refactor:**
- symlink squad/ → squad-fisico/
- pasta squad-fisico/
- "Segundo Cérebro/" (espaço + maiúscula + acento)
- arquivos pessoais do operador na raiz (eram do {{APP_PESSOAL}} — movidos pra app/docs/)
- duplicatas iCloud (* 2.md, * 3.md, etc)

**Bateria de segurança ativa:**
- 19 hooks PreToolUse (incluindo DCG: rm -rf /, git push --force, --no-verify, etc bloqueados)
- Gitleaks + detect-secrets pré-commit
- Tag rollback: pre-rename-workspace-2026-05-18

---

---

## ⚡ FOCO ATUAL

**Meta:** R$100k de lucro líquido/mês
**Caminho:** YouTube → Imersão quinta 19h → Mentoria → {{NOME_CURSO}} como escala
**Esta semana:** Fase 2 ativa — preparar Imersão 14/05 ("Monte seu squad de agentes") + página inscrição R$47 + repo GitHub alunos

---

## 📊 ESTADO DO NEGÓCIO

| | |
|---|---|
| Baseline mar/2026 | R$5.746 lucro (receita R$68k, despesa R$62k) |
| Gap para meta | ~R$94k/mês |
| Prioridade #1 | Mentoria — maior ticket, pipeline via Imersão de quinta |
| Prioridade #2 | Newsletter semanal — base capturada mas não nutrida |
| Prioridade #3 | Criativos de tráfego pago sem agência |

---

## 🏗️ ARQUITETURA DO SQUAD

Jade (COO) coordena 7 squads especializados:

| Squad | Agentes ativos | Memória |
|-------|---------------|---------|
| jade | jade (COO), estrategista | [`squads/gestao/`](squads/gestao/) |
| conteudo | newsletter, carrossel | [`squads/conteudo/`](squads/conteudo/) |
| copy | copywriter, paginas | [`squads/copy/`](squads/copy/) |
| dev | paginas-dev, {{app_pessoal}} (a criar) | [`squads/dev/`](squads/dev/) |
| trafego | trafego | [`squads/trafego/`](squads/trafego/) |
| financeiro | financeiro (ativo) | [`squads/financeiro/`](squads/financeiro/) |
| midia | a criar | [`squads/conteudo/`](squads/conteudo/) |
| infra | a criar | [`squads/dev/`](squads/dev/) |
| radar | a criar | [`squads/radar/`](squads/radar/) |

Mentoria = produto, não squad. Skill independente.

---

## 🗂️ TOPIC FILES

- [`projetos.md`](workspace/memory/projetos.md) — projetos ativos, status, bloqueios
- [`decisoes.md`](workspace/memory/decisoes.md) — decisões permanentes com data e contexto
- [`aprendizados.md`](workspace/memory/aprendizados.md) — lições gerais do squad
- [`pessoas.md`](workspace/memory/pessoas.md) — time, parceiros, como acionar
- [`pendencias.md`](workspace/memory/pendencias.md) — pendências abertas e evoluções do squad

---

## 🗓️ DIÁRIO

Notas brutas em [`workspace/memory/diario/`](workspace/memory/diario/) — retenção 30 dias, depois descarta.
Mais recente: `2026-05-05.md`

---

## 🤖 SQUAD

**Fase atual:** 2 — COO (Jade) orquestra via Agent tool. {{OPERADOR}} nunca invoca skills manualmente — apenas aprova outputs.
**Como funciona:** {{OPERADOR}} fala com Jade → Jade despacha subagentes via Agent tool → subagentes entregam → Jade consolida e apresenta ao {{OPERADOR}}
**Slash commands:** `/jade-iniciar`, `/jade`, `/escrever-copy`, `/escrever-newsletter`, `/criar-carrossel`, `/escrever-pagina`, `/criar-criativo`, `/ver-agenda`, `/revisar-semana`

---

## 🌍 SQUAD JADE — TEMPLATE PÚBLICO PROS ALUNOS (CRÍTICO)

**URL:** [github.com/{{github_user}}/jade](https://github.com/{{github_user}}/jade) — **PÚBLICO** + **Template Repository** ativo (botão "Use this template")

**Para que serve:** alunos do {{NOME_CURSO}} baixam essa versão sanitizada do squad da Jade pra usar no negócio deles.

**Skills relacionadas:**
- `/publicar-jade` — **EU (Jade)** rodo pra publicar nova versão do squad principal pro repo público ({{OPERADOR}} dispara quando quer empurrar atualização)
- `/atualizar-jade` — **ALUNO** roda no squad dele pra puxar atualizações da Jade preservando customização (two-track update)

**Regras INVIOLÁVEIS pra território público (Regra §18 AGENTS.md):**
1. ZERO refs sensíveis ({{EMPRESA_COFUNDADA}}, {{EMPRESA_HOLDING}}, Mágica, {{handle}}.com, CNPJs, clientes, nomes próprios)
2. ZERO histórico interno (tasks #NNN, decisões {{OPERADOR}}-Jade, datas operacionais)
3. ZERO arquivos pessoais (arquivos pessoais do operador (mantidos fora do template))
4. Skill `/publicar-jade` tem 5 validações bloqueantes — qualquer FAIL aborta sync
5. Push pra repo público SÓ via `/publicar-jade` — nunca direto

**Estrutura do template (espelhada do squad principal):**
- `CLAUDE.md`, `AGENTS.md`, `IDENTIDADE.md` (placeholders), `MEMORY.md` (vazio), `README.md`
- `workspace/`, `squads/`, `segundo-cerebro/` (vazio), `.claude/`
- Skill `/configurar-jade` que aluno roda 1x pra substituir placeholders pela identidade dele

---

## 📋 REGRAS DE ATUALIZAÇÃO

- Atualizar este arquivo sempre que o estado mudar
- Antes de compactar: extrair para topic files, depois atualizar este índice
- Nota diária: criar `workspace/memory/diario/YYYY-MM-DD.md` antes de encerrar sessão
- Fila de execução: atualizar `workspace/memoria-coo/sintese.md` após cada tarefa
