---
name: varrer-tendencias
description: Radar de hot topics e tendências emergentes no nicho de IA / agentes / automação. Varre YouTube, Reddit e Twitter/X. Alimenta pauta de conteúdo do operador antes dos temas virarem mainstream.
type: skill
---

# /varrer-tendencias

**Squad:** radar
**Agente:** @analista-tendencias
**Status:** ✅ FUNCIONAL
**Trigger:** sob demanda | cron semanal terça 08:00 BRT (depois do monitorar-concorrentes)

---

## Contexto

{{NOME_OPERADOR}} publica conteúdo sobre squads de agentes de IA para infoprodutores.
YouTube é o motor do seu funil. Chegar cedo numa tendência = vantagem competitiva real.
Esta skill entrega sinais fracos ANTES de se tornarem óbvios — pautas que ainda não viraram trend mas estão ganhando tração.

---

## Fluxo

```
Input (nicho: IA, agentes, automação, infoprodutor)
  ↓
1. Varrer Reddit: r/ClaudeAI, r/AIAgents, r/MachineLearning, r/artificial, r/Entrepreneur
2. Varrer YouTube: trending queries + vídeos em ascensão no nicho
3. Varrer Twitter/X: termos quentes + criadores do nicho
4. Identificar: O que está ganhando tração? O que gerou debate? O que ainda não foi coberto em PT-BR?
5. Classificar por potencial (🔥 quente agora | 🌱 emergente | 📌 evergreen relevante)
6. Sugerir ângulo para operador (como ele pode cobrir com sua perspectiva única)
7. Salvar output em workspace/output/radar/tendencias/{YYYY-MM-DD}.md
  ↓
Output (lista de 5-10 tendências com ângulo pra operador)
```

---

## Termos a pesquisar

### Português (Brasil)
- "agentes de IA", "squad de IA", "time de IA", "automação com IA"
- "Claude AI", "ChatGPT agentes", "infoprodutor IA"
- "lançamento com IA", "escalar negócio IA"

### Inglês (detectar antes de chegar ao Brasil)
- "AI agents", "agentic workflows", "Claude Code", "multi-agent systems"
- "AI for solopreneurs", "AI automation 2025", "autonomous AI"
- "MCP servers", "tool use AI", "AI workforce"

---

## O que entregar

### Top 5 tendências (ordenado por urgência)

Para cada uma:
```
🔥 [NOME DA TENDÊNCIA]
- O que é: [1 linha]
- Sinal detectado: [onde viu, quantos posts/views, data]
- Por que importa pro operador: [1 linha]
- Ângulo sugerido: [título de vídeo/post para o operador explorar]
- Fonte: [URL]
```

### Pauta pronta (bônus)
- 1 ideia de roteiro YouTube pronto pra despachar pro @copywriter

---

## Output canônico

`workspace/output/radar/tendencias/{YYYY-MM-DD}.md`

---

## Instruções para o @analista-tendencias

1. Usar WebSearch e WebFetch — nunca inventar dados
2. Priorizar sinais de FORA do Brasil (chegam aqui 2-4 semanas depois)
3. Não listar o óbvio — se todo mundo já fala, não é tendência emergente
4. Sempre traduzir o sinal pra contexto do operador: "Como o operador pode ser o primeiro a falar sobre isso em PT-BR?"
5. Tom do output: direto, sem jargão — operador lê e age em < 5 minutos

---

## Bateria de testes

- [x] Skill criada e documentada
- [ ] Primeira execução manual: `@analista-tendencias /varrer-tendencias`
- [ ] Output salvo no path canônico
- [ ] Pelo menos 3 tendências com ângulo pra operador

---

## Aprendizados + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
