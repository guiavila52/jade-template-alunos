# /rotina-gui-ausente-do-squad — rotina autônoma específica do squad-empresa

Você (Jade) vai executar a rotina autônoma completa do squad enquanto o {{NOME_OPERADOR}} está fora. Volta com a palavra-chave **Caqui** quando estiver tudo redondo + testado + auditado + commitado + deployado.

## Regras invioláveis (não pode esquecer)
- NUNCA pare pra perguntar — tome decisão técnica sozinha + registre raciocínio
- Atualize `PROGRESS.md` + `squad/memory/pendencias.md` + memórias persistentes A CADA item concluído
- Use APENAS agentes registrados em `.claude/agents/` (subagent_type específico)
- NUNCA `subagent_type: "general-purpose"` exceto research denso, infra atípica, multi-domínio sem dono
- Se travar > 30min na mesma tarefa: STALLED + skip + registra
- Notificação macOS quando terminar

## Despacho via agentes registrados — REGRA #155

| Tipo de trabalho | subagent_type |
|---|---|
| Codar Astro / deploy / scripts | `paginas-dev` |
| Copy de página (Light Copy) | `paginas` |
| Copy geral / carrossel / email / LinkedIn | `copywriter` |
| Estratégia / ângulo / posicionamento | `estrategista` |
| Newsletter | `newsletter` |
| Carrossel Instagram | `carrossel` |
| Criativos tráfego | `trafego` |
| Financeiro (NF/impostos/contabilidade) | `financeiro` |
| Bug hunting / pre-deploy QA | `bug-hunter` |
| Orquestração macro | `jade` |

## Pre-flight OBRIGATÓRIO (antes de qualquer despacho)

