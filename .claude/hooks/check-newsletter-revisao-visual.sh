#!/usr/bin/env bash
# Hook: check-newsletter-revisao-visual.sh
# Bloqueia PATCH newsletter sem evidência REAL de revisão visual aprovada
# Criado: 12/05/2026 | Endurecido: 13/05/2026 (Regra #33 — revisor independente)

set -euo pipefail

# Captura o comando Bash completo sendo executado
BASH_CMD="$*"

# Detecta se é PATCH via {{Plataforma_Conteudo}} API
if [[ "$BASH_CMD" =~ curl.*-X\ PATCH.*{{plataforma_conteudo}}\.guiavila\.com/api/content/newsletters ]]; then
  
  OUTPUT_DIR="~/Documents/Projetos IA Gui Ávila/Squad Empresa Gui Ávila/workspace/output/newsletter"
  
  # Critério 1 — Arquivo de revisão aprovado pelo revisor independente (< 24h)
  REVISAO_APROVADO=$(find "$OUTPUT_DIR" -name "*REVISAO-APROVADO*.md" -mtime -1 2>/dev/null | head -n1)
  
  # Critério 2 — Body HTML real do painel baixado após último PATCH (< 24h)
  EMAIL_REAL=$(find "$OUTPUT_DIR" -name "*EMAIL-REAL-INBOX*.html" -mtime -1 2>/dev/null | head -n1)
  
  # Critério 3 — Screenshot Gmail real do Gui (< 6h) — OPCIONAL mas avisa
  TESTE_INBOX=$(find "$OUTPUT_DIR" -name "*TESTE-INBOX-OK*.png" -mmin -360 2>/dev/null | head -n1)
  
  # Bloqueia se faltar 1 ou 2 (evidências obrigatórias)
  if [[ -z "$REVISAO_APROVADO" ]]; then
    echo "❌ HOOK BLOQUEOU: newsletter PATCH sem arquivo *REVISAO-APROVADO*.md recente (< 24h)."
    echo "Jade NÃO pode aprovar — precisa revisor independente (Regra #33)."
    echo "Localização esperada: $OUTPUT_DIR/*REVISAO-APROVADO*.md"
    exit 2
  fi
  
  if [[ -z "$EMAIL_REAL" ]]; then
    echo "❌ HOOK BLOQUEOU: newsletter PATCH sem arquivo *EMAIL-REAL-INBOX*.html recente (< 24h)."
    echo "Body HTML do painel deve ser baixado e revisado ANTES de PATCH."
    echo "Localização esperada: $OUTPUT_DIR/*EMAIL-REAL-INBOX*.html"
    exit 2
  fi
  
  # Avisa se faltar critério 3 (soft warning, não bloqueia)
  if [[ -z "$TESTE_INBOX" ]]; then
    echo "⚠️  ATENÇÃO: Não encontrado screenshot Gmail real (*TESTE-INBOX-OK*.png < 6h)."
    echo "Hook permite passar, mas recomenda aprovação visual do Gui antes de produção."
  fi
  
  # Passou — evidências suficientes
  echo "✅ Hook check-newsletter-revisao-visual: evidências OK"
  echo "   → Revisão aprovada: $REVISAO_APROVADO"
  echo "   → Email real inbox: $EMAIL_REAL"
  [[ -n "$TESTE_INBOX" ]] && echo "   → Teste inbox OK: $TESTE_INBOX"
fi

exit 0
