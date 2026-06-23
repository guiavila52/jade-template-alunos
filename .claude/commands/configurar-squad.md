---
name: configurar-squad
description: Skill onboarding pra aluno que clonou o squad-template. Faz perguntas estratégicas, substitui placeholders em todos os arquivos. Squad fica operacional pro negócio do aluno. Use UMA vez após git clone.
model: claude-sonnet-4-5
---

# /configurar-squad — onboarding do aluno

Você acabou de clonar `{{GITHUB_USER}}/squad-template`. Bem-vindo ao seu squad de agentes IA.

Esta skill faz **uma vez só** a configuração inicial: pergunta o que precisa saber sobre você e seu negócio, substitui placeholders, e deixa o squad operacional.

## RODAR APENAS UMA VEZ

Após rodar com sucesso, ela pode ser deletada. Rodar de novo NÃO causa dano (idempotente), mas não há porque.

## PRÉ-FLIGHT

Antes de tudo, garantir:

1. CWD = raiz do clone (existe `CLAUDE.md` + `AGENTS.md` + `.claude/commands/`)
2. Backup automático do estado atual:
   ```bash
   ts=$(date +%Y%m%d-%H%M%S)
   cp -R . ../squad-template-backup-$ts/ 2>/dev/null
   echo "Backup em ../squad-template-backup-$ts"
   ```
3. Detectar OS pra usar sed correto:
   ```bash
   if [[ "$OSTYPE" == "darwin"* ]]; then SED_I="-i ''"; else SED_I="-i"; fi
   ```

## Placeholders do template (auditado na criação)

O template usa 18 placeholders. Divididos em 3 tiers:

### TIER 1 — Obrigatórios (8 perguntas principais)

