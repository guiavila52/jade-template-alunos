---
name: revisar-newsletter
description: Valida copy da newsletter (tom, Light Copy, fechamento canonico, acentuacao) antes do PATCH {{PLATAFORMA_NEWSLETTER}} e disparo GHL.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /revisar-newsletter

Skill de validação INDEPENDENTE de newsletter antes do disparo. Despachada pelo agente `@revisor-newsletter` (squad-conteudo).

## Quando invocar

- Imediatamente após `@copywriter` produzir/atualizar `workspace/output/newsletter/YYYY-MM-DD-{slug}.md`
- Antes de qualquer PATCH no {{PLATAFORMA_NEWSLETTER}} com body novo
- Antes de qualquer disparo via GHL (skill `/disparar-newsletter`)
- Sempre que houver mudança no body (mesmo correção pontual de acento)

## Inputs

- `path` (obrigatório): path do markdown da newsletter (`workspace/output/newsletter/...`)
- `briefing_id` (opcional): ID do briefing original — pra checar frase-âncora original

## Antes de validar — leitura obrigatória

1. `segundo-cerebro/01-identidade/tom-de-voz.md`
2. `segundo-cerebro/01-identidade/exemplos-copy.md`
3. `segundo-cerebro/01-identidade/icp.md`
4. `squads/conteudo/agentes/revisor-newsletter/aprendizados.md`
5. Memórias persistentes correlatas (ver arquivo do agente)

## Checklist obrigatória (12 itens)

### 1. Marker INTERNO presente + posição correta

```bash
grep -c '<!-- INTERNO — NÃO ENVIAR' "$PATH"  # esperado: 1+
```

Marker deve estar imediatamente após `— {{NOME_OPERADOR}}` (assinatura) + linha em branco.
**REPROVADO** se: ausente, em posição errada, ou múltiplas ocorrências.

### 2. Body acima do marker = só email

Cortar arquivo no marker:
```python
body_email = raw.split('<!-- INTERNO', 1)[0]
```

`body_email` NÃO pode conter:
- "Notas pro" / "Notas internas"
- "Ajustes v" / "Histórico de revisão"
- "Palavra-chave escolhida"
- "Total de palavras"
- "Frase-âncora" (quando é meta-comentário, não a frase em si)

**REPROVADO** se: qualquer string acima aparece no body_email.

### 3. Acentuação portuguesa perfeita

Checklist palavras-armadilha (ler `feedback_acentuacao_obrigatoria.md`):
- voce → você
- nao → não
- so → só
- ja → já
- tambem → também
- ate → até
- atraves → através
- alem → além
- porem → porém
- esta (verbo) → está
- e (verbo) → é
- automacao → automação
- funcao → função
- secao → seção
- construcao → construção
- estrategia → estratégia
- logica → lógica
- trafego → tráfego
- negocio → negócio
- raciocinio → raciocínio
- publico → público
- ultimo → último
- Avila → Ávila

**REPROVADO** se: 1+ palavras-armadilha sem acento.

### 4. Light Copy: sem 3 Ps na abertura

Primeira frase NÃO pode começar com:
- "Porque..." (Porque)
- "Você precisa..." / "Você tem..." (Promessa imperativa)
- "Você sabia que...?" / "Já parou pra pensar...?" (Pergunta)

**REPROVADO** se: abertura é 1 dos 3 Ps.

### 5. Preheader bate com 1ª frase do body

Preheader (linha `**Preheader:**` no body) deve antecipar/complementar a 1ª frase, não duplicar.

**APROVADO COM RESSALVAS** se: preheader não casa bem (sugere alternativa).

### 6. CTA único e claro (sem CTA secundário escondido)

UM objetivo por email. Newsletter NÃO pode ter 2 CTAs concorrentes (ex: "compra X" + "responde Y" + "clica em Z" todos como primary).

CTAs secundários OK desde que hierarquicamente subordinados.

**REPROVADO** se: 2+ CTAs primários competindo.

### 7. Tom alinhado com tom-de-voz + exemplos-copy

Comparar com amostras canônicas em `exemplos-copy.md`:
- Saudação calorosa, não formal
- "pra vocês" / "no seu negócio" (inclusivo, não distante)
- Verbo no presente contínuo quando for obra viva
- Vulnerabilidade calibrada (não soberba)
- Frase final curta + impactante

**APROVADO COM RESSALVAS** se: tom levemente fora.

### 8. `{{contact.first_name}}` preservado

```bash
grep -c '{{contact.first_name}}' "$PATH"  # 1+ esperado em maioria das newsletters
```

