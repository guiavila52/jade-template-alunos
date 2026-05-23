# Histórico das regras invioláveis — squad

Doc viva com cronologia, reforços datados, casos com citação literal do Gui e decisões macro de refactors. As regras atemporais ficam em `AGENTS.md` (versão consolidada). Aqui mora o contexto histórico que justifica cada § e o rastro de quando foram reforçadas.

> **TTL de limpeza:** pasta `workspace/historico-mudancas/2026-05-14-refactor-arquitetura/` pode ser deletada após **2026-08-14** (3 meses pra consolidação). Esta doc preserva o essencial pós-deleção.

---

## Refactor 2026-05-14 — 35 regras originais → 12 regras-mãe atemporais

ClickUp task: `{{CLICKUP_TASK_ID}}`. Decisão: AGENTS.md tinha virado documento histórico (35 regras, ~1014 linhas, datas "Reforço 11/05" e "Decisão 13/05" dentro das regras, redundâncias). Refatorado em 12 regras-mãe atemporais. Casos históricos + reforços datados saíram do AGENTS.md e vieram pra esta doc.

### Mapeamento original → novo

| Original | Destino |
|---|---|
| #1 | Memória `feedback_processo.md` (seção "Extração antes de /clear") |
| #2 | DELETADA — comportamento padrão do Claude (não interrompe raciocínio) |
| #3 | Absorvida em §5 (Aprendizado cumulativo — "não inventar contexto") |
| #4 | Movida pra `workspace/regras/style-guide.md` (URL sempre como link) |
| #5 | DELETADA — redundante com §1 (fila ClickUp já garante atualização incremental) |
| #6 | DELETADA — Edit tool já exige Read first nativamente |
| #7 | Absorvida em §9 (segundo-cerebro read-only pra workers) |
| #8 | §11 (`.claude/` só via Bash heredoc/sed) |
| #9 | Memória `feedback_jade_comportamento.md` (seção "Segundo fracasso = mudar perspectiva") |
| #10 | §7 (MAPA estrutural em toda pasta) |
| #11 | §1 (Fila ClickUp source-of-truth) |
| #12 | §1 (Fila ClickUp source-of-truth) |
| #13 | §2 (Jade orquestra; matriz 4-gates; nunca aprova) |
| #14 | §5 (Aprendizado cumulativo) |
| #15 | §6 (Bateria de testes + triple-check) |
| #16 | §8 (DNS de produção com aprovação) |
| #17 | §3 (Skill canônica obrigatória — verbo no nome) |
| #18 | §9 (Proibido excluir repos) |
| #19 | §5 (Aprendizado cumulativo — 4 lugares + retrofit) |
| #20 | §3 (Skill canônica — fluxo doc obrigatório) |
| #21 | §8 (Secrets em `.env.local`) |
| #22 | §3 (Skill canônica — confiabilidade 100%) |
| #23 | §6 (Triple-check antes de produção) |
| #24 | §6 (Bateria de testes obrigatória) |
| #27 | §10 (Doc histórica viva de integrações) |
| #28 | §2 (Jade orquestra — toda demanda mapeia skill) |
| #29 | §2 (Matriz 4-gates) |
| #30 | `squads/conteudo/aprendizados.md` (seção "Newsletter PATCH — revisão visual antes") + §4 |
| #31 | Meta-nota no topo do AGENTS.md (lista de hooks ativos) |
| #33 | §2 (Jade nunca aprova; veredicto vem de revisor independente) |
| #34 | §8 (Supply chain — Shai-Hulud procedure) |
| #35 | §1 (Comentário antes de mudança de status ClickUp) |
| #36 | DELETADA — Gui pediu remoção em 2026-05-14 |
| #37 | §3 (Toda produção via skill canônica) |
| #38 | §4 (Revisão visual real Playwright obrigatória) |
| (nova) | §12 (Skill nova exige aval explícito do Gui — hook `check-skill-nova-sem-aval`) |

