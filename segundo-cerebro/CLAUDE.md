# CLAUDE.md — segundo-cerebro de {{NOME_OPERADOR}}

Este repositório é a fonte única de verdade sobre {{NOME_OPERADOR}} — marca pessoal, negócio, tom de voz e sistemas. É usado como contexto pelos agentes de IA e pelo próprio operador.

---

## O que é

Uma base de conhecimento modular, versionada com Git, organizada para ser carregada por agentes de IA de forma seletiva (não inteira de uma vez). Consulte `README.md` e `mapa.md` para saber qual pasta carregar para cada tarefa.

---

## Regras para qualquer agente que trabalhe aqui

### Nunca invente conteúdo
Todo conteúdo vem de fontes reais: documentos do operador, transcrições de vídeos, falas reais. Se a informação não existe nos arquivos, não preencha com suposição.

### Carregue apenas o que for relevante
Não leia o repositório inteiro. Use a tabela do `README.md` para saber qual pasta carregar.

### Não duplique conteúdo entre arquivos
Se algo precisa ser referenciado em dois lugares, escolha um arquivo "dono" e cite o outro. Uma única fonte de verdade por tópico.

### Commits descritivos
- `feat:` novo arquivo ou seção
- `update:` atualização de conteúdo existente
- `fix:` correção de informação errada

---

## Estrutura rápida

```
01-identidade/   → quem é o operador, tom de voz, histórias, exemplos de copy
02-negocios/     → produtos, marca pessoal, parcerias, iscas
03-operacao/     → rotinas, automações, stack, time, CTAs
04-decisoes/     → decisões estratégicas + estrategia-viva.md
05-audiencia/    → ICP: dores, desejos, linguagem, objeções
06-oferta/       → arquitetura de cada oferta
07-conteudo/     → estratégia, pilares, canais
08-integracoes/  → histórico técnico por ferramenta
09-financeiro/   → metas, métricas, números
10-conhecimento/ → insights destilados
99-arquivo/      → matéria-prima histórica
```

---

## Governança — quem pode editar e como

**Quem pode editar:** a COO (Jade) com instrução explícita do operador, ou o próprio operador. Os demais agentes só consultam — nunca editam.

**Protocolo ao editar:**
1. Ler o arquivo completo antes de qualquer alteração.
2. Edição incremental — mudar só a seção que mudou, nunca reescrever o arquivo inteiro.
3. Nunca apagar conteúdo sem registrar o motivo — informação histórica vai para `99-arquivo/`.
4. Commit imediato com mensagem descritiva após cada atualização.

| Evento | Arquivo |
|--------|---------|
| Novo produto ou mudança de preço | `06-oferta/produtos-servicos.md` |
| Mudança de posicionamento | `01-identidade/identidade.md` + `04-decisoes/` |
| Mudança de tom de voz | `01-identidade/tom-de-voz.md` |
| Nova decisão estratégica | `04-decisoes/YYYY-MM-[nome].md` |
| Novo membro do time | `03-operacao/time.md` |
| Nova ferramenta | `03-operacao/stack.md` |
