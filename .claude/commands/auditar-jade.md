<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /auditar-jade — Red team adversarial do template público

Roda **auditoria adversarial completa** do repo público `{{GITHUB_USER}}/jade` pra garantir ZERO vazamentos de dados sensíveis. Clona fresh do GitHub, aplica 13 categorias de validação (mesmas usadas no red team que encontrou 78 vazamentos em 18/05/2026), gera relatório, alerta se achar regressão.

## Quando rodar

- **Antes de divulgar pros alunos** (validação final pré-lançamento)
- **Semanalmente** (rotina automática via `/schedule` — recomendado)
- **Após cada `/publicar-jade`** (validação pós-sync — obrigatório)
- **Após qualquer mudança suspeita** no squad principal que possa vazar (criar feedback novo, adicionar MCP, mudar settings.json)
- **Manualmente** quando o operador quiser confiança

## Comportamento

1. Clone fresh do repo público em `/tmp/auditar-jade-{timestamp}/`
2. Roda 13 grupos de checagem adversarial
3. Gera relatório `workspace/output/auditorias/YYYY-MM-DD-auditar-jade.md`
4. Saída:
   - ✅ ZERO vazamentos → "Template limpo, sem ação necessária"
   - ❌ N vazamentos → relatório detalhado + sugestão de correção
5. Limpa o clone temp ao final

## 13 grupos de validação (adversarial)

| # | Categoria | Pattern | O que protege |
|---|---|---|---|
| 1 | Nome operador | `\bgui\s?[áa]vila\b\|\bguiavila\b` | Nome próprio do dono do squad |
| 2 | Paths absolutos | `/Users/[a-z]+` ou `/home/[a-z]+` | Username do sistema operacional |
| 3 | Nomes pessoais | `Luiz Fosc\|{{NOME_SUPORTE}}\|{{NOME_PARCEIRO_PLATAFORMA}}\|\|{{NOME_BACKUP_ADMIN}}\|{{CONTADORA}}\|cliente_exemplo` | Parceiros, suporte, clientes |
| 4 | Empresas reais | `{{EMPRESA_COFUNDADA}}\|{{EMPRESA_HOLDING}}\|{{EMPRESA_NEGOCIO}}\|{{plataforma_conteudo}}` (case insensitive, não-placeholder) | Empresas do operador |
| 5 | ClickUp Task IDs | `\b86[a-z0-9]{7,8}\b` | IDs rastreáveis de tasks internas |
| 6 | MCP privados | `armavita` (e qualquer outro registrado) | MCP servers proprietários |
| 7 | Emails reais | `@(gmail\|hotmail\|outlook)\.com` (exceto `@exemplo`) | Endereços reais |
| 8 | CNPJs reais | `[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}` (exceto `00.000.000`) | Documentos fiscais reais |
| 9 | Workspace IDs | `\b30978229\b` (e outros IDs ClickUp/{{PLATAFORMA_NF}}) | Identificadores de contas externas |
| 10 | Skills só do operador | `consultar-nf\|publicar-{{plataforma_conteudo}}\|responder-{{suporte}}\|tweet-imagem\|analisar-fiscal` | Skills que não fazem sentido pro aluno |
| 11 | API tokens | `sk_(test\|live)_\|pk_[A-Za-z0-9]{20,}\|AKIA[A-Z0-9]{16}\|ghp_\|github_pat_` | Chaves de API expostas |
| 12 | Arquivos perigosos | `.mcp.json\|feedback_*.md\|*.preFix*\|*.bak*\|.secrets.baseline` | Arquivos que vazam config privada |
| 13 | Docs de produtos paralelos | `\b(PRD\|business-rules\|database\|integrations)\.md\b` | Documentação de apps internos |

## Implementação

