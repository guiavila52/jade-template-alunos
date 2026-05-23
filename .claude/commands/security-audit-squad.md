<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /security-audit-squad

Auditoria recorrente de segurança da INFRAESTRUTURA do squad (`.claude/`, `~/.claude.json`, `~/.claude/mcp.json`, hooks, plugins, settings). Diferente de `/security-audit` (que cobre código de app).

## Quando invocar
- Rotina semanal (cron sugerido: domingo 8h BRT)
- Após instalar plugin/MCP/dependência nova
- Após mudança em `.claude/settings.json` ou hooks
- Antes de aceitar PR que toca infraestrutura

## Escopo — 7 verificações (Regra §16)

### 1. Lethal trifecta
Mapear agentes/skills que combinam: (a) acesso a dados privados, (b) processamento de conteúdo untrusted, (c) comunicação externa. Sinalizar combinações sem mitigação estrutural.

### 2. Hook bypass
Testar PreToolUse hooks com agente sintético reproduzindo issue #45427 (subagent que fura hook do parent). Validar se cada hook bloqueante resiste.

### 3. Secret leak
Rodar `gitleaks detect --source workspace/ --source .claude/ --redact` e comparar contra baseline `.secrets.baseline`. Reportar diffs.

### 4. Self-modification
Auditar quem modifica `.claude/settings.json`, hooks, `~/.claude.json`, `~/.claude/mcp.json`. Garantir que SÓ Bash heredoc/sed alcança esses paths (Regra §11). Detectar Write/Edit tool em logs recentes.

### 5. Supply chain
Comparar `app/package.json` e `requirements.txt` contra DBs Shai-Hulud + variantes (Mini Shai-Hulud, TeamPCP). Verificar lockfile integrity.

### 6. MCP novo
Listar MCP servers ativos (`~/.claude/mcp.json` + `app/.mcp.json`), diff vs última auditoria. Rodar `mcp-scan` (invariantlabs-ai) se disponível.

### 7. Plugin novo
Listar plugins marketplace instalados. Auditar `hooks/hooks.json` + `skills/*/SKILL.md` de cada plugin. Bloquear se `allowed-tools: Bash(*)` sem justificativa.

## Vetores 2026 ativos
- CVE-2025-59536 (CVSS 8.7) — RCE via hooks settings.json não-trustado
- CVE-2026-21852 — API token exfil via `ANTHROPIC_BASE_URL`
- Mini Shai-Hulud / TeamPCP — worm em `~/.claude.json` e `~/.claude/mcp.json`
- Tool poisoning MCP (descrição reescrita pós-auth)
- Subagent hook bypass (issue anthropics/claude-code #45427)

## Output

Arquivo: `workspace/output/seguranca/YYYY-MM-DD-audit-squad.md`

Estrutura:
- Header com data + summary (X ✅ · Y ⚠️ · Z 🔴)
- 7 seções (uma por verificação)
- Cada seção: status + evidência (path/hash/comando) + ação recomendada

Atualizar `workspace/output/seguranca/mapa.md` (Regra §7).

## Critério de aceitação
- 7 seções preenchidas com evidência rastreável (nada inventado)
- Idempotente: rodar 2x consecutivas com mesmo estado = mesmo output
- Sem alucinação: cada finding tem comando reproduzível

## Tratamento de erros
- `gitleaks` ausente → reportar + sugerir `brew install gitleaks` (Jade executa)
- `mcp-scan` ausente → skip seção 6, reportar como gap
- Permissão negada em `~/.claude/*` → reportar + pular item

## Aprendizado + pendência (Regra §5)
- Toda finding 🔴 → criar pendência ClickUp via `/criar-pendencia` automaticamente
- Reincidência da mesma finding em 2 audits seguidas → escalar pro Gui
