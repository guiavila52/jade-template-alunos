# Processo: criar carrossel a partir de vídeo YouTube

**Squad:** orquestração macro = jade. Operação = squad-conteudo (carrossel/copywriter) + squad-jade (estrategista) + squad-dev (revisor-visual, bug-hunter).

**Skill ponta-a-ponta:** `/criar-carrossel-de-video`  
**Skill genérica (tema solto):** `/criar-carrossel`

---

## Objetivo

Gui manda URL YouTube → squad entrega carrossel Instagram pronto (PNGs 1080x1350 + roteiro markdown + briefing visual) sem fricção, em < 30min.

---

## Fluxo completo

```
Gui: "quero carrossel sobre [URL YouTube ou tema]"
   ↓
┌─────────────────────────────────────────────────────┐
│ JADE (COO) — entende input, detecta tipo            │
│ - URL YouTube? → despacha /transcrever-video        │
│ - Tema solto? → pula pra estrategista direto        │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ /transcrever-video (Sonnet 4.6)                     │
│ - Extrai transcrição completa do vídeo              │
│ - Salva em workspace/output/transcricoes/               │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ ESTRATEGISTA (squad-jade)                           │
│ - Recebe transcrição (ou tema)                      │
│ - Define: tema, ângulo único, payoff, qtd lâminas,  │
│   estrutura (hook→desenvolvimento→CTA), tom         │
│ - Gera 3 candidatos de ângulo (se vídeo), recomenda│
│ - Output: briefing schema (ver memoria.md)          │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ /revisar-estrategia (JADE)                          │
│ - Valida: ângulo claro? payoff falável? hook+CTA?  │
│ - Se não: volta pro estrategista                    │
│ - Se sim: despacha copywriter                       │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ CARROSSEL (squad-conteudo)                          │
│ - Recebe briefing do estrategista                   │
│ - Escreve copy slide-a-slide (Light Copy)           │
│ - Gera briefing-visual.md (template por slide)      │
│ - Salva em workspace/output/carrosseis/YYYY-MM-DD-slug/ │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ /revisar-carrossel (revisor-carrossel)              │
│ - Valida: Light Copy? Slide 1 hook? CTA só final?  │
│ - Regra #188: Cormorant NÃO em dígitos?            │
│ - Se não: volta pro carrossel                       │
│ - Se sim: despacha squad-imagem                     │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ SQUAD-IMAGEM (gerar-imagem.mjs)                     │
│ - Pra cada slide: HTML→PNG (Playwright screenshot)  │
│ - Dimensões: 1080x1350, ≤ 500KB                     │
│ - Fontes: Syne+Inter (NUNCA Cormorant em números)  │
│ - Salva PNGs na mesma pasta                         │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ TRIPLE-CHECK                                        │
│ 1. revisor-visual (squad-dev) — estética OK?        │
│ 2. revisor-carrossel — copy OK?                     │
│ 3. Regra #188/#19 — Cormorant em dígitos? propagado?│
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ JADE — apresenta ao Gui                             │
│ - Pasta: workspace/output/carrosseis/YYYY-MM-DD-slug/   │
│ - Arquivos: roteiro.md, briefing-visual.md, PNGs    │
│ - Aguarda aprovação                                 │
└─────────────────────────────────────────────────────┘
   ↓
Gui aprova → Jade marca tarefa concluída em pendencias.md
```

---

## Skills envolvidas

| Skill | Quem dispara | Quando |
|---|---|---|
| `/transcrever-video` | Jade | input = URL YouTube (auto-detecta) |
| `/escrever-estrategia` | Jade | após transcrição (ou direto se tema) |
| `/revisar-estrategia` | Jade | output do estrategista antes de seguir |
| `/criar-carrossel` | (skill mãe genérica) | encadeia estrategista→copywriter→imagem |
| `/criar-carrossel-de-video` | (skill mãe ponta-a-ponta) | encadeia transcrição→estratégia→copy→imagem |
| `/revisar-carrossel` | Jade | após copywriter entregar roteiro |
| (script gerar-imagem.mjs) | carrossel agent | gera PNGs via Playwright |
| revisor-visual (Agent) | Jade | após PNGs prontos (estética) |

---

## Tabela de tarefas (registro contínuo)

| # | Data | Input | Slug | Status | Lâminas | Output path |
|---|---|---|---|---|---|---|
|   |      |       |      |        |         |             |

---

## Critérios de aprovação final

- [ ] Roteiro respeita Light Copy (1 premissa/slide, slide 1 = hook, CTA só no último)
- [ ] Cormorant não aparece em dígitos (Regra #188)
- [ ] Cada PNG = 1080x1350, ≤ 500KB, fonte Syne+Inter (NÃO Cormorant em números)
- [ ] revisor-visual aprovou (sem defeitos estéticos)
- [ ] `/revisar-carrossel` aprovou (texto OK)
- [ ] Pasta `workspace/output/carrosseis/YYYY-MM-DD-[slug]/` tem `roteiro.md`, `briefing-visual.md`, slides PNG, `mapa.md` da pasta

---

## Memórias relevantes

- `project_foco_carrossel_youtube_e_meta_ads.md` — foco macro
- `feedback_propagacao_correcoes.md` — Regra #19
- `design_rules_paginas.md` — Cormorant proibida em dígitos (vale pra carrossel também)
