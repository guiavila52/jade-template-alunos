---
name: escrever-estrategia
description: Despacha o agente estrategista-marketing pra produzir briefing estrategico de 11 secoes antes de qualquer copy ou peca nova.
type: skill
---

<!-- Modelo recomendado: claude-opus-4-5 (estratégia exige raciocínio estratégico forte) -->

# /escrever-estrategia — Despacha o agente Estrategista

> Skill que despacha o agente `@estrategista-marketing` (squad-gestao) pra produzir um briefing estratégico antes de qualquer copy ou peça nova.
>
> Acionada por `/criar-pagina-nova` (passo 2), por `/jade` (quando há decisão de produto/oferta) ou diretamente pelo {{OPERADOR}}.

---

## ANTES DE COMEÇAR — LEITURA OBRIGATÓRIA (BLOQUEANTE)

> **Esta seção não é opcional.** O agente NÃO escreve uma linha de estratégia antes de confirmar que leu cada item. Se algum estiver inacessível, REGISTRAR pendência e PARAR.

### Documentos canônicos (ler nesta ordem)

1. **`segundo-cerebro/04-decisoes/estrategia-viva.md`**
   - Olhar a seção **"ATUAL"** primeiro (datas, posicionamento, métricas vigentes).
   - Olhar o HISTÓRICO recente (últimas 3 entradas) pra entender o contexto das decisões em vigor.
   - Se for citar uma data/posicionamento/métrica: ela tem que estar literalmente nesse documento. Se não está → pendência, NÃO inventar.

2. **`squads/gestao/agentes/estrategista-marketing/instructions.md`**
   - Treinamento completo do agente. Princípios estratégicos, output canônico (11 seções), quando o estrategista entra ou não.

3. **`squads/gestao/agentes/estrategista-marketing/memoria.md`**
   - Estado e projetos ativos do agente.

4. **`squads/gestao/agentes/estrategista-marketing/aprendizados.md`**
   - Lições anteriores do estrategista (não repetir erro corrigido).

5. **MEMORY.md index** em `~/.claude/projects/-Users-{{handle}}-Documents-Projetos-IA-{{OPERADOR}}--vila-Squad-Empresa-{{OPERADOR}}--vila/memory/MEMORY.md` + memórias relevantes pra essa estratégia específica:
   - SEMPRE: `user_posicionamento_gui.md`, `project_empresas_cnpj.md`, `project_posicionamento_squads.md`
   - SE MENCIONAR FUNIL: `project_jornada_cliente_reverso.md`
   - SE MENCIONAR {{EMPRESA_COFUNDADA_UPPER}}: `{{empresa_cofundada}}_comercial.md`, `{{empresa_negocio}}_origem_{{empresa_cofundada}}.md`
   - SE MENCIONAR PÁGINA WORDPRESS: `project_redirects_wordpress.md`
   - SE MENCIONAR MENTORIA: feedback sobre mentoria-só-grupo (entrada de 2026-05-06 em `estrategia-viva.md`)

6. **`segundo-cerebro/mapa.md`** — pra localizar qualquer outra fonte citada.

7. **`segundo-cerebro/01-identidade/banco-de-historias.md`** (se existir) — histórias canônicas do {{OPERADOR}} pra usar como gancho.

### Confirmação antes de produzir

Antes de gerar a estratégia, o agente DEVE responder internamente:

- [ ] Li `estrategia-viva.md` seção ATUAL
- [ ] Conferi data de lançamento vigente (não vou inventar nem chutar)
- [ ] Conferi posicionamento atual de cada produto que vou citar
- [ ] Conferi quais métricas posso usar publicamente (nada de faturamento)
- [ ] Li as memórias relevantes do MEMORY.md
- [ ] Li `instructions.md` do estrategista (formato 11 seções)

Se algum item não puder ser confirmado: PARAR e pedir input via Jade.

---

## Inputs esperados

A skill é chamada com (no mínimo):

- **Objetivo da estratégia** (ex: "página /mentoria nova", "campanha de aquecimento Imersão de 21/05", "repositioning {{NOME_CURSO}}")
- **Contexto** (ex: "{{OPERADOR}} decidiu mentoria só em grupo, página atual está desatualizada")
- **Slug/identificador** (ex: `mentoria`, `imersao-21-05`, `reverso-repositioning`)
- **Quem aprova** (default: Jade COO via `/revisar-estrategia`)
- **Output destino** (default: `workspace/output/estrategia/{YYYY-MM-DD}-{slug}-estrategia.md`)

Se faltar input crítico → perguntar via Jade. Não chutar.

---

## Fluxo

### 1. Confirmar leitura obrigatória

Rodar a checklist da seção "ANTES DE COMEÇAR". Sem checklist completa, não avançar.

### 2. Mapear estado atual relevante

Extrair de `estrategia-viva.md`:
- Datas relevantes pro objetivo
- Posicionamento dos produtos citados
- Métricas públicas permitidas
- Histórico recente que afeta a tese

### 3. Produzir estratégia no formato 11 seções

Conforme `squads/gestao/agentes/estrategista-marketing/instructions.md` → seção "Output canônico".

