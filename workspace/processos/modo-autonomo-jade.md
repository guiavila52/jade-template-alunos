# Modo Autônomo da Jade — como funciona

> Documento canônico do mecanismo de autonomia da Jade quando o Gui está ausente.
> Criado 10/05/2026 noite | Atualizado a cada otimização.

## A verdade técnica fundamental

**Claude Code é REATIVO por design.** Eu não tenho "loop em background" rodando sozinha. Eu só processo quando recebo um TURNO — seja do Gui, de um wake-up agendado, ou de notificação de subagent.

Autonomia da Jade = **combinar 4 mecanismos** que criam turnos artificiais sem o Gui presente.

---

## Mapa visual — 4 mecanismos de autonomia

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│   GUI MANDA MENSAGEM (turno orgânico)                                │
│         │                                                             │
│         ▼                                                             │
│   ┌──────────┐                                                       │
│   │   JADE   │  (sessão Claude Code ativa)                           │
│   └──────────┘                                                       │
│         │                                                             │
│         ├─────────────────────────────────┐                         │
│         │                                  │                         │
│         ▼                                  ▼                         │
│  ┌──────────────┐                  ┌──────────────┐                  │
│  │  EXECUTA     │                  │  DESPACHA    │                  │
│  │  (Bash,Edit, │                  │  SUBAGENT    │                  │
│  │   Write etc) │                  │  (background)│                  │
│  └──────────────┘                  └──────────────┘                  │
│         │                                  │                         │
│         └────────────┬─────────────────────┘                         │
│                      │                                                │
│                      ▼                                                │
│              ┌───────────────┐                                       │
│              │ JADE RESPONDE │  ← fim do turno                       │
│              └───────────────┘                                       │
│                      │                                                │
│                      ▼                                                │
│              ┌───────────────┐                                       │
│              │  GUI AUSENTE  │  ← problema: sem turno = Jade parada  │
│              └───────────────┘                                       │
│                                                                       │
│   ═══════════════════════════════════════════════════════════════    │
│                                                                       │
│   SOLUÇÃO: criar turnos artificiais via 4 mecanismos                 │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Os 4 mecanismos

### Mecanismo 1 — Subagents em background

```
┌─────────────────┐     dispatch         ┌────────────────┐
│      JADE       │  ─────────────────▶  │ SUBAGENT BG    │
│  (thread main)  │                       │ (paginas-dev)  │
└─────────────────┘                       └────────────────┘
        │                                          │
        │  continua respondendo                    │  trabalha sozinho
        │  novos turnos do Gui                     │  até concluir
        │                                          │
        │   ◀─────── notificação completion ───────┘
        ▼
   integra resultado
```

**Quando usar:** trabalho longo paralelo (codar página, gerar carrossel, etc) enquanto Gui ainda está presente.

**Limites:**
- ~30min timeout antes de subagent travar
- Cada subagent = 1 sessão Claude separada (consome quota)
- Subagent não pode despachar outro subagent (limite atual)

### Mecanismo 2 — ScheduleWakeup (dynamic loop)

```
Gui sai (sem mais turnos) ──▶ JADE agenda wake-up: "me acorde em 25min"
                                            │
                                            ▼
                                  ⏱ ─ ─ ─ 25min ─ ─ ─ ▶
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │ JADE acorda      │
                                  │ (turno artificial)│
                                  └──────────────────┘
                                            │
                                            ▼
                                  ataca próxima Onda
                                            │
                                            ▼
                                  ScheduleWakeup de novo
                                  (loop até quota/Caqui)
```

**Quando usar:** sessão atual em andamento + Gui acabou de sair. Mecanismo IMEDIATO.

**Limites:**
- Sessão fica em "pause" mas alocada — cada wake-up consome contexto + quota
- Só dura enquanto a sessão Claude estiver alocada (~24h limite Anthropic)
- Não atravessa `/clear` ou compactação forçada

### Mecanismo 3 — `/loop` (auto-pace)

