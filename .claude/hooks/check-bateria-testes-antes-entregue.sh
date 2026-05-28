#!/bin/bash
# Regra Inviolável #24 — bateria de testes externa antes de marcar entregue
# Detecta Edit/Write em pendencias.md mudando status pra "entregue"

if [ "$JADE_CONTEXT" = "rotina-autonoma" ] || [ "$JADE_CONTEXT" = "silencioso" ]; then
  exit 0
fi

TOOL_NAME="${CLAUDE_TOOL_NAME:-}"
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

if [[ "$TOOL_NAME" =~ ^(Edit|Write)$ ]] && [[ "$TOOL_INPUT" == *"pendencias.md"* ]] && [[ "$TOOL_INPUT" == *"entregue"* ]]; then
  echo "🟡 REGRA INVIOLÁVEL #24 — bateria de testes"
  echo "   Antes de marcar entregue, revisor externo APROVOU?"
  echo "   Matriz: páginas→triple-check #23, skills→paginas-dev, carrossel→revisor-visual, copy→paginas, MCP→paginas-dev, fix→bug-hunter"
  echo "   Se NÃO: despache revisor ANTES de marcar."
fi

exit 0