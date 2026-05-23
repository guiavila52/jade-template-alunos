---
name: humanizar-newsletter
description: Humaniza newsletter escrita por IA — faz soar como se o Gui tivesse sentado e escrito. Passa mecânica de 10 regras contra padrões delatores de IA.
type: skill
---

# /humanizar-newsletter

**Papel:** @copywriter aplica pass de humanização  
**Input:** markdown da newsletter já escrita  
**Output:** markdown humanizado (mesmo arquivo, sobrescrito)  
**Squad:** conteudo  
**Maturidade:** 🟡 EM TESTE — criada 21/05/2026, afinar com feedback do Gui  
**Posição no pipeline:** após @copywriter escrever rascunho → **humanizar** → @revisor-newsletter

---

## Propósito

Newsletter escrita por IA tem padrões delatores concretos: ritmo uniforme, conectores formais, adjetivos vazios, neutralidade total. Este pass aplica 10 correções mecânicas para fazer o texto soar como o Gui escreveu — casual, direto, com posição, com ritmo humano.

**Não é reescrever.** É editar cirurgicamente. O conteúdo e as ideias ficam. A voz muda.

---

## Quando usar

- Sempre após @copywriter entregar rascunho e ANTES de @revisor-newsletter
- Quando Gui falar "tá cheirando IA" em qualquer texto
- Quando o revisor-newsletter reprovar por tom genérico/corporativo

---

## Orquestração

Jade despacha @copywriter com:
- Path do markdown a humanizar
- Briefing completo abaixo
- Instrução de sobrescrever o mesmo arquivo (não criar versão nova)

---

## Briefing para @copywriter

Você vai aplicar um pass de humanização num texto de newsletter já escrito. Não reescreva o conteúdo — edite a voz. As ideias e a estrutura ficam. O que muda: ritmo, conectores, adjetivos, posição, detalhes.

Leia o texto completo primeiro. Depois aplique as 10 regras abaixo em sequência. Ao final, leia em voz alta — o que tropeçar ainda está errado.

---

## As 10 regras (aplicar em sequência)

### Regra 1 — Ritmo: quebrar uniformidade

IA escreve todas as frases com o mesmo comprimento. Parece metrônomo.

**O que fazer:** identificar 3+ sequências de frases de tamanho parecido e quebrar. Inserir frases de 3–5 palavras após frases longas. Ou frases longas com subordinada após sequência de frases curtas.

**Fórmula:**  
Frase longa (15–25 palavras) → Frase curtíssima (3–5 palavras) → Frase média (10–15 palavras)

**Antes:** "A IA está mudando o mercado de trabalho. As empresas que adotam IA conseguem reduzir custos. Os profissionais que dominam IA têm mais vantagens."  
**Depois:** "A IA está mudando o mercado de trabalho — não daqui a 10 anos. Agora. Empresas que já adotaram economizaram custo e ganharam margem."

---

### Regra 2 — Banir conectores formais no início de parágrafo

Deletar ou substituir quando aparecem abrindo parágrafo:

| Banido | Substituto |
|---|---|
| "Além disso" | "Também", "E mais", "Ah, e" |
| "No entanto" | "Mas", "Só que", "Aí" |
| "Portanto" | "Então", "Por isso", "Daí" |
| "Ou seja" | "Na prática", "Traduzindo" |
| "Contudo" / "Todavia" | "Mas" |
| "Em suma" | "No fim das contas" |
| "Ademais" | deletar |
| "Por conseguinte" | "Então" |
| "Outrossim" | nunca usar |

---

### Regra 3 — Deletar frases de preenchimento

Buscar e destruir — não dizem nada:
- "É importante notar que..."
- "Vale ressaltar que..."
- "Como todos sabemos..."
- "Não é segredo que..."
- "É fato que..."
- "Para contextualizar..."
- "No contexto atual..."
- "De certa forma..."
- "De maneira geral..."
- "No final do dia..."

Se a frase seguinte precisa desse preâmbulo para funcionar, o problema é a frase seguinte — reescrever direto.

---

### Regra 4 — Trocar adjetivos vazios por dados concretos

Adjetivos banidos (podem se aplicar a qualquer coisa — não dizem nada):

| Banido | Substituto |
|---|---|
| "fascinante" | o que especificamente fascina? descrever |
| "incrível" / "impressionante" | o que concretamente aconteceu? |
| "revolucionário" | o que muda na prática? |
| "poderoso" | para quem, em que situação? |
| "essencial" / "crucial" | por quê? sem resposta: deletar |
| "robusto" | traduzir: "não quebra", "aguenta carga" |
| "completo" | listar o que inclui |
| "eficiente" | mais rápido em quanto? |

**Regra:** se o adjetivo pode ser aplicado a qualquer produto/ideia sem mudar o sentido, deletar.

---

### Regra 5 — Injetar ponto de vista

