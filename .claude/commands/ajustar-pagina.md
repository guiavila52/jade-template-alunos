<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /ajustar-pagina

Skill DEFAULT pra mudança cirúrgica em página Astro existente. Sem pipeline pesado, sem designer-revisor 3 passadas, sem aprovação cedo em DESIGN.md.

## Quando invocar

- Trocar copy/texto em página existente
- Ajustar layout/CSS pontual
- Adicionar/remover seção pequena
- Fix de bug visual
- Qualquer mudança incremental em página JÁ NO AR

## NÃO invocar quando

- Página NOVA do zero → `/criar-pagina-nova`
- Redesign COMPLETO da página → `/criar-pagina-nova`
- Migrar de GHL/Framer → `/migrar-pagina`

## Fluxo (4 steps — rápido)

1. **Dev aplica mudança** (Agent `desenvolvedor-frontend`, briefing curto)
2. **Build limpo** (`npm run build` no `Páginas Astro {{NOME_OPERADOR}}/`)
3. **Push + PR** (`git push` + `gh pr create` se não existe, senão atualiza)
4. **Link preview Vercel pro {{OPERADOR}}** ({{OPERADOR}} valida visualmente direto, sem revisor)

## Critério de aceitação

- Build passou
- Push feito
- Link preview Vercel respondido pro {{OPERADOR}}
- {{OPERADOR}} aprova → merge main → produção (com triple-check Regra §6 só aqui)

## Anti-improviso

- Pra fix maior que 30 linhas de diff: pausar e perguntar se vira `/criar-pagina-nova`
- Sem screenshots Playwright a menos que {{OPERADOR}} peça
- Sem despachar designer-revisor a menos que {{OPERADOR}} peça

## Histórico

- 2026-05-18: Skill criada (rename de `/codar-pagina`) + simplificação total. Motivo: pipeline pesado de `/criar-pagina-nova v2` virou padrão por engano, gerando ciclos de 2h pra fix de 3 linhas. Aval {{OPERADOR}} registrado.
