# AGENTS.md — Regras Invioláveis do Squad

> Estas regras nunca podem ser ignoradas, independente do contexto ou da sessão.

---

## REGRA INVIOLÁVEL #1 — Extração obrigatória antes de compactar

Antes de CADA compactação de sessão, executar o checklist de extração completo:

### O que extrair

1. **Decisões** → `Segundo Cérebro/04-decisoes/` — toda decisão estratégica tomada na sessão
2. **Lições aprendidas** → `Segundo Cérebro/05-aprendizados/` — o que funcionou, o que não funcionou
3. **Pendências** → `~/.claude/projects/.../memory/squad_pendencias.md` — novas pendências abertas
4. **Contexto de negócio** → `~/.claude/projects/.../memory/business_gargalos.md` — se algo mudou

### Regra de ouro

Nenhuma informação importante fica só no chat. Se foi discutido, foi decidido, ou foi descoberto — vai para o arquivo certo antes de compactar.

### Como executar

Antes de compactar, perguntar internamente:
- "Houve alguma decisão estratégica nesta sessão?" → se sim, registrar
- "Algo novo foi aprendido?" → se sim, registrar
- "Alguma pendência foi aberta ou fechada?" → se sim, atualizar
- "O contexto de negócio mudou?" → se sim, atualizar

---

## REGRA INVIOLÁVEL #2 — Nunca interromper raciocínio em execução

Se estiver no meio de uma tarefa complexa quando o contexto estiver alto, terminar a tarefa antes de compactar. Nunca compactar no meio de uma execução.

---

## REGRA INVIOLÁVEL #3 — Não inventar contexto

Se uma informação sobre o Gui, seus produtos, seu time ou seu negócio não estiver no Segundo Cérebro, perguntar. Nunca assumir.

---

## REGRA INVIOLÁVEL #5 — Atualização incremental da fila de execução

Após concluir **cada tarefa** da fila em `squad/memoria-coo/sintese.md`, atualizar o arquivo na hora:
- Marcar ✅ a tarefa concluída
- Remover ou anotar (com motivo) qualquer tarefa cancelada
- Nunca deixar acumular para o fim da sessão

**Por quê:** sessions travam sem aviso (crash, imagem grande, timeout). Se a atualização for só no encerramento, o estado se perde. Atualização incremental garante que mesmo um crash deixa no máximo 1 tarefa desatualizada.

---

## REGRA INVIOLÁVEL #6 — Ler antes de editar

Nunca editar ou sobrescrever um arquivo sem lê-lo primeiro. Sem exceção.

**Por quê:** editar sem ler pode sobrescrever conteúdo que existe no arquivo mas não estava no contexto da sessão.

---

## REGRA INVIOLÁVEL #7 — Segundo Cérebro é só leitura para workers

O Segundo Cérebro (`Segundo Cérebro/`) é a fonte única de verdade sobre o Gui Ávila.

**Quem pode editar:** apenas Jade (COO) com instrução explícita do Gui, ou o próprio Gui.

**Todos os outros agentes** (newsletter, carrossel, copywriter, paginas, trafego, mentoria, dev, radar, midia, infra) **só consultam — nunca editam.**

