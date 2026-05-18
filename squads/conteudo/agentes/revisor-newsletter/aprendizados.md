# Aprendizados — revisor-newsletter

Registro cronológico de lições aprendidas em revisões reais. Padrões de armadilha que viraram itens do checklist.

---

**Criado em:** 2026-05-12 — primeiro aprendizado vem da primeira revisão real.

## Princípio fundador (12/05/2026)

A criação deste agente foi consequência da Regra Inviolável #19 sendo aplicada ao bug newsletter v5:

- Falha original: Jade escreveu newsletter direto via Bash heredoc — sem acentos + metadata interna vazou pro {{APP_PESSOAL}}
- Skill `/escrever-newsletter` foi atualizada com regra do marker INTERNO
- Mas faltava revisor INDEPENDENTE pra captar esse tipo de gap antes do disparo
- Agente `@revisor-newsletter` nasceu pra ser essa última linha de defesa

**Princípio:** reprovar é melhor que aprovar com gap. Reputação do {{OPERADOR}} > qualquer cronograma.

---

## Revisão #1 — newsletter squad-agentes-anuncio v5 (12/05/2026)

**Arquivo:** `workspace/output/newsletter/2026-05-11-squad-agentes-anuncio.md`
**Veredicto:** 🟡 APROVADO COM RESSALVAS

### O que passou (12/14 limpos)

- Marker INTERNO posicionado corretamente após `— {{NOME_OPERADOR}}` (linha 61 → marker linhas 63-65)
- Body acima do marker = só email (sem notas/histórico/Light Copy/total-palavras)
- Acentuação portuguesa 100% íntegra — nenhuma palavra-armadilha sem acento (varredura: nao, voce, so, ja, automacao, funcao, estrategia, trafego, negocio, raciocinio, ultimos, Avila — todas acentuadas)
- Abertura "Oi {{contact.first_name}}!" + afirmação — sem 3 Ps
- CTA primário (link acesso antecipado) + secundário (responder SQUAD) com hierarquia explícita nas notas internas
- Tom alinhado: saudação calorosa, "no seu negócio" inclusivo, presente contínuo ("estou construindo", "tô construindo"), smile pontual ":)", paralelismo final ("Não é roadmap. É construção ativa.")
- `{{contact.first_name}}` preservado
- Hiperlinks padrão `{{handle}}.com/reverso` corretos em ambas as menções
- Zero métricas privadas (R$/MRR/faturamento)
- Frase-âncora documentada: 4/5 literais, 1 adaptada com justificativa explícita nas notas
- Título capitalizado: "O que eu venho construindo..."
- Body sem title/preheader inline

### Ressalvas (2/14)

**Item 5 — Preheader vs 1ª frase:** preheader "pela primeira vez falando publicamente sobre isso" não bate com a 1ª frase real do body ("Nesses últimos meses eu tenho trabalhado pra simplificar..."), mas casa perfeitamente com a 2ª frase ("Pela primeira vez eu vou falar publicamente sobre isso"). Complementa, não duplica — aceitável mas digno de nota.

**Item 12 — Total de palavras:** 420 palavras no body. Alvo 300-400. Dentro da tolerância de 10% (limite 440), mas excede o alvo nominal em 20 palavras. Bloco "O que você recebe" + dupla "Se você já entrou / Se você ainda não é aluno" inflam o total. Não bloqueia disparo.

### Padrões pra incorporar ao checklist em revisões futuras

- **Preheader vs 1ª frase**: aceitar quando preheader casa com a 2ª frase imediata (proximidade narrativa), não apenas a 1ª literal. Útil em newsletter que abre com setup + revela na frase 2.
- **CTA dupla com hierarquia documentada**: aprovar quando as notas internas (abaixo do marker) declaram explicitamente qual é primário e qual é secundário. Sem nota = reprovar.
- **Tolerância 10% no total**: 420 palavras passa (limite 440), mas 441+ reprova. Calibrar comunicação: ressalva é alerta, não aprovação tácita pra inflar nas próximas.
