#!/bin/bash
# Hook PreToolUse — Regra Inviolável #29
# Bloqueia declarações de "Caqui parcial" ou "aguarda Gui" sem o checklist obrigatório das 4 categorias.

# Lê o comando que vai ser executado (passado via stdin como JSON Claude Code)
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.content // ""' 2>/dev/null)

# Detecta strings de bloqueio
if echo "$COMMAND" | grep -qiE "Caqui parcial|aguarda Gui|espera Gui voltar|aguardando Gui|aguardando aprovação"; then
    # Verifica se PROGRESS.md tem o checklist Regra #29 respondido nas últimas 50 linhas
    PROGRESS="$(cd "$(dirname "$0")/../.." && pwd)/PROGRESS.md"
    if [ -f "$PROGRESS" ] && tail -50 "$PROGRESS" | grep -qE "Regra #29|PRÉ-DECLARAÇÃO DE CAQUI"; then
        # Checklist presente — permitir
        exit 0
    fi
    
    # Bloqueio: falta checklist
    echo "BLOQUEIO Regra Inviolável #29: você está prestes a declarar 'Caqui parcial' / 'aguarda Gui' SEM ter respondido o checklist das 4 categorias de gate." >&2
    echo "" >&2
    echo "Antes de continuar, responda em PROGRESS.md:" >&2
    echo "  [ ] É DISPARO público irreversível? (cat 1)" >&2
    echo "  [ ] É DEPLOY em produção? (cat 2)" >&2
    echo "  [ ] É INPUT EXTERNO físico que só Gui tem? (cat 3)" >&2
    echo "  [ ] É DECISÃO ESTRATÉGICA real entre opções? (cat 4)" >&2
    echo "" >&2
    echo "Se NENHUMA marcada → NÃO declarar Caqui parcial. Continue atacando." >&2
    echo "Se 1+ marcada → Caqui legítimo. Justifique qual gate em 1 linha." >&2
    echo "" >&2
    echo "Ver: AGENTS.md Regra Inviolável #29 + memória feedback_matriz_autonomia_jade.md" >&2
    exit 2
fi

exit 0
