# Histórico de Atualizações — Template Alunos

Registro obrigatório (§18) de todas as alterações no template público.

---

## 2026-05-28 — Propagação nova estrutura segundo-cerebro (10 pastas)

- Adicionadas 5 novas pastas ao `segundo-cerebro/`: `06-oferta/`, `07-conteudo/`, `08-integracoes/`, `09-financeiro/`, `10-conhecimento/`
- Cada pasta recebeu `mapa.md` genérico com placeholders (sem conteúdo real)
- `segundo-cerebro/mapa.md` raiz atualizado para refletir estrutura de 10 pastas
- Motivação: alinhamento com reestruturação do projeto pessoal (5 → 10 pastas temáticas)
- Arquivos alterados: `segundo-cerebro/mapa.md`, `segundo-cerebro/06-oferta/mapa.md`, `segundo-cerebro/07-conteudo/mapa.md`, `segundo-cerebro/08-integracoes/mapa.md`, `segundo-cerebro/09-financeiro/mapa.md`, `segundo-cerebro/10-conhecimento/mapa.md`

## 2026-05-28 21:41 — Sanitização cirúrgica de slugs pessoais em 13 skills/agentes

**Motivação:** Auditoria revelou que 13 arquivos de skills e o agente `analista-qa.md` haviam sido portados para o template ANTES da criação da skill `/portar-para-template` (25/05/2026). Esses arquivos entraram via sync regex que só conhecia nomes/emails, mas não slugs de produtos (reverso, clickup8x, automacoes, magicaonline, imersao, sistema-reverso), URLs com "gui-avila" literal, e o sobrenome "Ávila" em paths absolutos.

**Arquivos alterados (sanitizados):**
- `.claude/commands/escrever-copy.md` — /imersao adicional encontrado pós-sessão anterior
- `.claude/commands/escrever-estrategia.md` — magica_online_origem, reverso-repositioning, funil Imersão/Reverso
- `.claude/commands/escrever-newsletter.md` — /reverso, /mentoria como slugs hardcoded
- `.claude/commands/escrever-pagina.md` — lista de slugs (reverso, clickup8x, etc.)
- `.claude/commands/executar-bateria-qa.md` — slugs em lista default + "Ávila" literal em path
- `.claude/commands/migrar-pagina.md` — "gui-avila" literal em URL + /reverso, /clickup8x
- `.claude/commands/revisar-codigo-pagina.md` — /reverso como referência, listas de slugs, gui-avila em URL
- `.claude/commands/revisar-copy-pagina.md` — lista de slugs, métricas "15 mil inscritos YouTube"
- `.claude/commands/revisar-estrategia.md` — funil Imersão/Reverso, lista de slugs, "Imersão muda..."
- `.claude/commands/revisar-newsletter.md` — "Automações PRO e ClickUp 8x" na assinatura, lista slugs
- `.claude/commands/testar-pagina.md` — magicaonline e lista ClickUp 8x/Automações/Reverso/Imersão
- `.claude/commands/atualizar-estrategia.md` — /imersao como exemplo de slug
- `.claude/commands/check-up-estrutura.md` — automacoes em exemplos, App Reverso, gui-avila em exclusion list
- `.claude/agents/analista-qa.md` — /squad-time-ia, /reverso, /automacoes como exemplos de páginas

**Scan de segurança pós-sanitização:** ✅ PASSOU — nenhum dado sensível detectado.

**Causa-raiz documentada:** Arquivos portados via sync manual/regex antes de 25/05/2026 (data de criação de `/portar-para-template`). Regex cobria nomes/emails, mas nunca slugs de produtos ou padrões de URL com nome do operador.

**Fix estrutural adicionado:** `workspace/scripts/scan-template-completo.sh` recebeu 3 novos padrões de detecção: slugs de produto pessoais, "gui-avila" em URL, sobrenome "Ávila" em path.

