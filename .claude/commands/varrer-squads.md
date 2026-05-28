---
name: varrer-squads
description: Skill autônoma que varre workspace/memory/pendencias.md, detecta Ondas atacáveis sem dependência do {{NOME_OPERADOR_CURTO}} ou APIs externas, prioriza por caminho crítico (Regra M3), executa via Jade direta ou subagents, e gera relatório de progresso. Disparada por /rotina-autonoma OU /schedule cron.
model: claude-opus-4-5
---

<!-- Modelo recomendado: claude-opus-4-5 (decisão estratégica de priorização) -->

## Propósito

Skill autônoma que faz Jade trabalhar SOZINHA enquanto {{NOME_OPERADOR_CURTO}} está fora. Diferente de `/rotina-autonoma` (rotina manual com {{NOME_OPERADOR_CURTO}} presente no início), esta é otimizada pra ser disparada por cron (`/schedule`) ou wake-up — gera plano + executa + reporta + reagenda.

## Memórias relevantes (ler antes)

1. `~/.claude/projects/.../memory/feedback_nao_perguntar_obvio.md` — Jade decide blindagem
2. `~/.claude/.../memory/feedback_confiabilidade_skills.md` — Regra #22
3. `~/.claude/.../memory/project_foco_carrossel_youtube_e_meta_ads.md` — foco macro
4. `workspace/processos/modo-autonomo-jade.md` — 4 mecanismos de autonomia

## Quando usar

- **Cron diário** via `/schedule` (ex: matinal 8h BRT)
- **Wake-up** dentro de rotina autônoma longa
- **Disparada por {{NOME_OPERADOR_CURTO}}** quando quer ver "o que tem pra fazer agora"

NÃO usar quando {{NOME_OPERADOR_CURTO}} está ativo na sessão (use `/rotina-autonoma` que tem mais etapas).

## Fluxo

```
[ Trigger: /varrer-squads ou cron ]
        ↓
[ 0. Setup ]
   export JADE_CONTEXT=rotina-autonoma
   log: workspace/output/varreduras/{stamp}-varredura.md
        ↓
[ 1. Health-check (M2) ]
   disco / internet / APIs externas / git status / hooks
        ↓
[ 2. Ler pendencias.md ]
   grep "## ONDA" — listar Ondas
   pra cada Onda: status (📋/🚧/✅/❌), bloqueado-por, urgente, deadline
        ↓
[ 3. Filtrar Ondas atacáveis ]
   - Status 📋 ou 🚧 (não ✅, não bloqueada)
   - Sem dependência de {{NOME_OPERADOR_CURTO}} (não "Aguarda {{NOME_OPERADOR_CURTO}}...", "Bloqueado pelo {{NOME_OPERADOR_CURTO}}...")
   - Sem dependência de API externa down (consultando health-check)
        ↓
[ 4. Priorizar por caminho crítico (M3) ]
   1º: 🚨 URGENTE
   2º: Deadline < 7 dias
   3º: Bloqueia mais Ondas (cascata)
   4º: Resto FIFO
        ↓
[ 5. Pra cada Onda atacável (até timebox 30min ou 3 Ondas) ]
   a) Atualizar pendencias.md: 🚧 em curso + timestamp
   b) Executar:
      - Trabalho meta (skill update, doc, memória) → Jade direta via Bash
      - Trabalho de produto (copy, código, design) → despachar subagent
   c) Validar output
   d) Atualizar pendencias.md: ✅ entregue + sumário
   e) Commit + push (squad-empresa, sites-astro)
        ↓
[ 6. Gerar relatório ]
   workspace/output/varreduras/{stamp}-varredura.md:
   - Ondas atacadas (✅/🚧/❌)
   - Quota estimada consumida
   - Próximas Ondas atacáveis no próximo ciclo
   - Bloqueios novos detectados (precisam {{NOME_OPERADOR_CURTO}})
        ↓
[ 7. Atualizar dashboard performance Jade (M5) ]
   workspace/output/metricas/jade-performance.md
        ↓
[ 8. Notif macOS (se aplicável) ou append em PROGRESS.md ]
        ↓
[ 9. Re-agendar próximo wake-up (se loop autônomo) ]
   ScheduleWakeup +3600s (1h)
   OR /schedule cron next firing
        ↓
   ⟶ FIM
```

