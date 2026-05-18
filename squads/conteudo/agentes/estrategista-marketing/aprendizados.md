# aprendizados.md — Agente @estrategista-marketing (squad-conteudo)

> Licoes do agente Estrategista. Toda revisao reprovada pela Jade deve gerar entrada aqui (Regra #14).

---

## 2026-05-12 — Estrategia {{NOME_CURSO}} (Fase B Onda mestra)

**Tarefa:** Onda `/reverso-curso-completo` — Fase B
**Status:** entregue (aguardando aprovacao {{OPERADOR}})
**Output:** `Segundo Cerebro/04-decisoes/2026-05-12-estrategia-sistema-reverso.md`

### Padrao estrategico aplicado: Framework 5 niveis x 7 esferas

**O que e:** Arquitetura didatica em 2 eixos que diferencia o {{NOME_CURSO}} de qualquer outro curso de IA:
- Eixo vertical = 5 niveis de maturidade (chat solto → squads)
- Eixo horizontal = 7 esferas de aplicacao (produtividade ate metricas)

**Por que funciona:**
1. Cria framework proprietario (ninguem mais fala em "5 niveis" assim)
2. Permite autodiagnostico ("em qual nivel estou?")
3. Promete progressao mensuravel sem prometer quantidade
4. Diferencia de cursos ferramenteiros ("aprenda o Make") — foco em TIME, nao ferramenta

**Como replicar em futuras estrategias:**
- Sempre buscar framework proprio que crie categoria mental nova
- Preferir matriz 2 eixos quando ha progressao vertical + aplicacao horizontal
- Evitar promessas de quantidade (modulos, horas) — usar transformacao

### Padrao estrategico aplicado: Inimigo comum como comportamento

**O que e:** Definir o vilao como um COMPORTAMENTO, nao uma pessoa ou empresa concorrente.

**Por que funciona:**
1. Nao ataca ninguem (evita guerra)
2. Cria identidade por oposicao ("quem entra deixa de ser X e passa a ser Y")
3. E reconhecivel — ICP se ve no comportamento criticado

**Exemplo aplicado:**
> *"Abrir o ChatGPT, mandar uma pergunta, fechar. Nenhuma memoria. Nenhum aprendizado."*

**Como replicar:**
- Descrever o comportamento com detalhes visuais (abre, manda, fecha)
- Nomear a consequencia negativa (sem memoria, sem time)
- Contrastar com o comportamento-alvo (squad orquestrado)

### Checklist consolidado pra proximas estrategias

- [ ] Framework proprio (categoria mental nova)?
- [ ] Promessa sem numeros volateis?
- [ ] Inimigo como comportamento, nao pessoa?
- [ ] 3 angulos pra conteudo com frase-ancora literal?
- [ ] Prova social cruzada com `estrategia-viva.md`?
- [ ] Briefing pro agente downstream acionavel (nao vago)?
- [ ] Narrativa de origem (banco de historias) referenciada?

---

## 2026-05-16 — Skill nova canônica: /criar-ideia-conteudo ({{APP_PESSOAL}})

**Contexto:** {{OPERADOR}} pediu pra cadastrar 2 ideias de vídeo (YouTube longo + vertical) no {{APP_PESSOAL}} com prioridade alta, via skill canônica. Skill nova criada em `.claude/commands/criar-ideia-conteudo.md` após aval explícito (Regra §13).

**Quando o estrategista usa:**
- Capturar insight de pauta vindo do {{OPERADOR}} ("quero gravar sobre X")
- Detectar gap de conteúdo num pilar durante /escrever-estrategia
- Após /atualizar-voz-{{handle}} identificar tema quente nos vídeos recentes

**Workflow canônico:**
1. Definir título, formato (youtube-longo/vertical/carrossel/linkedin/newsletter), ângulo (1-2 frases), prioridade
2. Invocar skill → POST cria card + PATCH preenche conteúdo
3. Card aparece em https://{{app_pessoal}}.{{handle}}.com/{{handle}}/conteudos/{id}

**Pegadinhas a evitar (descobertas 16/05/2026):**
- Vertical sobrescreve status pra `pronto_para_gravar` mesmo enviando `proximos`
- Campo de conteúdo varia por formato: youtube usa `idea`+`summary`+`magnetic_hook`, vertical usa `script`, newsletter usa `body`
- Priority canônico em inglês: `urgent`/`high`/`normal`/`low`
- `$` no shell expande sem `--rawfile` (`R$5.000` vira `R.000`)

**Matriz canônica origem → priority + status (correção {{OPERADOR}} 16/05/2026, segunda iteração):**

| Origem | Priority | Status |
|---|---|---|
| {{OPERADOR}} passou direto pela Jade ("adiciona na fila", "quero gravar") | `urgent` | `pronto_para_gravar` |
| `estrategista-marketing` capturou pauta consolidada | `high` | `proximos` |
| `copywriter` captou tema em brainstorm | `high` | `proximos` |
| `analista-tendencias` capturou raw do radar | `normal` | `ideia_crua` |
| Rotina autônoma / bulk import sem triagem | `low` | `ideia_crua` |

**Por quê:** Quando {{OPERADOR}} passa direto, é sempre "ideia fresca que quero gravar logo" → topo da fila. `pronto_para_gravar` validado pra `youtube` e `vertical`. Status `ideia_crua` é só pra captura sem qualquer triagem.

**Casos de uso recentes (rastreabilidade):**
- 16/05/2026 — Ideia "Barra de chocolate — produto barato cérebro reptiliano" (longo `ee284221` + vertical `137eb20d`), tese central do Tripwire R$47.

---

*(Proximas entradas abaixo)*
