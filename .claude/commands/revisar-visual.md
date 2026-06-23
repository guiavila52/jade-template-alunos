---
name: revisar-visual
description: Revisa esteticamente outputs visuais (carrossel, criativo, thumb, post, pagina) reportando defeitos com coordenadas e sugestao.
type: skill
---

# Skill: /revisar-visual

**Agente:** @designer-revisor (squad-dev)  
**Maturidade:** 🟡 FUNCIONAL  
**Propósito:** Revisão estética de outputs visuais antes do publish. Detecta defeitos de composição, cor, tipografia, brand consistency, espaçamento e legibilidade mobile. NÃO corrige — apenas reporta com coordenadas + sugestão de fix.

---

## Input

- **tipo:** `carrossel` | `criativo` | `thumbnail` | `post` | `pagina`
- **path:** caminho do arquivo visual (PNG/JPG/Figma URL/preview URL)
- **contexto:** produto/campanha relacionada ({{PLATAFORMA_CURSOS}}, {{PRODUTO_PARCERIA}}, Projeto {{NOME_OPERADOR_CURTO}}, etc)

**Exemplo:**
```bash
/revisar-visual --tipo=carrossel --path=/workspace/output/conteudo/carrossel-2026-05-11.png --contexto="Projeto {{NOME_OPERADOR}}"
```

---

## O que fazer

Auditar 6 categorias visuais:

### 1. **Alinhamento / Composição**
- Elementos centrados corretamente (não deslocados 2-3px)
- Grid alignment (textos/imagens respeitam guias invisíveis)
- Gaps consistentes (não 20px entre A-B, 25px entre B-C)
- Padding simétrico ou intencional
- Hierarquia visual clara (principal → secundário → terciário óbvio)
- Eye flow natural (Z-pattern em carrossel, F-pattern em página)

**Red flags:**
- Texto cortado por borda
- Elementos sobrepostos sem intenção
- CTA perdido (não é o ponto focal)
- Muito espaço negativo vazio (desperdiça real estate)

### 2. **Cor / Contraste**
- Brand consistency (paleta do produto/contexto)
- WCAG AA mínimo (4.5:1 text pequeno, 3:1 text grande)
- Cores não brigam (sem vermelho+verde adjacentes, azul+laranja saturados juntos)
- Fundos claros com texto escuro (ou vice-versa, nunca medium-on-medium)
- CTA se destaca (cor de ação diferente do resto)

