---
name: configurar-squad
description: Skill onboarding pra aluno que clonou o squad-template. Faz perguntas estratégicas, substitui placeholders em todos os arquivos. Squad fica operacional pro negócio do aluno. Use UMA vez após git clone.
model: claude-sonnet-4-5
---

# /configurar-squad — onboarding do aluno

Você acabou de clonar `{{GITHUB_USER}}/squad-template`. Bem-vindo ao seu squad de agentes IA.

Esta skill faz **uma vez só** a configuração inicial: pergunta o que precisa saber sobre você e seu negócio, substitui placeholders, e deixa o squad operacional.

## ⚠️ RODAR APENAS UMA VEZ

Após rodar com sucesso, ela pode ser deletada. Rodar de novo NÃO causa dano (idempotente), mas não há porque.

## ⚠️ PRÉ-FLIGHT

Antes de tudo, garantir:

1. CWD = raiz do clone (existe `CLAUDE.md` + `AGENTS.md` + `.claude/commands/`)
2. Backup automático do estado atual:
   ```bash
   ts=$(date +%Y%m%d-%H%M%S)
   cp -R . ../squad-template-backup-$ts/ 2>/dev/null
   echo "✅ Backup em ../squad-template-backup-$ts"
   ```
3. Detectar OS pra usar sed correto:
   ```bash
   if [[ "$OSTYPE" == "darwin"* ]]; then SED_I="-i ''"; else SED_I="-i"; fi
   ```

## Placeholders do template REAL (auditado 12/05/2026)

O template usa 18 placeholders. Divididos em 3 tiers:

### TIER 1 — Obrigatórios (7 perguntas principais)

