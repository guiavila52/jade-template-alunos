---
name: popular-segundo-cerebro
description: Preenche o Segundo Cérebro do squad automaticamente usando perfis públicos do Instagram e/ou YouTube do aluno. Chamada ao final do /configurar-squad ou manualmente depois. Extrai nicho, ICP, tom e produtos via WebFetch e cria os arquivos de contexto do negócio.
model: claude-sonnet-4-5
---

# Skill: /popular-segundo-cerebro

Você acabou de configurar seu squad. Agora vamos dar contexto real para os agentes — eles precisam saber quem é você, quem é seu cliente e o que você vende para produzir no seu tom e alinhados ao seu negócio.

Esta skill extrai isso automaticamente dos seus perfis públicos (Instagram e/ou YouTube) e preenche as pastas do Segundo Cérebro.

---

## Passo 1 — Pedir os perfis

Enviar uma única mensagem amigável ao aluno:

```
Para preencher o Segundo Cérebro com informações reais do seu negócio, preciso de pelo menos um dos seus perfis públicos:

- Handle do Instagram (ex: @joaosilva) — recomendado
- URL ou nome do canal YouTube (ex: youtube.com/@joaosilva ou só "João Silva")

Pelo menos um dos dois é necessário para continuar.
Se quiser pular essa etapa, me diz e preenchemos manualmente.
```

Aguardar resposta. Validar:
- Extrair handle sem o `@` se o aluno colocar com `@`
- Aceitar "pular" → ir direto para as 3 perguntas manuais do Passo 3
- Se nenhum dado fornecido → pedir de novo uma vez, se ainda nada → ir pro Passo 3

---

## Passo 2 — Extrair informações via WebFetch

### Instagram

Tentar na seguinte ordem (parar quando tiver dados suficientes):

1. `https://www.instagram.com/{handle}/` — HTML público
2. Se bloqueado ou sem conteúdo: `https://www.instagram.com/{handle}/?__a=1`

Extrair do HTML:
- `meta[name="description"]` ou `og:description` → bio/descrição do perfil
- `og:title` → nome completo
- Qualquer menção a produto, serviço, nicho na bio
- Número de posts se visível (indicador de atividade)

Se Instagram retornar 401/403 ou página de login → perfil privado ou bloqueado → registrar como "Instagram indisponível" e prosseguir com YouTube ou Passo 3.

### YouTube

Tentar na seguinte ordem:

1. `https://www.youtube.com/@{handle}/about`
2. `https://www.youtube.com/c/{handle}/about`
3. `https://www.youtube.com/user/{handle}/about`

Extrair do HTML:
- Descrição do canal (`meta[name="description"]` ou seção "Sobre")
- Nome do canal
- Tópicos, categorias, palavras-chave mencionados
- Número de inscritos se visível (indicador de escala)

Se nenhuma URL funcionar → registrar como "YouTube indisponível" e prosseguir.

---

## Passo 3 — Complementar com perguntas diretas (quando perfis insuficientes)

Se os perfis não retornaram informação suficiente para inferir nicho + ICP + produto, fazer 3 perguntas rápidas (uma por vez):

1. "Qual é o seu nicho? (ex: marketing digital, fitness feminino, finanças pessoais)"
2. "Quem é seu cliente ideal? (em uma frase, ex: 'empreendedores que querem escalar sem contratar')"
3. "Qual seu principal produto ou serviço hoje? (ex: curso online, mentoria, serviço de consultoria)"

Registrar respostas e usar em conjunto com o que foi extraído.

---

## Passo 4 — Inferir dados do negócio

Com base em tudo que foi coletado, inferir:

| Campo | Como inferir | Exemplo |
|---|---|---|
| Nicho principal | Bio + descrição do canal + palavras-chave | "marketing digital para pequenas empresas" |
| Público-alvo (ICP) | Linguagem da bio + tipo de conteúdo + resposta direta | "empreendedores iniciantes 25-40 anos" |
| Tom de comunicação | Análise da bio: formal/informal, direto/inspiracional, técnico/acessível | "direto e educativo, sem jargão" |
| Produtos/serviços | Qualquer menção a curso, mentoria, serviço, produto na bio ou canal | "curso online, mentoria em grupo" |
| Canais principais | Onde os perfis foram encontrados com mais conteúdo | "YouTube principal, Instagram complementar" |
| Funil inferido | Do conteúdo gratuito para produtos identificados | "YouTube → curso → mentoria" |

Se não conseguir inferir algum campo com confiança → marcar como "(a confirmar)" para o aluno revisar no Passo 5.

---

## Passo 5 — Preencher os arquivos do Segundo Cérebro

Criar os arquivos abaixo via Bash heredoc ou python3 (`cat >` ou `python3 -c`). **Nunca usar Write/Edit tool** nesses arquivos.

Criar diretórios se não existirem antes de criar os arquivos.

### `segundo-cerebro/01-identidade/perfil-operador.md`

Criar ou sobrescrever:

```bash
mkdir -p "segundo-cerebro/01-identidade"
DATA_HOJE=$(date +%Y-%m-%d)
cat > "segundo-cerebro/01-identidade/perfil-operador.md" << EOF
# Perfil do Operador

## Nome
[nome extraído ou nome do aluno coletado no /configurar-squad]

## Nicho
[nicho inferido]

## Tom de comunicação
[tom inferido — ex: direto e educativo, inspiracional, técnico acessível]

## Canais ativos
[listar só os que foram fornecidos]
- Instagram: @[handle] — [bio resumida]
- YouTube: [canal] — [descrição resumida]

## Bio resumida
[bio extraída ou síntese das informações coletadas]

## Produtos e serviços mencionados
[lista do que foi encontrado ou informado]

_Preenchido automaticamente via /popular-segundo-cerebro em $DATA_HOJE_
EOF
```

