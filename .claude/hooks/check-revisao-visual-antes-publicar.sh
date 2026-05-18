#!/usr/bin/env bash
# Regra Inviolavel #38 - Revisao visual real obrigatoria
# Bloqueia PATCH/deploy/push sem screenshot REVISAO-APROVADO do designer-revisor recente.

set -uo pipefail

INPUT=$(cat 2>/dev/null || true)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' 2>/dev/null || echo "")
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")
BYPASS="${JADE_CONTEXT:-}"

[[ "$BYPASS" == "desenvolvendo-revisor" ]] && exit 0
[[ "$BYPASS" == "rotina-autonoma" ]] && exit 0

NEEDS_REVIEW=0
CTX=""

# 1. PATCH/POST body {{APP_PESSOAL}}
if echo "$COMMAND" | grep -qE '{{app_pessoal}}.{{handle}}.com/api/content/(newsletters|car[a-z]+|ideias)'; then
  if echo "$COMMAND" | grep -qE '"body"' && echo "$COMMAND" | grep -qE '(PATCH|POST)'; then
    NEEDS_REVIEW=1
    CTX="PATCH/POST body {{APP_PESSOAL}}"
  fi
fi

# 2. Deploy producao
if echo "$COMMAND" | grep -qE 'vercel.* --prod'; then
  NEEDS_REVIEW=1
  CTX="deploy producao"
fi

# 3. Write/Edit em .astro ou src/pages/
if [[ "$TOOL" =~ ^(Write|Edit)$ ]]; then
  if [[ "$FILE_PATH" == *".astro" ]] || [[ "$FILE_PATH" == *"src/pages/"* ]]; then
    NEEDS_REVIEW=1
    CTX="$TOOL em pagina front-end"
  fi
fi

# 4. Meta Ads MCP
if echo "$COMMAND" | grep -qE 'mcp__meta-ads__(create_ad|update_ad|upload_ad_image)'; then
  NEEDS_REVIEW=1
  CTX="push Meta Ads"
fi

if [[ "$NEEDS_REVIEW" -eq 1 ]]; then
  PROJ="$CLAUDE_PROJECT_DIR
  RECENT=$(find "$PROJ/workspace/output/screenshots-revisao" -type f -name "*REVISAO-APROVADO*" -mmin -10 2>/dev/null | head -1)

  if [[ -z "$RECENT" ]]; then
    echo "BLOQUEADO - Regra Inviolavel #38: output visual sem revisao visual real." >&2
    echo "" >&2
    echo "Operacao: $CTX" >&2
    echo "" >&2
    echo "Nenhum REVISAO-APROVADO encontrado em workspace/output/screenshots-revisao/ (ultimos 10min)." >&2
    echo "" >&2
    echo "Desbloqueio:" >&2
    echo "  1. Despache agent designer-revisor pra renderizar via Playwright + screenshot desktop+mobile + checklist" >&2
    echo "  2. Se REPROVADO: corrige output + re-despacha revisor" >&2
    echo "  3. So com APROVADO recente: prossiga" >&2
    echo "" >&2
    echo "Bypass (apenas se desenvolvendo revisor):" >&2
    echo "  export JADE_CONTEXT=desenvolvendo-revisor" >&2
    echo "" >&2
    echo "Source: AGENTS.md Regra #38 + memoria feedback_revisao_visual_real_obrigatoria.md" >&2
    exit 2
  fi
fi

exit 0