| Placeholder | Pergunta ao aluno | Exemplo | Validação |
|---|---|---|---|
| `{{NOME_OPERADOR}}` | Seu nome completo? | "João Silva" | não-vazio |
| `{{HANDLE_OPERADOR}}` | Seu @ no Instagram/Twitter (sem @)? | "joaosilva" | sem @ no início |
| `{{DOMINIO}}` | Seu domínio principal (sem https://)? | "joaosilva.com" | sem https:// |
| `{{USERNAME_MAC}}` | Seu username do Mac (rode `whoami`)? | "joaosilva" | não-vazio, sem espaços |
| `{{EMPRESA_PRINCIPAL}}` | Nome da sua empresa principal? | "Silva Holdings" | não-vazio |
| `{{PRODUTO_PRINCIPAL}}` | Nome do seu produto/negócio principal? | "Curso de Fotografia Pro" | não-vazio |
| `{{NOME_AGENTE_COO}}` | Nome do agente COO (default: Jade) | "Ana" | aceita vazio (usa Jade) |
| `{{CLICKUP_LIST_ID}}` | ID da lista ClickUp do COO (opcional — ver Pergunta 9) | "[seu-list-id]" | numérico ou "nao-usa" |
| `{{CLICKUP_WORKSPACE_ID}}` | ID do workspace ClickUp (auto-extraído da URL) | "[seu-workspace-id]" | numérico ou "nao-usa" |
| `{{NOME_OPERADOR_CURTO}}` | Seu primeiro nome ou apelido curto? | "João" | não-vazio |
| `{{DESCRICAO_OPERADOR}}` | Em 1 frase, o que você faz/é? | "especialista em tráfego pago" | não-vazio |
| `{{DESCRICAO_EMPRESA_1}}` | Descrição da sua empresa principal (1 linha)? | "agência de performance digital" | não-vazio |
| `{{CANAL_TOPO}}` | Qual canal de topo de funil você usa? | "YouTube" | não-vazio |
| `{{PRODUTO_ENTRADA}}` | Nome do seu produto de entrada/isca? | "Imersão Gratuita" | não-vazio |
| `{{PRODUTO_TOPO}}` | Nome do seu produto topo de funil (high-ticket)? | "Mentoria Individual" | não-vazio |
| `{{OBJETIVO_FINANCEIRO}}` | Sua meta financeira de curto prazo? | "R$ 50k de lucro mensal" | não-vazio |

### TIER 2 — Derivados automáticos (não perguntar)

| Placeholder | Como gerar | Exemplo |
|---|---|---|
| `{{DOMINIO_OPERADOR}}` | = {{DOMINIO}} | "joaosilva.com" |
| `{{DOMINIO_OPERADOR_REGEX}}` | escapar `.` do domínio | "joaosilva\\.com" |
| `{{AUTOR}}` | = {{NOME_OPERADOR}} | "João Silva" |
| `{{HANDLE}}` | = {{HANDLE_OPERADOR}} | "joaosilva" |
| `{{EMPRESA_GUARDA_CHUVA}}` | = {{EMPRESA_PRINCIPAL}} | "Silva Holdings" |

### TIER 3 — Produto de parceria (opcional, perguntar só se aplicável)

| Placeholder | Pergunta | Validação |
|---|---|---|
| `{{PRODUTO_PARCERIA}}` | Tem produto/empresa cofundada (diferente do principal)? Nome? | opcional, aceita vazio |
| `{{PRODUTO_PARCERIA_SLUG}}` | auto-gerar de PRODUTO_PARCERIA | lowercase, hífens |

### TIER 4 — Runtime (NÃO substituir aqui)

Estes são placeholders **dinâmicos** usados por skills e outros. Permanecem como estão:
- `{{TEXTO}}`, `{{FOTO_HTML}}`, `{{NUMERO}}`, `{{DATA}}`

## Fluxo de execução

```
[ 1. Pre-flight: cwd + backup + detect OS ]
       │
       ▼
[ 2. Fazer 7 perguntas obrigatórias + 1 condicional (ClickUp) ]
   uma por vez, com validação
       │
       ▼
[ 3. Gerar valores TIER 2 automaticamente ]
       │
       ▼
[ 4. Perguntar TIER 3 (produto parceria) — opcional ]
       │
       ▼
[ 5. Mostrar resumo + confirmar ]
   "Vou substituir X por Y em N arquivos. OK?"
       │
       ▼
[ 6. Aplicar substituições via sed ]
       │
       ▼
[ 7. Validar: placeholders restantes? ]
   (exceto {{TEXTO}}, {{NUMERO}}, etc — são runtime)
       │
       ▼
[ 8. Inicializar arquivos de estado ]
   PROGRESS.md, identidade.md
       │
       ▼
[ 9. Reportar sucesso + próximos passos ]
```

## Implementação técnica

### 1. Pre-flight

```bash
# Confirmar CWD válido
[[ -f CLAUDE.md && -f AGENTS.md ]] || { echo "Não está na raiz do squad-template"; exit 1; }

# Backup
ts=$(date +%Y%m%d-%H%M%S)
cp -R . ../squad-template-backup-$ts/ 2>/dev/null
echo "Backup em ../squad-template-backup-$ts"

# Detectar OS
if [[ "$OSTYPE" == "darwin"* ]]; then 
  SED_I="-i ''"
else 
  SED_I="-i"
fi
```

### 2. Coletar respostas (UMA pergunta por vez)

Não despejar perguntas de uma vez. Fazer conversacionalmente, no tom da Jade.
Atenção: o aluno pode ter enviado Instagram/YouTube/materiais na mensagem inicial —
EXTRAIR primeiro o que já foi enviado antes de perguntar de novo.

**Bloco A — Identidade básica (placeholders):**
1. "Qual o seu nome completo?"
2. "Qual seu @ no Instagram? (sem o @, só o nome)"
3. "Qual seu domínio principal? (ex: joaosilva.com, sem https://)"
4. "Qual o username do seu Mac? (rode `whoami` no terminal e me manda o resultado)"
5. "Nome da sua empresa principal?"
6. "Nome do seu produto ou negócio principal?"
7. "Como quer chamar seu agente COO? Padrão é Jade — pode manter ou escolher outro nome."
8. "Como as pessoas te chamam? (primeiro nome ou apelido — ex: João, JP)"
9. "Em uma frase, o que você faz?"
10. "Descreva sua empresa em 1 linha:"
11. "Qual é seu principal canal pra atrair audiência? (YouTube, Instagram, Podcast…)"
12. "Nome do seu produto de entrada ou isca?"
13. "Nome do seu produto high-ticket / topo de funil?"
14. "Qual é sua meta financeira de curto prazo?"

**Bloco B — Segundo Cérebro (perguntas adicionais para preencher os arquivos corretos):**

15. "Me manda o link do seu canal do YouTube (se tiver). Se não tiver, pode pular."
    → Guarda como YOUTUBE_URL

16. "Me manda exemplos do jeito que você escreve/fala — quanto mais, melhor. Pode ser: post do Instagram com legenda, vídeo do YouTube, artigo do LinkedIn, print de newsletter que você enviou, qualquer coisa que você produziu. Manda o link ou o texto direto aqui."
    → Ler os exemplos enviados, analisar padrões de linguagem, tom, estrutura
    → Extrair: vocabulário característico, nível de formalidade, ritmo, o que evita
    → Sintetizar em TOM_DE_VOZ_DESC baseado nos exemplos reais — não em autodefinição do aluno

17. "Quem é o cliente que você atende? Descreve em 3-4 linhas: quem é, qual dor tem, o que ele quer conquistar."
    → Guarda como ICP_DESC

18. "Tem documentos, páginas de vendas, PDFs ou qualquer material que descreva seus produtos/serviços? Me manda aqui."
    → Ler e extrair para os arquivos corretos (ver Passo 9)

Validações leves inline. Se resposta inválida → reformular UMA vez.

### 3. Gerar derivados automaticamente

```bash
DOMINIO_OPERADOR="$DOMINIO"
DOMINIO_OPERADOR_REGEX=$(echo "$DOMINIO" | sed 's/\./\\./g')
AUTOR="$NOME_OPERADOR"
HANDLE="$HANDLE_OPERADOR"
EMPRESA_GUARDA_CHUVA="$EMPRESA_PRINCIPAL"
NOME_AGENTE_COO="${NOME_AGENTE_COO:-Jade}"
```

### 4. Produto de parceria (opcional)

Perguntar: "Você tem outro produto/empresa cofundada (diferente do principal)? Se sim, qual o nome? Se não, deixe vazio ou escreva 'nenhum'"

Se não vazio:
```bash
PRODUTO_PARCERIA="[resposta]"
PRODUTO_PARCERIA_SLUG=$(echo "$PRODUTO_PARCERIA" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
```

Se vazio:
```bash
PRODUTO_PARCERIA="(não aplicável)"
PRODUTO_PARCERIA_SLUG="nenhum"
```

### 5. Confirmar resumo

Mostrar:
```
Vou substituir:
  {{NOME_OPERADOR}}          → João Silva
  {{HANDLE_OPERADOR}}        → joaosilva
  {{HANDLE}}                 → joaosilva
  {{DOMINIO}}                → joaosilva.com
  {{DOMINIO_OPERADOR}}       → joaosilva.com
  {{DOMINIO_OPERADOR_REGEX}} → joaosilva\.com
  {{USERNAME_MAC}}           → joaosilva
  {{EMPRESA_PRINCIPAL}}      → Silva Holdings
  {{EMPRESA_GUARDA_CHUVA}}   → Silva Holdings
  {{PRODUTO_PRINCIPAL}}      → Curso de Fotografia Pro
  {{NOME_AGENTE_COO}}        → Jade
  {{AUTOR}}                  → João Silva
  {{PRODUTO_PARCERIA}}       → (não aplicável)
  {{PRODUTO_PARCERIA_SLUG}}  → nenhum

Em todos os arquivos .md, .json, .ts, .astro, .html (exceto node_modules, .git, backups).

Backup já feito. Confirmar? (sim/não)
```

Só prosseguir após "sim".

### 6. Aplicar substituições

```bash
# Escapar valores pra sed (caracteres especiais: / & \)
escape_sed() {
  printf '%s' "$1" | sed -e 's/[\/&]/\\&/g'
}

NOME_OPERADOR_ESC=$(escape_sed "$NOME_OPERADOR")
NOME_OPERADOR_CURTO_ESC=$(escape_sed "$NOME_OPERADOR_CURTO")
DESCRICAO_OPERADOR_ESC=$(escape_sed "$DESCRICAO_OPERADOR")
DESCRICAO_EMPRESA_1_ESC=$(escape_sed "$DESCRICAO_EMPRESA_1")
CANAL_TOPO_ESC=$(escape_sed "$CANAL_TOPO")
PRODUTO_ENTRADA_ESC=$(escape_sed "$PRODUTO_ENTRADA")
PRODUTO_TOPO_ESC=$(escape_sed "$PRODUTO_TOPO")
OBJETIVO_FINANCEIRO_ESC=$(escape_sed "$OBJETIVO_FINANCEIRO")
HANDLE_OPERADOR_ESC=$(escape_sed "$HANDLE_OPERADOR")
DOMINIO_ESC=$(escape_sed "$DOMINIO")
DOMINIO_REGEX_ESC=$(escape_sed "$DOMINIO_OPERADOR_REGEX")
USERNAME_MAC_ESC=$(escape_sed "$USERNAME_MAC")
EMPRESA_PRINCIPAL_ESC=$(escape_sed "$EMPRESA_PRINCIPAL")
PRODUTO_PRINCIPAL_ESC=$(escape_sed "$PRODUTO_PRINCIPAL")
PRODUTO_PARCERIA_ESC=$(escape_sed "$PRODUTO_PARCERIA")
PRODUTO_PARCERIA_SLUG_ESC=$(escape_sed "$PRODUTO_PARCERIA_SLUG")
NOME_AGENTE_COO_ESC=$(escape_sed "$NOME_AGENTE_COO")
CLICKUP_LIST_ID_ESC=$(escape_sed "$CLICKUP_LIST_ID")
CLICKUP_WORKSPACE_ID_ESC=$(escape_sed "$CLICKUP_WORKSPACE_ID")

# Buscar todos arquivos relevantes
FILES=$(find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.ts" -o -name "*.astro" -o -name "*.html" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/_backup*" \
  -not -path "*/squad-template-backup*")

# Aplicar substituições (ordem importa: mais específico primeiro)
for file in $FILES; do
  sed $SED_I \
    -e "s/{{DOMINIO_OPERADOR_REGEX}}/$DOMINIO_REGEX_ESC/g" \
    -e "s/{{DOMINIO_OPERADOR}}/$DOMINIO_ESC/g" \
    -e "s/{{DOMINIO}}/$DOMINIO_ESC/g" \
    -e "s/{{HANDLE_OPERADOR}}/$HANDLE_OPERADOR_ESC/g" \
    -e "s/{{HANDLE}}/$HANDLE_OPERADOR_ESC/g" \
    -e "s/{{NOME_OPERADOR}}/$NOME_OPERADOR_ESC/g" \
    -e "s/{{AUTOR}}/$NOME_OPERADOR_ESC/g" \
    -e "s/{{EMPRESA_GUARDA_CHUVA}}/$EMPRESA_PRINCIPAL_ESC/g" \
    -e "s/{{EMPRESA_PRINCIPAL}}/$EMPRESA_PRINCIPAL_ESC/g" \
    -e "s/{{PRODUTO_PRINCIPAL}}/$PRODUTO_PRINCIPAL_ESC/g" \
    -e "s/{{NOME_AGENTE_COO}}/$NOME_AGENTE_COO_ESC/g" \
    -e "s/{{CLICKUP_LIST_ID}}/$CLICKUP_LIST_ID_ESC/g" \
    -e "s/{{CLICKUP_WORKSPACE_ID}}/$CLICKUP_WORKSPACE_ID_ESC/g" \
    -e "s/{{USERNAME_MAC}}/$USERNAME_MAC_ESC/g" \
    -e "s/{{PRODUTO_PARCERIA_SLUG}}/$PRODUTO_PARCERIA_SLUG_ESC/g" \
    -e "s/{{PRODUTO_PARCERIA}}/$PRODUTO_PARCERIA_ESC/g" \
    -e "s/{{NOME_OPERADOR_CURTO}}/$NOME_OPERADOR_CURTO_ESC/g" \
    -e "s/{{DESCRICAO_OPERADOR}}/$DESCRICAO_OPERADOR_ESC/g" \
    -e "s/{{DESCRICAO_EMPRESA_1}}/$DESCRICAO_EMPRESA_1_ESC/g" \
    -e "s/{{CANAL_TOPO}}/$CANAL_TOPO_ESC/g" \
    -e "s/{{PRODUTO_ENTRADA}}/$PRODUTO_ENTRADA_ESC/g" \
    -e "s/{{PRODUTO_TOPO}}/$PRODUTO_TOPO_ESC/g" \
    -e "s/{{OBJETIVO_FINANCEIRO}}/$OBJETIVO_FINANCEIRO_ESC/g" \
    "$file"
done

echo "Substituições aplicadas em $(echo "$FILES" | wc -l) arquivos"
```

### 7. Validação pós-execução

```bash
# Buscar placeholders restantes (exceto os de runtime)
REMAINING=$(grep -rE '{{[A-Z_]+}}' . \
  --include='*.md' --include='*.json' --include='*.ts' --include='*.astro' --include='*.html' \
  2>/dev/null \
  | grep -vE '({{TEXTO}}|{{FOTO_HTML}}|{{NUMERO}}|{{DATA}})' \
  | head -20)

if [[ -z "$REMAINING" ]]; then
  echo "Sem placeholders remanescentes (exceto runtime)."
else
  echo "Placeholders ainda presentes:"
  echo "$REMAINING"
  echo ""
  echo "Quer informar valores pra esses agora?"
fi
```

### 8. Inicializar arquivos do Segundo Cérebro

**REGRA CRÍTICA: NUNCA criar arquivos novos. Sempre usar os arquivos que já existem.**

Mapa obrigatório — informação → arquivo correto:

| O que preencher | Arquivo existente | Fonte |
|---|---|---|
| Identidade completa | `segundo-cerebro/01-identidade/identidade.md` | Respostas 1-10 |
| Tom de voz | `segundo-cerebro/01-identidade/tom-de-voz.md` | Resposta 16 + análise |
| ICP / cliente ideal | `segundo-cerebro/05-audiencia/icp.md` | Resposta 17 |
| Produtos e serviços | `segundo-cerebro/06-oferta/produtos-servicos.md` | Respostas 6, 12, 13 + docs |
| Canal YouTube | `segundo-cerebro/02-negocios/canal-youtube.md` | Resposta 15 |
| Ofertas e funil | `segundo-cerebro/06-oferta/ofertas.md` | Respostas 11, 12, 13 |

Se o aluno não tiver info pra preencher algum arquivo, deixar o arquivo como está (com os campos em branco marcados com `_`). Não apagar, não criar arquivo novo.

Escrever em cada arquivo assim:

```bash
# identidade.md
cat > "segundo-cerebro/01-identidade/identidade.md" << EOF
# Identidade — $NOME_OPERADOR

## Quem é o operador
$NOME_OPERADOR — $DESCRICAO_OPERADOR

## Empresas
- $EMPRESA_PRINCIPAL: $DESCRICAO_EMPRESA_1

## Produto principal
$PRODUTO_PRINCIPAL

## Contato e presença
- Instagram: @$HANDLE_OPERADOR
- Domínio: $DOMINIO

## Meta financeira
$OBJETIVO_FINANCEIRO

Configurado em $(date +%Y-%m-%d).
EOF

# tom-de-voz.md — só preencher se TOM_DE_VOZ_DESC não estiver vazio
if [[ -n "$TOM_DE_VOZ_DESC" ]]; then
  cat > "segundo-cerebro/01-identidade/tom-de-voz.md" << EOF
# Tom de Voz — $NOME_OPERADOR

## Como escreve
$TOM_DE_VOZ_DESC

## Canal principal
$CANAL_TOPO — @$HANDLE_OPERADOR

## O que é característico
_(completar conforme mais exemplos forem aparecendo)_

## O que é banido
_(completar conforme correções do operador)_

Configurado em $(date +%Y-%m-%d).
EOF
fi

# canal-youtube.md — só preencher se YOUTUBE_URL não estiver vazio
if [[ -n "$YOUTUBE_URL" ]]; then
  cat > "segundo-cerebro/02-negocios/canal-youtube.md" << EOF
# Canal YouTube — $NOME_OPERADOR

## URL do canal
$YOUTUBE_URL

## Posicionamento do canal
_(extrair da análise dos vídeos ou do que o operador descreveu)_

## Tipos de vídeo que publica
_(completar conforme análise)_

## CTA padrão dos vídeos
_(completar conforme análise)_

Configurado em $(date +%Y-%m-%d).
EOF
fi

# icp.md (05-audiencia) — só preencher se ICP_DESC não estiver vazio
if [[ -n "$ICP_DESC" ]]; then
  cat > "segundo-cerebro/05-audiencia/icp.md" << EOF
# Perfil do Cliente Ideal (ICP) — $NOME_OPERADOR

## Quem é
$ICP_DESC

## Dores principais
_(completar conforme mais info)_

## Sonhos
_(completar conforme mais info)_

## Como fala
_(completar conforme exemplos reais)_

Configurado em $(date +%Y-%m-%d).
EOF
fi

# produtos-servicos.md — preencher com o que já se sabe (NUNCA criar "produtos.md")
cat > "segundo-cerebro/06-oferta/produtos-servicos.md" << EOF
# Produtos e Serviços — $NOME_OPERADOR

## Produto principal
$PRODUTO_PRINCIPAL

## Produto de entrada / isca
$PRODUTO_ENTRADA

## High-ticket / topo de funil
$PRODUTO_TOPO

## Detalhes adicionais
_(completar com materiais enviados pelo operador)_

Configurado em $(date +%Y-%m-%d).
EOF

# ofertas.md — preencher com estrutura do funil
cat > "segundo-cerebro/06-oferta/ofertas.md" << EOF
# Estrutura de Ofertas e Funil — $NOME_OPERADOR

## Topo (geração de audiência)
Canal: $CANAL_TOPO

## Meio (qualificação e aquecimento)
Isca/entrada: $PRODUTO_ENTRADA

## Fundo (conversão)
High-ticket: $PRODUTO_TOPO

## Ascensão
_(completar conforme evolução do funil)_

Configurado em $(date +%Y-%m-%d).
EOF

echo "Segundo Cérebro inicializado."
```

Após escrever os arquivos, confirmar para o aluno: "Preenchido: [lista dos arquivos preenchidos]. Vazio por falta de info: [lista]."

### 9. Processar documentos enviados pelo aluno

Se o aluno mandou documentos (página de vendas, PDF, texto sobre produtos, etc.):

1. **Ler o conteúdo** de cada documento
2. **Extrair e escrever nos arquivos EXISTENTES corretos** (nunca criar arquivo novo):

| Tipo de conteúdo encontrado | Arquivo existente pra atualizar |
|---|---|
| Descrição de produto, preço, formato | `segundo-cerebro/06-oferta/produtos-servicos.md` |
| Funil, jornada do cliente, ofertas | `segundo-cerebro/06-oferta/ofertas.md` |
| Tom de voz, exemplos de copy | `segundo-cerebro/01-identidade/tom-de-voz.md` |
| Quem é o cliente ideal, dores, sonhos | `segundo-cerebro/05-audiencia/icp.md` |
| Ferramentas, plataformas usadas | `segundo-cerebro/03-operacao/ferramentas.md` |
| Estratégia atual, prioridades | `segundo-cerebro/04-decisoes/estrategia-atual.md` |
| Concorrentes, diferenciais | `segundo-cerebro/02-negocios/concorrentes.md` |

3. **Nunca criar** `produtos.md`, `servicos.md`, `meu-negocio.md` ou qualquer arquivo fora do mapa acima
4. **Confirmar** quais arquivos foram preenchidos e com o quê — em lista curta, sem jargão

Se o aluno não tiver documentos agora:
- Dizer que tudo bem, pode mandar depois a qualquer hora
- Confirmar o que já foi preenchido com as respostas dadas

### 10. Output final

```
Squad pronto pra operar, [NOME_OPERADOR]!

Segundo Cérebro inicializado em segundo-cerebro/01-identidade/identidade.md
[listar outras pastas preenchidas se houver]

Próximos passos:
1. Chame /jade-iniciar pra abrir sua primeira sessão
2. Complete o Segundo Cérebro com seus documentos (arrasta pro chat a qualquer hora)
[Se configurou ClickUp]: 3. Crie algumas tasks em Tasks [NOME_COO] COO pra testar o /listar-pendencias

Bom uso!
```

## Restrições

- **Idempotente** — rodar 2x não corrompe (só perde tempo)
- **Validações leves** — handle sem @, domínio sem https://, username sem espaços
- **Modo "preview"** ANTES de aplicar — mostra resumo, pede OK
- **Backup automático obrigatório** — `cp -R` antes de aplicar
- **macOS-friendly** — sed -i '' com aspas vazias (detectar OS)
- **Escapar valores** com caracteres especiais antes de passar pro sed
- **Não tocar .git/, node_modules/, dist/, backups**
- **Ordem das substituições importa** — mais específico primeiro (DOMINIO_OPERADOR_REGEX antes de DOMINIO_OPERADOR antes de DOMINIO)

## Como saber que funcionou

- Operador consegue chamar `/jade` e ela responde com nome dele
- `grep -rE '{{[A-Z_]+}}' .` retorna só placeholders de runtime (TEXTO, NUMERO, etc)
- Sem nada sensível do operador anterior remanescente (exceto em exemplos/comentários)