IA é neutra por padrão. Encontrar o parágrafo mais "em cima do muro" e reescrever com posição clara.

**Padrões de voz do Gui:**
- "Na minha visão..." / "Pra mim..."
- "Honestamente, acho que..."
- "Esse aqui é subestimado."
- "É a parte que a maioria ignora."
- "Testei. Funciona." (curto, assertivo)
- "Discordo disso." (quando relevante)

**Antes (IA):** "Existem diversas abordagens. Cada uma apresenta vantagens e desvantagens."  
**Depois (humano):** "Testei 4 abordagens. Uma funciona. As outras são hype."

---

### Regra 6 — Substituir generalização por detalhe específico

IA generaliza. Humano lembra o detalhe real.

**O que fazer:** encontrar a generalização mais óbvia e substituir por:
- Número real no lugar de "muitos" ou "vários"
- Situação concreta: "semana passada eu..." no lugar de "frequentemente"
- Nome de ferramenta, lugar, data, pessoa
- Resultado específico no lugar de "resultados melhores"

**Antes:** "Muitas pessoas têm dificuldade com produtividade."  
**Depois:** "A maioria das pessoas que conheço checa o Slack de 15 em 15 minutos e chama isso de trabalho."

---

### Regra 7 — Imperfeição deliberada (1–2 por newsletter)

Inserir 1–2 imperfeições que sinalizam voz real. Escolher as mais naturais:

- **Parêntese como aparte:** "(e olha, já tentei de outro jeito — não funciona)"
- **Reticências para pausa real:** "Aí eu percebi... isso muda tudo."
- **Frase incompleta para ênfase:** "O resultado? Exatamente o que eu esperava."
- **Autocorreção:** "Ou melhor: não é só isso."
- **Interjeição:** "Olha.", "Sabe o que é?", "Pois é."

⚠️ **Travessão (—):** a IA abusou tanto que virou marca registrada dela. Prefira parêntese ou ponto separado. No máximo 1 travessão por parágrafo.

---

### Regra 8 — Verificar abertura

Se o texto começa com qualquer um destes padrões, reescrever:
- "No mundo atual..." / "No cenário atual..."
- "Em um mundo onde..."
- "Você já se perguntou..."
- "Imagine que..."
- "Neste artigo, vamos explorar..."
- "Vivemos em uma era de..."

**Aberturas humanas:**
- Começa no meio da ação: "Semana passada quebrei uma regra que sigo há 3 anos."
- Começa com dado específico: "43% das newsletters são abertas no banheiro."
- Começa com posição: "Automação de conteúdo está destruindo mais do que criando."
- Começa simples e direto: "Você não precisa de mais ferramentas."

---

### Regra 9 — Verificar fechamento

Se o texto termina com variante de "Em conclusão" ou resumo do que já foi dito: reescrever.

**Encerramentos humanos:**
- Posição final: "No fim das contas: funciona. Testei. Recomendo."
- Pausa: "Isso fica aqui por hoje. Pensa nisso."
- Gancho: "Semana que vem conto o que aprendi errando isso por meses."
- Reversão: "Mas sabe o que é engraçado? Depois de tudo isso, voltei pro começo."

---

### Regra 10 — PT-BR informal (tom Gui)

Ajustes de voz para o português do Gui:
- "para" → "pra" (sempre, em contexto informal)
- "você/seu" — nunca "tu/teu/ti"
- Hedge a eliminar: "talvez", "pode ser que", "em alguns casos", "de certa forma" — se não é necessário, deletar
- Tom direto: opinião clara, sem rodeios, sem corporativismo

---

## Checklist antes de entregar

- [ ] Tem sequências de frases de mesmo tamanho? → quebrar
- [ ] Tem conector formal abrindo parágrafo? → trocar
- [ ] Tem frase de preenchimento? → deletar
- [ ] Tem adjetivo vazio? → trocar ou deletar
- [ ] Tem pelo menos 1 ponto de vista claro? → inserir se não tiver
- [ ] Tem pelo menos 1 detalhe específico no lugar de generalização?
- [ ] Tem 1–2 imperfeições deliberadas naturais?
- [ ] A abertura é humana? → reescrever se não for
- [ ] O fechamento não é resumo? → reescrever se for
- [ ] Tudo "você/pra/seu"? → corrigir

---

## Regras invioláveis

- **Não reescrever o conteúdo** — só editar voz e ritmo. As ideias ficam.
- **Não adicionar informações** que não estão no texto original
- **Não remover seções** — só editar dentro de cada seção
- **Assinatura canônica nunca é tocada** — o renderer cuida disso
- **PS obrigatório nunca é removido** — só pode humanizar o texto do PS se necessário
- **Acentuação PT-BR obrigatória** em todo o texto

---

## Próximo passo após humanizar

→ @revisor-newsletter (revisor independente valida copy humanizada)
