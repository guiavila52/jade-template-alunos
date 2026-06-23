# Workspace — Estado Operacional

Esta pasta contém o estado operacional do squad. Ao contrário do `segundo-cerebro/` (knowledge atemporal), aqui ficam dados que mudam com o tempo.

## Estrutura

```
workspace/
├── memory/         Estado de trabalho — pendências, decisões, diário
├── output/         Artefatos gerados pelos agentes (gitignored)
├── regras/         Histórico de regras e reforços
├── integracoes/    Documentação de integrações externas
├── processos/      Fluxos e processos do squad
├── scripts/        Scripts utilitários
├── design-systems/ Sistemas visuais e tokens de design
└── agents/         Briefings para agentes específicos
```

## Regras

- `output/` é gitignored — nunca commitar artefatos
- `memory/` contém estado pessoal — não vai para template público
- Toda integração nova → criar doc em `integracoes/{nome}.md`
