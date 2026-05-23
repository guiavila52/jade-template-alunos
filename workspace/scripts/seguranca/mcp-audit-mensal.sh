#!/usr/bin/env bash
# mcp-audit-mensal.sh
# Audit recorrente dos MCP servers ativos no Claude Code.
# Fecha vetor R8 (MCP tool poisoning) em ritmo mensal.
# Pendência mãe (origem): ClickUp {{CLICKUP_TASK_ID}} (Item 0.5 hardening Fase 0).
#
# Uso manual:
#   ./workspace/scripts/seguranca/mcp-audit-mensal.sh
#
# Cron (NÃO instalar automaticamente — exige aval Gui):
#   0 9 1 * * cd "{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}" && ./workspace/scripts/seguranca/mcp-audit-mensal.sh

set -euo pipefail

REPO_ROOT="{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"
TODAY="$(date +%Y-%m-%d)"
OUTPUT_DIR="${REPO_ROOT}/workspace/output/auditorias"
OUTPUT_FILE="${OUTPUT_DIR}/${TODAY}-mcp-audit-auto.md"
LOG_DIR="${REPO_ROOT}/workspace/output/auditorias/logs"

mkdir -p "${OUTPUT_DIR}" "${LOG_DIR}"

echo "==> MCP audit mensal — ${TODAY}"
echo "==> Output: ${OUTPUT_FILE}"

# 1. Verifica ferramenta instalada
if ! command -v snyk-agent-scan >/dev/null 2>&1; then
  echo "[ERRO] snyk-agent-scan não instalado. Rode: pipx install snyk-agent-scan"
  exit 1
fi

VERSION="$(snyk-agent-scan inspect 2>&1 | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo 'unknown')"
echo "==> snyk-agent-scan ${VERSION}"

# 2. Roda inspect (free, sem SNYK_TOKEN)
INSPECT_LOG="${LOG_DIR}/${TODAY}-inspect.log"
echo "==> Rodando inspect…"
snyk-agent-scan inspect --verbose > "${INSPECT_LOG}" 2>&1 || true

# 3. Extrai MCPs ativos do claude.ai sync
MCP_ACTIVE_JSON="$(cat ~/.claude.json | jq -r '.claudeAiMcpEverConnected // [] | join(", ")' 2>/dev/null || echo "ERRO leitura ~/.claude.json")"

# 4. Snapshot das permissions allow contendo "mcp__"
PROJECT_SETTINGS="${REPO_ROOT}/.claude/settings.json"
GLOBAL_SETTINGS="${HOME}/.claude/settings.json"
PROJ_MCP_ALLOWS="$(jq -r '.permissions.allow // [] | map(select(startswith("mcp__"))) | join("\n  ")' "${PROJECT_SETTINGS}" 2>/dev/null || echo "ERRO")"
GLOB_MCP_ALLOWS="$(jq -r '.permissions.allow // [] | map(select(startswith("mcp__"))) | join("\n  ")' "${GLOBAL_SETTINGS}" 2>/dev/null || echo "ERRO")"

# 5. Verifica hooks deprecated ainda ativos
DEPRECATED_HOOKS_OK="yes"
for h in check-mcp-clickup-deprecated.sh check-mcp-{{plataforma_conteudo}}-deprecated.sh; do
  if [[ ! -x "${REPO_ROOT}/.claude/hooks/${h}" ]]; then
    DEPRECATED_HOOKS_OK="no (faltando ${h})"
  fi
done

# 6. Gera relatório
cat > "${OUTPUT_FILE}" <<EOF
# MCP Security Audit — ${TODAY} (auto)

**Gerado por:** \`workspace/scripts/seguranca/mcp-audit-mensal.sh\`
**Origem:** Item 0.5 hardening Fase 0 (ClickUp {{CLICKUP_TASK_ID}}), Regra §16
**Ferramenta:** snyk-agent-scan ${VERSION}

---

## MCPs ativos via claude.ai (~/.claude.json claudeAiMcpEverConnected)

${MCP_ACTIVE_JSON}

## Permissions allow contendo mcp__ — projeto

  ${PROJ_MCP_ALLOWS}

## Permissions allow contendo mcp__ — global

  ${GLOB_MCP_ALLOWS}

## Hooks deprecated MCP ativos

${DEPRECATED_HOOKS_OK}

## snyk-agent-scan inspect output

\`\`\`
$(cat "${INSPECT_LOG}" | head -80)
\`\`\`

## Checklist manual (humano valida)

- [ ] Algum MCP novo apareceu em claudeAiMcpEverConnected sem aval? (deveria ser bloqueado pela governança)
- [ ] Permissions allow contém MCP deprecated (ClickUp, {{Plataforma_Conteudo}})?
- [ ] Hooks deprecated ainda ativos?
- [ ] Algum tool name com palavra suspeita (stealth, hidden, exfil, ignore, bypass)?
- [ ] Algum MCP custom (não-mcp__claude_ai_*, não-mcp__meta-ads__*) registrado?

---

Próximo audit: $(date -j -v+1m +%Y-%m-%d 2>/dev/null || date -d "+1 month" +%Y-%m-%d)
EOF

echo "==> Relatório salvo: ${OUTPUT_FILE}"
echo "==> Log inspect: ${INSPECT_LOG}"
echo "==> DONE."
