---
name: revisar-estrategia
description: Jade revisa output do estrategista contra estrategia-viva.md, formato canonico e aprendizados — gate antes da copy.
type: skill
---

<!-- Modelo recomendado: claude-opus-4-5 (revisão estratégica exige raciocínio forte) -->

# /revisar-estrategia — Jade revisa o output do Estrategista

> Skill da Jade COO. Recebe documento de estratégia produzido pelo `@estrategista-marketing` e aprova ou devolve com apontamentos. É o gate ANTES da copy.
>
> Acionada automaticamente após `/escrever-estrategia` salvar o output, ou diretamente pelo Gui quando ele quiser que a Jade revise uma estratégia anterior.

---

## ANTES DE COMEÇAR — CONTEXTO OBRIGATÓRIO

A Jade carrega ANTES de revisar:

1. **`segundo-cerebro/04-decisoes/estrategia-viva.md`** — pra checar se data/métrica/posicionamento citado bate com estado vigente.
2. **`squads/gestao/agentes/estrategista-marketing/instructions.md`** — formato canônico de 11 seções + princípios + anti-padrões.
3. **`squads/gestao/agentes/estrategista-marketing/aprendizados.md`** — não aprovar repetição de erro já corrigido.
4. **MEMORY.md** — checar se a estratégia bate com posicionamento e feedbacks ativos.
5. **O documento estratégico submetido** — `workspace/output/estrategia/{YYYY-MM-DD}-{slug}-estrategia.md`.

Se o documento NÃO existe → devolve pra `@estrategista-marketing` com nota.

---

## Inputs esperados

- Caminho do documento de estratégia (`workspace/output/estrategia/{YYYY-MM-DD}-{slug}-estrategia.md`)
- Tarefa # de origem
- (Opcional) contexto adicional do despacho

---

## Fluxo

### 1. Carregar contexto obrigatório
Conforme bloco acima.

### 2. Aplicar checklist de revisão (formato 11 seções + princípios)

Marcar `[x]` ou `[ ]` em cada item. Documento aprovado = TODOS `[x]`.

#### Estrutura do documento
- [ ] Tem as 11 seções com nomes idênticos ao template do `instructions.md`
- [ ] Resumo executivo (SEÇÃO 1) entrega tese + público + ação esperada em 3 linhas
- [ ] Contexto (SEÇÃO 2) explica o que motivou a estratégia
- [ ] Estado atual da `estrategia-viva.md` (SEÇÃO 3) foi consultado e citado com versão/data
- [ ] Rodapé cita fontes consultadas (segundo-cerebro + memórias usadas)

#### ICP e posicionamento
- [ ] Público-alvo bate com perfil do `01-identidade/icp.md` (citação ou referência explícita)
- [ ] Estado emocional do lead ao chegar está descrito
- [ ] Origem de tráfego identificada (YouTube/Email/Instagram/LinkedIn/Pago/Direto)
- [ ] Posicionamento honesto, sem inflar
- [ ] Tese reforça "Gui = especialista nº 1 em construir squads de agentes de IA" (direta ou indiretamente)
- [ ] Funil canônico respeitado (YouTube → Imersão → Mentoria/Reverso → Consultoria)

#### Ângulo único
- [ ] Ângulo único definido em 1 frase (não tenta capturar todos os públicos)
- [ ] Banco de histórias do Gui referenciado (≥1 história do `banco-de-historias.md`)
- [ ] Ângulo está ancorado em história real (não é tese abstrata)

#### Narrativa
- [ ] Sequência narrativa tem objetivo emocional + lógico por bloco
- [ ] Comprimento por bloco está sinalizado (curto/médio/longo)
- [ ] Hero abre sem cair nos 3 Ps (Porque/Promessa imperativa/Pergunta)

#### Oferta
- [ ] Oferta cruzada com `produtos-servicos.md` e `estrategia-viva.md`
- [ ] Preço/garantia (se citados) batem com fonte canônica
- [ ] Sem prometer o que o produto não entrega
- [ ] Sem números voláteis na promessa (duração de programa, nº encontros, prazos que mudam)

#### Prova social
- [ ] Prova social escolhida está na lista permitida (sem 400k/35+/3 continentes/faturamento)
- [ ] Toda métrica citada existe literalmente em `estrategia-viva.md` (seção "Métricas que podem ser mencionadas publicamente")
- [ ] Cada item de prova tem justificativa de por quê entra NESTA página
- [ ] Sem ambiguidade em "400k usuários {{EMPRESA_COFUNDADA}}" (sempre com contexto: plataforma, não público pessoal)
- [ ] Sem mencionar Mente Matemática / {{NOME_BACKUP_ADMIN}} como empresas

#### Vocabulário
- [ ] Light Copy framework citado
- [ ] Lista de palavras-chave permitidas presente
- [ ] Lista de palavras-chave PROIBIDAS presente (qualificação, screening, triagem, "passar pelo filtro", "se você for aprovado", "fit com o perfil")
- [ ] Tom geral definido (consultivo/direto/acolhedor/provocativo) com justificativa
- [ ] Sem jargão novo inventado sem combinar (`feedback_sem_jargao.md`)

#### CTA e jornada
- [ ] CTA primário definido (texto + destino)
- [ ] CTA secundário definido (texto + destino)
- [ ] Reforços de CTA ao longo da página alinhados à narrativa
- [ ] Próximo passo no funil declarado (pra onde o lead vai depois)
- [ ] Sem CTA múltiplo no mesmo bloco