## Critérios de "Onda atacável autônoma"

✅ Pode atacar SEM {{NOME_OPERADOR_CURTO}}:
- Atualizar skills/regras/memórias
- Refatorar docs
- Criar skills novas (com spec clara)
- Polimento (MAPAs, indexar memórias órfãs, aprendizados)
- Trabalho local (sem precisar API externa down)
- Implementar fix de bug conhecido
- Commit + push

❌ NÃO ataca autônomo:
- Decisão estratégica (ângulo, posicionamento)
- Aprovação de output final
- Decisão de produto (preço, escopo, nome)
- Input externo (chave API nova, conta de terceiro)
- Trabalho que precisa {{NOME_OPERADOR_CURTO}} gravar/produzir (clipes "outro", apontar bugs)
- Deploy production (requer triple-check + {{NOME_OPERADOR_CURTO}} aprovar quando possível)

## Comandos auxiliares (executados pela skill)

```bash
# 1. Listar Ondas no pendencias
grep -nE "^## .*ONDA " workspace/memory/pendencias.md

# 2. Status de cada Onda
for n in $(grep -oE "ONDA [0-9]+" workspace/memory/pendencias.md | sort -u); do
  echo "$n:"
  grep -A 30 "^## .*$n " workspace/memory/pendencias.md | grep -E "Status|status|✅|🚧|📋|❌" | head -3
done

# 3. Bloqueio detectado?
grep -B 1 -A 5 "Aguarda {{NOME_OPERADOR_CURTO}}\|Bloqueado pelo {{NOME_OPERADOR_CURTO}}\|Bloqueio:" workspace/memory/pendencias.md

# 4. Commit padrão da varredura
git add <arquivos específicos>
git commit -m "feat(squad): varredura autônoma Onda X — [sumário]"
git push origin main
```

## Restrições

- **Regra #11/#12** — TODA Onda atacada vai pra pendencias.md ANTES com status 🚧
- **Regra #19** — TODA correção propaga 4 lugares (skill produtor + revisor + memória + retrofit)
- **Regra #22** — comandos externos com timeout + stderr + exit code
- **Regra #23** — triple-check obrigatório antes de deploy production
- **Regra #8** — edição em `.claude/` via Bash/Python
- **Regra #18** — backup `.preFix-onda<N>` antes de modificar

## Captura de aprendizado (Regra #19)

A cada varredura, registra em `squads/gestao/aprendizados.md`:
```
### YYYY-MM-DD HH:MM — Varredura autônoma
**Ondas atacadas:** [lista]
**O que funcionou:** [padrão]
**O que travou:** [bloqueios]
**Próxima vez:** [ajuste]
```

## Triple-check da própria skill

Validação interna antes de marcar Onda como ✅:
- [ ] Output gerado existe + tem conteúdo válido
- [ ] Commit push OK
- [ ] Pendencias.md atualizado (status correto)
- [ ] MEMORY.md indexa novas memórias se houver
- [ ] CLAUDE.md atualizado se houver mudança estrutural

Se qualquer falhar: marca Onda como 🚧 (não ✅) + registra bloqueio + segue.

## Output canônico

```
workspace/output/varreduras/YYYY-MM-DD-HHMM-varredura.md
├── Health-check inicial
├── Ondas listadas + status
├── Plano priorizado (caminho crítico)
├── Execução (Ondas atacadas)
├── Bloqueios detectados (precisam {{NOME_OPERADOR_CURTO}})
├── Quota estimada
└── Próxima ação (re-agendar / aguardar {{NOME_OPERADOR_CURTO}})
```

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{NOME_OPERADOR_CURTO}} testar — testa antes.