### `segundo-cerebro/05-audiencia/perfil-ideal-cliente.md`

Criar ou sobrescrever:

```bash
mkdir -p "segundo-cerebro/05-audiencia"
DATA_HOJE=$(date +%Y-%m-%d)
cat > "segundo-cerebro/05-audiencia/perfil-ideal-cliente.md" << EOF
# Perfil Ideal de Cliente (ICP)

## Quem é
[descrição inferida do público-alvo — incluir faixa etária e contexto se disponível]

## Dores principais
[inferir 3-5 dores prováveis com base no nicho e tipo de produto — ex: "não sabe por onde começar", "desperdiça tempo em tarefas manuais"]

## O que busca
[o que esse público quer alcançar — resultado desejado]

## Onde está
- Instagram: [sim/não — baseado nos perfis fornecidos]
- YouTube: [sim/não]

## Linguagem que ressoa
[tipo de linguagem que funciona com esse público — baseado no tom do operador e no nicho]

_Preenchido automaticamente via /popular-segundo-cerebro em $DATA_HOJE_
EOF
```

### `segundo-cerebro/02-negocios/produtos-servicos.md` (só criar se produtos foram encontrados)

Se identificou pelo menos um produto ou serviço:

```bash
mkdir -p "segundo-cerebro/02-negocios"
DATA_HOJE=$(date +%Y-%m-%d)
cat > "segundo-cerebro/02-negocios/produtos-servicos.md" << EOF
# Produtos e Serviços

## Oferta principal
[produto/serviço principal identificado]

## Outros produtos
[lista se encontrou mais de um — ou "a confirmar" se não encontrou]

## Funil inferido
[o que foi identificado do conteúdo gratuito até a oferta paga]

_Preenchido automaticamente via /popular-segundo-cerebro em $DATA_HOJE_
EOF
```

---

## Passo 6 — Mostrar resultado ao aluno

Após criar os arquivos, apresentar um resumo claro:

```
Segundo Cérebro preenchido. Aqui está o que eu identifiquei:

**Nicho:** [nicho]
**Cliente ideal:** [ICP em uma frase]
**Produtos encontrados:** [lista ou "nenhum encontrado — verifique segundo-cerebro/02-negocios/"]
**Tom de comunicação:** [tom]

**Arquivos criados:**
- segundo-cerebro/01-identidade/perfil-operador.md
- segundo-cerebro/05-audiencia/perfil-ideal-cliente.md
[- segundo-cerebro/02-negocios/produtos-servicos.md (se criado)]

Isso está correto? Quer ajustar alguma coisa?
```

Aguardar confirmação do aluno.

Se o aluno quiser ajustar:
- Perguntar o que está errado (campo específico)
- Aplicar correção no arquivo correspondente via Bash (`sed -i` ou reescrever com `cat >`)
- Confirmar que foi corrigido

Se confirmar que está OK → ir pro Passo 7.

---

## Passo 7 — Mensagem de encerramento

Após confirmação final, fechar o onboarding:

```
Seu squad está configurado e pronto pra trabalhar.

Os agentes já conhecem seu negócio. Experimente:
- /criar-criativo — anúncio do zero em segundos
- /escrever-newsletter — newsletter completa com revisor
- /criar-carrossel — pauta vira carrossel visual

Quer ir mais fundo? O {{NOME_PRODUTO}} ensina a montar e operar
esse time de IA no seu negócio:
→ {{DOMINIO}}/{{PRODUTO_PRINCIPAL_SLUG}}
```

---

## Notas de implementação

### Quando perfis são privados ou inacessíveis

- Instagram retornou 401/403/redirect para login → pular, anotar no resumo final como "não acessível"
- YouTube não encontrado em nenhuma variação da URL → pular, anotar
- Nenhum perfil disponível → ir direto para as 3 perguntas do Passo 3
- Ao menos um perfil funcionou + complementado pelas perguntas → suficiente para prosseguir

### Sobre os arquivos criados

- Os arquivos SUBSTITUEM templates vazios (não acumular conteúdo com `>>`)
- Sempre usar `cat >` ou `python3` para escrever — nunca Write/Edit tool (§11 AGENTS.md)
- Criar diretório com `mkdir -p` antes de criar o arquivo
- Campos insuficientes → marcar como "(a confirmar)" para o aluno preencher depois manualmente
- A data no rodapé de cada arquivo usa `$(date +%Y-%m-%d)` no momento da criação

### Esta skill pode ser chamada

- **Ao final do /configurar-squad** — caminho principal
- **Manualmente pelo aluno depois** — basta chamar `/popular-segundo-cerebro`
- **Após atualização de perfis** — sobrescreve os arquivos com dados mais recentes

### Tom com o aluno

- Amigável, direto, sem jargão técnico
- Não explicar o que é "heredoc", "WebFetch", "inferência" — só usar
- Ao apresentar resultados, mostrar o que foi descoberto como se fosse uma pesquisa natural, não um processo técnico
- Se algo não foi encontrado, normalizar ("Instagram estava privado, então respondi com base no que você me disse")