### Sumário quantitativo

- **35 regras originais** processadas
- **1 deletada por pedido explícito do Gui** (#36)
- **3 deletadas por redundância/nativo** (#2, #5, #6)
- **7 movidas pra fora do AGENTS.md** (#1→memória, #4→style-guide, #9→memória, #30→aprendizados conteudo, #31→meta-nota, + #2/#5/#6 deletadas)
- **27 consolidadas em 12 regras-mãe atemporais** (algumas regras alimentam mais de um §)
- **1 regra nova criada** (§12 — aval Gui pra skill nova)

---

## Reforços datados das regras que sobreviveram

### §1 — Fila ClickUp source-of-truth
- **10/05/2026** — reforço #11/#12: "sem exceção pra demanda pequena. Atualizar 1 skill, renomear arquivo, mudar 1 linha — TUDO vai pra pendencias antes". Memória `feedback_registrar_pendencia_antes_de_executar.md`.
- **12/05/2026** — Regra #28 codificada. Gui: *"A partir de agora, tudo que eu fizer eu vou pedir pra você primeiro. Não quero fazer nada por conta própria. Quero que você tenha skills corretas pra fazer as coisas."*
- **12/05/2026** — migração `pendencias.md` → ClickUp `901327194775` (Tasks Jade COO). Source of truth virou ClickUp; `pendencias.md` virou ponteiro.
- **13/05/2026** — Regra #35: comentário ANTES de mudança de status. Caso: Jade fechou tasks `{{CLICKUP_TASK_ID}}` e `{{CLICKUP_TASK_ID}}` sem comentário, status órfão. Gui pediu regra explícita.

### §2 — Jade orquestra; matriz 4-gates; nunca aprova
- **11/05/2026 ~15h45** — reincidência da Regra #13. Gui: *"Eu já tinha falado isso e aí falou que fez hook, ou fez alguma coisa pra evitar que isso comece antes. Então como é que vai ser feito agora? Como é que a gente vai garantir que o que eu passo pra Jade, a Jade orquestra com o time e não executa sozinha?"* Sistema passou de educativo pra hook bloqueante (`check-jade-producao-direta.sh`, exit 2).
- **12/05/2026** — Regra #29 (matriz autonomia v2). 2 reincidências de "Caqui parcial" no mesmo dia. Gui: *"Por que você esperou eu voltar pra fazer essas coisas? Você sabe que esses pontos devem ser feitos. Por que já não fez sem parar? Como fazer pra resolver isso definitivamente?"* Matriz v1 (5 categorias) → matriz v2 (4 gates), removida categoria "aprovação de copy" (era falsa escapatória).
- **13/05/2026** — Regra #33 (Jade nunca aprova). Caso: 12/05 Jade afirmou "aprovado" várias vezes baseada em preview local que não batia com painel/Gmail real. Gui exigiu regra estrutural.

### §3 — Skill canônica obrigatória
- **06/05/2026** — Regra #17 (verbo no nome). Decisão Gui: padrão verbo-primeiro pra reduzir ambiguidade entre skill (ação) e agente (papel).
- **10/05/2026** — Regra #22 (confiabilidade 100%). Gui: *"Se travou, o que será feito para isso nunca mais acontecer? As skills precisam ser 100% seguras e confiáveis. Confiabilidade é a palavra!"* Contexto: slide 1 do carrossel travou em background sem feedback, Mac sem `timeout` nativo, sem stderr capturado.
- **13/05/2026** — Regra #37 (toda produção via skill canônica). Caso: newsletter `cadc4df0-21e2-4b0b-84d8-adb517ab1275` criada por subagent improvisando HTML completo (`<!DOCTYPE><html><body padding>`) em vez de fragment limpo. Buracos visuais + DOCTYPE duplicado. Newsletter anterior `62bec9ff` (mesma feature) ficou perfeita porque foi gerada por caminho sem improvisação. Gui: *"se você tivesse gerado a que deu certo pela skill, se fosse a mesma skill, não teria dado errado."* Maturidade ⚪→🔵→🟡→🟢→🟥 codificada.

### §4 — Revisão visual real Playwright
- **13/05/2026** — Regra #38 codificada após 3 incidentes no mesmo dia: newsletter `cadc4df0` com buracos brancos + DOCTYPE duplicado (auto-checklist passou); bullets `<ul>/<li>` viraram `<p>` sem bolinha (Gui apontou 3 vezes); botão CTA do vídeo desconectado da capa. Todos detectáveis em 1 screenshot Playwright do `designer-revisor`. Squad-design criado separado dos squads produtores pra garantir independência (cruza com §2 — Jade nunca aprova).

### §5 — Aprendizado cumulativo
- **06/05/2026 ~21h** — Regra #19 codificada. Citação literal Gui: *"Sempre que eu te mandar alguma correção de copy, de página, alguma coisa, eu nunca quero ficar pedindo pra você atualizar as skills. Sempre atualize a skill de quem fez, pra isso nunca mais acontecer, e também a skill de quem revisa, pra isso nunca mais passar batido. Isso tem que ser uma regra de ouro. (...) Eu quero que você coloque isso até no claude.md, como regra fundamental e principal da Jade."*
- **06/05/2026** — Regra #14 (rejeição final = aprendizado + checklist). Gui rejeitou /consultoria com 6 erros básicos. #19 depois generalizou a #14.

### §6 — Bateria de testes + triple-check
- **06/05/2026** — Regra #15 (bateria mínima de páginas). Gui formalizou após rejeitar /consultoria com 6 erros básicos.
- **10/05/2026** — Regra #23 (triple-check). Gui questionou se 100% das páginas passavam por checkup. Resposta honesta: NÃO sistematicamente. Antes da #23, triple-check era obrigatório só dentro de `/rotina-gui-ausente` etapa 4.
- **11/05/2026** — Regra #24 (bateria em TODA entrega, não só páginas). Gui: *"Tudo que vc fizer, features e etc, sempre rode uma bateria de testes e utilize os agentes que fazem revisão e fazem testes em frontend e backend para garantir 100% de segurança e 100% de confiabilidade sem precisar me dizer para testar."* Contexto: Ondas 10.4 e 10.6 marcadas "entregue" só com auto-testes do agent produtor.

### §7 — MAPA estrutural
- **06/05/2026** — Citação Gui: *"Tem que atualizar o mapa de como funciona a nossa estrutura de agentes e squad. (...) Só botar como regra que sempre tem que atualizar o mapa quando tem alguma mudança nessa estrutura."* Codificada a obrigação de atualizar 5 lugares em mudança estrutural (squad MAPA + pai + página pública + CLAUDE.md + memória).

### §8 — Secrets + DNS + supply chain
- **08/05/2026** — Regra #21 (path canônico secrets). Jade criou `~/.openrouter/key` quando Gui pediu pra abrir documento pra colar OpenRouter API key. Memória `feedback_secrets_em_env_local.md` já existia mas não foi consultada. Gui: *"Vc teve essa ideia do nada, ou vc consultou nosso protocolo e base antes?"*
- **06/05/2026** — Regra #16 (DNS produção). `sites.{{DOMINIO}}` em produção (Next) — repontar antes da hora derrubaria páginas funcionando.
- **12/05/2026** — Regra #34 (supply chain Shai-Hulud). Ataque atingiu 205+ npm/PyPI artifacts via CI poisoning. Squad-empresa + sites-astro + {{Plataforma_Conteudo}} auditados 🟢 LIMPOS. Carlos suspendeu deploys 12/05. Recomendação aplicada: renovar .env.local {{Plataforma_Conteudo}} por precaução.

### §9 — Proibido excluir repos + segundo-cerebro read-only
- **06/05/2026** — Regra #18 codificada. Citação Gui: *"É muito, muito, muito perigoso. Isso não pode acontecer de jeito nenhum."*

### §10 — Doc histórica viva
- **11/05/2026** — Regra #27 codificada durante setup Meta Ads. Doc canônica modelo: `segundo-cerebro/03-operacao/meta-ads-historico.md`.

### §11 — `.claude/` só via Bash
- **05/05/2026** — Regra #8 original. Antigravity mantém modal mesmo com bypassPermissions.
- **11/05/2026** — reincidência 5+ vezes. Gui frustrado: *"Já pedi diversas vezes. Se não conseguir resolver, use o bash em vez de edit pra ficar me perguntando toda hora!!!"* Hook `check-edit-em-claude-paths.sh` registrado em `.claude/settings.local.json` retornando exit 2.

---

## Casos históricos preservados (citação literal do Gui)

1. **Aprendizado cumulativo (06/05/2026 ~21h)** — *"Sempre que eu te mandar alguma correção de copy, de página, alguma coisa, eu nunca quero ficar pedindo pra você atualizar as skills."*
2. **Jade orquestra (11/05/2026)** — *"Como é que a gente vai garantir que o que eu passo pra Jade, a Jade orquestra com o time e não executa sozinha?"*
3. **Confiabilidade (10/05/2026)** — *"Se travou, o que será feito para isso nunca mais acontecer? As skills precisam ser 100% seguras e confiáveis. Confiabilidade é a palavra!"*
4. **Bateria de testes (11/05/2026)** — *"Tudo que vc fizer, features e etc, sempre rode uma bateria de testes... sem precisar me dizer para testar."*
5. **Matriz autonomia (12/05/2026)** — *"Por que você esperou eu voltar pra fazer essas coisas? Você sabe que esses pontos devem ser feitos. Por que já não fez sem parar?"*
6. **Squad perfeito mapeado (12/05/2026)** — *"A partir de agora, tudo que eu fizer eu vou pedir pra você primeiro. Não quero fazer nada por conta própria."*
7. **Skill canônica determinística (13/05/2026)** — *"Se você tivesse gerado a que deu certo pela skill, se fosse a mesma skill, não teria dado errado."*
8. **MAPA estrutural (06/05/2026)** — *"Tem que atualizar o mapa de como funciona a nossa estrutura de agentes e squad."*
9. **Proibido excluir (06/05/2026)** — *"É muito, muito, muito perigoso. Isso não pode acontecer de jeito nenhum."*
10. **`.claude/` via Bash (11/05/2026)** — *"Já pedi diversas vezes. Se não conseguir resolver, use o bash em vez de edit pra ficar me perguntando toda hora!!!"*
11. **Path secrets (08/05/2026)** — *"Vc teve essa ideia do nada, ou vc consultou nosso protocolo e base antes?"*

---

## Manutenção desta doc

- Cada reforço novo de regra existente vai pra seção "Reforços datados" do § correspondente.
- Cada citação literal nova do Gui que justifica regra vai pra "Casos históricos preservados".
- Refactors macro de AGENTS.md (regra deletada, regra nova, consolidação) ganham seção própria com tabela de mapeamento.
- Não duplicar conteúdo de AGENTS.md aqui — esta doc é cronologia, AGENTS.md é princípio atemporal.

---

## Boas práticas não-invioláveis

### Commits granulares (caqui parcial)
1 commit por step do plano. Mensagem `feat/refactor/chore/fix/docs(squad):`. Sem commits monolíticos.

### Matriz autonomia Jade (4 gates) — Regra #29 absorvida em §2
Gates: (1) executa sozinha — operação trivial; (2) executa e reporta — operação rotineira; (3) aprovação prévia — decisão estratégica; (4) aprovação visual — output público. Hook ativo: `check-caqui-parcial-regra29.sh`.
