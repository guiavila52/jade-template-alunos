#!/usr/bin/env bash
# test-mcp-meta-ads.sh — Testa conexão do MCP Meta Ads
# Uso: ./scripts/test-mcp-meta-ads.sh

set -euo pipefail

cd "$(dirname "$0")/.."

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Teste MCP Meta Ads ===${NC}\n"

# 1. Verificar se comando está instalado
MCP_CMD=""
if command -v armavita-meta-ads-mcp &> /dev/null; then
    MCP_CMD="armavita-meta-ads-mcp"
elif [ -f "$HOME/.local/bin/armavita-meta-ads-mcp" ]; then
    MCP_CMD="$HOME/.local/bin/armavita-meta-ads-mcp"
else
    echo -e "${RED}✗ armavita-meta-ads-mcp não encontrado${NC}"
    echo "Instale via: pipx install git+https://github.com/EfrainTorres/armavita-meta-ads-mcp.git"
    exit 1
fi

echo -e "${GREEN}✓ armavita-meta-ads-mcp instalado em $MCP_CMD${NC}"

# 2. Verificar versão
VERSION=$($MCP_CMD --version 2>&1 || echo "unknown")
echo -e "${GREEN}✓ Versão: $VERSION${NC}\n"

# 3. Verificar variáveis de ambiente
if [ -f "app/.env.local" ]; then
    echo -e "${YELLOW}Verificando vars de env...${NC}"

    if grep -q "^META_ADS_ACCESS_TOKEN=" app/.env.local; then
        echo -e "${GREEN}✓ META_ADS_ACCESS_TOKEN presente${NC}"
    else
        echo -e "${RED}✗ META_ADS_ACCESS_TOKEN ausente em app/.env.local${NC}"
        exit 1
    fi

    if grep -q "^META_GRAPH_API_VERSION=" app/.env.local; then
        echo -e "${GREEN}✓ META_GRAPH_API_VERSION presente${NC}"
    else
        echo -e "${YELLOW}⚠ META_GRAPH_API_VERSION ausente (usará v25.0 padrão)${NC}"
    fi
else
    echo -e "${RED}✗ app/.env.local não encontrado${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=== Configuração OK ===${NC}"
echo ""
echo -e "${YELLOW}Próximo passo:${NC}"
echo "1. Abra uma nova conversa com a Jade"
echo "2. Digite: @jade lista minhas contas de anúncios do Meta"
echo "3. Se retornar contas → MCP funcionando ✓"
echo "4. Se retornar erro de token → gerar novo em Meta Business Suite"
echo ""
echo "Documentação completa: workspace/processos/mcp-meta-ads.md"
