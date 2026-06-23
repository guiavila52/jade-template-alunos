# Skill: /criar-lancamento

Organiza uma campanha/lançamento do zero. Cria lista dedicada no ClickUp com todas as tasks (operador como responsável nas que dependem dele), registro canônico, mapa visual TXT, e atualiza a estratégia viva.

Skill canônica para QUALQUER campanha recorrente: mentoria, {{PRODUTO_PRINCIPAL}}, webinário, carrinho aberto, pré-lançamento.

> **Aval operador:** 02/06/2026

---

## Estrutura universal de um lançamento

Todo lançamento tem a mesma espinha dorsal:

```
AQUECIMENTO → CAPTURA → [LÓGICA DE ABERTURA] → VENDA → FECHAMENTO → [SEGUNDA CHANCE]
```

**Variantes de fluxo:**

| Tipo | Caminho |
|---|---|
| **A — Direto** | Aquecimento → Captura → Carrinho abre → Página de vendas → Fechamento |
| **B — Webinário** | Aquecimento → Captura (inscrição webinário) → Webinário ao vivo → Pitch → Carrinho abre → Página de vendas → Fechamento |

---

## Inputs obrigatórios

| Campo | Descrição | Exemplo |
|---|---|---|
| `nome` | Nome interno da campanha | "Turma de Exemplo" |
| `slug` | Identificador único (sem espaços) | "turma-exemplo" |
| `produto` | Produto sendo lançado | "{{PRODUTO_PRINCIPAL}}" |
| `tipo` | `direto` ou `webinario` | "direto" |
| `preco` | Preço público | "R$X.XXX" |
| `meta_vagas` | Meta interna (NÃO divulgar publicamente) | 20 |
| `data_aquecimento` | Início do aquecimento (YYYY-MM-DD) | "AAAA-MM-DD" |
| `data_aviso_youtube` | Vídeo de aviso YouTube (YYYY-MM-DD) | "AAAA-MM-DD" |
| `data_abertura` | Abertura do carrinho (YYYY-MM-DD) | "AAAA-MM-DD" |
| `data_fechamento` | Fechamento do carrinho (YYYY-MM-DD) | "AAAA-MM-DD" |
| `data_primeira_aula` | Primeira aula/entrega (YYYY-MM-DD, opcional) | "AAAA-MM-DD" |
| `pagina_captura` | URL da página de captura com form GHL | "{{DOMINIO}}/{{SLUG_CAPTURA}}" |
| `pagina_vendas` | URL da página de preços/vendas | "{{DOMINIO}}/{{SLUG_VENDAS}}" |
| `link_checkout` | URL do checkout direto | "{{DOMINIO}}/{{ROTA_CHECKOUT}}" |
| `ghl_form_id` | ID do form GHL (para referência) | "abc123" |

Se `tipo = webinario`, adicionar: `data_webinario` (YYYY-MM-DD HH:MM) e `pagina_webinario`.

---

## Estados da página de captura (4 estados via Env vars Vercel)

| Estado | Env var | Comportamento |
|---|---|---|
| **Normal** (padrão) | — | Form GHL. Lead → CRM → WhatsApp API + email |
| **Carrinho aberto** | `{SLUG}_CARRINHO_ABERTO=true` | Redirect → `pagina_vendas` |
| **Carrinho fechado** | `{SLUG}_CARRINHO_FECHADO=true` | Banner "inscrições encerradas" + form lista espera |
| **Segunda chance** | `{SLUG}_SEGUNDA_CHANCE=true` | Redirect → `pagina_vendas` |

Precedência: aberto > segunda_chance > fechado > normal. Após cada mudança de env var → Redeploy no Vercel.

**GHL obrigatório** em todos os forms — nunca form customizado sem GHL (quebra automações WhatsApp/email).

---

## Arquitetura de páginas

| Página | URL | O que tem |
|---|---|---|
| **Captura** | `{{DOMINIO}}/{slug-captura}` | Hero + benefícios + form GHL + urgência |
| **Vendas** | `{{DOMINIO}}/{slug}-precos` | Copy completa + preço + bônus + FAQ + checkout |

---

## Fluxo de execução

### Passo 1 — Verificar inputs
Confirmar todos os campos obrigatórios. Se `data_aviso_youtube` ausente: `data_abertura - 12 dias`.

### Passo 2 — Criar lista dedicada no ClickUp

Criar nova lista no espaço Empresa (ID `{{CLICKUP_SPACE_ID}}`) com nome `🚀 Lançamento {nome}`:

```bash
curl -X POST -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "🚀 Lançamento {nome}"}' \
  "https://api.clickup.com/api/v2/space/{{CLICKUP_SPACE_ID}}/list"
```

Guardar o `list_id` retornado.

### Passo 3 — Criar tasks na lista com responsáveis

**USER_ID = {{CLICKUP_USER_ID}}** ({{NOME_OPERADOR}} — assignee obrigatório nas tasks que dependem dele)

