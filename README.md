# Squad de Agentes — Template

Sistema operacional de agentes de IA para negócios digitais. Criado pelo Gui Ávila como parte do **[Sistema Reverso](https://guiavila.com/reverso)**.

## Como começar

1. Clone este repositório
2. Abra no Claude Code
3. Execute `/jade-iniciar` como primeira mensagem
4. Se for a primeira vez, rode `/configurar-squad` e responda as perguntas sobre seu negócio
5. Sua Jade estará pronta para operar

## Estrutura

```
squad/
├── CLAUDE.md          — framework e regras do squad
├── AGENTS.md          — regras invioláveis
├── IDENTIDADE.md      — seus dados (preenchido via /configurar-squad)
├── segundo-cerebro/   — conhecimento do seu negócio (fica só na sua máquina)
├── squads/            — 8 squads funcionais com agentes especializados
├── workspace/         — estado operacional (gerado em uso)
└── .claude/           — skills, agentes e hooks
```

## Skills principais

| Skill | O que faz |
|---|---|
| `/jade-iniciar` | Abre sessão — detecta fresh install ou operador configurado |
| `/configurar-squad` | Configura identidade do operador (rodar 1x após clonar) |
| `/jade` | COO — orquestra qualquer demanda |
| `/criar-carrossel` | Cria carrossel de conteúdo |
| `/escrever-newsletter` | Escreve newsletter |
| `/criar-criativo` | Cria anúncio pago |
| `/escrever-pagina` | Cria página de vendas |
| `/atualizar-jade` | Puxa updates do template sem apagar seus dados |

## Recebendo atualizações

Quando o Gui lançar melhorias no template, rode `/atualizar-jade`. O squad atualiza o framework (skills, agentes, hooks) sem tocar nos seus dados pessoais (IDENTIDADE.md, segundo-cerebro/).

## Sistema Reverso

Esse template é parte do **Sistema Reverso** — o curso onde o Gui Ávila ensina como montar e operar seu próprio time de agentes de IA.

👉 [guiavila.com/reverso](https://guiavila.com/reverso)
