# Agente: qa-responsividade

**Squad:** dev  
**Criado em:** 2026-06-09  
**Status:** 🟢 ATIVO  
**Definição executável:** `.claude/agents/qa-responsividade.md`

## Responsabilidade

Especialista em QA de responsividade mobile. Garante que páginas LP funcionam 100% em dispositivos móveis. Testa múltiplos viewports, verifica overflow horizontal, tap targets, legibilidade, sliders, hero, formulários e toda interação.

## Quando é chamado

- Junto com `designer-revisor` no fluxo `/revisar-visual-pagina`
- Antes de qualquer `vercel --prod`
- Após mudanças de layout, CSS, breakpoints

## Viewports obrigatórios

320px · 375px · 390px · 414px · 768px

## Checklist (20 pontos)

Ver `.claude/agents/qa-responsividade.md` — definição completa com checklist, script Playwright e formato de output.

## Aprendizados

Ver `squads/dev/agentes/qa-responsividade/aprendizados.md` — lido ANTES de qualquer execução.

## Integração no fluxo

Adicionado na skill `/revisar-visual-pagina` como **segundo gate obrigatório** (primeiro = designer-revisor estética, segundo = qa-responsividade mobile). Ambos devem APROVAR antes do triple-check e deploy.
