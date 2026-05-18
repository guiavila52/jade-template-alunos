# Aprendizados — squad-copy (ponteiro)

Aprendizados cross-agente do squad convergiram pra auto-memory consolidada (Task 2 do refactor 14/05/2026). Este arquivo é só ponteiro.

## Onde estão os aprendizados agora

- **Cross-squad / copy macro** → `~/.claude/projects/.../memory/feedback_copy.md`, `feedback_paginas.md` (auto-load via MEMORY.md)
- **Específico de cada agente** → `squads/copy/agentes/{agente}/aprendizados.md`
  - copywriter, copywriter-lp, paginas, revisor-copy
- **Backup pré-faxina** → `workspace/historico-mudancas/2026-05-14-refactor-arquitetura/backup-task10/squads-copy-aprendizados.md.bak`

## Skills macro do squad-copy

- `/escrever-copy` + `/revisor-copy`
- `/escrever-pagina` + `/revisar-copy-pagina` + `/criar-pagina-nova` + `/migrar-pagina`
- `/escrever-estrategia` + `/revisar-estrategia` + `/atualizar-estrategia`

## Regra

Aprendizado novo cross-agente → memória `~/.claude/.../memory/feedback_*.md` (não aqui).
Aprendizado novo específico de um agente → `squads/copy/agentes/{agente}/aprendizados.md`.

---

## Padrão recorrente observado em revisões (anotar pra retrofit nas skills)

### FAQ comparativo cross-página é a armadilha clássica de violação de vagueza calibrada

Caso: revisão /mentoria-redesign 2026-05-14 (tarefa #6) reprovou em 3 itens críticos — TODOS concentrados no FAQ #5 ("Qual a diferença entre mentoria e consultoria?"). O copywriter-lp tentou ser útil pro leitor explicando duração, vagas e valor — e acabou violando ao mesmo tempo:

1. Briefing §9 "preço não revelar na página" (escapou: R$ 15k+ da consultoria)
2. Memória `feedback_copy:vagueza_calibrada_copy` Regra B (comparativo cross-página em valor banido)
3. Briefing §9 "vagas vagas, sem número específico" (escapou: 8-12 pessoas)

**Diretriz pra próxima skill `/escrever-pagina` rodar:** quando o briefing pedir FAQ tipo "qual a diferença entre X e Y", o copywriter-lp DEVE escrever só em formato + abordagem, NUNCA em duração + vagas + valor. Lista canônica das dimensões permitidas:
- Modalidade (grupo vs 1:1)
- Ritmo (toda semana vs customizado)
- Abordagem (você implementa, {{OPERADOR}} guia vs {{OPERADOR}} implementa COM você)
- Tipo de turma (fechada vs sob demanda)
- Profundidade (acompanhamento contínuo vs imersão concentrada)

Lista canônica das dimensões PROIBIDAS em copy comparativa pública:
- Duração (X meses, Y semanas)
- Quantidade de encontros/aulas/sessões
- Tamanho da turma (N vagas, N pessoas)
- Valor / investimento / faixa de preço

Aplicação: vale retroalimentar a skill `/escrever-pagina` com seção explícita "FAQ comparativo cross-página" + a skill `/revisar-copy-pagina` com checklist específico desse caso. Próximo ciclo de Onda quando essas skills forem atualizadas (project-level `.claude/commands/escrever-pagina.md` e `.claude/commands/revisar-copy-pagina.md` — edição via Bash heredoc por causa da Regra §11).