```
Gui invoca: /loop /atacar-pendencias
                │
                ▼
   ┌─────────────────────────┐
   │ JADE roda /atacar-..    │
   │ Decide próximo intervalo│
   └─────────────────────────┘
                │
        re-agenda automático
                │
                ▼
        executa de novo
        (até skill terminar OU Gui interromper)
```

**Quando usar:** babá de processo (checar deploy, polling status). Ou autopilot em sessão ativa.

**Limites:** mesmo da ScheduleWakeup (sessão precisa ficar alocada).

### Mecanismo 4 — `/schedule` (Anthropic Routines remote cron) ⭐ MAIS PODEROSO

```
Gui (ou Jade) cria routine:
  "weekdays 08:00 BRT → /rotina-gui-ausente"
                │
                ▼
   ┌──────────────────────────────┐
   │ Anthropic Cloud (infra)      │
   │  - Cron interno              │
   │  - Mac do Gui pode estar OFF │
   └──────────────────────────────┘
                │
   toda manhã 8h:
                ▼
   ┌──────────────────────────────┐
   │ Sessão Claude NOVA disparada │
   │ Executa /rotina-gui-ausente  │
   │ Trabalha até Caqui           │
   │ Notifica Gui (Telegram)      │
   └──────────────────────────────┘
                │
                ▼
   Gui acorda com trabalho entregue
```

**Quando usar:** TUDO recorrente. Rotina diária matinal, varredura semanal de tráfego, etc.

**Limites:**
- Cada execução conta na quota
- Routine não tem memória entre execuções (precisa ler estado de arquivo)
- Precisa ser pensada como "função pura" — entra, executa, sai

---

## Matriz de decisão — qual mecanismo usar

| Cenário | Mecanismo |
|---|---|
| Despachar 1 tarefa longa enquanto Gui ainda tá | **Subagent BG** |
| Gui acabou de sair, atacar fila imediato | **ScheduleWakeup** |
| Polling de status (deploy, build) | **`/loop`** |
| Rotina diária recorrente | **`/schedule`** |
| Resposta a evento externo (webhook Telegram, etc) | **Hook custom** (futuro) |

## Combinação ideal pro caso {{NOME_OPERADOR}}

```
                    JADE AUTÔNOMA
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   /schedule          ScheduleWakeup    Subagents BG
   (cron remoto)     (dynamic loop)    (paralelo)
        │                 │                 │
        │                 │                 │
   ┌────▼─────┐      ┌────▼────┐       ┌───▼────┐
   │ Diário   │      │ Imediato│       │ Tarefa │
   │ Semanal  │      │ Ad hoc  │       │ pesada │
   │ Backups  │      │ Wake-up │       │ Single │
   │ Reports  │      │ Loops   │       │ shot   │
   └──────────┘      └─────────┘       └────────┘
        │
        └──▶ resultado entregue via Telegram bot (quando ativo)
                 ou email
                 ou notif macOS
                 ou append em PROGRESS.md
```

## Estado atual de cada mecanismo (10/05/2026)

| Mecanismo | Status | Onda relacionada |
|---|---|---|
| Subagents BG | ✅ ATIVO (usado hoje) | — |
| ScheduleWakeup | ✅ ATIVO (usado hoje pela 1ª vez) | — |
| `/loop` | ⚠️ Disponível mas não testado | — |
| `/schedule` Anthropic Routines | ⚠️ Spec registrada, sem implementação | **Onda 7** |
| Webhook Telegram (push) | ⏸️ Aguarda Onda 5 | **Onda 5** |

## Plano de evolução (otimização contínua)

### Fase 1 — Já implementado (10/05/2026)
- Subagents BG funcionais
- ScheduleWakeup testado
- M1-M5 melhorias estruturais da `/rotina-gui-ausente`
- Health-check pré-execução (M2)
- Checkpoint resumability (M1)
- Priorização caminho crítico (M3)
- Hooks contextuais JADE_CONTEXT (M4)
- Dashboard performance jade (M5)

