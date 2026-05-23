# MAPA — squads/dev/agentes/designer-revisor/

> Última atualização: 2026-05-07 (Tarefa #183)

## Propósito

Memória e aprendizados específicos do agente **revisor-visual** (squad-dev), responsável
por auditar **defeitos estéticos** de outputs visuais (carrossel, criativo, thumbnail,
post visual) ANTES da publicação.

Diferente do `bug-hunter` (defeitos técnicos: peso, dimensões, alt, console errors), o
`revisor-visual` foca em design/UX visual: alinhamento, contraste, brand consistency,
tipografia, leitura mobile, hierarquia, espaçamento.

## Escopo

- Carrossel Instagram (PNG/JPG)
- Criativo de tráfego (Meta Ads — estático ou em frames)
- Thumbnail YouTube
- Post LinkedIn com imagem
- Qualquer asset visual PNG/JPG/SVG antes de publish

**Fora de escopo:**
- Páginas (LP) — vai pro `revisor-pagina` + `revisor-codigo-pagina` + `bug-hunter`
- Vídeo — squad-midia
- Defeitos técnicos (console, 404, peso, alt) — `bug-hunter`

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `mapa.md` | Este arquivo |
| `memoria.md` | Contexto operacional do agente (regras vivas, source of truth) |
| `aprendizados.md` | Lições do agente (especialmente registros de rejeições do Gui — Regra #14) |

## Skills relacionadas

O `revisor-visual` é despachado dentro do triple-check pelas skills:
- `/criar-carrossel` (squad conteudo) — antes do publish
- `/criar-criativo` (squad trafego) — antes do publish
- `/revisar-carrossel` — pode invocar como dupla-checagem visual

## Triple-check de output visual

1. `revisor-visual` (este agente) — defeitos estéticos
2. `bug-hunter` — defeitos técnicos (peso, dimensões, alt text, asset 404)
3. Revisor de copy do squad (carrossel/copywriter/trafego) — defeitos de texto

## Referências

- `feedback_design_rico_contextual.md` (#182) — toda página/output tem alma
- `feedback_metricas_publicas_gui.md` — sem expor faturamento
- `design_rules_paginas.md` — Cormorant zero em números, fontes em preços
- `segundo-cerebro/01-identidade/` — tom visual do Gui
