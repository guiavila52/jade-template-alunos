---
name: rotina-gui-ausente
description: Rotina autonoma do squad enquanto Gui esta fora — pre-flight, priorizacao, execucao, triple-check, bateria, commits, aprendizados.
type: skill
---

# /rotina-gui-ausente — rotina autônoma do squad-empresa

> Consolidada em 10/05/2026 — esta é a ÚNICA skill de rotina autônoma agora. Versão genérica user-level movida pra `.legado-onda16` (Regra #18).

Você (Jade) vai executar a rotina autônoma completa do squad enquanto o Gui está fora. Volta com a palavra-chave **Caqui** quando estiver tudo redondo + testado + auditado + commitado + deployado.

## Regras invioláveis (não pode esquecer)
- NUNCA pare pra perguntar — tome decisão técnica sozinha + registre raciocínio
- Atualize `PROGRESS.md` + `workspace/memory/pendencias.md` + memórias persistentes A CADA item concluído
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
1. `AGENTS.md` (todas as Regras Invioláveis #1-#22)
2. `~/.claude/projects/.../memory/MEMORY.md` (todas memórias persistentes)
3. `workspace/memory/pendencias.md` (estado atual)
4. `squads/dev/tarefas.md` (tail 100 linhas — tarefas ativas/recentes)
5. `git status` nos 3 repos (squad-empresa, sites-astro, App Reverso)

Sem isso, vai despachar com regra desatualizada.

### Pre-flight de SECRETS (Regra Inviolável #21)

ANTES de qualquer despacho que envolva criar/editar arquivo de config, secret, key, token, credential ou API key:

1. `find . -name '.env*' -not -path '*/node_modules/*' -not -path '*/.git/*'` no projeto — listar `.env*` existentes
2. Conferir memórias: `feedback_secrets_em_env_local.md` + `feedback_consultar_protocolo_antes_de_criar_secret.md` + `feedback_abrir_env_textedit_para_keys.md`
3. **Path canônico ÚNICO do squad-empresa: `app/.env.local`** — toda nova key entra aí, com placeholder em `app/.env.example`
4. Se Gui precisa colar nova key: rodar `open -a TextEdit "<path>/app/.env.local"` automaticamente (Persistence já desativada — não vai pedir versão)
5. NUNCA criar arquivo de secret em path novo (`~/.{tool}/`, `/tmp/`, etc) sem aprovar com Gui

Sem esse pre-flight, risco de repetir o erro `~/.openrouter/key` (08/05/2026).

### Pre-flight de PENDÊNCIAS (Regra Inviolável #11/#12 reforçada — 10/05/2026)

ANTES de executar QUALQUER demanda (mesmo pequena):

1. Demanda do Gui chegou → **REGISTRAR em `workspace/memory/pendencias.md` ANTES de fazer qualquer coisa**
2. Sem exceção pra "demanda pequena", "trabalho meta", "só atualização" — TUDO vai pra fila primeiro
3. Status inicial: `🚧 em curso`; ao final: `✅ entregue` com sumário
4. Ler memória `feedback_registrar_pendencia_antes_de_executar.md` se em dúvida
5. **Hook ativo:** `.claude/hooks/check-pendencia-antes-trabalho-estrutural.sh` dispara em Write/Edit/Bash em paths estruturais (`.claude/`, `squads/`, `AGENTS.md`, `CLAUDE.md`, `MEMORY.md`) — recebe lembrete automático se esquecer

Violação = "trabalho invisível" que não deixa rastro pra próximo turno retomar.

### Pre-flight de CONFIABILIDADE (Regra Inviolável #22 — 10/05/2026)

ANTES de despachar agent ou rodar comando externo:

1. Toda skill que executa Playwright, ffmpeg, yt-dlp, curl, API call → confiabilidade obrigatória (timeout + stderr + exit code + retry + graceful degradation)
2. Bugs conhecidos hoje: `tweet-imagem.mjs` trava silenciosamente (Onda 9 ataca)
3. Se subagent timeoutar / travar > 30min: **NÃO só skip** — diagnosticar causa (logs + stderr), aplicar fallback Bash direto (mesma estratégia das Ondas anteriores), registrar como aprendizado da Jade

Ler memória `feedback_confiabilidade_skills.md` se em dúvida.

## Atualização de memória + pendências (OBRIGATÓRIO a cada item)

A cada item do checklist concluído:
- `workspace/memory/pendencias.md` → mudança de status
- `~/.claude/.../memory/feedback_*.md` (criar/atualizar se aprendizado novo)
- `MEMORY.md` (auto-memory) → indexar nova memória se houver
- `PROGRESS.md` → estado atual

Se travar a qualquer momento, tudo fica organizado pro próximo turno retomar.

## Antes de despachar — checar conflito de arquivo (memória `feedback_nao_paralelizar_mesmo_arquivo.md`)

NUNCA 2+ agents simultâneos no mesmo arquivo. Antes de despachar:
1. `grep "Status:.*em curso" squads/dev/tarefas.md`
2. Conferir se algum mexe no arquivo X
3. Se sim → ENFILEIRAR

## Etapa 0.5 — HEALTH-CHECKS PRÉ-EXECUÇÃO (M2 — sem isso, queima quota sem fazer nada útil)

ANTES de qualquer outra coisa, validar:

```bash
# 1. Disco — pelo menos 5GB livre
df -h ~ | awk 'NR==2 {gsub("G",""); if ($4 < 5) print "FAIL_DISK"; else print "OK_DISK"}'

# 2. Internet básico
curl -s --max-time 5 -o /dev/null -w "%{http_code}" https://api.anthropic.com/ || echo "FAIL_NET"

# 3. APIs externas críticas (health-check leve, GET de domínio)
for api in "https://{{PLATAFORMA_NF_URL}}" "https://{{BANCO_PJ_API_URL}}" "https://graph.facebook.com"; do
  code=$(curl -s --max-time 5 -o /dev/null -w "%{http_code}" "$api")
  echo "$api → $code"
done

# 4. Git working trees — quais repos têm mudanças não-commitadas?
for repo in "Squad Empresa {{NOME_OPERADOR}}" "Páginas Astro {{NOME_OPERADOR}}" "App Reverso"; do
  cd "/Users/guiavila/Documents/Projetos IA {{NOME_OPERADOR}}/$repo" 2>/dev/null &&     echo "$repo: $(git status --short | wc -l | tr -d ' ') arquivos não-commitados"
done

# 5. Hooks ativos
ls .claude/hooks/*.sh 2>/dev/null | wc -l

# 6. Quota Anthropic? (não há API pra isso; estimar por contexto da sessão atual)
```

**Decisão baseada em health-check:**
- Disco < 5GB → STOP, registra como bloqueio crítico, notifica Gui
- Internet down → STOP, registra, notifica
- API externa down → REGISTRAR em PROGRESS.md "skip tarefas que dependem de [API]" + continuar com tarefas independentes
- Working tree dirty → DECIDIR: commitar o que existe agora antes de começar, OU isolar trabalho da rotina em arquivos novos

**Setar JADE_CONTEXT pra suprimir hooks durante rotina:**
```bash
export JADE_CONTEXT=rotina-autonoma
```

---

## Etapa 0.7 — PRIORIZAÇÃO POR CAMINHO CRÍTICO (M3 — dependências importam)

Em `workspace/memory/pendencias.md`, cada Onda pode declarar:
```
**Bloqueia:** Onda X, Y, Z
**Bloqueado por:** Onda A, B
**Deadline:** YYYY-MM-DD (se aplicável)
**Urgente:** 🚨 SIM/NÃO
```

**Algoritmo de priorização:**
1. Construir grafo: Ondas como nodes, "Bloqueia" como arestas
2. Calcular caminho crítico: Onda que destrava MAIS outras = prioridade 1
3. Ondas com `Deadline próximo` (< 7 dias) sobem na fila
4. Ondas marcadas `🚨 URGENTE` no topo absoluto
5. Ondas `Bloqueado por: X` só atacam quando X = ✅

**Exemplo concreto (10/05/2026):**
- Onda 9 (fix carrossel) bloqueia 10.1 → ataca primeiro
- Onda 10.6 (MCP Meta) bloqueia 10.7, 10.8 → ataca segundo
- Onda 10.9 URGENTE (cortar-youtube) → top da fila
- Onda 11/12 sem dependências = baixa prioridade

---

## Etapa 0.9 — CHECKPOINT INICIAL (M1 — resumability se crashar)

```bash
TIMESTAMP=$(date -u +"%Y-%m-%d-%H%M")
CHECKPOINT="workspace/output/rotinas-autonomas/${TIMESTAMP}-checkpoint.json"

cat > "$CHECKPOINT" <<JSON
{
  "rotina_id": "${TIMESTAMP}",
  "iniciada_em": "$(date -u -Iseconds)",
  "ondas_em_curso": [],
  "ondas_concluidas": [],
  "ondas_bloqueadas": [],
  "tool_uses_acumulados": 0,
  "ultimo_check_em": "$(date -u -Iseconds)",
  "next_action": "iniciar etapa 1"
}
JSON
```

**A cada tarefa concluída na etapa 3:** atualizar `checkpoint.json` com `ondas_concluidas[].push(X)` + `ultimo_check_em` + `next_action`.

**Se rotina invocada e checkpoint existe < 24h:** OFERECER retomada antes de iniciar nova. Próxima Jade lê checkpoint, identifica ondas em curso, retoma de `next_action`.

---

## Etapas

**0. Setup**
- Criar log `workspace/output/rotinas-autonomas/{YYYY-MM-DD-HHMM}-rotina-autonoma.md`
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
Roda a skill (16 categorias: A-N). Esperado: 0 findings CRITICAL/HIGH. Se houver: atacar caso a caso conforme regras desta skill.

**7. Auditoria de segurança contextual**
Detecta se mudou squad-empresa / sites-astro / App Reverso e roda auditoria adequada:
- Squad/Astro só: leve (5-10min) — secrets, .env, headers, GTM, Astro nativo
- {{Plataforma_Conteudo}}: `/security-audit` completa (overnight)
- Ambos: leve + completa
Resolver CRITICAL/HIGH antes de prosseguir.

**8. Commit + push 3 repos**
- `squad-empresa` privado: narrativa do que mudou na estrutura
- `sites-astro` privado: narrativa das páginas deployadas
- `squad-template` público: rodar `/publicar-jade` se houver mudanças relevantes pros alunos. Auditar diff por PII antes de mergear/abrir.

`git add` por arquivos específicos (NUNCA `add .` cego). Mensagem narrativa do PORQUÊ. Validar `git status` limpo.

**9. Aprendizados em 3 camadas (Regra Inviolável #19 + alinhado com `/preparar-clear-jade`)**

Varre TODA a rotina autônoma atrás de correções/lições. Registra em CADA camada que aplica:

- **Camada SQUAD** → `squads/{squad}/aprendizados.md` (padrões do squad inteiro)
- **Camada AGENTE** → `squads/{squad}/agentes/{agente}/aprendizados.md` (lições específicas)
- **Camada JADE** → `squads/gestao/aprendizados.md` (orquestração: padrões de briefing, decisões autonomas, erros de processo)

Template aprendizado em `/preparar-clear-jade` passo 4.

**10. Relatório final + Caqui**
Em `PROGRESS.md` final:
- Concluído: lista
- Bloqueado: lista (precisa Gui)
- Decisões técnicas tomadas + raciocínio
- Resultado dos testes
- Resultado das auditorias
- Status dos commits
- Aprendizados registrados (Squad: X. Agentes: Y. Jade: Z)
- Path do log estruturado

Notificar macOS: `osascript -e 'display notification "Caqui — squad pronto" with title "Jade — Squad" sound name "Glass"'`

Encerrar com: **Caqui** (se 100% redondo) OU **Caqui parcial** + lista de bloqueios (se houve algum item que dependeu do Gui).

## Detecção de loop / 529 / timeout (Regra Inviolável #22 — confiabilidade)

- **Tarefa sem progresso > 30min:** NÃO só skip. Diagnosticar:
  1. Capturar stderr do subagent
  2. Identificar causa raiz (timeout? API down? bug?)
  3. **Fallback Bash:** se trabalho era de skill conhecida (skill update, file edit), Jade faz direto via Bash/Python (Regra #8)
  4. Registrar como aprendizado da Jade
- **Subagent caiu com 529 Overloaded:** re-despachar até 3x com backoff (60s → 180s → 600s)
- **3+ falhas seguidas:** pular item + registrar bloqueio + relatar — NUNCA fingir que entregou
- **Travamento de comando externo (Playwright, ffmpeg, etc):** ver memória `feedback_confiabilidade_skills.md` — toda skill com command externo deve ter timeout explícito. Se não tem, registra como gap na Onda 9.

## Fluxo

```
[ Gui ausente chama /rotina-gui-ausente-do-squad ]
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
   ↓ (decisão técnica)         (só Gui)   ↓
   decide + registra           bloqueado + segue
   └──────────────┬───────────────────────┘
        ↓
[ 4. Triple-check ] — paginas + paginas-dev + bug-hunter (todos aprovam)
        ↓
[ 5. Bateria pós-deploy ] — 10 páginas + smoke FUNCIONAL Playwright
        ↓
[ 6. /check-up-estrutura ] — 16 categorias; 0 CRITICAL/HIGH
        ↓
[ 7. Auditoria contextual ] — leve / completa / ambas conforme escopo
        ↓
[ 8. Commit + push 3 repos ] — narrativo, sem add cego
        ↓
[ 9. Aprendizados em 3 camadas ] — Squad + Agente + Jade (Regra #19)
        ↓
[ 10. Relatório + Caqui ]
        ↓
   ⟶ notif macOS + palavra-chave **Caqui** 🍑
```

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro Gui testar — testa antes.


---

## Regra de autonomia (12/05/2026 — adicionada após incidente Caqui parcial)

**ANTES de declarar Caqui parcial, esgotar todas as Ondas autônomas atacáveis.**

Jade só declara Caqui parcial quando os bloqueios pendentes caem em UMA destas 5 categorias REAIS:

1. **Disparo público irreversível** (email pra lista, post publicado, anúncio Meta no ar)
2. **Deploy em produção** (`vercel --prod`)
3. **Inputs externos físicos** (chave API nova, autorização Meta/Google, conta nova em terceiro)
4. **Decisão estratégica REAL entre opções diferentes** (preço, escopo, lançamento, branding)
5. **Aprovação de copy final pública** (última conferência antes de virar conteúdo de marca)

**Antes de declarar Caqui parcial, perguntar internamente:**

- O item bloqueado cai em UMA das 5 categorias acima? Se NÃO → tem ação autônoma possível, continuar.
- "Esperar revisão Gui" antes do trabalho NEM TER SIDO produzido = falso bloqueio. Despacha produção, junta tudo pra revisão consolidada depois.
- "Sessão paralela não respondeu" = assíncrono via ClickUp, ataca outras Ondas.
- "Mandar arquivo X pra Gui" não trava produção atual.

**Padrão correto: pipeline com gates**

```
Estratégia (autônomo) → Currículo (autônomo) → Copy (autônomo)
  → Implementação (autônomo) → Build + smoke (autônomo)
  → ⛔ GATE Gui aprova disparo/deploy → Caqui completo
```

**Cross-reference:** `feedback_matriz_autonomia_jade.md`, AGENTS.md Regra #13.
