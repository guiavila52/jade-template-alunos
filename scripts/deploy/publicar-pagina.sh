#!/usr/bin/env bash
# /publicar-pagina — deploy resiliente com fallback CLI→git push
#
# Tentativa 1: vercel --prod (timeout 90s) — útil quando CLI funciona
# Tentativa 2: git push origin main (se CLI travou) — Vercel auto-deploy GitHub
#
# Uso:
#   ./publicar-pagina.sh                  # repo atual
#   ./publicar-pagina.sh /path/to/repo    # repo específico

set -uo pipefail

REPO="${1:-$(pwd)}"
cd "$REPO" || { echo "❌ repo não existe: $REPO" >&2; exit 1; }

echo "📍 Repo: $REPO"
echo ""

# Sanidade
if [ ! -d .git ]; then
    echo "❌ não é repo git" >&2; exit 1
fi

# Vê branch atual + status
BRANCH=$(git branch --show-current)
echo "🌿 Branch atual: $BRANCH"

if [ "$BRANCH" != "main" ]; then
    echo "⚠️  Não está em main. Esta skill assume main. Aborte ou faça checkout/merge primeiro." >&2
    exit 1
fi

if ! git diff --quiet HEAD || ! git diff --cached --quiet; then
    echo "⚠️  Working tree sujo. Commite antes." >&2
    git status --short >&2
    exit 1
fi

# Estratégia 1 — vercel --prod com timeout
echo ""
echo "=== Tentativa 1: vercel --prod (timeout 90s) ==="
TMPLOG=$(mktemp)

if command -v gtimeout &>/dev/null; then TO=gtimeout
elif command -v timeout &>/dev/null; then TO=timeout
else TO=""; fi

if [ -n "$TO" ]; then
    if $TO 90 vercel --prod --yes 2>&1 | tee "$TMPLOG"; then
        URL=$(grep -oE 'https://[a-z0-9-]+\.vercel\.app[^ ]*' "$TMPLOG" | tail -1)
        echo ""
        echo "✅ Deploy via CLI funcionou. URL: $URL"
        rm -f "$TMPLOG"
        exit 0
    else
        EXIT=$?
        echo ""
        echo "⚠️  Vercel CLI falhou ou travou (exit $EXIT). Caindo pra fallback git push." >&2
    fi
else
    echo "⚠️  Sem 'timeout' disponível, pulando direto pra git push fallback." >&2
fi

rm -f "$TMPLOG"

# Estratégia 2 — git push (Vercel auto-deploy GitHub)
echo ""
echo "=== Fallback: git push origin main ==="
git push origin main
echo ""
echo "✅ Push feito. Vercel detecta e builda em ~30-90s."
echo "   Monitore em: vercel.com/<team>/paginas-guiavila-astro/deployments"
