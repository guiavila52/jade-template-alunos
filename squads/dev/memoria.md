# memoria.md — Squad Dev

> Memória operacional do squad-dev. Atualizar conforme agentes entregam e padrões emergem.

---

## Contexto do Squad

Responsável pelo Gimmick (App Reverso), integração via API REST do Gimmick (Bearer `sk-sq-*`, endpoints em `segundo-cerebro/03-operacao/gimmick-historico.md`) e infraestrutura de código. **Nota:** o antigo MCP server do Gimmick foi descontinuado em 12/05/2026 — retorna 401.

**Projeto principal:** `/Users/{{SEU_USUARIO}}/Documents/Projetos IA {{NOME_OPERADOR}}/App Reverso/` — Next.js + Supabase + Claude API
**Status:** squad a estruturar — agentes a criar

---

## Padrões e preferências

- Ler `SECURITY.md` do Gimmick antes de qualquer implementação
- Nunca commitar sem revisão do {{NOME_OPERADOR}}

---

## Projeto Astro do squad — `Páginas Astro {{NOME_OPERADOR}}/` (registrado 06/05/2026)

**Caminho absoluto:** `/Users/{{SEU_USUARIO}}/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}/`

Projeto paralelo ao Next legado (`Sites {{NOME_OPERADOR}}/`). Roda em `localhost:4321`. Toda página nova (criada via `/criar-pagina-nova` ou migrada via `/migrar-pagina`) vai para `src/pages/[slug]/index.astro`.

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
- `/criar-pagina-nova` — adicionados passos [12]-[16]: preview localhost → OK do {{NOME_OPERADOR}} → `vercel --prod` → registros
- `/migrar-pagina` — adicionada seção `## Fluxo` (Regra #20, antes #13 duplicada) e integração com a esteira (despacha `/ajustar-pagina` → `/revisar-codigo-pagina` → `/publicar-pagina` após aprovação do markdown)

Skill nova:
- `/publicar-pagina` — build local, preview, OK do {{NOME_OPERADOR}}, deploy `vercel --prod`, atualização automática dos 3 registros (`squads/dev/tarefas.md`, `workspace/output/paginas/mapa.md`, `workspace/processos/pipeline-paginas.md`).

---

## Visão de integração: Squad ↔ Gimmick (registrado 05/05/2026)

**O Gimmick é o painel visual que complementa o trabalho do squad.**

O squad produz — o Gimmick organiza, exibe e gerencia aprovação.

Exemplo do fluxo ideal:
1. {{NOME_OPERADOR}} pede ao squad: "faz uma thumbnail para o vídeo X"
2. Squad dev gera a thumbnail
3. Squad chama a API REST do Gimmick (Bearer `sk-sq-*`) — aparece lá para aprovar
4. {{NOME_OPERADOR}} aprova no painel visual do Gimmick

Endpoints REST canônicos (newsletters, carrossel, linkedin, vertical, youtube — métodos POST/GET/PATCH + approve/send): ver `segundo-cerebro/03-operacao/gimmick-historico.md` (fonte completa, com exemplos curl).

**Arquitetura:**
Squad (Claude Code) → HTTP `Authorization: Bearer ${CONTENT_API_KEY}` em `https://gimmick.{{DOMINIO}}/api/content/*` → Painel visual para o {{NOME_OPERADOR}} aprovar

**Nota histórica [DEPRECATED 2026-05-14]:** o caminho antigo era Squad → MCP server (tools `mcp__{{CONTENT_PLATFORM}}__*`) → API do Gimmick. MCP descontinuado em 12/05/2026 — chamadas retornam 401. Migração consolidada pela API REST descrita acima.

**Pré-requisito:** API key por usuário no Gimmick (já está na fila do Squad Dev).

---

## Estado atual dos agentes

| Agente | Status | Observações |
|--------|--------|-------------|
| — | a criar | Prioridade: API key → MCP server → integração com squad |
