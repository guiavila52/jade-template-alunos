# segundo-cerebro — {{NOME_OPERADOR}}

Fonte única de verdade sobre {{NOME_OPERADOR}} e o negócio — modular, versionada com Git, consultável pelos agentes de IA e pelo próprio operador. Cada arquivo tem propósito claro e pode ser carregado de forma independente.

> No começo, este cérebro está vazio (só a estrutura). Ele é preenchido no onboarding: abra o projeto, mande "oi", e a Jade te guia para montar o seu Segundo Cérebro a partir do seu Instagram, YouTube e materiais do negócio.

---

## Como usar (para agentes de IA)

Carregue **apenas os arquivos relevantes** para a tarefa, nunca o cérebro inteiro — isso é desperdício de contexto. Use a tabela abaixo como guia.

| Tipo de tarefa | Pastas a carregar |
|---|---|
| Copy / página de venda | `01-identidade/` + `05-audiencia/` + `06-oferta/` |
| Roteiro / post / conteúdo | `01-identidade/` + `05-audiencia/` + `07-conteudo/` |
| Decisão estratégica | `04-decisoes/` (inclui `estrategia-viva.md`) |
| Integração técnica | `08-integracoes/{ferramenta}-historico.md` |
| Financeiro | `09-financeiro/` |
| Onboarding de novo agente | `01-identidade/` |

---

## Estrutura da pasta (11 áreas)

```
.
├── README.md          → este arquivo
├── mapa.md            → índice das pastas (fonte da estrutura)
├── 01-identidade/     → quem é o operador: identidade, tom de voz, histórias, exemplos de copy
├── 02-negocios/       → estrutura do negócio: produtos, marca pessoal, parcerias, iscas
├── 03-operacao/       → processos e rotinas: rotinas, automações, stack, time, CTAs
├── 04-decisoes/       → decisões estratégicas datadas + estrategia-viva.md (source of truth)
├── 05-audiencia/      → ICP profundo: dores, desejos, linguagem, objeções
├── 06-oferta/         → arquitetura de cada oferta: pitch, preço, argumentos, provas
├── 07-conteudo/       → inteligência de conteúdo: estratégia, pilares, canais
├── 08-integracoes/    → histórico técnico por ferramenta
├── 09-financeiro/     → metas, métricas, números do negócio
├── 10-conhecimento/   → insights destilados a partir do 99-arquivo
└── 99-arquivo/        → matéria-prima histórica (transcrições brutas, legados)
```

---

## Como manter atualizado

- Toda atualização passa pelo Claude Code (não editar manualmente no editor).
- Mudanças importantes são commitadas com mensagem descritiva.
- Decisões estratégicas viram arquivos em `04-decisoes/`.
- Insights reaproveitáveis viram arquivos em `10-conhecimento/`.
- Pelo menos 1x por trimestre, revisar `01-identidade/` para ver se ainda reflete a realidade.
