# Template aluno — Lista canônica de exclusões

> **Decisão (18/05/2026):** ao rodar `/publicar-jade` (sync pro repo público `{{GITHUB_USER}}/squad-template`), os itens abaixo são EXCLUÍDOS antes da sanitização. Aluno não recebe nada disso porque é específico da operação pessoal do Gui.
>
> Aprovado por Gui em 18/05/2026 após auditoria conjunta com Jade.

## Como funciona

`/publicar-jade` deve rodar `rsync --exclude-from=workspace/integracoes/template-aluno-exclusoes.md` (ou lógica equivalente que consuma essa lista) ANTES da sanitização de placeholders.

Validação obrigatória pós-staging: rodar `grep -l "consultar-nf\|{{plataforma_conteudo}}\|{{contadora}}\|{{suporte}}" /tmp/template-staging/.claude/commands/*` — deve retornar VAZIO.

## Skills excluídas (.claude/commands/*.md)

| Skill | Por quê sai |
|---|---|
| consultar-nf.md | {{PLATAFORMA_NF}} com conta FATORIAL 8959 (CNPJ Gui) |
| atualizar-voz-gui-avila.md | Voz pessoal do Gui (YouTube/Instagram dele) |
| publicar-jade.md | Só Gui publica updates pro template — aluno não tem template pra publicar |
| responder-{{suporte}}.md | {{SUPORTE}} é assistente operacional pessoal do Gui |
| publicar-{{plataforma_conteudo}}.md | {{PLATAFORMA_CONTEUDO}} é o SaaS proprietário do Gui |
| security-audit-{{plataforma_conteudo}}.md | Idem {{PLATAFORMA_CONTEUDO}} |
| feature-checkup-geral.md | Específica do app {{PLATAFORMA_CONTEUDO}} |
| deploy-manual-{{plataforma_conteudo}}.md | Idem {{PLATAFORMA_CONTEUDO}} |
| clickup-task-done.md | Lista ClickUp específica do {{PLATAFORMA_CONTEUDO}} (901327190242) |
| {{plataforma_conteudo}}-iniciar.md | Idem {{PLATAFORMA_CONTEUDO}} |
| {{plataforma_conteudo}}-add-task.md | Idem {{PLATAFORMA_CONTEUDO}} |
| sincronizar-clickup.md | Lista ClickUp específica do {{PLATAFORMA_CONTEUDO}} |
| otimizar-claude-{{plataforma_conteudo}}.md | Idem {{PLATAFORMA_CONTEUDO}} |

## Scripts excluídos

| Path | Por quê sai |
|---|---|
| scripts/financeiro/ (pasta inteira) | consultar-nf-{{contadora}}-*.py — {{CONTADORA}} é contadora pessoal do Gui |
| scripts/segundo-cerebro/atualizar-voz-gui-avila.* | Voz pessoal |

## Skills que FICAM (mesmo nome confundir — atenção)

- **/atualizar-jade** — FICA. Aluno usa pra puxar updates do upstream `{{GITHUB_USER}}/squad-template` (papel "shadcn add"). Não confundir com `/publicar-jade`.
- **/configurar-squad** — FICA. Aluno usa uma vez no onboarding pós-clone.
- **/jade** + **/jade-iniciar** — FICA. Operação Jade genérica.

## Validação automatizada (incluir em /publicar-jade)

```bash
# Após staging em /tmp/template-staging/:
FORBIDDEN_SKILLS="consultar-nf|publicar-jade|responder-{{suporte}}|publicar-{{plataforma_conteudo}}|security-audit-{{plataforma_conteudo}}|feature-checkup-geral|deploy-manual-{{plataforma_conteudo}}|clickup-task-done|{{plataforma_conteudo}}-iniciar|{{plataforma_conteudo}}-add-task|sincronizar-clickup|otimizar-claude-{{plataforma_conteudo}}|atualizar-voz-gui-avila"
COUNT=$(ls /tmp/template-staging/.claude/commands/ 2>/dev/null | grep -E "^(${FORBIDDEN_SKILLS})\.md$" | wc -l | tr -d ' ')
[ "$COUNT" = "0" ] && echo "OK exclusao skills" || { echo "FAIL: $COUNT skills pessoais vazaram pro staging"; exit 1; }

[ ! -d "/tmp/template-staging/scripts/financeiro" ] && echo "OK financeiro removido" || { echo "FAIL: scripts/financeiro vazou"; exit 1; }
```

## Histórico

- 18/05/2026 — Gui questionou se `/consultar-nf` ({{PLATAFORMA_NF}} dele) devia ir pro aluno. Auditoria conjunta gerou esta lista. `/atualizar-jade` foi inicialmente listada pra sair mas Gui corrigiu — ela FICA, aluno usa pra atualizar squad dele do upstream.
