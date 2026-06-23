---
name: publicar-criativo
description: Sobe imagem aprovada + copy no Meta Ads e cria anúncio dentro de um ad set. Nasce PAUSED para aprovação.
type: skill
---

# /publicar-criativo

**Status:** 🟢 MADURA
**Token:** ler `META_ADS_ACCESS_TOKEN` de `app/.env.local`, passar como `meta_access_token` em TODOS os calls.
**Conta:** `{{META_ADS_ACCOUNT}}`

Verificar antes de executar:
- Criativo aprovado pelo operador (output de /criar-criativo)
- Passou pelo /revisar-criativo
- Imagem disponível (path local ou URL pública)

## Inputs obrigatórios

1. **Ad Set ID:** onde o anúncio vai (obter de /criar-campanha)
2. **Imagem:** path local OU URL pública
3. **Headline:** título (max 40 chars)
4. **Primary text:** texto principal (max 125 chars para feed)
5. **Link de destino:** URL final
6. **CTA button:** LEARN_MORE, SIGN_UP, DOWNLOAD, ou GET_QUOTE

## Fluxo

### 1. Subir imagem

`mcp__meta-ads__upload_ad_image_asset`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `image_file_path`: [path] OU `image_source_url`: [URL]
- `name`: [nome descritivo]

Salvar `image_hash`.

### 2. Criar criativo

`mcp__meta-ads__create_ad_creative`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `name`: "[Produto] — [Ângulo] — [Data]"
- `headline_text`: [headline aprovada]
- `primary_text`: [primary text aprovado]
- `ad_image_hash`: [image_hash]
- `link_url`: [URL destino]
- `call_to_action_type`: [CTA]
- `facebook_page_id`: [page_id da página do operador — consultar list_account_pages]

Salvar `creative_id`.

### 3. Criar anúncio

`mcp__meta-ads__create_ad`:
- `ad_account_id`: `{{META_ADS_ACCOUNT}}`
- `meta_access_token`: [token]
- `name`: "[Produto] — [Ângulo] — [Data]"
- `ad_set_id`: [ad_set_id informado]
- `ad_creative_id`: [creative_id]
- `status`: `PAUSED`

Salvar `ad_id`.

### 4. Verificar

`mcp__meta-ads__read_ad` com `ad_id` para confirmar PAUSED e sem erros.

### 5. Output

Atualizar `workspace/output/trafego/campanhas/` com:
- Ad ID, Creative ID, Image hash
- Headline, Primary text, Link
- Status: ⏸️ PAUSED

Reportar ao operador: ad_id criado, status PAUSED, como ativar.