### Fase 2 — Próxima sessão (Imersão 14/05)
- **Onda 7-A:** criar `/varrer-squads` (skill autônoma que detecta pendências + ataca)
- **Onda 7-C/D/E:** routines via `/schedule` (matinal 8h, semanal seg 9h, backup diário 22h)
- **Onda 5:** bot Telegram pro Gui (destino dos relatórios das routines)

### Fase 3 — Pós-Imersão
- Métricas de performance da Jade (consumo de quota, taxa de Caqui completo, top subagents)
- Routine pra auditar qualidade das próprias entregas
- Routine pra propor melhorias estruturais baseado em padrões detectados

### Fase 4 — Visão de longo prazo
- Jade lê próprios aprendizados e refatora skills automaticamente
- Sistema de prioridade dinâmica baseado em ROI (impacto / quota gasta)
- Multi-routine paralelas (3-4 routines diferentes em horários complementares)

## Como Gui vai usar isso na prática

**Diário (com /schedule ativa):**
- 8h: routine matinal varre pendências, ataca o que dá autônomo, manda relatório Telegram
- 22h: routine backup salva estado dos 3 repos + checkpoint
- Seg 9h: routine semanal gera /relatar-trafego + ranking criativos

**Ad hoc (sessão ativa):**
- Gui chega, manda demanda
- Jade despacha subagent BG pra coisa pesada
- Gui pode sair durante a sessão → ScheduleWakeup mantém workflow andando

**Pré-Imersão (mostrar pros alunos):**
- "Olha, minha COO acorda mais cedo que eu e ataca a lista de pendências sozinha"
- Mostra dashboard de performance acumulada
- Mostra relatório que veio no Telegram

## Restrições e limites honestos

- **Quota não é infinita.** Cada wake-up/subagent/routine consome plano Max/Pro. Sem cuidado, queima quota em 1 dia.
- **Subagents podem timeoutar.** Já vimos 4 timeouts nesta sessão. Regra #22 (confiabilidade) ajuda mas não elimina.
- **Sem ação fora de sessão Claude.** Web scraping, gerar vídeo no Final Cut, mexer em conta bancária — Jade NÃO faz. Precisa de integração externa (n8n, Make, Zapier, etc).
- **Memória sobrevive a sessão, mas não a `/clear`.** Por isso `/preparar-clear-jade` é crítico.

## Próximas otimizações (a estudar)

- [ ] Hook PostToolUse pra registrar métricas de cada tool call → dashboard M5
- [ ] Mecanismo de "freshness" — memórias velhas (>90 dias) viram candidatas a auditoria
- [ ] Routine semanal que audita todas as memórias e atualiza descrições
- [ ] Categoria nova em /check-up-estrutura: "Skills sem TimeBox declarado"
- [ ] Sistema de orçamento de quota por Onda

## Como contribuir com este documento

Este arquivo é vivo. Toda vez que:
- Um mecanismo novo é descoberto/criado
- Uma otimização funciona melhor que outra
- Um limite novo é detectado
- O Gui dá feedback sobre comportamento autônomo

→ atualizar este documento + linkar em CLAUDE.md.

## Memórias correlatas

- `feedback_nao_perguntar_obvio.md` — Jade decide blindagem sem perguntar
- `feedback_confiabilidade_skills.md` — Regra #22
- `feedback_registrar_pendencia_antes_de_executar.md` — Regra #11/#12 reforçada
- `feedback_comunicacao_uma_coisa_por_vez.md` — output da Jade pro Gui

## Skills correlatas

- `/rotina-gui-ausente` — execução autônoma multi-tarefa
- `/preparar-clear-jade` — handoff entre sessões
- `/varrer-squads` (a criar — Onda 7-A)
- `/check-up-estrutura` — auditoria contínua

---

**Última atualização:** 10/05/2026 noite | Próxima revisão: pós-Imersão 14/05
