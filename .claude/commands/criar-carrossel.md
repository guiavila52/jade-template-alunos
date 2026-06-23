---
name: criar-carrossel
description: Carrossel Instagram a partir de URL YouTube ou tema solto. Jade orquestra cadeia estrategista → copywriter (carrossel) → squad-imagem (HTML→PNG) → triple-check. Output canônico em workspace/output/carrosseis/YYYY-MM-DD-[slug]/.
model: claude-opus-4-5
---

<!-- Modelo recomendado: claude-opus-4-5 (orquestração estratégica) -->

## Quando usar

- {{NOME_OPERADOR_CURTO}} mandou URL do YouTube → carrossel a partir da transcrição
- {{NOME_OPERADOR_CURTO}} mandou tema/ângulo solto → estrategista define ângulo único antes da copy
- Tema vago/ambíguo → essa skill PERGUNTA antes de prosseguir

Pra atalho ponta-a-ponta sem fricção (URL YouTube + tema bem definido), usar `/criar-carrossel-de-video`.

## Memórias relevantes (ler antes)

1. `~/.claude/projects/<seu-project-hash>/memory/
  # Para descobrir o project-hash: rode `ls ~/.claude/projects/` e copie a pasta do seu projetoproject_foco_carrossel_youtube_e_meta_ads.md` — foco macro
