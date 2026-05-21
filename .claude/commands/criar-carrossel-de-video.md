---
name: criar-carrossel-de-video
description: Atalho ponta-a-ponta. Input = URL YouTube. Encadeia transcrição → estratégia → copy slide-a-slide → lâminas HTML→PNG → triple-check. Output: pasta workspace/output/carrosseis/YYYY-MM-DD-[slug]/ completa. Sem fricção, sem perguntar — {{NOME_OPERADOR}} delegou.
model: claude-opus-4-5
---

<!-- Modelo recomendado: claude-opus-4-5 (orquestração ponta-a-ponta) -->

## Quando usar

{{NOME_OPERADOR}} manda URL YouTube e quer carrossel pronto SEM ser perguntado nada. Atalho:

```
/criar-carrossel-de-video https://youtu.be/XXX
```

Skill encadeia: /transcrever-video → /escrever-estrategia → /escrever-copy carrossel → squad-imagem → triple-check.

**Diferente da `/criar-carrossel`:**
- `/criar-carrossel` é genérica e pergunta quando input vago
- `/criar-carrossel-de-video` é específica e NÃO pergunta — {{NOME_OPERADOR}} já delegou

Pra tema solto (sem URL), usar `/criar-carrossel`.

## Memórias relevantes (ler antes)

