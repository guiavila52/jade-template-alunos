# Estrutura por Áreas — Bruno Okamoto

> Modelo de organização por área do negócio. Referência para implementar no squad do Gui (Pendência #6).

---

## Conceito

Cada área do negócio tem 3 pastas base:

- `contexto/` — o que é a área: KPIs, equipe, ferramentas, estado atual
- `rotinas/` — o que o agente está fazendo: crons ativos, automações, frequência
- `skills/` — o que o agente sabe fazer: capacidades disponíveis sob demanda

**Distinção crítica:**
- **Skill** = capacidade. "Sei gerar relatório de Meta Ads."
- **Rotina** = execução ativa. "Gero relatório todo dia às 8h e 20h."

---

## Estrutura proposta para o Gui

```
Squad Empresa Gui Ávila/
└── areas/
    ├── conteudo/
    │   ├── contexto/     → o que é a área de conteúdo, KPIs, equipe
    │   ├── rotinas/      → crons ativos, frequência de posts, pipelines
    │   └── skills/       → skills disponíveis (carrossel, newsletter, etc.)
    ├── marketing/
    │   ├── contexto/
    │   ├── rotinas/
    │   └── skills/
    ├── comercial/
    │   ├── contexto/
    │   ├── rotinas/
    │   └── skills/
    ├── atendimento/
    │   ├── contexto/
    │   ├── rotinas/
    │   └── skills/
    ├── financeiro/
    │   ├── contexto/
    │   ├── rotinas/
    │   └── skills/
    └── operacoes/
        ├── contexto/
        ├── rotinas/
        └── skills/
```

---

## Status

Pendência #6 no squad — ainda não implementado. Implementar após estabilizar os agentes atuais.

**Regra:** não misturar com o segundo-cerebro (base de conhecimento sobre o Gui). São camadas separadas:
- **segundo-cerebro** = quem é o Gui, seus produtos, seu público, sua voz
- **Areas/** = como o squad opera, o que está rodando, o que sabe fazer