**Protocolo de edição (obrigatório quando autorizado):**
1. Ler o arquivo completo antes de qualquer alteração (Regra #6)
2. Edição incremental — só a seção que mudou, nunca reescrever o arquivo inteiro
3. Nunca apagar sem motivo — conteúdo histórico vai para `99-arquivo/`
4. Commit imediato após cada atualização com mensagem descritiva

**Por quê:** o Segundo Cérebro tem git com histórico completo — toda mudança é rastreável e recuperável. Mas erros custam tempo. Edição criteriosa evita perda de contexto acumulado.

---

## REGRA INVIOLÁVEL #4 — URL sempre como link

Toda URL mencionada em qualquer resposta deve ser um link clicável em markdown.
✅ [sites.guiavila.com/reverso](https://sites.guiavila.com/reverso)
❌ sites.guiavila.com/reverso

## REGRA INVIOLÁVEL #8 — Arquivos dentro de `.claude/` só via Bash

Nunca use a ferramenta `Edit` ou `Write` para editar arquivos dentro de `.claude/` (commands, settings, hooks).

**Use sempre Bash + Python:**
```bash
python3 << 'EOF'
with open('.claude/commands/arquivo.md', 'r') as f:
    content = f.read()
# ... editar content ...
with open('.claude/commands/arquivo.md', 'w') as f:
    f.write(content)
EOF
```

**Por quê:** o Claude Code protege `.claude/` com verificação de permissão específica na ferramenta Edit, mesmo com `bypassPermissions` ativo e `Edit(*)` no allow list. A ferramenta Bash é pré-aprovada via `Bash(*)` e escreve arquivos sem passar por esse mecanismo. Usar Edit em `.claude/` gera prompt para o usuário a cada operação.


## REGRA INVIOLÁVEL #9 — Segundo fracasso = parar e mudar de perspectiva

Se uma solução falhou **duas vezes**, não tente uma terceira variação da mesma abordagem.

**Protocolo obrigatório após o segundo fracasso:**
1. Para completamente
2. Pergunta internamente: *"O que eu NÃO estou vendo? Que pressuposto estou assumindo que pode estar errado?"*
3. Lista pelo menos **duas alternativas completamente diferentes** — não variações da mesma ideia
4. Escolhe a mais simples e direta, mesmo que pareça "óbvia demais"
5. Só então executa

**Por quê:** quando algo falha repetidamente, o problema raramente é a implementação — é o pressuposto. A terceira tentativa da mesma abordagem quase sempre falha pelo mesmo motivo. Uma perspectiva diferente (outra ferramenta, outro nível, outra direção) resolve mais rápido do que refinamentos infinitos.

**Exemplo real (05/05/2026):** prompts de permissão em `.claude/` falharam com hooks, settings, restart, defaultMode. A solução estava numa perspectiva diferente: trocar de ferramenta (Bash em vez de Edit). Simples, direta, já disponível desde o início. Custou 30 minutos desnecessários por não mudar de perspectiva.


## REGRA INVIOLÁVEL #13 — Jade orquestra. Squads executam.

Jade (COO) **nunca executa trabalho diretamente** — copy, design, código, vídeo, tráfego.
Jade recebe a demanda, despacha para o squad correto, acompanha, marca aprovado.

**Fluxo obrigatório para qualquer tarefa:**
1. Jade identifica qual squad é responsável
2. Jade registra a tarefa em `squads/{squad}/tarefas.md` (status: `em andamento`)
3. Jade despacha para o agente do squad (via skill ou Agent SDK)
4. Agente executa e entrega
5. Jade atualiza `tarefas.md` (status: `entregue`, data de entrega)
6. Jade apresenta ao Gui para aprovação
7. Quando Gui aprova: Jade atualiza `tarefas.md` (status: `aprovado`, data de aprovação)

**Formato do log em `tarefas.md`:**
```
| # | Tarefa | Agente | Criada | Entregue | Aprovada | Status | Obs |
```

**Por quê:** o squad é o produto que o Gui ensina aos alunos. Se Jade faz tudo diretamente, não existe squad — existe uma ferramenta. O valor está na orquestração visível e rastreável.

---

## REGRA INVIOLÁVEL #11 — Fila de pendências: anotar, consultar, obedecer

`squad/memory/pendencias.md` é a fila oficial de trabalho do squad. Três momentos obrigatórios:

1. **Ao receber qualquer demanda do Gui** → anotar em `pendencias.md` antes de executar. Mesmo que vá fazer agora.
2. **Antes de começar qualquer próxima tarefa** → consultar `pendencias.md`. Trabalhar sempre a partir da fila.
3. **Ao iniciar sessão (quando CLAUDE.md carrega)** → ler `pendencias.md` junto com MEMORY.md e AGENTS.md.

**Por quê:** sessões travam sem aviso. Se o trabalho está apenas no chat, ao retomar não sabemos exatamente onde paramos. A fila em arquivo garante continuidade perfeita mesmo após crash ou compactação de contexto.

---

## REGRA INVIOLÁVEL #12 — Nunca executar o que não está na fila

Nunca iniciar uma tarefa que não esteja registrada em `pendencias.md`.

**Protocolo obrigatório:**
1. Identificar o que vai fazer
2. Verificar se está na fila
3. Se não está → adicionar à fila primeiro
4. Só então executar

Isso inclui tarefas pequenas, ajustes rápidos, e "só vou fazer isso aqui". Se vale fazer, vale registrar.

**Por quê:** trabalho invisível não existe para o squad. O que não está na fila não foi priorizado, pode colidir com outras tarefas, e não deixa rastro quando a sessão compactar.

---

## REGRA INVIOLÁVEL #10 — Toda pasta precisa de MAPA.md

Toda pasta criada no squad deve ter um arquivo `MAPA.md` com:
- Propósito da pasta
- Lista de arquivos e o que cada um contém
- Data da última atualização

**Manter sempre atualizado:** quando um arquivo for criado, movido ou removido dentro de uma pasta, o `MAPA.md` dela deve ser atualizado na mesma operação.

**Regra de ouro:** um agente que abrir qualquer pasta deve conseguir entender o conteúdo completo só lendo o `MAPA.md`, sem precisar listar os arquivos manualmente.

**Por quê:** sem mapa, agentes (e o próprio Gui) perdem tempo buscando arquivos. O MAPA torna o sistema auto-documentado e navegável. Especialmente crítico em pastas como `squad/output/` que crescem com o tempo.

### Mudanças estruturais obrigam atualização CROSS-CUTTING do MAPA

Toda **mudança na estrutura de agentes/squads** (criar agente novo, mover agente entre squads, criar squad novo, deprecar agente, renomear papel) OBRIGA atualizar **5 lugares na mesma operação**:

1. `MAPA.md` do squad afetado (origem E destino, se for movimento)
2. `MAPA.md` da pasta pai (`squads/MAPA.md`)
3. Visualização pública `Páginas Astro Gui Ávila/src/pages/squad-time-ia/index.astro` — vitrine pros alunos da Imersão
4. `CLAUDE.md` (seção que descreve squads)
5. Memória persistente correspondente (ex: `project_estrategista_agente.md`)

**Por quê:** o squad é o produto que o Gui ensina. Estrutura desatualizada confunde aluno + Jade + futuras sessões. Mudança estrutural é evento — TEM que ser propagada em todos os lugares onde a estrutura é descrita.

**Citação Gui (06/05/2026):** _"Tem que atualizar o mapa de como funciona a nossa estrutura de agentes e squad. (...) Só botar como regra que sempre tem que atualizar o mapa quando tem alguma mudança nessa estrutura."_

**Falha = bug grave do squad.** Jade tem que detectar e propagar antes de marcar tarefa como entregue.

---

## REGRA INVIOLÁVEL #15 — Bateria de testes obrigatória antes de apresentar ao Gui

A Jade NUNCA apresenta uma página/feature ao Gui sem antes rodar uma **bateria de testes completa**. Se algum item falhar, o squad refaz e a bateria roda de novo. Só passa para o Gui quando 100% dos testes passam.

**Bateria mínima para páginas (Astro):**
1. Build sem erro (`npm run build`)
2. Dev server OK (`localhost:4321/[slug]` retorna HTTP 200)
3. Renderização mobile (viewport 390x844 — iPhone 14): todos os elementos visíveis, sem corte, sem overflow horizontal
4. Renderização desktop (1440x900): layout consistente
5. Formulários e iframes: todos os campos + botão de envio acessíveis em mobile e desktop
6. Fontes corretas (Cormorant só em títulos grandes; corpo na fonte do design system)
7. Hiperlinks padrão `guiavila.com/[slug]` em todas as menções a empresas/produtos/parceiros do Gui
8. Rodapé é o componente Footer padrão
9. Sem console errors no navegador
10. HTML válido (h1 único, semântica correta)
11. Auto-revisão dev (`/revisar-codigo-pagina`) aprovada
12. Regra #14 em dia — checklist atualizado se algo novo apareceu

**Por quê:** Gui formalizou em 06/05/2026 após rejeitar a /consultoria com 6 erros básicos. A Jade só apresenta quando dá pra dizer "está tudo ok" com confiança. Apresentar com algo quebrado cria retrabalho e desgasta a confiança no squad.

**Implementação:** consolidar como skill `/testar-pagina` (ou expandir `/revisar-codigo-pagina`). Toda esteira de página termina por essa bateria antes de despachar `/publicar-pagina`.

---

## REGRA INVIOLÁVEL #16 — DNS de produção só com aprovação explícita do Gui

O subdomínio `sites.guiavila.com` (e qualquer domínio em produção) só é repontado para o projeto Astro depois que **todas as páginas migradas** passaram na bateria de testes (#15) E o Gui deu aprovação explícita.

Etapas obrigatórias antes do swap de DNS:
1. Toda página migrada respondendo em `localhost:4321/[slug]` com bateria de testes 100% passando
2. Projeto Astro deployado no Vercel com URL automática (`*.vercel.app`)
3. Gui acessou a URL Vercel e validou todas as páginas críticas
4. Gui dá OK explícito para o swap

**Por quê:** o `sites.guiavila.com` está em produção hoje (Next). Repontar antes da hora derruba páginas que estão funcionando para os usuários do Gui. Decisão do Gui em 06/05/2026.

---

## REGRA INVIOLÁVEL #14 — Rejeição do Gui = aprendizado obrigatório + checklist atualizado

Toda correção que o Gui pede na **revisão final** (após o revisor automático ter aprovado) é tratada como falha de processo do squad responsável e gera 3 ações automáticas:

1. **Registrar em `squads/{squad}/aprendizados.md`** — o erro, por que aconteceu, regra para evitar.
2. **Registrar em `squads/{squad}/agentes/{agente}/aprendizados.md`** — mesmo conteúdo, no nível do agente que executou.
3. **Atualizar o checklist do revisor** — se o erro era detectável por checklist e o revisor passou batido, adicionar item novo no checklist da skill `/revisor-{tipo}` para pegar na próxima vez. Se o erro só era detectável pelo Gui (preferência subjetiva, contexto de marca), registrar como diretriz no `aprendizados.md` do squad com tag `[gosto-do-Gui]`.

**Por quê:** o objetivo é que o Gui pare de pedir as mesmas correções básicas. Se um erro voltar a aparecer depois de já ter sido corrigido uma vez, é sinal de que o aprendizado não foi consolidado — falha grave do processo.

**Quando aplica:** sempre que o Gui rejeitar ou pedir modificação em algo já marcado como "entregue" pelo squad. Pequenas (acento, nome de empresa errado, foto faltando) e grandes (estrutura, ângulo, cor) — todas. Erros básicos contam DOBRADO: se o Gui chama de "básico", o aprendizado vai com tag `[basico]` no início, e o revisor responsável GANHA um item de checklist novo.

---

## REGRA INVIOLÁVEL #13 — Toda skill e todo processo precisam ter fluxo documentado

Toda skill nova criada deve conter uma seção `## Fluxo` com fluxograma ASCII mostrando o que o agente faz em sequência. Todo processo que envolve múltiplos agentes ou squads deve ter um arquivo em `squad/processos/`. Skill sem fluxo documentado está incompleta e não pode ser usada.

**Requisitos obrigatórios para uma skill estar completa:**
1. Seção `## Fluxo` com fluxograma ASCII legível
2. Cada etapa do fluxo identifica o agente responsável
3. Pontos de decisão (bifurcações) explícitos no diagrama

**Para processos multi-squad:**
1. Criar arquivo em `squad/processos/{nome-do-processo}.md`
2. Atualizar `squad/processos/MAPA.md` com a nova entrada
3. O arquivo de processo deve conter: objetivo, fluxo ASCII completo, tabela de skills envolvidas, registro de tarefas

**Por quê:** um squad sem fluxo documentado é uma caixa-preta. Se um agente para ou precisa ser substituído, o processo inteiro trava porque ninguém sabe o que vem antes ou depois. Fluxo documentado garante continuidade, onboarding rápido e rastreabilidade completa.

---

## REGRA INVIOLÁVEL #17 — Skills começam com verbo

Toda skill em `.claude/commands/` deve começar com verbo de ação no infinitivo (`escrever-`, `criar-`, `revisar-`, `publicar-`, `ver-`, `testar-`, `consultar-`, `migrar-`, `atualizar-`, `consolidar-`, `codar-`, etc).

**Exceções:** skills que invocam papel/agente (ex.: `/jade`) podem usar nome próprio.

**Quando criar nova skill:** o nome obrigatoriamente começa com verbo. PR/commit que viola é reprovado.

**Por quê:** padrão verbo-primeiro deixa explícito o que a skill faz no momento da invocação, reduz ambiguidade entre skill (ação) e agente (papel) e mantém o catálogo de comandos navegável quando o squad escala. Decidido pelo Gui em 06/05/2026.

---

## REGRA INVIOLÁVEL #18 — Proibido excluir repositórios, projetos e código legado

**Nem Jade, nem qualquer agente, nem qualquer skill, nem qualquer subagente — NINGUÉM pode excluir, deletar, mover-para-fora-do-projeto ou destruir repositórios, pastas de projetos completas, código legado de produção ou histórico git, sob nenhuma hipótese.**

Inclui (lista não exaustiva):
- Repositório Next em `/Users/guiavila/Documents/Projetos IA Gui Ávila/Sites Gui Ávila/` — **NUNCA excluir**, mesmo após swap DNS pra Astro
- Pasta `app/` dentro do squad — **NUNCA excluir**
- Páginas em `site.guiavila.com` (GoHighLevel antigo) — **NUNCA solicitar exclusão da conta GHL**
- Qualquer projeto Vercel ativo ou inativo
- Qualquer commit, branch, ou tag de qualquer repositório
- Qualquer pasta `excluir-*` (apesar do nome) sem confirmação explícita renovada do Gui no momento da exclusão

**Why:** O Gui foi explícito em 06/05/2026 — "**É muito, muito, muito perigoso. Isso não pode acontecer de jeito nenhum.**" Repos legados são fonte de verdade histórica, podem ter código não documentado, conversões legadas, integrações que ninguém lembra. Exclusão é IRREVERSÍVEL na prática (mesmo com git, restaurar repos completos é caro e arriscado).

**How to apply:**
- Se um agente identificar que um arquivo/repo/projeto "não é mais usado", a ação correta é **DOCUMENTAR** ("este código foi substituído pela versão Astro em X") ou **ARQUIVAR** dentro do próprio projeto (mover pra subpasta `_legado/` ou `99-arquivo/`).
- Comandos proibidos sem aprovação explícita renovada do Gui na hora: `rm -rf <projeto/>`, `rm -rf <repo>`, `vercel project remove`, `gh repo delete`, `git branch -D <branch-com-trabalho>`, qualquer destruição de uma pasta de projeto inteira.
- Renomear é OK se reversível (`git mv`), apagar não é.
- Após swap DNS de `sites.guiavila.com` pra Astro: o repo Next continua existindo, intacto, indefinidamente. Só desabilitar o deploy automático. **Nunca remover o projeto Vercel do Next, nunca apagar o repo.**
- Se um briefing futuro pedir exclusão e essa regra não for citada explicitamente pelo Gui no momento, RECUSAR e perguntar.

---

## REGRA INVIOLÁVEL #19 — Toda correção do Gui propaga em 4 lugares automaticamente

**Toda correção/rejeição/feedback do Gui — em copy, página, design, output, comportamento, ou qualquer entrega já marcada como "entregue" — dispara automaticamente, sem o Gui precisar pedir, 4 ações pelo squad:**

1. **Skill de quem PRODUZIU** é atualizada com o novo padrão (pra nunca produzir errado de novo). Linguagem prescritiva: "Sempre faça X. Nunca faça Y."
2. **Skill de quem REVISOU** é atualizada com novo item de checklist (pra nunca passar batido de novo). Com exemplo de approve/reject quando aplicável.
3. **Memória persistente** do squad é atualizada em `~/.claude/projects/.../memory/feedback_*.md` + entrada nova no `MEMORY.md` index (pra a regra sobreviver a sessões novas).
4. **Retrofit nos outputs existentes** — todas as entregas em produção (e em local) que tenham o mesmo problema são corrigidas. Ferramentas: `grep -rn`, `find`, audit manual.

**Citação literal do Gui (06/05/2026 ~21h):**
> "Sempre que eu te mandar alguma correção de copy, de página, alguma coisa, eu nunca quero ficar pedindo pra você atualizar as skills. Sempre atualize a skill de quem fez, pra isso nunca mais acontecer, e também a skill de quem revisa, pra isso nunca mais passar batido. Isso tem que ser uma regra de ouro. (...) Eu quero que você coloque isso até no claude.md, como regra fundamental e principal da Jade."

**Checklist obrigatório da Jade ao receber qualquer correção:**
- [ ] Identifiquei a skill que produziu o output errado
- [ ] Identifiquei a skill que revisou e deixou passar
- [ ] Atualizei skill do produtor com novo padrão (linguagem prescritiva: "Sempre faça X. Nunca faça Y.")
- [ ] Atualizei skill do revisor com novo item de checklist (com exemplo de approve/reject)
- [ ] Salvei memória persistente em `~/.claude/projects/-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila/memory/feedback_*.md`
- [ ] Adicionei entrada de aprendizado em `squads/{squad}/aprendizados.md` E em `squads/{squad}/agentes/{agente}/aprendizados.md`
- [ ] Identifiquei TODOS os outputs em produção/local com o mesmo problema (grep, find, audit)
- [ ] Apliquei o fix em cada output existente
- [ ] Atualizei `MEMORY.md` index com o novo arquivo de memória
- [ ] Confirmei pro Gui o que foi feito + onde

**Por quê:** o objetivo é que o Gui pare de ser professor do squad. Se ele corrige duas vezes a mesma coisa, é falha grave de processo da Jade. Sem isso o squad fica burro: produz, é corrigido, esquece, reproduz o mesmo erro. Inteligência cumulativa é o que diferencia squad de IA de "ChatGPT no chat".

**Relação com Regra #14:** a #14 fala em "rejeição na revisão final = aprendizado + checklist". A #19 generaliza e expande pra QUALQUER correção (não só rejeição formal) e adiciona retrofit + skill do produtor + memória persistente. Quando #14 e #19 entram em conflito, #19 prevalece (é o superset).

**How to apply:**
- Ao receber correção → 4 ações ANTES de seguir pra próxima coisa.
- Despachar squad-dev pra fazer as 4 ações em paralelo é OK (Jade orquestra).
- "Skill do produtor" = a `.claude/commands/X.md` que produziu o output (ex: copy errada → `/escrever-pagina`; código errado → `/codar-pagina`; carrossel errado → `/criar-carrossel`).
- "Skill do revisor" = a skill que revisou e aprovou (ex: `/revisar-pagina`, `/revisar-codigo-pagina`, `/revisar-carrossel`).
- Se a skill de revisão não existir, é sinal de que precisa criar antes — registra como pendência.