**APROVADO COM RESSALVAS** se: ausente quando deveria estar (newsletter de relacionamento).

### 9. Hiperlinks padrão {{DOMINIO}}/[slug]

Se newsletter menciona produto/parceiro do {{NOME_OPERADOR_CURTO}}, link DEVE seguir padrão `{{DOMINIO}}/[slug]` (ver `project_hiperlinks_padrao.md` — slugs canônicos do operador — ver segundo-cerebro/03-operacao/ctas-links.md).

Exceção: URLs externas mencionadas em contexto (ex: {{plataforma_newsletter}}.{{DOMINIO}} inline).

**APROVADO COM RESSALVAS** se: link de produto sem padrão {{DOMINIO}}.

### 10. Sem métricas privadas

Body NÃO pode mencionar:
- Faturamento em R$ (R$ X mil/mês, MRR, ARR)
- Receita específica

Pode mencionar: usuários, alunos, criadores, cases, avaliações (`feedback_metricas_publicas.md`).

**REPROVADO** se: R$ ou métrica de receita aparece.

### 11. Frase-âncora preservada (se briefing tem)

Se o briefing original definiu frase-âncora literal, ela DEVE aparecer literalmente no body. Adaptações só com justificativa explícita nas notas internas.

**REPROVADO** se: frase-âncora foi alterada sem justificativa abaixo do marker.

### 12. Total de palavras dentro do alvo

```bash
wc -w <(echo "$body_email")  # 300-400 padrão
```

**APROVADO COM RESSALVAS** se: 250-300 ou 400-450 (10% de tolerância).
**REPROVADO** se: <250 ou >450.

### 13. Título capitalizado (primeira letra MAIÚSCULA)

Frontmatter `title:` deve começar com letra maiúscula.

```python
title = re.search(r'^title:\s*"(.+?)"', frontmatter, re.MULTILINE).group(1)
assert title[0].isupper(), f"Title começa com minúscula: {title!r}"
```

**REPROVADO** se: title começa com letra minúscula.

### 14. Body NÃO contém title nem preheader inline

Body markdown (acima do marker INTERNO) NÃO pode conter:
- Heading `# título` no início (title vai no frontmatter)
- Linha `**Preheader:** ...` (preheader vai no frontmatter)

```python
assert not body_email.lstrip().startswith('# '), "Body começa com # heading"
assert '**Preheader:**' not in body_email, "Body tem **Preheader:** inline"
```

**REPROVADO** se: body tem qualquer dos 3 padrões.

### 15. Body NÃO contém assinatura nem separador `---` antes do marker

**Regra desde {{DATA_EVENTO}}:** o markdown da newsletter NÃO carrega assinatura. O renderer (`scripts/newsletter/renderizar-html.py` → `renderizar_assinatura()`) monta automaticamente: foto 96x96 circular + 4 linhas canônicas ({{NOME_OPERADOR}} bold / Fundador e CEO da {{PLATAFORMA_CURSOS}} / Autor do {{PRODUTO_PRINCIPAL}}, {{PRODUTO_ENTRADA}}, {{PRODUTO_ENTRADA_2}} / Fundador do {{PRODUTO_PARCERIA}} · {{DOMINIO}}).

Body deve terminar em `Um abraço,` (vírgula) e em seguida vir DIRETO o marker INTERNO, sem `---` e sem bloco de assinatura.

```python
# Validação
ultima_linha_body = [l for l in body_email.strip().split('
') if l.strip()][-1]
assert ultima_linha_body.strip() == 'Um abraço,', f'Body deveria terminar em "Um abraço," (vírgula), terminou em: {ultima_linha_body!r}'
assert '**{{NOME_OPERADOR}}**' not in body_email, 'Assinatura no MD detectada — renderer monta sozinho, remover do markdown'
assert 'Site: [{{DOMINIO}}]' not in body_email, 'Linha "Site: [{{DOMINIO}}]" detectada — formato antigo, renderer não usa isso'
```

**REPROVADO** se: body contém qualquer linha de assinatura OU separador `---` antes do marker INTERNO.

**Não REPROVAR** baseado em formato de assinatura — quem garante é o renderer, não a checklist.

### 16. Pelo menos 1 bullet list (quando houver pontos enumeráveis)

Body deve conter ao menos 1 lista `- item` quando há ponto enumerável (ex.: "o que você recebe", "como funciona", lista de benefícios). Newsletter de informação pura pode ter zero — usar julgamento.