```bash
#!/bin/bash
set -e
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
CLONE_DIR="/tmp/auditar-jade-$TIMESTAMP"
REPORT_DIR="workspace/output/auditorias"
REPORT_FILE="$REPORT_DIR/$TIMESTAMP-auditar-jade.md"

mkdir -p "$REPORT_DIR"

echo "=== /auditar-jade — clone fresh do repo público ==="
git clone --depth=1 https://github.com/{{GITHUB_USER}}/jade.git "$CLONE_DIR" 2>&1 | tail -2
cd "$CLONE_DIR"

# Inicializar contadores
declare -A CHECKS

# 1. Nome operador
CHECKS[1_nome_operador]=$(grep -rEi '\bgui\s?[áa]vila\b|\bguiavila\b' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 2. Paths absolutos
CHECKS[2_paths_users]=$(grep -rE '/Users/[a-z]+|/home/[a-z]+' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 3. Nomes pessoais (HARDCODED — atualizar se mudar quem opera o squad principal)
CHECKS[3_nomes_pessoais]=$(grep -rE '\b(Luiz Fosc|{{NOME_SUPORTE}}|{{NOME_PARCEIRO_PLATAFORMA}}||{{NOME_BACKUP_ADMIN}}|{{CONTADORA}}|cliente_exemplo)\b' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 4. Empresas reais
CHECKS[4_empresas]=$(grep -rEi '\b({{lms_slug}}|fatorial|magica online|magica_online|{{plataforma_conteudo}})\b' . 2>/dev/null | grep -v '{{' | grep -v '.git/' | wc -l | tr -d ' ')

# 5. ClickUp Task IDs
CHECKS[5_clickup_ids]=$(grep -rE '\b86[a-z0-9]{7,8}\b' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 6. MCP privados
CHECKS[6_mcp_privado]=$(grep -rEi 'armavita' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 7. Emails reais
CHECKS[7_emails]=$(grep -rE '@(gmail|hotmail|outlook)\.com' . 2>/dev/null | grep -v '@exemplo' | grep -v '.git/' | wc -l | tr -d ' ')

# 8. CNPJs reais
CHECKS[8_cnpj]=$(grep -rE '[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}' . 2>/dev/null | grep -v '00\.000\.000' | grep -v '.git/' | wc -l | tr -d ' ')

# 9. Workspace IDs externos (atualizar lista se mudar)
CHECKS[9_workspace_ids]=$(grep -rE '\b30978229\b|\b{{META_AD_ACCOUNT_ID}}\b|\b{{META_APP_ID}}\b|\b{{META_BM_ID}}\b' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 10. Skills só do operador
CHECKS[10_skills_operador]=$(grep -rE 'consultar-nf|publicar-{{plataforma_conteudo}}|responder-{{suporte}}|tweet-imagem|analisar-fiscal' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 11. API tokens
CHECKS[11_api_tokens]=$(grep -rE 'sk_(test|live)_[a-zA-Z0-9]{10,}|pk_[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# 12. Arquivos perigosos (existência, não conteúdo)
CHECKS[12_arquivos_perigosos]=$(find . \( -name '.mcp.json' -o -name 'feedback_*.md' -o -name '*.preFix*' -o -name '*.bak*' -o -name '.secrets.baseline' -o -name '*.preMigracao*' -o -name '*.preFase*' \) 2>/dev/null | wc -l | tr -d ' ')

# 13. Docs de produtos paralelos
CHECKS[13_docs_paralelos]=$(grep -rE '\b(PRD|business-rules|database|integrations)\.md\b' . 2>/dev/null | grep -v '.git/' | wc -l | tr -d ' ')

# Total
TOTAL=0
for k in "${!CHECKS[@]}"; do
  TOTAL=$((TOTAL + ${CHECKS[$k]}))
done

# Gerar relatório
{
  echo "# Auditoria adversarial — {{GITHUB_USER}}/jade"
  echo ""
  echo "**Data:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "**Commit auditado:** $(git rev-parse --short HEAD)"
  echo "**URL:** https://github.com/{{GITHUB_USER}}/jade"
  echo ""
  echo "## Resultado"
  echo ""
  if [ "$TOTAL" = "0" ]; then
    echo "✅✅✅ **TEMPLATE 100% LIMPO** — ZERO vazamentos"
  else
    echo "❌ **REGRESSÃO DETECTADA** — $TOTAL refs sensíveis no template público"
    echo ""
    echo "**Ação obrigatória:** correr `/publicar-jade` pra re-sanitizar + force push. NÃO deixar nesse estado."
  fi
  echo ""
  echo "## Detalhamento por categoria"
  echo ""
  echo "| # | Categoria | Vazamentos | Status |"
  echo "|---|---|---|---|"
  for k in $(echo "${!CHECKS[@]}" | tr ' ' '\n' | sort); do
    count=${CHECKS[$k]}
    name=$(echo "$k" | sed 's/^[0-9]*_//' | tr '_' ' ')
    status=$([ "$count" = "0" ] && echo "✅" || echo "❌")
    num=$(echo "$k" | grep -oE '^[0-9]+')
    echo "| $num | $name | $count | $status |"
  done
  echo ""
  echo "## Detalhamento de vazamentos (se houver)"
  echo ""
  if [ "$TOTAL" != "0" ]; then
    echo '```'
    grep -rEi '\bgui\s?[áa]vila\b|/Users/[a-z]+|Luiz Fosc|{{NOME_SUPORTE}}|\b{{lms_slug}}\b|\bfatorial\b|\b{{plataforma_conteudo}}\b|\b86[a-z0-9]{7,8}\b|armavita|consultar-nf|publicar-{{plataforma_conteudo}}|responder-{{suporte}}|\b(PRD|business-rules|database|integrations)\.md\b' . 2>/dev/null | grep -v '.git/' | grep -v '{{' | head -20
    echo '```'
  else
    echo "_Nenhum vazamento detectado._"
  fi
  echo ""
  echo "## Stats do template"
  echo ""
  echo "- Arquivos: $(find . -type f -not -path './.git/*' | wc -l | tr -d ' ')"
  echo "- Tamanho: $(du -sh . 2>/dev/null | awk '{print $1}')"
  echo "- Skills: $(find .claude/commands -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  echo "- Agentes: $(find .claude/agents -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  echo ""
  echo "## Próximo passo"
  echo ""
  if [ "$TOTAL" = "0" ]; then
    echo "Nada. Voltar daqui 1 semana ou após próximo `/publicar-jade`."
  else
    echo "1. Identificar QUAL arquivo do squad principal vazou (rodar grep equivalente no squad local)"
    echo "2. Sanitizar no squad principal"
    echo "3. Rodar `/publicar-jade` pra re-sync + force push"
    echo "4. Re-rodar `/auditar-jade` pra confirmar correção"
  fi
} > "$OLDPWD/$REPORT_FILE"

