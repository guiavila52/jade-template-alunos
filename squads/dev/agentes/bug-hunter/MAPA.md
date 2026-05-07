# MAPA — squads/dev/agentes/bug-hunter/

> Última atualização: 07/05/2026

## Propósito

Memória e aprendizados do agente **bug-hunter** (squad-dev). Caça bugs ANTES do deploy via Playwright + análise de console/network/markup. Detecta e reporta com evidência — NÃO corrige (correção é responsabilidade do `paginas-dev` ou `paginas`).

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `MAPA.md` | Este arquivo. |
| `memoria.md` | Contexto operacional, categorias de bug caçadas, skills associadas. |
| `aprendizados.md` | Lições do agente — bugs recorrentes, falsos positivos calibrados, padrões. |

## Definição canônica

`.claude/agents/bug-hunter.md` — descrição/triggers/tools/model. Editar a definição do agente lá; aqui só vivem memória e aprendizados.

## Skills associadas

- Despachado pela Jade no **Triple-check** antes de cada `vercel --prod` (junto com `paginas` + `paginas-dev`)
- Output canônico em `squad/output/auditorias/bug-hunt-{slug}-{YYYY-MM-DD-HHMM}.md`

## Regras

- Manter atualizado quando categoria nova de bug for incorporada
