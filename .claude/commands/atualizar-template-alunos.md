---
name: atualizar-template-alunos
description: Sincroniza estrutura, skills e agentes sanitizados do squad atual pro repo publico {{GITHUB_USER}}/squad-template.
type: skill
---

# Skill: /atualizar-template-alunos

Sincroniza estrutura, skills e agentes (sanitizados) do squad atual pro repo público `{{GITHUB_USER}}/squad-template` — pra alunos baixarem como ponto de partida.

## Quando usar

- Squad atingiu marco que vale propagar pros alunos (skill nova testada, agente novo, regra nova)
- Disparo MANUAL pelo Gui ou Jade
- NÃO automático (cron é pendência futura sem prioridade — Tarefa #126)

## O que faz (alto nível)

1. Lê estado atual do squad (`Squad Empresa {{NOME_OPERADOR}}/`)
2. Sanitiza copiando pra `/tmp/template-staging/`:
   - **REMOVE:** memórias pessoais, pendências, diário, output, Segundo Cérebro, aprendizados específicos, tarefas específicas
   - **SANITIZA:** CLAUDE.md, instructions.md de agentes (placeholders `{{EMPRESA}}`, `{{NOME}}`, `{{ICP}}`)
   - **MANTÉM:** skills (após curadoria), AGENTS.md, estrutura de pastas, MAPAs (regenerados)
3. Curadoria skill-por-skill (algumas referenciam contexto sensível)
4. Diff vs `{{GITHUB_USER}}/squad-template` atual
5. Push pro repo (em `main` se primeira versão sem conflito; senão branch `vYYYY-MM-DD` + PR)

## Checklist do executor

### Etapa 1 — Snapshot

- [ ] Cria `/tmp/template-staging/` (limpa se já existir)
- [ ] `rsync -a --exclude=...` do squad pro staging com excludes:
  - `Segundo Cérebro/`
  - `squad-fisico/output/`
  - `squad-fisico/memory/diario/`
  - `squad-fisico/memory/pendencias.md`
  - `squad-fisico/memory/decisoes.md`
  - `squad-fisico/memory/aprendizados.md`
  - `squads/*/aprendizados.md`
  - `squads/*/tarefas.md`
  - `squads/*/agentes/*/aprendizados.md`
  - `node_modules/`
  - `.git/`
  - `.vercel/`
  - `.astro/`
  - `dist/`
  - `*.preFix*`
  - `*.preMigracao`

### Etapa 2 — Sanitização

- [ ] `CLAUDE.md`: trocar bloco "POSICIONAMENTO DO GUI" por placeholder genérico
- [ ] `CLAUDE.md`: trocar bloco "Empresas (2 CNPJs)" por `{{LISTA_EMPRESAS}}`
- [ ] `CLAUDE.md`: trocar "{{NOME_OPERADOR}}" por `{{NOME_OPERADOR}}`
- [ ] `CLAUDE.md`: trocar referências a {{EMPRESA_COFUNDADA}}, {{EMPRESA_NEGOCIO}}, {{EMPRESA_HOLDING}} por placeholders
- [ ] `MEMORY.md` (se existir): regerar como template vazio (sem memórias pessoais)
- [ ] `squads/*/agentes/*/instructions.md`: substituir bloco "ICP" por `{{ICP}}`, "Empresa" por `{{EMPRESA}}`
- [ ] `squads/*/agentes/*/memoria.md`: zerar (template vazio com header)
- [ ] `squads/gestao/agentes/jade/instructions.md`: preservar arquitetura, sanitizar exemplos específicos


- [ ] **CRÍTICO (gap descoberto 12/05/2026): Sanitizar TODAS skills em `.claude/commands/*.md`**
  - 21+ skills hoje referenciam {{EMPRESA_COFUNDADA}}, {{EMPRESA_HOLDING}}, {{EMPRESA_NEGOCIO}}, {{NOME_OPERADOR}}, CNPJ real, clientes reais
  - Trocas obrigatórias via `sed` antes do push:
    ```bash
    for f in /tmp/template-staging/.claude/commands/*.md; do
      sed -i '' 's/{{EMPRESA_COFUNDADA}}/{{EMPRESA_COFUNDADA}}/g; s/{{EMPRESA_HOLDING}}/{{EMPRESA_HOLDING}}/g; s/{{EMPRESA_NEGOCIO}}/{{EMPRESA_NEGOCIO}}/g; s/{{EMPRESA_NEGOCIO}}/{{EMPRESA_NEGOCIO}}/g; s/{{MARCA_PESSOAL}}/{{MARCA_PESSOAL}}/g; s/{{NOME_OPERADOR}}/{{NOME_OPERADOR}}/g; s/{{operador_slug}}\.com/{{DOMINIO}}/g; s/{{GITHUB_USER}}/{{GITHUB_USER}}/g; s/55\.965\.507\/0001-71/{{CNPJ_PRINCIPAL}}/g; s/{{NOME_SUPORTE}}/{{NOME_SUPORTE}}/g; s/{{NOME_PARCEIRO_PLATAFORMA}}/{{NOME_PARCEIRO_PLATAFORMA}}/g; s/{{NOME_BACKUP_ADMIN}}/{{NOME_BACKUP_ADMIN}}/g; s///g; s/{{EXEMPLO_CLIENTE_EMPRESA}}/{{EXEMPLO_CLIENTE_EMPRESA}}/g; s/cliente_exemplo@gmail\.com/cliente@exemplo.com/g; s/45\.675\.359\/0001-05/00.000.000\/0000-00/g; s/{{META_AD_ACCOUNT_ID}}/{{META_AD_ACCOUNT_ID}}/g; s/{{META_APP_ID}}/{{META_APP_ID}}/g; s/{{META_BM_ID}}/{{META_BM_ID}}/g' "$f"
    done
    ```
  - Validar pós-sanitização: `grep -riE "{{lms_slug}}|{{empresa_holding}}|{{empresa_negocio}}|{{DOMINIO}}\.com|@{{HANDLE_INSTAGRAM}}|55\.965\.507|{{suporte}}|{{parceiro_plataforma}}|{{backup_admin}}|cliente_exemplo|tsm fa|45\.675\.359" /tmp/template-staging/.claude/` deve retornar ZERO

- [ ] **CRÍTICO: Sanitizar TODAS skills em `.claude/agents/*.md`**
  - 10 agentes hoje referenciam {{EMPRESA_COFUNDADA}}, {{EMPRESA_HOLDING}}, {{EMPRESA_NEGOCIO}}, etc
  - Aplicar mesmos `sed` de cima em `/tmp/template-staging/.claude/agents/*.md`
  - Validar pós-sanitização

- [ ] **Adicionar README.md no template** com instrução `/configurar-squad` (skill que substitui placeholders pelos dados do aluno)

- [ ] **Auditar arquivos de hook `.claude/hooks/*.sh`** — sanitizar se contém paths absolutos do Gui


### Etapa 3 — Curadoria de skills

Pra cada `.claude/commands/*.md`:

- [ ] **Genéricas (manter):** `/criar-pagina`, `/escrever-copy`, `/criar-carrossel`, `/escrever-newsletter`, `/codar-pagina`, `/revisar-pagina`, `/testar-pagina`, `/publicar-pagina`, `/migrar-pagina`, `/escrever-estrategia`, `/jade`, `/consolidar-sessao`
- [ ] **Específicas do Gui (PERGUNTAR):** `/consultar-nf` ({{PLATAFORMA_NF}} dele), `/atualizar-voz-gui-avila`, `/publicar-{{plataforma_conteudo}}`
- [ ] **Sanitizar exemplos:** trocar URLs `{{DOMINIO}}/*` por `{{DOMINIO}}/...` em todas as skills mantidas
- [ ] **NÃO incluir:** `/atualizar-template-alunos` (esta skill é só do Gui — não vai pro template)

### Etapa 4 — Estrutura mínima do template

```
squad-template/
├── CLAUDE.md             (sanitizado, com placeholders)
├── AGENTS.md             (regras invioláveis — vale pra todos)
├── MEMORY.md             (template vazio)
├── MAPA.md               (regenerado refletindo estrutura sanitizada)
├── .claude/commands/     (skills curadas)
├── squads/
│   ├── jade/             (COO + estrategista)
│   ├── conteudo/         (newsletter, carrossel)
│   ├── copy/             (copywriter, paginas)
│   ├── dev/              (paginas-dev)
│   └── trafego/          (criativo)
└── squad/
    ├── memory/           (vazio com headers)
    └── output/           (vazio)
```

### Etapa 5 — Diff e push

- [ ] `git clone https://github.com/{{GITHUB_USER}}/squad-template /tmp/template-current` (se já existir)
- [ ] `diff -r /tmp/template-staging /tmp/template-current` — gerar resumo
- [ ] Apresentar resumo do diff pro Gui (skills adicionadas, removidas, modificadas)
- [ ] Se primeira versão (repo vazio): push direto pra `main` com commit "Initial template — {YYYY-MM-DD}"
- [ ] Se atualização: criar branch `v{YYYY-MM-DD}`, push, abrir PR pro Gui revisar antes de merge

## Output esperado

- Repo `https://github.com/{{GITHUB_USER}}/squad-template` atualizado
- Commit: `"Sync template — {data} — {marco}"`
- URL do PR (se branch nova) reportada pra Jade

## Restrições

- **Manual** (sem cron) — Tarefa #126 trata do cron futuro
- **Visibilidade do repo template:** PÚBLICO (alunos baixam direto)
- **Não inclui Segundo Cérebro** (knowledge pessoal do Gui)
- **Não inclui memórias do user** (`~/.claude/projects/...`)
- **Não inclui esta skill** no template
- **Curadoria sempre** — nunca push automático sem revisão de skill-por-skill

## Fluxo (Regra #20 — fluxo documentado obrigatório; despacho via Jade segue Regra #13)

```
[Gui ou Jade dispara] /atualizar-template-alunos
        |
        v
[squad-dev] cria /tmp/template-staging/
        |
        v
[squad-dev] sanitiza (placeholders, remove pessoal)
        |
        v
[squad-dev] curadoria skill-por-skill
        |
        v
[squad-dev] diff vs {{GITHUB_USER}}/squad-template
        |
        v
[Jade] apresenta resumo do diff pro Gui
        |
        v
[Gui aprova] -> push (main ou branch + PR)
```
