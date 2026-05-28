#!/bin/bash
# Varredura completa da pasta template — NÃO apenas arquivos staged
# Uso: bash workspace/scripts/scan-template-completo.sh

SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$SCRIPT_DIR"

echo "🔍 Varredura completa do template: $SCRIPT_DIR"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

FAIL=0
WARNINGS=0

# Arquivos meta de segurança — excluídos do scan (contêm os próprios patterns)
META_EXCLUDE='workspace/scripts/scan-template-completo\.sh|\.github/workflows/security-scan\.yml|\.git/hooks/pre-commit|\.git/hooks/pre-push'

check_pattern() {
  local label="$1"
  local pattern="$2"
  local exclude="${3:-NOMATCH_XYZ_PLACEHOLDER}"

  MATCHES=$(grep -rniE "$pattern" . \
    --include="*.md" --include="*.json" --include="*.sh" \
    --include="*.txt" --include="*.yml" --include="*.yaml" \
    --include="*.js" --include="*.ts" --include="*.py" \
    2>/dev/null \
    | grep -v ".git/" \
    | grep -vE "$META_EXCLUDE" \
    | grep -vE "$exclude" || true)

  if [ -n "$MATCHES" ]; then
    echo "❌ $label:"
    echo "$MATCHES" | head -5
    [ $(echo "$MATCHES" | wc -l) -gt 5 ] && echo "   ... ($(echo "$MATCHES" | wc -l | tr -d ' ') ocorrências total)"
    echo ""
    FAIL=1
  fi
}

check_warning() {
  local label="$1"
  local pattern="$2"
  local exclude="${3:-NOMATCH_XYZ_PLACEHOLDER}"

  MATCHES=$(grep -rniE "$pattern" . \
    --include="*.md" --include="*.json" --include="*.sh" \
    2>/dev/null \
    | grep -v ".git/" \
    | grep -vE "$META_EXCLUDE" \
    | grep -vE "$exclude" || true)

  if [ -n "$MATCHES" ]; then
    echo "⚠️  AVISO — $label:"
    echo "$MATCHES" | head -3
    echo ""
    WARNINGS=$((WARNINGS+1))
  fi
}

echo "=== ERROS CRÍTICOS (bloqueiam publicação) ==="

check_pattern "Nome operador"        '\bgui\s?[áa]vila\b|\bguiavila\b'                '\{\{|placeholder|canonical|README|guiavila52'
check_pattern "Empresa Ensinio"      '\b(ensinio)\b'                                   '\{\{'
check_pattern "Empresa Fatorial"     '\b(52 fatorial|fatorial)\b'                      '\{\{'
check_pattern "Empresa Mágica"       '\b(magica online|mágica online)\b'               '\{\{'
check_pattern "Gimmick SaaS"         '\bgimmick\b'                                     '\{\{|\.app\}'
check_pattern "Nome pessoal"         '\b(Lohan|Cleisson|Michella|Lisieux|Tarlis|Luiz Fosc)\b' ''
check_pattern "CNPJ"                 '[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}' '00\.000\.000|\{\{'
check_pattern "Email operador"       'gui@guiavila\.com|@guiavila\.com'                '\{\{|placeholder'
check_pattern "ClickUp IDs reais"    '\b30978229\b|\b901327[0-9]{6}\b'                 'CLICKUP_LIST_ID|\{\{'
check_pattern "Path absoluto"        '/Users/guiavila|/home/guiavila'                  ''
check_pattern "Token Anthropic"      'sk-ant-[a-zA-Z0-9]{20,}'                         ''
check_pattern "API keys"             'AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36,}'          ''
# Credenciais: só bloqueia quando há sinal de valor real (=, :, ou aspas com conteúdo)
check_pattern "Credencial com valor" '(NOTAZZ|GHL_API_KEY|MAILGUN_API_KEY|ENSINIO_API)[=:"\s]+[a-zA-Z0-9_\-]{8,}' '\{\{|placeholder|\.env\.example|app/\.env'
check_pattern "Task IDs reais"       '\b86[a-z0-9]{7,8}\b'                             '\{\{'
check_pattern "Google Calendar IDs"  'c_[a-z0-9]{20,}@group\.calendar\.google\.com'    '\{\{'

echo "=== AVISOS (revisar, não bloqueiam) ==="
check_warning "Domínio pessoal"  'guiavila\.com'  'canonical|\{\{|placeholder|README\.md|guiavila52'
check_warning "Handle social"    '@guiavila'      'guiavila52|\{\{'

echo "=== RESULTADO ==="
if [ "$FAIL" = "1" ]; then
  echo "🚫 FALHOU — dados sensíveis encontrados. NÃO publicar antes de corrigir."
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo "⚠️  $WARNINGS avisos encontrados. Revisar antes de publicar."
  exit 0
else
  echo "✅ PASSOU — nenhum dado sensível detectado."
  exit 0
fi
