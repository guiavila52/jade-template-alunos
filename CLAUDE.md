# Squad de Agentes — [SEU NOME]

Sistema de agentes de IA para fundadores e infoprodutores. Aqui vivem os agentes, o Segundo Cérebro (base de conhecimento) e os outputs produzidos pelo squad.

## Como começar

1. Preencha o `Segundo Cérebro/` com seu contexto (veja README em cada pasta)
2. Atualize o `squad/agents/estrategista.md` com sua meta e contexto
3. Chame `/estrategista` para começar

## Estrutura

```
squad-template/
├── .claude/commands/     → skills dos agentes (rotina, estrategista, copywriter, etc.)
├── Segundo Cérebro/      → base de conhecimento (identidade, negócios, operação)
├── squad/
│   ├── agents/           → definições e instruções de cada agente
│   ├── memory/           → memórias compartilhadas dos agentes
│   ├── output/           → outputs produzidos (carrossel, newsletter, páginas, etc.)
│   └── referencia/       → referências externas
└── CLAUDE.md             → este arquivo
```

## Segundo Cérebro

Base de conhecimento do fundador. Consultar antes de qualquer tarefa:
- `Segundo Cérebro/MAPA.md` — índice completo (leia primeiro)
- `Segundo Cérebro/01-identidade/` — identidade, tom de voz, ICP
- `Segundo Cérebro/02-negocios/` — produtos, serviços, parcerias
- `Segundo Cérebro/03-operacao/` — time, ferramentas, rotinas

## Agentes disponíveis

- `/estrategista` — orquestrador do squad (começar aqui)
- `/copywriter` — escrita em geral
- `/newsletter` — emails semanais
- `/carrossel` — carrosséis para redes sociais
- `/paginas` — páginas de captura e vendas
- `/mentoria` — gestão da mentoria
- `/trafego` — criativos e tráfego pago
- `/rotina` — cockpit do dia (agenda + emails + pendências)

## Regras

- Não inventar conteúdo sobre o fundador — se não estiver no Segundo Cérebro, perguntar
- Outputs vão em `squad/output/{agente}/`
- Decisões estratégicas vão em `Segundo Cérebro/04-decisoes/`
- Toda URL mencionada deve ser link clicável no markdown