```bash
grep -c '^- ' body_email  # esperado: >=1 quando há pontos enumeráveis
```

**APROVADO COM RESSALVAS** se: zero bullets mas tem pontos que mereciam bullet.

### 17. Pelo menos 2 sub-headings `##`

Body deve ter mínimo 2 `## Subheading` dividindo seções. Quebra muro de texto.

**APROVADO COM RESSALVAS** se: zero ou 1 subheading (newsletter pode ficar com aparência de blob).

### 18. Parágrafos curtos (média ≤ 3 frases)

Cada parágrafo do body deve ter no máximo 3 frases. Parágrafos de 4+ frases devem ser quebrados em 2.

```python
paragrafos = [p for p in body_email.split('

') if not p.startswith(('#', '-', '**'))]
media_frases = sum(p.count('. ') for p in paragrafos) / max(len(paragrafos), 1)
assert media_frases <= 3, "Parágrafos longos demais"
```

**REPROVADO** se: 2+ parágrafos com 4+ frases.

### 19. Camadas/Etapas/Fases — DEVE virar bullet list

Quando body menciona conceito enumerável como "Camada 1", "Camada 2", "Etapa A", "Etapa B", "Fase 1", "Fase 2" — esse tipo de estrutura DEVE ser renderizado como bullet list (`- **Camada 1:** ...`), NÃO como parágrafos sequenciais densos.

Detecção heurística:
```python
import re
# Procura padrões "Camada X" / "Etapa X" / "Fase X" / "Passo X" em parágrafos sequenciais
suspeitos = re.findall(r'\*\*(Camada|Etapa|Fase|Passo|Pilar|Nivel|Nível)\s+\w+:\*\*', body_email)
# Se >= 2 ocorrências NÃO em bullet list → REPROVADO
```

**REPROVADO** se: 2+ "Camada N" / "Etapa N" / "Fase N" em parágrafos sequenciais sem bullets.

### 20. Asset URL validado (imagem/vídeo)

Toda URL de imagem (markdown `![](URL)` ou HTML `<img src>`) DEVE estar acessível (HTTP 200) antes da newsletter ir pro {{PLATAFORMA_NEWSLETTER}}.

```bash
URLS=$(echo "$body_email" | grep -oE '!\[.*?\]\(https?://[^\)]+\)' | grep -oE 'https?://[^\)]+')
for url in $URLS; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    [ "$code" = "200" ] || echo "REPROVADO: $url = $code"
done
```

**REPROVADO** se: qualquer asset URL retornar != 200.


### 21. Sem gatilho-resposta com palavra-chave (PROIBIDO desde {{DATA_EVENTO}})

Newsletter tem CTA único (vídeo YouTube ou link único). Gatilho-resposta secundário pedindo "responda com X que recebe Y" é PROIBIDO.

```bash
BODY=$(python3 -c "import sys; raw=open(sys.argv[1]).read(); print(raw.split('<!-- INTERNO',1)[0])" "$PATH")
echo "$BODY" | grep -iE "responde.*palavra|envia.*palavra|comenta.*palavra|com a palavra [A-Z]+|responda com|envia.*pra receber" && echo "REPROVADO" || echo "OK"
```

**REPROVADO** se: qualquer match. Padrões proibidos:
- "Responde aqui com a palavra X"
- "Envia [PALAVRA] pra receber Y"
- "Comenta [PALAVRA]"
- "Responda com X que..."

Decisão {{NOME_OPERADOR_CURTO}} {{DATA_EVENTO}} — newsletter mapa-infoprodutos. Memória: `feedback_newsletter_sem_gatilho_resposta_palavra.md`.

## Output canônico

```markdown
# Revisão newsletter — {slug} — {data} — {VEREDICTO}

**Path:** {path}
**Veredicto:** ✅ APROVADO | ❌ REPROVADO | 🟡 APROVADO COM RESSALVAS

## Checklist (12 itens)

1. Marker INTERNO: ✓
2. Body limpo: ✓
3. Acentuação: ✓
...
12. Total palavras: ✓ (358 palavras — dentro do alvo)

## Findings (se aplicável)

### REPROVADO — item 3 (Acentuação)
- Linha 14: "ultimos meses" → deve ser "últimos meses"
- Linha 22: "Nao e um agente so" → deve ser "Não é um agente só"
- (+ N ocorrências)
- **Ação requerida:** despachar `@copywriter` pra acentuar + re-revisar

### APROVADO COM RESSALVAS — item 9 (Hiperlinks padrão)
- Linha 27: mencionou {{PRODUTO_PARCERIA}} sem link padrão `{{DOMINIO}}/{{SLUG_PARCERIA}}`
- **Sugestão:** acrescentar link na 2ª menção (não bloqueia disparo)
```

