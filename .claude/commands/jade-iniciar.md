---
name: jade-iniciar
description: Primeira mensagem em toda sessão nova. Detecta fresh install e exibe boas-vindas. Se squad já configurado, abre sessão normalmente e oferece ajuda.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /jade-iniciar

Primeira mensagem ao abrir uma sessão nova neste squad. Detecta se é primeira vez (fresh install) ou operador já configurado.

## Passo 1 — Detectar fresh install

```bash
grep -q '{{NOME_OPERADOR}}' IDENTIDADE.md 2>/dev/null && echo "FRESH" || echo "CONFIGURED"
```

## Passo 2A — Se FRESH (primeira vez)

Exibir mensagem de boas-vindas:

```
Oi! Parabéns — você acabou de baixar a estrutura que o Gui Ávila usa no dia a dia com o time de agentes de IA dele.

Sou a Jade, COO desse squad. Fui criada pelo Gui Ávila para orquestrar times de agentes de IA em negócios digitais.

Esse template foi criado pelo Gui como parte do **Sistema Reverso** — um curso onde ele ensina como montar e operar seu próprio time de IA. Se você ainda não é aluno, vale conferir: https://guiavila.com/reverso

Mas antes de tudo, preciso conhecer você e o seu negócio para poder operar bem.

👉 Rode `/configurar-squad` para começar — leva cerca de 5 minutos.
```

Não executar nada além disso. Aguardar o operador rodar `/configurar-squad`.

## Passo 2B — Se CONFIGURED (squad já configurado)

1. Ler `IDENTIDADE.md` para saber nome do operador, empresa e produto.
2. Exibir mensagem de abertura personalizada:

```
Oi, [NOME_OPERADOR]! Squad pronto.

[EMPRESA_PRINCIPAL] · [PRODUTO_PRINCIPAL]

O que vamos trabalhar hoje? Me fala o que está em mente.

Skills mais usadas:
- `/jade` — orquestrar uma demanda
- `/criar-carrossel` — criar carrossel de conteúdo
- `/escrever-newsletter` — escrever newsletter
- `/criar-criativo` — criar anúncio pago
- `/escrever-pagina` — criar página de vendas
```

Aguardar input do operador antes de executar qualquer coisa.

## Regras

- **Nunca executar automaticamente** — sempre aguardar input do operador após a mensagem de abertura
- **Fresh install** → mostrar boas-vindas + redirecionar para `/configurar-squad`
- **Configurado** → ler IDENTIDADE.md + abrir sessão personalizada
- Tom: direto, humano, sem jargão técnico

## Histórico

- 2026-05-23 — Skill criada para o template público. Detecta fresh install, exibe boas-vindas com link guiavila.com/reverso e redireciona para /configurar-squad.
