# MAPA — squads/gestao/agentes/

> Última atualização: 07/05/2026

## Propósito

Agentes do squad-gestao (camada de orquestração estratégica). Squad-jade NÃO produz entregáveis — orquestra (Jade) e define ângulo/posicionamento (estrategista) ANTES da copy ir pra produção.

## Agentes

| Agente | Pasta | Responsabilidade |
|--------|-------|------------------|
| estrategista | `estrategista/` | Define posicionamento, ângulo e narrativa de toda LP nova ANTES da copy. Skills: `/escrever-estrategia`, `/atualizar-estrategia`, `/revisar-estrategia`. |

## Notas

- Jade (COO) opera via skill `/jade` — não tem subpasta de agente dedicada (skill é o ponto de entrada)
- Estrategista migrado de squad-conteudo em 06/05/2026 (Tarefa #124) — agora é peer da Jade
- Toda LP nova: `/escrever-estrategia` → `/revisar-estrategia` → `/escrever-pagina` (squad-copy)
