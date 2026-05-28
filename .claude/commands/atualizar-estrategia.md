---
name: atualizar-estrategia
description: Registra mudanca estrategica (lancamento, posicionamento, oferta) no documento vivo estrategia-viva.md e dispara acoes consequentes.
type: skill
---

<!-- Modelo recomendado: claude-opus-4-5 (decisões estratégicas precisam de raciocínio forte) -->

# /atualizar-estrategia — Registrar mudança estratégica no documento vivo

> Skill invocada quando o {{NOME_OPERADOR_CURTO}} (ou a Jade detecta) que algo mudou no estado estratégico do squad: data de lançamento, posicionamento de produto, novo produto, métrica pública, foco do funil, decisão sobre canal, etc.
>
> **A skill atualiza** `segundo-cerebro/04-decisoes/estrategia-viva.md` **e dispara as ações consequentes.**

---

## Quando invocar

- {{NOME_OPERADOR_CURTO}} falou "vamos adiar o lançamento pra dezembro"
- {{NOME_OPERADOR_CURTO}} falou "mentoria agora é só em grupo"
- {{NOME_OPERADOR_CURTO}} falou "tira faturamento da copy"
- {{NOME_OPERADOR_CURTO}} decidiu pivot de produto, canal, oferta, preço
- Jade percebeu inconsistência entre `estrategia-viva.md` e a realidade
- Estrategista produziu estratégia que GERA decisão nova (precisa registrar)

**Não invocar** pra:
- Tarefa operacional (vai pra `pendencias.md`)
- Aprendizado de processo (vai pra `aprendizados.md` do squad)
- Decisão tática de copy (vai pra revisão da peça)

---

## Fluxo (passo a passo)

### 1. Diálogo com quem invocou ({{NOME_OPERADOR_CURTO}} ou Jade)

Perguntar nessa ordem (uma de cada vez, esperando resposta):

1. **O que mudou?** (uma frase clara — ex: "lançamento adiado de maio pra dezembro")
2. **Quem decidiu?** ({{NOME_OPERADOR_CURTO}} / Jade / {{NOME_OPERADOR_CURTO}}+sócio / etc)
3. **Por quê?** (motivo da mudança — ajuda no histórico)
4. **Qual o impacto?**
   - Quais páginas precisam de update? (ex: `/mentoria`, `/imersao`)
   - Quais skills/agentes precisam saber? (ex: estrategista, copywriter)
   - Quais memórias persistentes precisam ser criadas/atualizadas?
   - Quais peças em produção precisam ser refeitas/pausadas?

### 2. Ler `estrategia-viva.md`

```bash
cat "$CLAUDE_PROJECT_DIR/segundo-cerebro/04-decisoes/estrategia-viva.md"
```

Identificar exatamente quais campos da seção "ATUAL" precisam ser editados.

### 3. Adicionar entrada no HISTÓRICO (no topo da seção)

Formato:

```markdown
### YYYY-MM-DD — [Mudança em uma frase]
**Quem decidiu:** [{{NOME_OPERADOR_CURTO}} / Jade / {{NOME_OPERADOR_CURTO}}+sócio]
**Mudança:** [descrição curta da mudança concreta]
**Motivo:** [por quê]
**Impacto:**
- Páginas afetadas: [lista]
- Skills/agentes notificados: [lista]
- Peças em produção pausadas/refeitas: [lista]
- Memórias persistentes criadas/atualizadas: [lista]
```

### 4. Atualizar a seção "ATUAL"

Refletir o novo estado nos campos relevantes (Lançamentos e datas / Funil / Posicionamento / Métricas públicas / Métricas proibidas).

### 5. Atualizar o campo "Última atualização" no topo do documento

`**Última atualização:** YYYY-MM-DD por [Quem invocou + Jade]`

### 6. Listar páginas/skills/memórias que precisam de update consequente

Apresentar pro {{NOME_OPERADOR_CURTO}} (via Jade) uma checklist no formato:

```markdown
## Update consequente da mudança "[mudança]"

Ações pra Jade despachar:

- [ ] `/escrever-pagina /mentoria` — refazer copy (mentoria virou só grupo)
- [ ] `/revisar-copy-pagina /mentoria-precos` — remover card individual
- [ ] Criar memória persistente `feedback_mentoria_so_grupo.md` em `~/.claude/projects/.../memory/`
- [ ] Indexar nova memória em `MEMORY.md`
- [ ] Avisar squad-conteudo: pausar carrosséis sobre mentoria 1:1
- [ ] Avisar squad-trafego: pausar criativos que mencionam mentoria 1:1
```

### 7. Sugerir ação imediata pra Jade

Não terminar perguntando "o que você quer". Afirmar a próxima ação. Exemplo:

> "Registrei a mudança. Vou despachar `/escrever-pagina /mentoria` agora pro squad-copy. Os outros 5 itens do checklist consequente entram na fila de pendências. Me avisa se quiser desviar a ordem."

---

## Regras

- **Nunca apagar entrada do histórico.** Só anexar. Mudou de novo? Adiciona entrada nova com data nova.
- **Sempre refletir na seção "ATUAL"** — registrar histórico sem atualizar estado vigente quebra o documento.
- **Sempre atualizar "Última atualização"** no topo.
- **Se a mudança gera memória persistente** (algo que vai influenciar decisões futuras de outros agentes), CRIAR `feedback_*.md` ou `project_*.md` em `~/.claude/projects/.../memory/` e INDEXAR em `MEMORY.md`. Esse passo NÃO é opcional.
- **Se a mudança contradiz uma memória persistente existente**, atualizar a memória existente (não criar duplicata) e registrar isso no campo "Impacto" do histórico.
- **Se faltar info pra registrar** (ex: {{NOME_OPERADOR_CURTO}} não soube dizer o impacto em páginas), perguntar — não chutar. Decisão estratégica registrada errada vira veneno.

---

## Output

1. Versão atualizada de `estrategia-viva.md` (gravada no arquivo).
2. Checklist de update consequente (apresentada na conversa com a Jade/{{NOME_OPERADOR_CURTO}}).
3. Entradas em pendências (`workspace/memory/pendencias.md`) pras ações consequentes que precisam de execução.
4. Memórias persistentes criadas (quando aplicável).

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{NOME_OPERADOR_CURTO}} testar — testa antes.