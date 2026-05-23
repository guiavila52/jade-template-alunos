# memoria.md — Squad Dev

> Memória operacional do squad-dev. Atualizar conforme agentes entregam e padrões emergem.

---

## Contexto do Squad

Responsável pelo {{Plataforma_Conteudo}} (App Reverso), integração via API REST do {{Plataforma_Conteudo}} (Bearer `sk-sq-*`, endpoints em `segundo-cerebro/03-operacao/{{plataforma_conteudo}}-historico.md`) e infraestrutura de código. **Nota:** o antigo MCP server do {{Plataforma_Conteudo}} foi descontinuado em 12/05/2026 — retorna 401.

**Projeto principal:** `/Users/guiavila/Documents/Projetos IA Gui Ávila/App Reverso/` — Next.js + Supabase + Claude API
**Status:** squad a estruturar — agentes a criar

---

## Padrões e preferências

- Ler `SECURITY.md` do {{Plataforma_Conteudo}} antes de qualquer implementação
- Nunca commitar sem revisão do Gui

---

## Projeto Astro do squad — `Páginas Astro Gui Ávila/` (registrado 06/05/2026)

**Caminho absoluto:** `/Users/guiavila/Documents/Projetos IA Gui Ávila/Páginas Astro Gui Ávila/`

Projeto paralelo ao Next legado (`Sites Gui Ávila/`). Roda em `localhost:4321`. Toda página nova (criada via `/criar-pagina-nova` ou migrada via `/migrar-pagina`) vai para `src/pages/[slug]/index.astro`.

**Stack final escolhida (T1 — Onda 1):**
- Astro 6.2.2
- Tailwind CSS v4.2.4 via `@tailwindcss/postcss` (PostCSS) — **não** o plugin Vite
- Motivo: `@tailwindcss/vite@4.2.x` quebra com o rolldown/Vite 7 que vem no Astro 6 (erro `Missing field tsconfigPaths on BindingViteResolvePluginConfig.resolveOptions`). PostCSS é compatível e estável.

**Componentes base já criados:**
- `src/layouts/Base.astro` — head + fontes + GTM placeholder + slot
- `src/components/Button.astro` — variantes primary/secondary, tamanhos md/lg
- `src/components/Section.astro` — wrapper com sec-label e bg alternado
- `src/components/FAQ.astro` — accordion via `<details>` nativo
- `src/styles/global.css` — `@import "tailwindcss"` + tokens `@theme` (cores, fontes)

**Comandos:**
- `npm install`
- `npm run dev` → `http://localhost:4321`
- `npm run build` → `dist/`
- `vercel --prod` → produção

Build validado em 06/05/2026. Dev server respondendo HTTP 200 em `/`.

---

## Decisão arquitetural — Tailwind v4 via PostCSS, não Vite plugin

Tentamos primeiro `@tailwindcss/vite@4.2.4` (recomendação oficial atual). Falhou no build com:
```
[@tailwindcss/vite:generate:build] Missing field `tsconfigPaths` on BindingViteResolvePluginConfig.resolveOptions
```

A causa é o resolver oxc do rolldown (Vite 7) — o plugin Tailwind ainda não foi atualizado para a nova interface. Mudança de perspectiva (regra inviolável #9): trocamos para `@tailwindcss/postcss` + `postcss.config.mjs`. Build passou. Reavaliar quando `@tailwindcss/vite` >= 4.3 sair.

---

## Esteira de páginas — Onda 1 entregue (06/05/2026)

Skills atualizadas para Astro:
- `/ajustar-pagina` — output sempre `.astro`, reuso de componentes obrigatório
- `/revisar-codigo-pagina` — checklist Astro (frontmatter, Layout, props tipadas, tokens)
- `/criar-pagina-nova` — adicionados passos [12]-[16]: preview localhost → OK do Gui → `vercel --prod` → registros
- `/migrar-pagina` — adicionada seção `## Fluxo` (Regra #20, antes #13 duplicada) e integração com a esteira (despacha `/ajustar-pagina` → `/revisar-codigo-pagina` → `/publicar-pagina` após aprovação do markdown)

Skill nova:
- `/publicar-pagina` — build local, preview, OK do Gui, deploy `vercel --prod`, atualização automática dos 3 registros (`squads/dev/tarefas.md`, `workspace/output/paginas/mapa.md`, `workspace/processos/pipeline-paginas.md`).

---

## Visão de integração: Squad ↔ {{Plataforma_Conteudo}} (registrado 05/05/2026)

**O {{Plataforma_Conteudo}} é o painel visual que complementa o trabalho do squad.**

O squad produz — o {{Plataforma_Conteudo}} organiza, exibe e gerencia aprovação.

Exemplo do fluxo ideal:
1. Gui pede ao squad: "faz uma thumbnail para o vídeo X"
2. Squad dev gera a thumbnail
3. Squad chama a API REST do {{Plataforma_Conteudo}} (Bearer `sk-sq-*`) — aparece lá para aprovar
4. Gui aprova no painel visual do {{Plataforma_Conteudo}}

Endpoints REST canônicos (newsletters, carrossel, linkedin, vertical, youtube — métodos POST/GET/PATCH + approve/send): ver `segundo-cerebro/03-operacao/{{plataforma_conteudo}}-historico.md` (fonte completa, com exemplos curl).

**Arquitetura:**
Squad (Claude Code) → HTTP `Authorization: Bearer ${CONTENT_API_KEY}` em `https://{{plataforma_conteudo}}.{{DOMINIO}}/api/content/*` → Painel visual para o Gui aprovar

**Nota histórica [DEPRECATED 2026-05-14]:** o caminho antigo era Squad → MCP server (tools `mcp__{{CONTENT_PLATFORM}}__*`) → API do {{Plataforma_Conteudo}}. MCP descontinuado em 12/05/2026 — chamadas retornam 401. Migração consolidada pela API REST descrita acima.

**Pré-requisito:** API key por usuário no {{Plataforma_Conteudo}} (já está na fila do Squad Dev).

---

## Estado atual dos agentes

| Agente | Status | Observações |
|--------|--------|-------------|
| — | a criar | Prioridade: API key → MCP server → integração com squad |
