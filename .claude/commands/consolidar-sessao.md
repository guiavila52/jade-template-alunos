---
name: consolidar-sessao
description: Varre a conversa atual e salva regras, decisoes, preferencias, pendencias e informacoes novas que ainda nao foram registradas.
type: skill
---

# Skill: /consolidar-sessao

Passa por toda a conversa atual e salva o que ainda não foi registrado: regras de negócio, decisões, preferências, pendências novas, informações sobre o {{NOME_OPERADOR_CURTO}} ou o negócio.

## Quando usar

Quando o {{NOME_OPERADOR_CURTO}} sentir que deu muitas informações novas na sessão e quer garantir que nada foi perdido. Não tem limite de quantidade — usar sempre que o {{NOME_OPERADOR_CURTO}} pedir.

## O que fazer

### 1. Revisar a conversa completa da sessão atual

Passar por todas as mensagens trocadas nesta sessão. Para cada trecho, identificar se contém:

- **Regra de negócio nova** — como algo funciona operacionalmente (ex: "NF só sai 15 dias após a compra")
- **Decisão estratégica** — escolha que afeta produtos, squads, arquitetura, prioridades
- **Preferência ou feedback sobre o squad** — como o {{NOME_OPERADOR_CURTO}} quer que o squad se comporte
- **Informação nova sobre o {{NOME_OPERADOR_CURTO}}, o negócio ou os produtos** — algo que não estava no segundo-cerebro
- **Pendência nova** — tarefa, bloqueio ou demanda que surgiu na conversa e ainda não está em `workspace/memory/pendencias.md`
- **Aprendizado técnico** — decisão de stack, padrão de código, integração

### 2. Checar o que já existe

Antes de salvar qualquer coisa, verificar:

- `MEMORY.md` — índice de memórias persistentes
- `workspace/memory/pendencias.md` — fila de pendências
- `workspace/memory/decisoes.md` — decisões estratégicas
- `segundo-cerebro/mapa.md` — base de conhecimento do {{NOME_OPERADOR_CURTO}}

Só salvar o que genuinamente **não existe ainda** ou está **desatualizado**. Não duplicar.

### 3. Salvar o que falta

Para cada item novo encontrado:

**Memória persistente** (regras, feedback, preferências, contexto do negócio):
- Criar arquivo em `$HOME/.claude/projects/[project-hash]/memory/`
- Adicionar no `MEMORY.md`
- Tipos: `feedback`, `project`, `user`, `reference`

**Pendência nova**:
- Adicionar em `workspace/memory/pendencias.md` na seção correta (hoje, alta prioridade, média, backlog)

**Decisão estratégica**:
- Adicionar em `workspace/memory/decisoes.md`
- Se relevante para o segundo-cerebro, adicionar também em `segundo-cerebro/04-decisoes/`

**Regra de negócio de um squad específico**:
- Adicionar no arquivo de regras do squad correspondente (ex: `squads/financeiro/regras-nf.md`)

### 4. Reportar ao {{NOME_OPERADOR_CURTO}}

Ao final, apresentar resumo claro:

```
## Consolidação da sessão — [DATA]

### Salvo agora
- [tipo] [descrição breve] → [arquivo onde foi salvo]
- [tipo] [descrição breve] → [arquivo onde foi salvo]

### Já estava salvo (não duplicado)
- [lista do que já existia]

### Nada a salvar
(se não houver nada novo)
```

Se não encontrou nada novo: dizer isso diretamente. Não inventar itens para parecer produtivo.

## Regras

- Nunca salvar informações sensíveis (senhas, tokens, chaves de API) em arquivos de memória — essas ficam só no `.env.local`
- Datas relativas ("ontem", "semana passada") → converter para data absoluta antes de salvar
- Em caso de dúvida se algo é importante o suficiente para salvar: salvar. É melhor ter do que perder.

## Fluxo

```
[ {{NOME_OPERADOR_CURTO}} chama /consolidar-sessao ]
        ↓
[ 1. Varrer conversa atual ] → @jade
   identifica regras, decisões, feedback,
   pendências novas, aprendizados técnicos
        ↓
[ 2. Checar o que já existe ] → @jade
   lê MEMORY.md, pendencias.md,
   decisoes.md, segundo-cerebro/mapa.md
        ↓
   ┌──────────────────────────────┐
   ↓ (item novo)            (já existe / igual)
[ 3a. Salvar ] → @jade            [ pular item ]
   - memória persistente → $HOME/.claude/projects/.../memory/
                          + entrada em MEMORY.md
   - pendência nova       → workspace/memory/pendencias.md
   - decisão estratégica  → workspace/memory/decisoes.md
                          (+ segundo-cerebro/04-decisoes/ se relevante)
   - regra de squad       → squads/{squad}/regras-*.md
        ↓
[ 4. Reportar resumo ao {{NOME_OPERADOR_CURTO}} ] → @jade
   "Salvo agora / Já estava salvo / Nada a salvar"
        ↓
   ⟶ FIM (sessão consolidada — ok pra /clear)
```