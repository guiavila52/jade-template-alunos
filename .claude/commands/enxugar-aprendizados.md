---
name: enxugar-aprendizados
description: Manutenção mensal/sob-demanda dos arquivos aprendizados.md por agente. Detecta inchados (>200L), enxuga para 5-7 linhas por aprendizado, preserva backup integral em workspace/historico-mudancas/. Nunca descarta aprendizado — só formato.
type: skill
---

# /enxugar-aprendizados

**Squad:** dev (manutenção)  
**Maturidade:** 🟡 FUNCIONAL  
**Propósito:** Manter `squads/{sq}/agentes/{ag}/aprendizados.md` no formato enxuto canônico. Detecta arquivos inchados, faz backup, reescreve no formato 5-7 linhas/aprendizado, preserva 100% da substância em backup.

## Quando invocar

- Mensalmente (rotina manutenção)
- Sob demanda do Gui ("aprendizados tão grandes demais")
- Quando algum `aprendizados.md` ultrapassar 200 linhas (alerta `/check-up-estrutura`)
- Após onda de consolidação de agentes (fusão de pastas legacy)

## Princípio canônico (5-7 linhas por aprendizado)

```
### [Tarefa #N ou Data] — [Título curto]
**Regra:** [1 frase prescritiva — o que fazer/não fazer]
**Por quê:** [1 frase — incidente histórico que originou]
**Como aplicar:** [1 frase — gatilho/quando]
**Skill que aplica:** [/skill-x, /skill-y]
**Citação Gui (opcional):** "[curta, ≤1 linha]"
```

## O que ENXUGAR (vai pro backup)

- Exemplos antes/depois extensos (3+ casos)
- Justificativas longas com cross-references explícitas
- Lista exaustiva de skills atualizadas
- Citações longas do Gui (>1 linha) — preservar só essência
- Histórico de versões / changelogs internos
- Texto narrativo de contexto/motivação

## O que NUNCA descartar

- Regra prescritiva (o "o que fazer")
- Citação curta do Gui (1 linha)
- Skill que aplica (link curto)
- Aprendizado novo/único que ainda não virou regra/skill

## O que pode ser REMOVIDO (com link)

- Aprendizado que virou Regra Inviolável em AGENTS.md → remover, deixar linha "Ver AGENTS.md §N"
- Aprendizado que virou item de checklist em skill → remover, deixar linha "Ver `/skill-x` item N"

## Fluxo

```
1. /check-up-estrutura ou usuário invoca
        │
        ▼
2. Identificar inchados:
   find squads -name "aprendizados.md" -exec wc -l {} \; | awk '$1 > 200'
        │
        ▼
3. Pra cada inchado:
   a) Backup INTEGRAL pra workspace/historico-mudancas/YYYY-MM-DD-aprendizados-enxugados/{agente}-original-pre-enxugamento.md
   b) Ler arquivo
   c) Identificar aprendizados únicos + duplicatas + AGENTS.md/skills overlap
   d) Reescrever no formato enxuto
   e) Validar: wc -l < 200
        │
        ▼
4. Commit individual:
   git commit -m "chore({squad}): enxugar {agente}/aprendizados.md (N → M linhas)"
        │
        ▼
5. Comentar pendência mãe ClickUp
```

## Inputs

- **agente_path:** path específico (`squads/{sq}/agentes/{ag}/aprendizados.md`) — opcional
- **threshold_linhas:** mínimo pra considerar inchado (default: 200)

Sem args → varre todos os agentes e enxuga os que passarem do threshold.

## Critério de aceitação

- Backup integral preservado
- Reescrita ≤ 200 linhas
- Zero aprendizado único perdido (cross-check com backup obrigatório)
- Citações Gui curtas mantidas
- Skills/AGENTS.md referências mantidas
- Commit limpo + comentário ClickUp

## Restrições

- Backup é obrigatório ANTES de reescrever — se backup falhar, abortar
- Edição em `.claude/` proibida pra essa skill (não mexe em skills, só em squads/)
- Nunca apagar o arquivo original — só reescrever

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar: registrar pendência ClickUp via `/criar-pendencia`
- Ao concluir: comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do Gui, novo padrão de curadoria) → `squads/dev/agentes/devops/aprendizados.md`
- Reincidência (mesmo arquivo inchando de novo após X meses) → revisar formato de input dos aprendizados (algum agente está escrevendo verbose demais — atualizar skill /escrever-... pra forçar formato enxuto desde o início)
