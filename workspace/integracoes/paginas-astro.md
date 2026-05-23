# Páginas Astro Gui Ávila — Repo de produção

> **Decisão (18/05/2026):** páginas continuam em repo SEPARADO do squad Jade. Razão: Vercel já aponta pra esse repo, separação framework (Jade) vs produto (páginas), histórico git preservado.

## Path canônico

```
/Users/guiavila/Documents/Projetos IA Gui Ávila/Páginas Astro Gui Ávila/
```

Páginas individuais ficam em:
```
src/pages/{slug}/index.astro
```

Exemplos atuais:
- `src/pages/squad-time-ia/index.astro` — vitrine v1 (produção em `sites.{{DOMINIO}}/squad-time-ia`)
- `src/pages/squad-time-ia-v2/index.astro` — vitrine v2 (em iteração)
- `src/pages/reverso/index.astro` — Sistema Reverso
- `src/pages/mentoria/index.astro` — Mentoria
- `src/pages/consultoria/index.astro` — Consultoria
- `src/pages/automacoes/index.astro` — Automações
- `src/pages/clickup8x/index.astro` — ClickUp 8x
- `src/pages/inscricao-aula-gui-avila-{{lms}}/index.astro` — captura {{LMS}}
- `src/pages/oferta-irresistivel-{{lms}}/index.astro` — oferta {{LMS}}
- `src/pages/mentoria-precos/index.astro` — preços mentoria
- `src/pages/natal/index.astro` — campanha natal

## Comandos úteis (rodar dentro do repo)

```bash
cd "/Users/guiavila/Documents/Projetos IA Gui Ávila/Páginas Astro Gui Ávila"
npm run dev      # localhost preview
npm run build    # build estático
vercel --prod    # deploy produção (só após triple-check + designer-revisor APROVADO)
```

## Deploy

- Vercel projeto: aponta diretamente pra esse repo
- Domínio: `sites.{{DOMINIO}}` (rota raiz) + subrotas `/squad-time-ia`, `/reverso`, etc.
- DNS gerenciado: Hostinger (CNAME pra Vercel)
- Auto-deploy: push em `main` triggera build

## Para subagents (dev frontend, designer-revisor)

Quando Jade despachar tarefa de página, **sempre passar este path absoluto no briefing**. Subagent não tem que adivinhar — recebe o caminho pronto.

## Histórico

- 2026-05-18 — Gui questionou se devia mover páginas pro repo Jade. Decisão: manter separado. Criado este arquivo pra fixar path canônico e evitar perda de tempo de subagents procurando o repo.