1. `~/.claude/projects/-Users-{{github_user}}-Documents-Projetos-IA-{{NOME_OPERADOR}}--vila-Squad-Empresa-{{NOME_OPERADOR}}--vila/memory/project_foco_carrossel_youtube_e_meta_ads.md` — foco macro
2. `~/.claude/.../memory/feedback_propagacao_correcoes.md` — Regra #19
3. `~/.claude/.../memory/design_rules_paginas.md` — Cormorant proibida em dígitos (Regra #188)
4. `segundo-cerebro/01-identidade/banco-de-historias.md`
5. `segundo-cerebro/01-identidade/tom-de-voz.md`

## Comando

```
/criar-carrossel-de-video <URL>
```

URL aceita: `youtube.com/watch?v=XXX`, `youtu.be/XXX`, `youtube.com/shorts/XXX`.

Se input não for URL válida: skill aborta com erro claro ("input não é URL YouTube — usa /criar-carrossel pra tema solto").

## Schema do briefing — passo a passo entre agentes

(idêntico ao da `/criar-carrossel` — fonte única de verdade)

| De → Pra | Recebe | Entrega |
|---|---|---|
| **Jade → /transcrever-video** | URL YouTube | `transcricao.txt` em pasta de output |
| **Jade → estrategista** | transcrição completa + ICP do {{NOME_OPERADOR}} | briefing-estrategista.md (ângulo + narrativa + payoff + qtd lâminas + estrutura + tom + refs) |
| **estrategista → carrossel (copywriter)** | briefing-estrategista.md | roteiro.md (Light Copy slide-a-slide) + briefing-visual.md (template/texto/flags por slide) |
| **carrossel → squad-imagem** | briefing-visual.md | comandos `tweet-imagem.mjs` por slide → PNGs 1080x1350 |
| **squad-imagem → revisor-visual** | pasta PNGs | aprovação ou lista de defeitos |
| **carrossel → /revisar-carrossel** | roteiro.md | aprovação ou lista de fixes |

### Schema do briefing do estrategista (campos obrigatórios)

```yaml
tema: "string extraído da transcrição"
angulo_unico: "1 frase clara, não-genérica"
payoff: "conclusão que o último slide entrega"
qtd_laminas: 5  # 5=simples, 7=padrão (default pra vídeo médio), 10=denso
estrutura: "hook (1) → problema (2-3) → diagnóstico (4-5) → método (6) → CTA (7)"
tom: "didático+irônico | técnico+sério | íntimo+honesto"
referencias_segundo_cerebro:
  - "01-identidade/banco-de-historias.md"
  - "01-identidade/tom-de-voz.md"
transcricao_bruta: "..."
fonte:
  url: "https://youtu.be/XXX"
  titulo_video: "[extraído da transcrição metadata]"
  duracao_s: 0
```

## Output canônico

```
workspace/output/carrosseis/YYYY-MM-DD-[slug]/
├── transcricao.txt              # output de /transcrever-video (raw)
├── briefing-estrategista.md     # output do estrategista (auditável)
├── roteiro.md                   # copy slide-a-slide
├── briefing-visual.md           # briefing por slide (template+flags)
├── slide-01.png                 # 1080x1350
├── slide-02.png
├── slide-NN.png
└── mapa.md                      # Regra #10
```

`[slug]` = 2-4 palavras do tema (do estrategista) em kebab-case.

## Triple-check obrigatório

1. `/revisar-carrossel` — texto/posicionamento
2. `revisor-visual` (Agent) — defeitos estéticos por PNG
3. Auditoria Cormorant (Regra #188) — `grep -i "cormorant\|year-accent" briefing-visual.md` = 0

Se qualquer reprovar: corrige + re-roda. Sem exceção.

## Regras invioláveis

- Light Copy obrigatório (frase curta, 1 premissa/slide)
- Slide 1 = Setup+Punch ou Escalada (sem 3 Ps)
- CTA SÓ no último slide
- Cormorant Garamond NUNCA em dígitos (Regra #188)
- Métricas públicas: nunca expor faturamento (Regra `feedback_metricas_publicas_gui.md`)
- Cada PNG = 1080x1350, ≤ 500KB
- Edição da própria skill via Bash/Python (Regra #8)

## Restrições

- Aborta se input não-URL → instrui usar `/criar-carrossel`
- Aborta se transcrição vazia/<200 chars → "vídeo sem áudio detectável"
- NÃO pergunta nada no caminho (ao contrário da `/criar-carrossel`)
- Se algum agente reprovar 2x seguidas: pausa e relata ao {{NOME_OPERADOR}} (Regra #9 — segundo fracasso muda perspectiva)

## Fluxo

```
[ {{NOME_OPERADOR}} dispara /criar-carrossel-de-video <URL> ]
        ↓
[ Jade valida URL ]
   │
   ├─ Inválida → ABORTA com erro
   └─ Válida → segue
        ↓
[ /transcrever-video ] → @transcrever-video
   output: transcricao.txt
        ↓
   ⟶ se transcrição < 200 chars: ABORTA ("vídeo sem áudio")
        ↓
[ estrategista (squad-gestao) ]
   recebe: transcricao.txt + ICP {{NOME_OPERADOR}} + memórias
   define: ângulo único + narrativa + payoff + qtd lâminas + tom
   output: briefing-estrategista.md
        ↓
   ⟶ /revisar-estrategia (loop até APROVADO; max 2 retries — senão pausa)
        ↓
[ carrossel (squad-conteudo) ]
   recebe: briefing-estrategista.md + segundo-cerebro
   produz: roteiro.md (Light Copy) + briefing-visual.md
        ↓
   ⟶ /revisar-carrossel (loop até APROVADO)
        ↓
[ squad-imagem ]
   pra cada slide: roda tweet-imagem.mjs com flags do briefing-visual
   output: slide-01.png ... slide-NN.png
        ↓
[ revisor-visual (Agent squad-dev) ]
   audita cada PNG: alinhamento, contraste, Cormorant=0, brand
        ↓
   ⟶ se reprovar: volta corrigir
        ↓
[ Atualizar MAPA + aprendizados (Regra #10 + #19) ]
        ↓
[ Apresenta ao {{NOME_OPERADOR}} ]
   pasta completa + sumário: copy + thumbs PNGs + URL fonte
   notif macOS: "Carrossel pronto — [slug]"
        ↓
   ⟶ FIM
```

## Captura de aprendizado (Regra #19)

Quando {{NOME_OPERADOR}} aprovar/rejeitar:
- `squads/conteudo/agentes/designer-conteudo/aprendizados.md` (nível agente)
- `squads/conteudo/aprendizados.md` (se for padrão do squad)

Template aprovado:
```
### [título curto]
**Data:** YYYY-MM-DD | **Slug:** [slug] | **URL:** [url]
**Contexto:** [tema da transcrição]
**O que funcionou:** [o que {{NOME_OPERADOR}} aprovou]
**Padrão identificado:** [regra reutilizável]
```

Template rejeitado:
```
### [título curto]
**Data:** YYYY-MM-DD | **Slug:** [slug]
**O que não funcionou:** [o que {{NOME_OPERADOR}} rejeitou]
**Correção aplicada:** [o que mudou]
**Regra para não repetir:** [Regra #19 → propaga skill produtor + skill revisor + memória + retrofit]
```

## Atualizar MAPA + processo

Ao finalizar:
1. `workspace/output/carrosseis/mapa.md` — entrada nova (criar pasta+MAPA se não existir)
2. `workspace/processos/criar-carrossel-de-video.md` — adicionar linha na tabela de execuções (data, URL, slug, status, lâminas, output path)

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{NOME_OPERADOR}} testar — testa antes.