Toda rodada começa lendo:
1. `AGENTS.md` (todas as Regras Invioláveis #1-#19)
2. `~/.claude/projects/.../memory/MEMORY.md` (todas memórias persistentes)
3. `squad/memory/pendencias.md` (estado atual)
4. `squads/dev/tarefas.md` (tail 100 linhas — tarefas ativas/recentes)
5. `git status` nos 3 repos (squad-empresa, sites-astro, App Reverso)

Sem isso, vai despachar com regra desatualizada.

## Atualização de memória + pendências (OBRIGATÓRIO a cada item)

A cada item do checklist concluído:
- `squad/memory/pendencias.md` → mudança de status
- `~/.claude/.../memory/feedback_*.md` (criar/atualizar se aprendizado novo)
- `MEMORY.md` (auto-memory) → indexar nova memória se houver
- `PROGRESS.md` → estado atual

Se travar a qualquer momento, tudo fica organizado pro próximo turno retomar.

## Antes de despachar — checar conflito de arquivo (memória `feedback_nao_paralelizar_mesmo_arquivo.md`)

NUNCA 2+ agents simultâneos no mesmo arquivo. Antes de despachar:
1. `grep "Status:.*em curso" squads/dev/tarefas.md`
2. Conferir se algum mexe no arquivo X
3. Se sim → ENFILEIRAR

## Etapas

**0. Setup**
- Criar log `squad/output/rotinas-autonomas/{YYYY-MM-DD-HHMM}-rotina-autonoma.md`
- Snapshot: `git status` nos 3 repos + lista de tarefas ativas
- Notificar início via macOS: `osascript -e 'display notification "Rotina autônoma iniciada" with title "Jade — Squad"'`

**1. Pre-flight (já descrito acima)**

**2. Levantamento — checklist completo**
Mapear TUDO: tarefas em curso, enfileiradas, TODOs no código, bugs reportados não resolvidos. Salvar checklist em `PROGRESS.md`.

**3. Execução em sequência (respeitando conflito de arquivo)**
Item a item. Cada um:
- Despacha agente registrado (subagent_type específico)
- Aguarda resultado
- Atualiza `PROGRESS.md` + `pendencias.md` + memória se aplicável
- Move pra próximo

**4. Triple-check de revisores antes de cada deploy**
ANTES de `vercel --prod` em qualquer mudança visual ou de copy:
- Despacha `paginas` (revisor copy) — valida texto/posicionamento
- Despacha `paginas-dev` (revisor código) — valida implementação
- Despacha `bug-hunter` (caçador de bugs) — Playwright em todas as páginas: console errors, 404s, drag funcional, vídeos tocando, forms submetendo, links clicáveis, acessibilidade básica

Se qualquer dos 3 reprovar: corrige e re-roda os 3 até passar. Sem exceção.

**5. Bateria de testes pós-deploy**
- HTTP 200 nas 10 páginas em produção
- GTM-NN36ZRZ ≥ 2 (Regra #147)
- Favicon canônico (Regra #149)
- Astro nativo (`/_astro/` > 0, `framerusercontent` = 0)
- Slider rail sem snap (`scroll-snap-type: none`) + momentum (Regra #165)
- Cursor grab no hover desktop (Regra #139)
- Headers de segurança presentes
- Smoke test FUNCIONAL Playwright (não só estático): drag em sliders, vídeos readyState ≥ 3, forms enviam, links navegam

**6. Double check estrutural — `/check-up-estrutura`**
Roda a skill (13 categorias). Esperado: 0 findings CRITICAL/HIGH. Se houver: atacar caso a caso conforme regras desta skill.

**7. Auditoria de segurança contextual**
Detecta se mudou squad-empresa / sites-astro / App Reverso e roda auditoria adequada:
- Squad/Astro só: leve (5-10min) — secrets, .env, headers, GTM, Astro nativo
- Gimmick: `/security-audit` completa (overnight)
- Ambos: leve + completa
Resolver CRITICAL/HIGH antes de prosseguir.

**8. Commit + push 3 repos**
- `squad-empresa` privado: narrativa do que mudou na estrutura
- `sites-astro` privado: narrativa das páginas deployadas
- `squad-template` público: rodar `/atualizar-template-alunos` se houver mudanças relevantes pros alunos. Auditar diff por PII antes de mergear/abrir.

`git add` por arquivos específicos (NUNCA `add .` cego). Mensagem narrativa do PORQUÊ. Validar `git status` limpo.

**9. Relatório final + Caqui**
Em `PROGRESS.md` final:
- Concluído: lista
- Bloqueado: lista (precisa {{NOME_OPERADOR}})
- Decisões técnicas tomadas + raciocínio
- Resultado dos testes
- Resultado das auditorias
- Status dos commits
- Path do log estruturado

Notificar macOS: `osascript -e 'display notification "Caqui — squad pronto" with title "Jade — Squad" sound name "Glass"'`

Encerrar com: **Caqui** (se 100% redondo) OU **Caqui parcial** + lista de bloqueios (se houve algum item que dependeu do {{NOME_OPERADOR}}).

## Detecção de loop / 529 / timeout

- Tarefa sem progresso > 30min: STALLED + skip + relatar
- Subagent caiu com 529 Overloaded: re-despachar até 3x com backoff (60s → 180s → 600s)
- Mais de 3 falhas seguidas: pular item e relatar

## Fluxo

```
[ {{NOME_OPERADOR}} ausente chama /rotina-gui-ausente-do-squad ]
   regras: nunca para; usa agents registrados; atualiza memória/pendências sempre
        ↓
[ 0. Setup ] — log + snapshot + notif macOS
        ↓
[ 1. Pre-flight ] — AGENTS.md + MEMORY.md + pendencias.md + git status (obrigatório)
        ↓
[ 2. Levantamento ] — checklist em PROGRESS.md
        ↓
[ 3. Execução ] — item a item, agentes registrados, atualiza memória/pendências sempre
   ┌──────────────────────────────────────┐
   ↓ (decisão técnica)         (só {{NOME_OPERADOR}})   ↓
   decide + registra           bloqueado + segue
   └──────────────┬───────────────────────┘
        ↓
[ 4. Triple-check ] — paginas + paginas-dev + bug-hunter (todos aprovam)
        ↓
[ 5. Bateria pós-deploy ] — 10 páginas + smoke FUNCIONAL Playwright
        ↓
[ 6. /check-up-estrutura ] — 13 categorias; 0 CRITICAL/HIGH
        ↓
[ 7. Auditoria contextual ] — leve / completa / ambas conforme escopo
        ↓
[ 8. Commit + push 3 repos ] — narrativo, sem add cego
        ↓
[ 9. Relatório + Caqui ]
        ↓
   ⟶ notif macOS + palavra-chave **Caqui** 🍑
```

## Comparação com a genérica

A skill genérica `~/.claude/commands/rotina-gui-ausente.md` (user-level) é template base. **Esta** é específica do squad-empresa: conhece os 9 agentes, as 19 Regras Invioláveis, o `/check-up-estrutura`, os 3 repos, as 10 páginas em produção, todas as memórias persistentes. Use SEMPRE esta versão pra rodar no contexto deste projeto.
