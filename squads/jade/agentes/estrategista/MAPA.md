# MAPA — estrategista

**Propósito:** Agente Estrategista — define posicionamento, ângulo, narrativa e métricas ANTES da copy. Toda LP nova passa por aqui antes de ir pro `@paginas`.

**Última atualização:** 2026-05-06 (instructions.md preenchido + leitura obrigatória de `estrategia-viva.md`)

## Conteúdo

| Arquivo | Função |
|---|---|
| `instructions.md` | TREINAMENTO COMPLETO do agente — base de conhecimento, funil, framework de output, princípios estratégicos |
| `aprendizados.md` | lições registradas após aprovação/rejeição de estratégias |
| `memoria.md` | memória do agente (estado, projetos ativos, contexto) |

## Skills relacionadas

- `/escrever-estrategia` — agente é despachado por ela (começa com bloco BLOQUEANTE de leitura obrigatória)
- `/atualizar-estrategia` — registra decisões novas em `Segundo Cérebro/04-decisoes/estrategia-viva.md` (chamada após aprovação se gerar decisão nova)
- `/revisar-estrategia` — Jade revisa o output do agente
- `/criar-pagina` — orquestrador que aciona o estrategista no passo 2

## Documentos que o agente DEVE ler antes de produzir

- `Segundo Cérebro/04-decisoes/estrategia-viva.md` — estado vigente (datas, posicionamento, métricas)
- MEMORY.md index + memórias relevantes ao escopo
- `Segundo Cérebro/01-identidade/banco-de-historias.md` (se existir)
- Princípios e formato 11 seções → ver `instructions.md` desta pasta

## Output canônico

`squad/output/estrategia/{YYYY-MM-DD}-{slug}-estrategia.md` — formato de 11 seções definido em `instructions.md`.