| Placeholder | Pergunta ao aluno | Exemplo | Validação |
|---|---|---|---|
| `{{NOME_OPERADOR}}` | Seu nome completo? | "João Silva" | não-vazio |
| `{{HANDLE_OPERADOR}}` | Seu @ no Instagram/Twitter (sem @)? | "joaosilva" | sem @ no início |
| `{{DOMINIO}}` | Seu domínio principal (sem https://)? | "joaosilva.com" | sem https:// |
| `{{USERNAME_MAC}}` | Seu username do Mac (rode `whoami`)? | "joaosilva" | não-vazio, sem espaços |
| `{{EMPRESA_PRINCIPAL}}` | Nome da sua empresa principal? | "Silva Holdings" | não-vazio |
| `{{PRODUTO_PRINCIPAL}}` | Nome do seu produto/negócio principal? | "Curso de Fotografia Pro" | não-vazio |
| `{{COFUNDADOR}}` | Tem cofundador? Nome completo (ou "nenhum") | "Maria Costa" ou "nenhum" | aceita "nenhum" |

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

Estes são placeholders **dinâmicos** usados pela skill `/gerar-imagem` e outros. Permanecem como estão:
- `{{TEXTO}}`, `{{FOTO_HTML}}`, `{{NUMERO}}`, `{{DATA}}`

## Fluxo de execução

```
[ 1. Pre-flight: cwd + backup + detect OS ]
       │
       ▼
[ 2. Fazer 7 perguntas (TIER 1) ]
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
   PROGRESS.md, pendencias.md, identidade.md
       │
       ▼
[ 9. Reportar sucesso + próximos passos ]
```

## Implementação técnica

### 1. Pre-flight

```bash
# Confirmar CWD válido
[[ -f CLAUDE.md && -f AGENTS.md ]] || { echo "❌ Não está na raiz do squad-template"; exit 1; }

# Backup
ts=$(date +%Y%m%d-%H%M%S)
cp -R . ../squad-template-backup-$ts/ 2>/dev/null
echo "✅ Backup em ../squad-template-backup-$ts"

# Detectar OS
if [[ "$OSTYPE" == "darwin"* ]]; then 
  SED_I="-i ''"
else 
  SED_I="-i"
fi
```

### 2. Coletar respostas (UMA pergunta por vez)

Não despejar 7 perguntas de uma vez. Fazer conversacionalmente:

1. "Qual o seu nome completo?"
2. "Qual seu @ no Instagram/Twitter? (sem o @, só o nome)"
3. "Qual seu domínio principal? (ex: joaosilva.com, sem https://)"
4. "Rode `whoami` no terminal do seu Mac e me diga o resultado"
5. "Nome da sua empresa principal?"
6. "Nome do seu produto/negócio principal?"
7. "Tem cofundador? Se sim, nome completo. Se não, escreva 'nenhum'"

Validações leves inline. Se resposta inválida → reformular UMA vez.

### 3. Gerar derivados automaticamente

```bash
DOMINIO_OPERADOR="$DOMINIO"
DOMINIO_OPERADOR_REGEX=$(echo "$DOMINIO" | sed 's/\./\\./g')
AUTOR="$NOME_OPERADOR"
HANDLE="$HANDLE_OPERADOR"
EMPRESA_GUARDA_CHUVA="$EMPRESA_PRINCIPAL"
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
  {{COFUNDADOR}}             → Maria Costa
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
HANDLE_OPERADOR_ESC=$(escape_sed "$HANDLE_OPERADOR")
DOMINIO_ESC=$(escape_sed "$DOMINIO")
DOMINIO_REGEX_ESC=$(escape_sed "$DOMINIO_OPERADOR_REGEX")
USERNAME_MAC_ESC=$(escape_sed "$USERNAME_MAC")
EMPRESA_PRINCIPAL_ESC=$(escape_sed "$EMPRESA_PRINCIPAL")
PRODUTO_PRINCIPAL_ESC=$(escape_sed "$PRODUTO_PRINCIPAL")
COFUNDADOR_ESC=$(escape_sed "$COFUNDADOR")
PRODUTO_PARCERIA_ESC=$(escape_sed "$PRODUTO_PARCERIA")
PRODUTO_PARCERIA_SLUG_ESC=$(escape_sed "$PRODUTO_PARCERIA_SLUG")

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
    -e "s/{{COFUNDADOR}}/$COFUNDADOR_ESC/g" \
    -e "s/{{USERNAME_MAC}}/$USERNAME_MAC_ESC/g" \
    -e "s/{{PRODUTO_PARCERIA_SLUG}}/$PRODUTO_PARCERIA_SLUG_ESC/g" \
    -e "s/{{PRODUTO_PARCERIA}}/$PRODUTO_PARCERIA_ESC/g" \
    "$file"
done

echo "✅ Substituições aplicadas em $(echo "$FILES" | wc -l) arquivos"
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
  echo "✅ Sem placeholders remanescentes (exceto runtime)."
else
  echo "⚠️ Placeholders ainda presentes:"
  echo "$REMAINING"
  echo ""
  echo "Quer informar valores pra esses agora?"
fi
```

### 8. Inicializar arquivos de estado

```bash
# PROGRESS.md (se não existir)
[[ -f PROGRESS.md ]] || cat > PROGRESS.md << EOF
# PROGRESS — Squad de $NOME_OPERADOR

Squad configurado em $(date +%Y-%m-%d).

Próximas tarefas: ver workspace/memory/pendencias.md
EOF

# workspace/memory/pendencias.md — adicionar primeira entry
mkdir -p workspace/memory
cat >> workspace/memory/pendencias.md << EOF

## #1 — Setup inicial concluído
Squad configurado via /configurar-squad em $(date +%Y-%m-%d).
Operador: $NOME_OPERADOR
Empresa: $EMPRESA_PRINCIPAL
Produto: $PRODUTO_PRINCIPAL
Próximo passo sugerido: invocar /jade pra começar a operar.
Status: entregue
EOF

# segundo-cerebro/01-identidade/identidade.md — preencher básico
mkdir -p "segundo-cerebro/01-identidade"
cat > "segundo-cerebro/01-identidade/identidade.md" << EOF
# Identidade — $NOME_OPERADOR

## Básico

- Nome: $NOME_OPERADOR
- Handle: @$HANDLE_OPERADOR
- Domínio: $DOMINIO
- Empresa principal: $EMPRESA_PRINCIPAL
- Produto principal: $PRODUTO_PRINCIPAL
- Cofundador: $COFUNDADOR

Squad configurado em $(date +%Y-%m-%d).
EOF

echo "✅ Arquivos de estado inicializados"
```

### 9. Output final

```
✅ Squad configurado pra $NOME_OPERADOR ($EMPRESA_PRINCIPAL).

Backup do estado original: ../squad-template-backup-$ts/

Próximos passos:
1. Inicie sessão chamando: /jade
2. Veja sua agenda: /ver-agenda
3. Pra criar uma página: /criar-pagina-nova
4. Pra criar carrossel: /criar-carrossel

Skills disponíveis: ver lista em CLAUDE.md.

Squad operacional. Bom uso!
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

- Aluno consegue chamar `/jade` e ela responde com nome dele
- `grep -rE '{{[A-Z_]+}}' .` retorna só placeholders de runtime (TEXTO, NUMERO, etc)
- Sem nada de "{{NOME_OPERADOR}}", "{{GITHUB_USER}}", "{{EMPRESA_COFUNDADA}}", "{{EMPRESA_NEGOCIO}}" remanescente (exceto em exemplos/comentários)

## Lições aplicadas

- `feedback_decisoes_operacionais_jade.md` — pergunta SÓ inputs que SÓ o aluno pode dar
- `feedback_sem_jargao.md` — linguagem clara, sem termos novos
- `project_jornada_cliente_reverso.md` — esta skill é a fronteira aluno → squad operacional
- `feedback_proibido_excluir_repos.md` — backup obrigatório antes de aplicar
- `feedback_salvar_info_automaticamente.md` — toda info nova do aluno vira memória/identidade