Salvar em: `workspace/output/estrategia/{YYYY-MM-DD}-{slug}-estrategia.md`

Garantir que o rodapé cite as fontes consultadas (incluindo versão da `estrategia-viva.md`).

### 4. Listar decisões pendentes

Se a estratégia depende de decisões que SÓ o {{OPERADOR}} pode dar: listar no campo "Decisões pendentes" (seção 11). Bloqueia despacho consequente até resposta.

### 5. Despachar pra Jade revisar

Notificar Jade: "Estratégia pronta em `[caminho]`. Decisões pendentes: [lista ou nenhuma]. Aguardando revisão."

### 6. Após aprovação do {{OPERADOR}} — verificação consequente

Se a estratégia gerar uma DECISÃO NOVA (mudança de data, posicionamento, métrica, foco):
→ DESPACHAR `/atualizar-estrategia` pra registrar na `estrategia-viva.md`.
Não termina o ciclo só com a peça aprovada — o estado canônico precisa refletir.

### 7. Registrar conclusão

- `squads/conteudo/tarefas.md` — marcar tarefa concluída
- `squads/gestao/agentes/estrategista-marketing/memoria.md` — adicionar projeto ativo / projeto concluído
- `squads/conteudo/aprendizados.md` — se houve correção do {{OPERADOR}} na revisão, registrar aprendizado
- Atualizar `mapa.md` da pasta de output se for o primeiro arquivo lá

---

## Critérios objetivos de aprovação (checklist do revisor — Jade)

- [ ] As 11 seções estão preenchidas (não pular nenhuma)
- [ ] Toda data citada existe literalmente em `estrategia-viva.md`
- [ ] Toda métrica pública citada está na lista permitida da `estrategia-viva.md`
- [ ] Posicionamento dos produtos citados bate com `estrategia-viva.md`
- [ ] Tese central reforça posicionamento {{OPERADOR}} = especialista nº 1 em squads de agentes de IA
- [ ] Funil canônico respeitado (YouTube → Imersão → Mentoria/Reverso → Consultoria)
- [ ] Não inventou conteúdo sobre o {{OPERADOR}} (tudo citado tem fonte no segundo-cerebro)
- [ ] Não usou jargão novo sem combinar
- [ ] Briefing pra peças derivadas é executável dentro de Light Copy
- [ ] Decisões pendentes estão listadas (não escolheu pelo {{OPERADOR}})
- [ ] Rodapé cita fontes consultadas

Falhou em qualquer item → devolve pro estrategista com correção.

---

## Regras (do agente, durante a execução)

- **Não inventar data nem métrica.** Se não está em `estrategia-viva.md`, é pendência.
- **Não escolher pelo {{OPERADOR}}** decisões estratégicas — listar como pendente.
- **Não escrever copy final** — só briefing. Copy é do `/escrever-copy` ou `/escrever-pagina`.
- **Não desenhar layout** — só hierarquia narrativa.
- **Pixel-perfect não passa por aqui** — `/migrar-pagina` copia design original.
- **Toda decisão nova após aprovação → `/atualizar-estrategia`.**

---

## Quando estratégia é pra carrossel (Onda 1 — fluxo carrossel-YouTube)

Quando o estrategista é despachado dentro do fluxo `/criar-carrossel` ou `/criar-carrossel-de-video`, o output esperado tem schema específico (não é os 11 blocos canônicos de página):

```yaml
tema: "string"
angulo_unico: "1 frase clara, não-genérica"
payoff: "conclusão que o último slide entrega"
qtd_laminas: 5  # 5=simples, 7=padrão, 10=denso
estrutura: "hook (1) → problema (2-3) → diagnóstico (4-5) → método (6) → CTA (7)"
tom: "didático+irônico | técnico+sério | íntimo+honesto"
referencias_segundo_cerebro:
  - "01-identidade/banco-de-historias.md"
  - "01-identidade/tom-de-voz.md"
transcricao_bruta: "..."  # se input foi vídeo YouTube
fonte:
  url: "https://youtu.be/XXX"
  titulo_video: "..."
```

Se input foi transcrição YouTube: estrategista identifica **3 candidatos de ângulo único** (não 1 — {{OPERADOR}} escolhe o melhor) e recomenda 1 com justificativa.

Detalhes em `squads/gestao/agentes/estrategista-marketing/memoria.md` — seção "Output schema pra carrossel" + "Quando ângulo vem de transcrição YouTube".

Output salvo em `workspace/output/carrosseis/YYYY-MM-DD-[slug]/briefing-estrategista.md` (não em pasta de páginas).

## Bateria de testes (Regra Inviolável #24)

ANTES de marcar entregue:
1. Despachar revisor externo conforme matriz `AGENTS.md` Regra #24 (carrossel→revisor-visual, copy→paginas, skill/MCP/script→paginas-dev, fix→bug-hunter, página→triple-check #23)
2. Revisor APROVA ou REPROVA + gaps
3. REPROVADO → corrige + re-revisa até APROVADO
4. SÓ aí marca entregue em pendencias.md + commita

Jade NUNCA pede pro {{OPERADOR}} testar — testa antes.