Tasks que dependem do operador (assignee = {{CLICKUP_USER_ID}}):

| Task | Due date | Prio |
|---|---|---|
| 🎥 Lives de aquecimento — toda quarta | data_aquecimento → data_aviso_youtube | high |
| 📹 Gravar e publicar vídeo de aviso no YouTube | data_aviso_youtube | urgent |
| 📹 Gravar vídeo de convite pessoal (WhatsApp/email base) | data_abertura - 2 dias | urgent |
| ⚡ Ativar carrinho: `{SLUG}_CARRINHO_ABERTO=true` no Vercel | data_abertura | urgent |
| ⚡ Fechar carrinho: `{SLUG}_CARRINHO_FECHADO=true` no Vercel | data_fechamento | urgent |

Tasks do squad (sem assignee específico):

| Task | Due date | Status |
|---|---|---|
| ✅ Páginas criadas e estados configurados | — | complete (se já feito) |
| ✅ Redirect implementado | — | complete (se já feito) |
| 📧 Disparar para base no dia da abertura | data_abertura | — |
| 🎓 Primeira aula | data_primeira_aula | — |
| Se webinário: 🎙️ Webinário ao vivo | data_webinario | — |

Para tasks do tipo webinário, adicionar também:
- 📹 Gravar vídeo de aviso do webinário (uma semana antes)
- 📧 Sequência de emails/WhatsApp de lembrete do webinário

### Passo 4 — Criar registro canônico

Arquivo: `workspace/memory/lancamentos/{slug}.md`

```markdown
# Lançamento: {nome}
Criado: {hoje} | Status: planejado | Tipo: {tipo}
Lista ClickUp: https://app.clickup.com/{{CLICKUP_WORKSPACE_ID}}/v/l/6-{list_id}-1

## Produto
- Nome: {produto} | Preço: {preco} | Meta interna: {meta_vagas} vagas (NÃO divulgar)

## Datas
| Marco | Data |
|---|---|
| Início do aquecimento | {data_aquecimento} |
| Vídeo de aviso YouTube | {data_aviso_youtube} |
| Abertura do carrinho | {data_abertura} |
| Fechamento do carrinho | {data_fechamento} |
| Primeira aula | {data_primeira_aula ou "—"} |

## Páginas & Links
- Captura: {pagina_captura}
- Vendas: {pagina_vendas}
- Checkout: {link_checkout}

## Env vars Vercel
| Env var | Quando ativar | Efeito |
|---|---|---|
| `{SLUG}_CARRINHO_ABERTO=true` | {data_abertura} | Redirect → vendas |
| `{SLUG}_CARRINHO_FECHADO=true` | {data_fechamento} | Aviso fechado |
| `{SLUG}_SEGUNDA_CHANCE=true` | A definir | Redirect → vendas |

## Histórico
- {hoje}: criado por Jade
```

### Passo 5 — Gerar mapa visual TXT

Criar `workspace/memory/lancamentos/{slug}-mapa.txt` com diagrama ASCII completo do fluxo (tipo A ou B conforme `tipo`).

### Passo 6 — Atualizar estrategia-viva.md

Registrar na seção `### Lançamentos e datas`. Edição incremental.

### Passo 7 — Confirmar

```
✅ Lançamento [{nome}] organizado.

📋 Lista ClickUp: https://app.clickup.com/{{CLICKUP_WORKSPACE_ID}}/v/l/6-{list_id}-1

Depende de você:
- 🎥 Lives toda quarta de junho
- 📹 Gravar vídeo de aviso YouTube (até {data_aviso_youtube})
- 📹 Gravar vídeo de convite pessoal
- ⚡ Ativar carrinho no Vercel em {data_abertura}
- ⚡ Fechar carrinho no Vercel em {data_fechamento}

Squad resolve o resto.
```

---

## Regras

- **Nunca divulgar `meta_vagas` publicamente** — "vagas limitadas" sempre
- **GHL obrigatório** em todos os forms — nunca form sem GHL
- **Lista dedicada por lançamento** — nunca misturar tasks de lançamento na fila geral Tasks Jade COO
- **operador como assignee** em todas as tasks que dependem de ação pessoal dele
- **Mapa TXT obrigatório** em todo lançamento
- **Fonte de verdade do produto**: `segundo-cerebro/06-oferta/produtos-servicos.md`

---

## Histórico

- **02/06/2026** — v1: skill criada com aval operador. Estrutura básica.
- **02/06/2026** — v2: variantes direto/webinário, 4 estados de página, GHL obrigatório, mapa ASCII.
- **02/06/2026** — v3: lista dedicada por lançamento no ClickUp (não misturar com Tasks Jade COO), operador como assignee nas tasks que dependem dele. Motivação: "cada lançamento tem uma lista no ClickUp, mapeando todas as tasks. O que depender de mim, me marca como responsável."