# Output pro usuário
cd "$OLDPWD"
echo ""
if [ "$TOTAL" = "0" ]; then
  echo "✅ Template público 100% limpo — $TOTAL vazamentos"
else
  echo "❌ REGRESSÃO — $TOTAL vazamentos detectados"
  echo "Categorias afetadas:"
  for k in $(echo "${!CHECKS[@]}" | tr ' ' '\n' | sort); do
    [ "${CHECKS[$k]}" != "0" ] && echo "  - $(echo $k | sed 's/^[0-9]*_//') (${CHECKS[$k]} matches)"
  done
fi
echo ""
echo "📋 Relatório: $REPORT_FILE"

# Limpar clone
rm -rf "$CLONE_DIR"
```

## Output esperado

```
=== /auditar-jade — clone fresh do repo público ===
Cloning into '/tmp/auditar-jade-2026-05-18-201234'...

✅ Template público 100% limpo — 0 vazamentos

📋 Relatório: workspace/output/auditorias/2026-05-18-201234-auditar-jade.md
```

OU (se achou vazamento):

```
❌ REGRESSÃO — 3 vazamentos detectados
Categorias afetadas:
  - paths users (1 matches)
  - clickup ids (2 matches)

📋 Relatório: workspace/output/auditorias/2026-05-18-201234-auditar-jade.md
```

## Restrições

- **Read-only** no repo público (só clona, não mexe)
- **NÃO faz auto-fix** — apenas alerta. Correção via `/publicar-jade` manual.
- **Clone fresh sempre** — não confiar em cache local (que pode estar desatualizado)
- **Bypass DCG nem precisa** — só faz `git clone`, não push
- **Output em `workspace/output/auditorias/`** (gitignored — não vai pro template)

## Ampliar lista de patterns

Quando descobrir novo dado sensível (ex: cliente novo, parceiro novo, MCP novo, conta nova), ADICIONAR aos 13 grupos acima. Princípio: **se vazou uma vez, nunca mais** (Regra §5).

## Histórico

- **2026-05-18:** Skill criada após red team encontrar 78 vazamentos em primeira publicação do `{{GITHUB_USER}}/jade` (PRD, paths absolutos, Luiz Fosc, ClickUp IDs, memórias `feedback_*.md`, MCP `armavita`, etc). Decisão Gui: "Eu quero que você crie uma skill pra eu rodar ela de tempos em tempos pra garantir que é uma auditoria completa."

## Como agendar pra rodar semanal

```
/schedule "weekly /auditar-jade"
```

Auditoria roda toda semana, sem precisar lembrar.
