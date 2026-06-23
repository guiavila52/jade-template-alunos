---
name: monitorar-concorrentes
description: Varre o que os principais players do nicho de squads de IA / infoprodutores de IA estão publicando, lançando e posicionando. Alimenta estratégia de conteúdo e diferenciação do operador.
type: skill
---

# /monitorar-concorrentes

**Squad:** radar
**Agente:** @analista-mercado
**Status:** ✅ FUNCIONAL
**Trigger:** sob demanda | cron semanal segunda 08:00 BRT

---

## Contexto

Nicho do operador: squads de agentes de IA para infoprodutores e donos de negócio digital.
Funil operador: YouTube/Instagram → {{PRODUTO_PRINCIPAL}} → Mentoria → Consultoria.
Objetivo: saber o que concorrentes estão fazendo ANTES que vire mainstream. Identificar gaps de posicionamento, pautas não exploradas, lançamentos que podem afetar a demanda.

---

## Fluxo

```
Input (nicho: squads IA / agentes / infoprodutores)
  ↓
1. Identificar players relevantes (lista canônica abaixo + novos detectados)
2. Varrer últimas publicações no YouTube (títulos, thumbnails, views, data)
3. Varrer Instagram / LinkedIn (posts, stories, reels recentes)
4. Verificar páginas de vendas ativas (produtos, preços, promessas)
5. Identificar movimentos: novo lançamento? Reposicionamento? Collab? Promoção?
6. Comparar posicionamento deles vs operador (onde operador diferencia?)
7. Salvar output em workspace/output/radar/concorrentes/{YYYY-MM-DD}.md
  ↓
Output (resumo executivo: quem se moveu, o que mudou, oportunidade pra operador)
```

---

## Players a monitorar (lista canônica — atualizar conforme mercado)

### Nicho principal (squads/agentes de IA Brasil)
- Pesquisar via WebSearch: "squad de agentes IA", "time de agentes IA Brasil", "agentes de IA infoprodutor"
- Verificar top resultados YouTube nos últimos 30 dias

### Nicho adjacente (automação + IA para negócios digitais)
- Pesquisar via WebSearch: "automação com IA negócio digital", "IA para infoprodutor", "Claude Code Brasil"

### Internacional (referência de posicionamento)
- Pesquisar via WebSearch: "AI agents business 2025", "AI squad for entrepreneurs"

---

## O que entregar

### Resumo executivo (pra operador — máx 10 linhas)
- Quem se moveu essa semana
- O que lançaram / publicaram / mudaram
- Uma oportunidade clara pra operador (pauta, posicionamento, contra-narrativa)

### Detalhamento por player (para o squad)
- Nome + canal
- Última publicação: título, data, views estimados
- Posicionamento atual (promessa principal)
- Mudança detectada vs semana anterior (se houver)

---

## Output canônico

`workspace/output/radar/concorrentes/{YYYY-MM-DD}.md`

---

## Instruções para o @analista-mercado

1. Usar WebSearch e WebFetch para varrer os players
2. NÃO inventar dados — só reportar o que encontrar com URL de fonte
3. Se player não tiver publicação nova → registrar "sem movimento"
4. Sempre comparar com posicionamento do operador em `segundo-cerebro/01-identidade/identidade.md`
5. Oportunidade = gap entre o que concorrente promete e o que operador entrega melhor

---

## Bateria de testes

- [x] Skill criada e documentada
- [ ] Primeira execução manual: `@analista-mercado /monitorar-concorrentes`
- [ ] Output salvo no path canônico
- [ ] Resumo executivo legível em < 30 segundos

---

## Aprendizados + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
