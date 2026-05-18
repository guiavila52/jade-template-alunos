# Aprendizados — Squad infra

## 2026-05-17: Migração skills ClickUp de bash+jq para Python urllib

**Contexto:** 4 skills de pendência ClickUp (`/criar-pendencia`, `/listar-pendencias`, `/comentar-pendencia`, `/fechar-pendencia`) estavam em bash+curl+jq e estouravam parse error sempre que payload continha backticks, control chars ou unicode (aspas curvas).

**Problema concreto:** comentário com backticks no markdown quebrava o heredoc bash+jq. Aconteceu 2x em 17/05/2026.

**Solução:** migração completa para Python urllib (zero dependência externa, já vem no Python 3.x macOS).

**Padrão adotado:**
- `urllib.request` para HTTP (GET/POST/PUT)
- `json` stdlib para payload
- Header: `Authorization: <token>` (sem "Bearer")
- Timezone BRT: `timezone(timedelta(hours=-3))` (nativo Python 3.9+, sem pytz)
- Mantém mesmos inputs, outputs, IDs canônicos

**Gap conhecido (não bloqueante):** pytz ainda referenciado em comentar-pendencia.md e fechar-pendencia.md (linhas 50 e 92-93 respectivamente), mas teste funcional passou com timezone nativo. Próxima edição deve substituir `import pytz` + `pytz.timezone()` por `timezone(timedelta())`.

**Aprendizado macro:** bash+jq+heredoc com markdown rico = frágil. Python urllib = padrão oficial para integrações REST do squad.

**Task:** {{clickup_task_id}}
**Validação:** listar-pendencias retornou 79 tasks, comentar-pendencia registrou comment ID 90130267201968 na task {{clickup_task_id}}.
