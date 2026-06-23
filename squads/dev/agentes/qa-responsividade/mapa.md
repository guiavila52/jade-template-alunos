# MAPA — squads/dev/agentes/qa-responsividade/

> Última atualização: 2026-06-10

## Propósito

Agente **qa-responsividade** (squad-dev) — especialista em QA mobile. Testa páginas em 5 viewports padrão (320px, 375px, 390px, 414px, 768px) verificando overflow horizontal, tap targets, legibilidade, hero section, sliders, formulários, navegação e todos os elementos interativos.

Despachado SEMPRE junto com `designer-revisor` no fluxo `/revisar-visual-pagina` — gate duplo obrigatório antes de qualquer deploy (Regra §6).

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `aprendizados.md` | Lições do agente — padrões de bug mobile encontrados em auditorias reais. |
| `mapa.md` | Este arquivo. |

## Skills relacionadas

- `/revisar-visual-pagina` — skill principal que despacha este agente (gate duplo)
- `/qa-responsividade` — invocação direta quando necessário
- `/publicar-pagina` — só pode prosseguir após QA-MOBILE-APROVADO deste agente

## Ferramentas

Bash (Playwright headless), Read, Grep, Glob.

## Viewports testados

| Viewport | Dispositivo referência |
|---|---|
| 320px | iPhone SE (menor viewport comum) |
| 375px | iPhone 13 mini |
| 390px | iPhone 14 |
| 414px | iPhone Plus |
| 768px | iPad (tablet) |

## Output canônico

- `QA-MOBILE-APROVADO` — página passa em todos os viewports
- `QA-MOBILE-REPROVADO` — lista de problemas com viewport + descrição

## Histórico

Criado em 2026-06-09. Gate duplo (designer-revisor + qa-responsividade) implementado como resposta à necessidade de garantia mobile separada da revisão estética.