2. `~/.claude/.../memory/feedback_propagacao_correcoes.md` — Regra #19
3. `~/.claude/.../memory/design_rules_paginas.md` — Cormorant proibida em dígitos (Regra #188)
4. `segundo-cerebro/01-identidade/banco-de-historias.md` — Light Copy + histórias reais
5. `segundo-cerebro/01-identidade/tom-de-voz.md` — tom + o que nunca fazer

⚠️ **segundo-cerebro = só leitura.** Workers consultam, nunca editam (Regra #7).

## Detecção de input

Jade roteia conforme input:

```
INPUT?
├─ URL YouTube (youtube.com/watch | youtu.be/...) → /transcrever-video → texto → estrategista
├─ Path arquivo de transcrição local → ler arquivo → estrategista
├─ Tema bem definido (>20 chars, contexto claro) → estrategista direto
└─ Tema vago/curto → PERGUNTA ao {{NOME_OPERADOR_CURTO}} antes (ângulo, ICP, qual produto)
```

## Schema do briefing — passo a passo entre agentes

| De → Pra | Recebe | Entrega |
|---|---|---|
| **Jade → estrategista** | input bruto (URL/tema) + transcrição (se vídeo) + ICP do {{NOME_OPERADOR_CURTO}} | ângulo único + narrativa + payoff + qtd lâminas + estrutura hook→desenvolvimento→CTA + tom + refs segundo-cerebro |
| **estrategista → carrossel (copywriter)** | briefing acima | copy slide-a-slide (Light Copy) + briefing visual por slide (template + texto + autor + número) |
| **carrossel → squad-imagem** | briefing visual | comandos `gerar-imagem.mjs --template X --texto "..."` por slide |
| **squad-imagem → revisor-visual** | pasta com PNGs 1080x1350 | aprovação ou lista de defeitos estéticos |
| **carrossel → /revisar-carrossel** | roteiro.md | aprovação ou lista de pontos de copy a corrigir |
| **revisor-visual + revisor-carrossel → Jade** | duplo OK | desbloqueia entrega |

### Schema do briefing do estrategista (campos obrigatórios)

```yaml
tema: "string"
angulo_unico: "1 frase clara, não-genérica"
payoff: "conclusão que o último slide entrega"
qtd_laminas: 5  # 5=simples, 7=padrão, 10=denso
estrutura: "hook (1) → problema (2-3) → diagnóstico (4-5) → método (6) → CTA (7)"
tom: "didático+irônico | técnico+sério | íntimo+honesto"
referencias_segundo_cerebro:
  - "01-identidade/banco-de-historias.md"
  - "01-identidade/tom-de-voz.md"
  - "02-negocios/produtos-servicos.md"
transcricao_bruta: "..." # só se input foi vídeo
```

### Schema do output do agente carrossel

`roteiro.md`:
```markdown
# [tema] — Carrossel YYYY-MM-DD

**Ângulo:** ...
**Payoff:** ...

## Slide 1 — Hook
[texto curto, 1 premissa, Setup+Punch ou Escalada]

## Slide 2 — [função]
[texto]

...

## Slide N — CTA
[chamada final clara]
```

`briefing-visual.md`:
```markdown
# Briefing visual — slides 1 a N

| # | Template | Texto exato | Autor | Handle | Número | Notas |
|---|---|---|---|---|---|---|
| 1 | quote | "..." | {{NOME_OPERADOR}} | @{{HANDLE_SOCIAL}} | 1/N | hook curto |
| 2 | default | "..." | — | — | 2/N | tweet-card padrão |
| 3 | lista | título + 3 itens | — | — | 3/N | numerado |
| 4 | antes-depois | antes/depois | — | — | 4/N | divisão 50/50 |
| ... |
| N | story | "Próximo passo: ..." | — | — | N/N | CTA fechado |
```

## Output canônico — UMA pasta com tudo

```
workspace/output/carrosseis/YYYY-MM-DD-[slug]/
├── roteiro.md              # copy slide-a-slide aprovado
├── briefing-visual.md      # briefing por slide (template + texto + flags)
├── slide-01.png            # 1080x1350
├── slide-02.png
├── slide-NN.png
├── transcricao.txt         # só se input foi vídeo
├── briefing-estrategista.md # output do estrategista (auditável)
└── mapa.md                 # Regra #10 — propósito, lista, última atualização
```

`[slug]` = 2-4 palavras do tema em kebab-case. Ex: `2026-05-08-orquestracao-vence-modelo`.

## Triple-check obrigatório (antes de entregar ao {{NOME_OPERADOR_CURTO}})

1. **`/revisar-carrossel`** — texto/posicionamento. APROVADO ou lista de fixes.
2. **`revisor-visual` (Agent)** — defeitos estéticos por PNG. APROVADO ou lista.
3. **Auditoria Cormorant** (Regra #188) — `grep -i "cormorant\|year-accent" briefing-visual.md` deve retornar 0 hits em qualquer slide com dígito.

Se qualquer dos 3 reprovar: corrige + re-roda os 3. Sem exceção.

## Regras invioláveis pra carrossel

- **Light Copy obrigatório** — frase curta, premissa única por slide
- **Slide 1** = Setup+Punch ou Escalada de Atenção (sem 3 Ps: Porque/Promessa-imperativa/Pergunta)
- **CTA SÓ no último slide**
- **Cormorant Garamond NUNCA em dígitos** (Regra #188 absoluta — número/ano/data/preço/percentual/cupom = Syne ou Inter, nunca Cormorant)
- **Métricas públicas** — nunca expor faturamento (R$/MRR) das empresas (Regra `feedback_metricas_publicas.md`); usar usuários, alunos, criadores
- **Banco de histórias** = fonte de exemplos reais
- Cada PNG = 1080x1350, ≤ 500KB

## Comandos

### Modo guiado (interativo)
```
/criar-carrossel [URL ou tema]
```
Skill detecta input, dispara fluxo. Pergunta se tema vago.

### Geração técnica das lâminas (após copywriter aprovar)
```bash
cd "Páginas Astro {{NOME_OPERADOR}}"
node scripts/gerar-imagem.mjs \
  --template default \
  --texto "..." \
  --autor "{{NOME_OPERADOR}}" \
  --handle "@{{HANDLE_SOCIAL}}" \
  --foto /caminho/foto-perfil.jpg \
  --numero "1/5" \
  --output "../Squad Empresa {{NOME_OPERADOR}}/workspace/output/carrosseis/YYYY-MM-DD-[slug]/slide-1.png"
```

5 templates disponíveis: `default` (tweet card), `quote` (autoral grande), `lista` (numerada), `antes-depois` (50/50), `story` (número GIGANTE).

## Atualizar MAPA + aprendizados

Ao finalizar:
1. Adicionar entrada em `workspace/output/carrosseis/mapa.md` (criar pasta+MAPA se não existir)
2. Atualizar `workspace/processos/criar-carrossel-de-video.md` (tabela de execuções)
3. Registrar aprendizado em `squads/conteudo/agentes/designer-conteudo/aprendizados.md` (Regra #19)

## Fluxo

```
[ {{NOME_OPERADOR_CURTO}} dispara /criar-carrossel <input> ]
        ↓
[ Jade detecta tipo de input ]
   │
   ├─ URL YouTube → [ /transcrever-video ] → texto
   │                         ↓
   ├─ Path local → [ ler arquivo ] → texto
   │                         ↓
   ├─ Tema definido → segue direto
   │                         ↓
   └─ Tema vago → ⟶ PERGUNTA ao {{NOME_OPERADOR_CURTO}}
                            ↓
[ estrategista (squad-gestao) ]
   define: ângulo único + narrativa + payoff + qtd lâminas + estrutura + tom
   output: briefing-estrategista.md
        ↓
   ⟶ aguarda /revisar-estrategia (loop até APROVADO)
        ↓
[ carrossel (squad-conteudo) ]
   recebe: briefing-estrategista.md + segundo-cerebro
   produz: roteiro.md (copy Light Copy slide-a-slide)
         + briefing-visual.md (template + texto + flags por slide)
        ↓
   ⟶ /revisar-carrossel (loop até APROVADO)
        ↓
[ squad-imagem ]
   pra cada slide: roda gerar-imagem.mjs com flags do briefing-visual
   output: slide-01.png ... slide-NN.png em workspace/output/carrosseis/[slug]/
        ↓
[ revisor-visual (Agent squad-dev) ]
   audita cada PNG: alinhamento, contraste, Cormorant em dígito (Regra #188), brand
   output: APROVADO ou lista de defeitos
        ↓
   ⟶ se reprovar: volta pro carrossel/squad-imagem corrigir
        ↓
[ Atualizar MAPA + aprendizados (Regra #10 + #19) ]
        ↓
[ Apresenta ao {{NOME_OPERADOR_CURTO}} ]
   pasta workspace/output/carrosseis/[slug]/ completa
   sumário: copy + thumbs dos PNGs + path
        ↓
   ⟶ FIM (aguarda aprovação final do {{NOME_OPERADOR_CURTO}})
```

## Captura de aprendizado (Regra #19 — obrigatório após aprovação ou rejeição)

Quando {{NOME_OPERADOR_CURTO}} aprovar/rejeitar, registrar em DOIS lugares:
1. `squads/conteudo/agentes/designer-conteudo/aprendizados.md` (nível agente)
2. `squads/conteudo/aprendizados.md` (se for padrão do squad inteiro)

Template:

**Aprovado:**
```
### [título curto]
**Data:** YYYY-MM-DD | **Slug:** [slug]
**Contexto:** [tema + input]
**O que funcionou:** [o que o {{NOME_OPERADOR_CURTO}} aprovou e por quê]
**Padrão identificado:** [regra reutilizável]
```

**Rejeitado:**
```
### [título curto]
**Data:** YYYY-MM-DD | **Slug:** [slug]
**O que não funcionou:** [o que o {{NOME_OPERADOR_CURTO}} rejeitou]
**Correção aplicada:** [o que mudou]
**Regra para não repetir:** [Regra #19 → propaga em 4 lugares: skill produtor + skill revisor + memória + retrofit]
```

## Restrições

- **NÃO** criar arquivo de carrossel sem rodar /revisar-carrossel (Regra: nunca pular revisão)
- **NÃO** publicar PNGs sem aprovar revisor-visual (Regra: triple-check obrigatório)
- **NÃO** usar Cormorant Garamond em dígito (Regra #188 absoluta)
- **NÃO** colocar mais de 1 premissa por slide (Light Copy)
- **NÃO** começar slide 1 com 3 Ps
- Edição da própria skill via Bash/Python (Regra #8)

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{NOME_OPERADOR_CURTO}} testar — testa antes.