## Fluxo

```
[ Jade despacha /revisar-newsletter path=X.md ]
        ↓
[ Revisor lê tom-de-voz + exemplos + ICP + memórias ]
        ↓
[ Aplica 12 itens da checklist ]
        ↓
   ┌──────────────────┬───────────────────────────────┐
   ↓ (12/12 OK)       ↓ (1+ REPROVADO)               ↓ (1+ ressalva)
   ✅ APROVADO         ❌ REPROVADO + findings        🟡 APROVADO COM RESSALVAS
   Jade segue pra      Jade despacha @redator         Jade decide: aceita
   /disparar-newsletter pra corrigir + re-revisa      ressalva OU despacha
                                                       redator pra ajuste fino
   └──────────────────┴───────────────────────────────┘
```

## Regra de aprendizado (Regra Inviolável #19)

Ao final de cada revisão (especialmente as que REPROVAM ou voltam pra refazer), registre em `squads/conteudo/agentes/revisor-newsletter/aprendizados.md`:

- Padrão de erro recorrente que deve virar item de checklist
- Falsos positivos da própria skill que precisam ser ajustados
- Novas armadilhas (palavras sem acento, expressões fora de tom, etc)

## Pendências registradas

Toda execução desta skill cria/atualiza task no ClickUp (lista `{{CLICKUP_LIST_ID}}`) via `/criar-pendencia` ou `/comentar-pendencia`.

## Bateria de testes (Regra Inviolável #24)

Esta skill É a bateria de testes da newsletter. Não delega revisão pra outra skill — ela é a última linha antes do disparo.

## Checklist adicional — preheader + email_subject (12/05/2026)

- [ ] preheader começa com letra maiúscula (regex `^[A-ZÁÉÍÓÚÂÊÔÃÕÇ]`)
- [ ] preheader desperta curiosidade (não factual seco — pergunta/gancho/promessa)
- [ ] preheader 60-110 chars + não duplica title
- [ ] email_subject começa com letra maiúscula
- [ ] email_subject geralmente igual ao title (salvo exceção justificada)


### 13. Fechamento canônico (atualizado 21/05/2026)

Toda newsletter termina com:
1. Bloco vídeo embed (quando origem é YouTube)
2. Frase forte (máx 20 palavras — síntese/moral)
3. Pitch/CTA (OPCIONAL — só quando {{NOME_OPERADOR_CURTO}} pediu explicitamente)
4. "Um abraço," (vírgula — nunca exclamação)

Validações obrigatórias:

```bash
grep -c "Um abraço," "$PATH"                              # esperado: 1
grep -c "Um abraço!" "$PATH"                              # esperado: 0 (exclamação proibida)
grep -ciE "Bora aplicar|qualquer coisa.*chama|garanta.*vaga|últimas chances|espero que ajude" "$PATH"  # esperado: 0
```

**REPROVADO** se:
- ❌ "Um abraço!" (exclamação) — canônico é vírgula
- ❌ Frase forte vira pergunta retórica vaga ou CTA solto
- ❌ Hard-sell ("garanta sua vaga", "últimas chances") mesmo quando há pitch
- ❌ 2+ CTAs primários concorrentes no mesmo email

**APROVADO** sem pitch — newsletter de conhecimento puro não precisa de CTA.
**REPROVADO** se pitch presente sem {{NOME_OPERADOR_CURTO}} ter pedido — verificar notas internas abaixo do marker.



---

## Check obrigatório — Conhecimento ≠ informação ({{DATA_EVENTO}})

REPROVAR newsletter que afirme "conhecimento é commodity" ou variações que depreciem conhecimento estruturado.

**Distinção canônica {{NOME_OPERADOR}}:**
- Informação = commodity (Google/YouTube/ChatGPT, grátis)
- Conhecimento = produto (curso/mentoria/sistema, o que se vende)

**Procurar e flagar:**
- Frase literal "conhecimento é commodity"
- Equivalentes que joguem conhecimento como grátis/descartável
- "Conhecimento tá grátis na internet"
- "Qualquer um aprende sozinho"
- "Não precisa de curso/mentoria pra aprender"

**OK:**
- "Informação é commodity"
- "Informação tá grátis em qualquer lugar"
- Atribuições de "commodity" SÓ a informação solta, nunca a conhecimento estruturado

Memória: `feedback_copy_conhecimento_vs_informacao.md`