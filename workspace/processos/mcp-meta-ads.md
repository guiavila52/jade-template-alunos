# MCP Meta Ads — Pipeboard

Servidor MCP local para gerenciar campanhas Meta Ads (Facebook + Instagram) via Claude Code.

**Provider escolhido:** [armavita-meta-ads-mcp](https://github.com/EfrainTorres/armavita-meta-ads-mcp)  
**Motivo:** Python puro, stdio local, bem documentado, AGPLv3, suporta Meta Marketing API v25.0, 30+ tools.

---

## Instalação

**Status:** ✅ INSTALADO (11/05/2026)

```bash
# Instalar pipx (gerenciador de CLIs Python isolados)
brew install pipx

# Instalar MCP Meta Ads do GitHub (não está no PyPI ainda)
pipx install git+https://github.com/EfrainTorres/armavita-meta-ads-mcp.git

# Adicionar ao PATH (só precisa rodar uma vez)
pipx ensurepath

# Verificar
armavita-meta-ads-mcp --version
# Output esperado: 1.1.0
```

Path do comando: `/Users/guiavila/.local/bin/armavita-meta-ads-mcp`

---

## Configuração — Variáveis de ambiente

O MCP precisa de um **Access Token** do Meta Marketing API.

### Onde pegar cada variável

#### 1. META_ACCESS_TOKEN (obrigatório)

**Caminho manual:**
1. Acesse [Meta Business Suite](https://business.facebook.com)
2. Menu > Configurações de Negócios > Integrações > API de Marketing
3. Clique em "Gerar Token"
4. Selecione:
   - Conta de Anúncios: (a conta do Gui)
   - Permissões: `ads_read`, `ads_management`, `business_management`
5. Copie o token gerado (começa com `EAA...`)
6. Cole no `app/.env.local`:

```bash
META_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Caminho OAuth (alternativa):**
1. Crie um app em [Meta for Developers](https://developers.facebook.com/apps)
2. Adicione produto "Marketing API"
3. Copie App ID + App Secret
4. Execute:
```bash
pipeboard-meta-ads-mcp --login
```
(abre navegador, faz OAuth, salva token localmente)

#### 2. META_AD_ACCOUNT_ID (opcional, mas útil)

Formato: `act_XXXXXXXXX`

1. Meta Business Suite > Configurações de Negócios > Contas de Anúncios
2. Copie o ID da conta (ex: `act_123456789`)
3. Cole no `.env.local`:

```bash
META_AD_ACCOUNT_ID=act_123456789
```

(Se não definir, o MCP retorna todas as contas acessíveis)

#### 3. META_GRAPH_API_VERSION (opcional)

Padrão: `v25.0` (atual em maio 2026)

```bash
META_GRAPH_API_VERSION=v25.0
```

---

## Tools disponíveis (30+)

### Contas
- `list_ad_accounts` — lista contas acessíveis pelo token
- `read_ad_account` — detalhes de uma conta específica

### Campanhas
- `list_campaigns` — lista campanhas de uma conta
- `read_campaign` — detalhes de uma campanha
- `create_campaign` — criar campanha nova
- `update_campaign` — editar campanha existente
- `clone_campaign` — duplicar campanha

### Conjuntos de anúncios (Ad Sets)
- `list_ad_sets` — lista ad sets de uma campanha
- `read_ad_set` — detalhes de um ad set
- `create_ad_set` — criar ad set novo
- `update_ad_set` — editar ad set existente
- `clone_ad_set` — duplicar ad set

### Anúncios (Ads)
- `list_ads` — lista ads de um ad set
- `read_ad` — detalhes de um ad
- `list_ad_previews` — preview visual do ad (desktop/mobile)
- `create_ad` — criar ad novo
- `update_ad` — editar ad existente
- `clone_ad` — duplicar ad

### Criativos
- `list_ad_creatives` — lista criativos de uma conta
- `read_ad_creative` — detalhes de um criativo
- `create_ad_creative` — criar criativo novo
- `update_ad_creative` — editar criativo existente
- `clone_ad_creative` — duplicar criativo
- `upload_ad_image_asset` — upload de imagem (retorna hash)
- `read_ad_image` — detalhes de uma imagem (por hash)
- `export_ad_image_file` — download de imagem como arquivo

### Insights (métricas)
- `list_insights` — métricas de performance (campanha/ad set/ad)
  - Suporta: impressions, clicks, spend, ctr, cpc, cpm, reach, conversions, roas
  - Breakdowns: age, gender, placement, device, country
  - Date presets: last_7d, last_14d, last_30d, maximum
- `create_report` — relatório customizado (async job)

### Targeting (segmentação)
- `search_interests` — buscar interesses (ex: "tech", "yoga")
- `suggest_interests` — sugestões baseadas em seed
- `estimate_audience_size` — estimar alcance de um público-alvo
- `search_behaviors` — buscar comportamentos do público
- `search_demographics` — buscar dados demográficos
- `search_geo_locations` — buscar localizações (cidade/país)

### Orçamento
- `create_campaign_budget_schedule` — agendar mudança de orçamento

### Páginas
- `search_pages` — buscar páginas do Facebook (por nome)
- `list_account_pages` — páginas associadas à conta

### Ads Library (biblioteca de anúncios)
- `search_ads_archive` — buscar anúncios de concorrentes na biblioteca pública

### Research (ferramentas auxiliares)
- `search_web_content` — buscar conteúdo na web (proxy via MCP)
- `read_web_content` — ler conteúdo de URL (proxy via MCP)

---

## Como a Jade vai usar

### Exemplo 1: Listar campanhas ativas

```
Jade: Me mostra as campanhas ativas com ROI > 2
→ Tool: mcp_meta_ads_get_campaigns (filters: {status: "ACTIVE"})
→ Tool: mcp_meta_ads_get_insights (metric: roas, threshold: 2)
→ Output: [lista de campanhas com métricas]
```

### Exemplo 2: Pausar ad com CTR baixo

```
Jade: Pausa todos os ads com CTR < 0.5% nos últimos 7 dias
→ Tool: mcp_meta_ads_get_insights (date_preset: "last_7d", metric: "ctr")
→ Filtra: ctr < 0.005
→ Tool: mcp_meta_ads_update_ad (status: "PAUSED") pra cada ad
→ Confirma com o Gui antes de executar
```

### Exemplo 3: Criar criativo novo

```
Gui: Cria um criativo com essa copy + imagem XYZ
Jade:
→ Tool: mcp_meta_ads_upload_image (file: XYZ)
→ Tool: mcp_meta_ads_create_ad_creative (headline, description, image_hash)
→ Tool: mcp_meta_ads_create_ad (creative_id, ad_set_id)
→ Output: ID do ad criado + preview
```

### Exemplo 4: Relatório semanal

```
Skill /relatar-trafego (cron):
→ Tool: mcp_meta_ads_get_insights (last_7d, all campaigns)
→ Agrega: spend, impressions, clicks, conversions, roas
→ Compara com semana anterior
→ Output: relatório Markdown → Jade envia pro Gui
```

---

## Comandos de teste

### 1. Testar conexão

```bash
cd "/Users/guiavila/Documents/Projetos IA Gui Ávila/Squad Empresa Gui Ávila"

# Via Python direto
python -c "
from meta_ads_mcp import MetaAdsClient
import os
client = MetaAdsClient(access_token=os.getenv('META_ACCESS_TOKEN'))
accounts = client.get_ad_accounts()
print(f'✓ Conectado. {len(accounts)} contas encontradas.')
for acc in accounts:
    print(f'  - {acc[\"name\"]} ({acc[\"id\"]})')
"
```

### 2. Testar via Claude Code

Na conversa com a Jade:

```
@jade lista as contas de anúncios do Meta acessíveis
```

Esperado: lista com nome + ID + saldo de cada conta.

### 3. Listar campanhas

```
@jade mostra as 5 campanhas com maior gasto nos últimos 30 dias
```

---

## Segurança

- Access token NUNCA commitado (`.env.local` está no `.gitignore`)
- Token redactado nos logs do MCP (URLs com `access_token` são sanitizados)
- Todas as operações de escrita (create/update/delete) exigem confirmação explícita do Gui via Jade

---

## Limitações conhecidas

1. **Rate limits Meta:** 200 calls/hour por user, 4800/hour por app. MCP não tem retry automático — Jade precisa gerenciar.
2. **Paginação:** insights de períodos longos retornam async job ID. Jade precisa fazer polling.
3. **Criativos com vídeo:** upload de vídeo é chunked (>10MB). MCP simplificado suporta só imagem direta.

---

## Troubleshooting

### Erro: "Invalid OAuth access token"

- Token expirado (validade padrão: 60 dias)
- Gerar novo em Meta Business Suite > API de Marketing
- Atualizar `META_ACCESS_TOKEN` no `.env.local`

### Erro: "Permissions error"

- Token sem permissões `ads_management`
- Regenerar token com scopes corretos

### Erro: "Ad account not found"

- `META_AD_ACCOUNT_ID` errado
- Formato correto: `act_123456789` (prefixo `act_` obrigatório)

### MCP não aparece no Claude Code

1. Verificar `.mcp.json` válido (sem vírgula no último item)
2. Reiniciar Claude Code (Cmd+Shift+P > "Reload Window")
3. Verificar logs: `tail -f ~/.claude/logs/mcp-meta-ads.log`

---

## Próximos passos (Gui)

1. Gerar `META_ACCESS_TOKEN` no Meta Business Suite
2. Colar em `app/.env.local` (TextEdit já aberto)
3. Testar: `@jade lista minhas contas de anúncios do Meta`
4. Se funcionar: skill `/relatar-trafego` pode começar a usar

---

**Atualizado:** 11/05/2026  
**Autor:** paginas-dev (Onda 10.6)  
**Status:** configurado, bloqueado por credentials do Gui