#### Hiperlinks
- [ ] Hiperlinks `{{DOMINIO}}/[slug]` mapeados (somente os usados nesta página)
- [ ] Slugs canônicos respeitados: {{produto_slug}}, manychat, clickup, clickup8x, level, automacoes, reverso, youtube, mentoria, consultoria, {{lms_slug}}
- [ ] Toda menção a empresa/produto/parceiro vira link inline (na palavra, não URL como texto)

#### Briefing pra peças derivadas (SEÇÃO 10)
- [ ] Diretrizes pra copywriter explícitas (NÃO faça + tom + estrutura sugerida)
- [ ] Pontos de atenção (aprendizados aplicáveis) listados com link
- [ ] Quando perguntar pro Gui antes de redigir está descrito
- [ ] Briefing é executável dentro de Light Copy (sem reinventar tom)

#### Decisões pendentes (SEÇÃO 11)
- [ ] Tudo que SÓ o Gui pode dar está listado
- [ ] Estrategista NÃO escolheu pelo Gui (sem decisão silenciosa)

#### Métricas de validação
- [ ] Métrica primária (conversão) definida
- [ ] Métricas secundárias propostas (tempo, scroll depth, etc.)
- [ ] Janela de avaliação definida
- [ ] Critério de "funcionou" e "falhou e revisar" claros

### 3. Decisão

**APROVADO** = todos os itens `[x]`.
- Despachar `/escrever-pagina` (ou `/escrever-copy` / `/criar-carrossel` / `/criar-criativo`, conforme aplicável) passando o documento estratégico INTEIRO.
- Atualizar `squads/conteudo/tarefas.md`: status `aprovado`.
- Notificar Gui: "Estratégia [slug] aprovada. Despachei [skill consequente]."

**REPROVADO** = qualquer item `[ ]`.
- Devolver ao `@estrategista-marketing` com:
  - Briefing original
  - Lista exata dos itens reprovados (citação)
  - Sugestão de correção por item
- NÃO regenera a estratégia sozinha — força o estrategista a refazer.
- Aprendizado obrigatório (Regra #14): registrar em 3 lugares + item novo no checklist se for padrão sistêmico.

### 4. Verificação consequente — decisão NOVA?

Se a estratégia, ao ser aprovada, **introduz uma decisão nova** (data, posicionamento, métrica, foco):
→ DESPACHAR `/atualizar-estrategia` pra registrar na `estrategia-viva.md`.

Exemplos que disparam:
- "Vamos focar em Sistema Reverso pelos próximos 90 dias"
- "Mentoria volta a ter opção 1:1"
- "Nova métrica pública: 12 squads em produção"
- "Imersão muda de 2x/mês pra semanal"

---

## Anti-padrões que reprovam INSTANTANEAMENTE

1. Documento sem ângulo único ("fala pra empreendedor digital em geral")
2. Prova social inflada (faturamento, "400k usuários" como público pessoal, "35+ empresas")
3. Vocabulário interno ("qualificação", "screening", "triagem")
4. Números voláteis na promessa ("21 dias", "4 meses garantidos", "32 encontros")
5. Inventar contexto do Gui sem fonte no segundo-cerebro
6. Pular o `banco-de-historias.md` (ângulo abstrato sem âncora real)
7. CTA múltiplo no mesmo bloco
8. Diretriz vaga pra copywriter ("escrever bem", "tom acolhedor")
9. Esquecer hiperlinks `{{DOMINIO}}/[slug]` quando há menção a produto interno
10. Documento curto demais (<300 linhas equivalente — sinal de superficialidade)
11. Não consultar `estrategia-viva.md` ou usar dado divergente sem flag
12. Não listar decisões pendentes quando há claramente input que falta

---

## Output da revisão

Independente do resultado, gravar relatório em:

`workspace/output/estrategia/{YYYY-MM-DD}-{slug}-revisao.md`

Formato:

```markdown
# Revisão de estratégia — [slug]

**Documento revisado:** workspace/output/estrategia/{YYYY-MM-DD}-{slug}-estrategia.md
**Revisor:** Jade (COO)
**Data da revisão:** YYYY-MM-DD
**Resultado:** APROVADO | REPROVADO | APROVADO COM RESSALVAS

## Checklist (resultado por item)
[colar checklist com [x]/[ ]]

## Itens reprovados (se houver)
- **Item:** [nome do item]
  **Citação do documento:** "[trecho problemático]"
  **Sugestão de correção:** [acionável]

## Decisão nova detectada?
- [ ] Sim → despachar `/atualizar-estrategia` para registrar
- [ ] Não

## Próximo passo
- [skill consequente despachada | devolução pro estrategista | aguardando input do Gui]
```

---

## Regras

- **Jade não reescreve o documento** — devolve com apontamentos. Estrategista refaz.
- **Não aprova com pendência crítica** — qualquer item `[ ]` = REPROVADO.
- **Sempre citar `estrategia-viva.md`** ao questionar data/métrica/posicionamento.
- **Não pular checklist** — mesmo se a estratégia "parece boa". Checklist é a blindagem (Regra #14).
- **Reprovação repetida do mesmo erro** = causa raiz no agente, não na peça. Disparar atualização de `instructions.md` via Tarefa.

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro Gui testar — testa antes.