**Paletas conhecidas:**
- **Projeto {{NOME_OPERADOR}}:** preto + dourado (#D4AF37) em LPs, Light Copy (#F5F5F5 bg, #1A1A1A text) em carrosséis
- **{{PLATAFORMA_CURSOS}}:** azul (#0066CC) + branco
- **{{PRODUTO_PARCERIA}}:** vermelho (#E63946) + preto

**Red flags:**
- Texto low-contrast (cinza claro em branco, amarelo em branco)
- Paleta errada ({{PLATAFORMA_CURSOS}} azul em LP do Projeto {{NOME_OPERADOR_CURTO}})
- Gradiente excessivo (degrada legibilidade)

### 3. **Tipografia**
- Legibilidade mobile: mínimo 16px body, 22px headings, 14px fine-print
- Max 2-3 fontes (não 5 weights/families misturadas)
- Line-height adequado (1.5-1.7 body, 1.2-1.3 headings)
- Letter-spacing em display fonts (hero > 4rem precisa -0.02em mín)
- Texto não cortado (overflow, line-clamp sem reticências)
- Hierarquia tipográfica (H1 > H2 > Body óbvio)

**Regra específica (design_rules_paginas.md):**
- **Cormorant Garamond NUNCA em números** (preço, ano, data, percentual, cupom)

**Red flags:**
- Syne weight > 600 em hero (fica grosso demais)
- All-caps em parágrafo (ok em CTA/label, não em body)
- Justified text (deixa buracos em mobile)
- Texto menor que 14px (ilegível mobile)

### 4. **Brand consistency**
- Logo presente (quando aplicável — carrossel/criativo/página hero)
- Foto autor consistente (não foto A no carrossel, foto B na página)
- Paleta coerente com produto (não misturar {{PLATAFORMA_CURSOS}}+{{PRODUTO_PARCERIA}})
- Tom visual alinhado com {{NOME_OPERADOR_CURTO}} (profissional-acessível, não corporativo-frio nem casual-meme)

**Source of truth:**
- `segundo-cerebro/01-identidade/` — tom visual {{NOME_OPERADOR_CURTO}}
- `segundo-cerebro/02-negocios/` — paletas por produto

**Red flags:**
- Logomarcas de ferramentas via emoji (🔧) — usar SVG/PNG oficial
- Foto autor inconsistente entre peças da mesma campanha
- Visual não-alinhado com posicionamento ({{NOME_OPERADOR_CURTO}} = especialista IA, não influencer fitness)

### 5. **Espaço pra respirar**
- Margem segura >= 60px (não colar texto na borda)
- White space entre seções (não 100% preenchido)
- Não sobrecarregar (máx 3 elementos de atenção por slide)
- CTA tem padding generoso (não texto apertado em botão pequeno)

**Red flags:**
- 0 margin (texto encostado em borda)
- Seções coladas (sem separador visual)
- Informação demais (parágrafo gigante em carrossel)

### 6. **Leitura mobile**
- 320-360px largura ainda legível (iPhone SE, Android pequenos)
- CTA visível sem scroll (above fold)
- Imagens não cortam conteúdo crítico (rosto do {{NOME_OPERADOR_CURTO}} cortado)
- Touch targets >= 44x44px (botões grandes o suficiente)
- Não exige zoom pra ler

**Red flags:**
- Texto < 14px mobile
- CTA abaixo de fold (usuário não vê)
- Imagem hero corta rosto (mal-enquadrada)

---

## Fluxo

```
┌─────────────────────────────────────────────┐
│ 1. Recebe tipo + path + contexto             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 2. Carrega source of truth:                 │
│    - DESIGN-SYSTEM.md (páginas)             │
│    - segundo-cerebro/01-identidade/         │
│    - design_rules_paginas.md (memória)      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 3. Inspeciona visual (screenshot OU url):   │
│    - Abre imagem/URL preview                │
│    - Audita 6 categorias                    │
│    - Anota defeitos com coordenada          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 4. Classifica severidade:                   │
│    - CRÍTICO: ilegível, contraste < 3:1     │
│    - ALTO: brand errada, texto cortado      │
│    - MÉDIO: espaçamento off, hierarquia     │
│    - BAIXO: sugestão de polish              │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 5. Gera veredicto:                          │
│    APROVADO / APROVADO COM RESSALVAS /      │
│    REPROVADO                                │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 6. Salva relatório markdown:                │
│    workspace/output/auditorias/revisao-visual-  │
│    {slug}-{timestamp}.md                    │
└─────────────────────────────────────────────┘
```

---

## Regras

### Quando reprovar
- **CRÍTICO >= 1:** REPROVAR (ilegível, contraste < 3:1, brand errada, texto cortado)
- **ALTO >= 2:** REPROVAR
- **MÉDIO >= 5:** APROVAR COM RESSALVAS (pode publicar, mas corrigir no próximo)
- **BAIXO qualquer quantidade:** APROVAR (apenas anota sugestões)

### Regra Inviolável #14
Toda correção do {{NOME_OPERADOR_CURTO}} vira aprendizado permanente:
1. Skill do produtor atualizada (não errar de novo)
2. Skill do revisor-visual atualizada (não passar batido de novo)
3. Memória persistente salva (design_rules_paginas.md ou nova)

### O que NÃO faz
- **NÃO corrige** — não é designer, não edita a peça
- **NÃO redesenha** — só reporta com coordenadas + sugestão
- **NÃO audita técnica** — peso, dimensões, alt text, 404 = job do @analista-qa
- **NÃO publica** — publish só após APROVADO + {{NOME_OPERADOR_CURTO}} OK

---

## Matriz de despacho

Quando invocar /revisar-visual (pra Jade):

| Output | Revisor | Momento |
|---|---|---|
| Carrossel Instagram | revisor-visual | Antes de salvar em workspace/output/conteudo/ |
| Criativo Meta Ads | revisor-visual | Antes de upload API |
| Thumbnail YouTube | revisor-visual | Antes de publicar vídeo |
| Post LinkedIn | revisor-visual | Antes de postar |
| Página nova | revisor-codigo-pagina (não revisor-visual) | Depois de build, antes de --prod |
| Página migrada | revisor-codigo-pagina + revisor-visual | Migração = pixel-perfect = visual conta |

**Nota:** Páginas Astro = revisor-codigo-pagina é responsável. Revisor-visual só entra se migração pixel-perfect OU se {{NOME_OPERADOR_CURTO}} pedir explicitamente.

---

## Bateria de testes da skill

Antes de dar commit nesta skill, validar:

```bash
# 1. Testa contra carrossel aprovado (deve APROVAR)
/revisar-visual --tipo=carrossel --path=/workspace/output/conteudo/carrossel-exemplo-aprovado.png --contexto="Projeto {{NOME_OPERADOR_CURTO}}"

# 2. Testa contra criativo com texto cortado (deve REPROVAR)
/revisar-visual --tipo=criativo --path=/workspace/output/trafego/criativo-com-texto-cortado.png --contexto="{{PLATAFORMA_CURSOS}}"

# 3. Testa contra thumbnail com contraste baixo (deve REPROVAR)
/revisar-visual --tipo=thumbnail --path=/workspace/output/midia/thumb-contraste-baixo.jpg --contexto="YouTube"

# 4. Valida que relatório é gerado em workspace/output/auditorias/
ls -lh workspace/output/auditorias/revisao-visual-*.md

# 5. Valida classificação severidade (grep no relatório)
grep -E "CRÍTICO|ALTO|MÉDIO|BAIXO" workspace/output/auditorias/revisao-visual-*.md
```

**Critérios de sucesso:**
- REPROVAR se texto ilegível (contraste < 3:1)
- REPROVAR se Cormorant Garamond em número (design_rules_paginas.md)
- APROVAR peças sem defeito crítico
- Relatório tem coordenadas claras ("Slide 3, canto superior direito")

---

## Source of truth

Visual:
- `segundo-cerebro/01-identidade/` — tom visual {{NOME_OPERADOR_CURTO}}
- `segundo-cerebro/02-negocios/` — paletas por produto
- `Páginas Astro {{NOME_OPERADOR}}/DESIGN-SYSTEM.md` — design system páginas

Regras persistentes:
- `feedback_design_rico_contextual.md` (#182) — output tem que ter alma
- `design_rules_paginas.md` — Cormorant nunca em números
- `feedback_metricas_publicas.md` — faturamento nunca exposto
- `feedback_logomarcas_ferramentas.md` — SVG/PNG oficial, nunca emoji
- `feedback_prova_social_honesta.md` — autoridade pessoal, não métrica inflada

---

## Output canônico

Path: `workspace/output/auditorias/revisao-visual-{slug}-{YYYY-MM-DD-HHMM}.md`

Estrutura:
```markdown
# Revisão Visual — {tipo} — {contexto} — {timestamp}

## Input
- Tipo: carrossel
- Path: /workspace/output/conteudo/carrossel-2026-05-11.png
- Contexto: Projeto {{NOME_OPERADOR}}

---

## Auditoria

### 1. Alinhamento / Composição
✅ Eye flow natural (Z-pattern)
⚠️ [MÉDIO] Gap inconsistente entre slides 2-3 (20px) vs 3-4 (30px)

### 2. Cor / Contraste
✅ Paleta Light Copy ok (bg #F5F5F5, text #1A1A1A)
✅ WCAG AA: 12.6:1 (excelente)

### 3. Tipografia
✅ Syne 500 em hero (correto)
⚠️ [BAIXO] Letter-spacing hero poderia ser -0.025em (atualmente 0)

### 4. Brand consistency
✅ Logo {{NOME_OPERADOR_CURTO}} presente slide 1
✅ Foto autor consistente com última campanha

### 5. Espaço pra respirar
✅ Margem 80px (acima do mínimo 60px)
✅ White space adequado entre seções

### 6. Leitura mobile
✅ 16px body (legível)
✅ CTA 48x48px (acima mínimo 44x44px)

---

## Veredicto
**APROVADO COM RESSALVAS**

Pode publicar. Sugestões de polish pro próximo:
- Padronizar gap entre slides (25px consistente)
- Letter-spacing hero -0.025em (mais elegante)

---

## Defeitos encontrados
- Total CRÍTICO: 0
- Total ALTO: 0
- Total MÉDIO: 1
- Total BAIXO: 1

---

Agente: @designer-revisor  
Data: 2026-05-11 14:32
```

---

## Última atualização
11/05/2026 — skill criada (Onda B4)

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{NOME_OPERADOR_CURTO}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente