# Aprendizados — @designer-revisor (squad-dev)

> Append-only. Cada rejeição do {{OPERADOR}} vira entrada permanente aqui (Regra #14).
> Formato: data, contexto, falha, correção, regra incorporada.

---

<!-- vazio inicial — Tarefa #183 (07/05/2026) -->

### Bug crítico — footer duplicado passou batido (2026-05-14)
**Contexto:** /mentoria redesign top-ticket. Dei APROVADO com 80 screenshots, footer duplicado em prod descoberto pelo {{OPERADOR}}.
**O que não funcionou:** rolar 80 screenshots sem identificar âncora estrutural (footer/header aparecendo 2x na full-page).
**Correção aplicada:** novo item 13 na skill `/revisar-visual-pagina` — "Header/Footer únicos: capturar screenshot full-page e VER se há rodapé/header repetido. Se mesmo bloco aparece 2x, REPROVAR."
**Regra pra não repetir:** ao revisar screenshot full-page, sempre rodar do topo ao rodapé SEM PULAR. Se identificar mesmo bloco visualmente (cores, layout, conteúdo) repetido, REPROVAR mesmo se markup parece OK.
**Validação extra:** complementar Playwright com grep no HTML servido — `grep -c 'Copyright' dist/[slug]/index.html` = 1.
