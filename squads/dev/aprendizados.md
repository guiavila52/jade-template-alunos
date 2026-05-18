# Aprendizados do squad-dev — não existe mais

Conteúdo migrado em 2026-05-14 pra `squads/dev/agentes/desenvolvedor-frontend/aprendizados.md`.

Regra: aprendizados moram em agente-level (`squads/{squad}/agentes/{agente}/aprendizados.md`), nunca squad-level.
Cross-squad vai pra auto-memory `~/.claude/.../memory/feedback_*.md`.

### Footer/Header duplicado — Base.astro já renderiza por default
**Data:** 2026-05-14
**Tarefa:** /mentoria redesign top-ticket — fix footer duplicado em prod
**Bug:** Dev adicionou `<Footer />` manual no index.astro + Base.astro já renderiza por default = 2 footers em produção. Passou batido pelos 3 revisores (visual 80 screenshots, código, bug-hunter).
**Causa-raiz processual:** revisor visual rolou screenshots full-page mas não verificou se elementos âncora (footer, header) aparecem 1x vs 2x. Revisor código não tinha item explícito de grep `<Footer\b`.
**Regra pra nunca repetir:**
1. Page que estende `<Base>` NUNCA adiciona `<Footer />` ou `<Header />` manual (Base tem footer/header = true default)
2. Revisor código roda `grep -c '<Footer\b' src/pages/[slug]/index.astro` antes de aprovar — deve ser 0
3. Revisor visual rola screenshot full-page identificando blocos âncora — se algum aparecer 2x, REPROVAR
4. Bug-hunter inclui no smoke test: `grep -c 'Copyright' dist/[slug]/index.html` = 1
**Skills atualizadas:** `/ajustar-pagina`, `/revisar-codigo-pagina`, `/revisar-visual-pagina` (item 13)
**Memória cross-squad:** `feedback_paginas.md` atualizada
