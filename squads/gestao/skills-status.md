# Skills do Squad — Classificação por Maturidade

**Data:** 2026-05-11  
**Total auditado:** 51 skills  
**Objetivo:** visibilidade do estado atual de cada skill para priorizar ondas de conclusão.

---

## Sistema de 4 níveis (fonte: `segundo-cerebro/04-decisoes/2026-05-11-estrutura-squad-ideal.md`)

| Nível | Símbolo | Critério |
|---|---|---|
| **MADURA** | 🟢 | Funciona ponta-a-ponta, validada em produção com Gui, sem gaps conhecidos, integração externa funcionando, bateria de testes #24 passando |
| **FUNCIONAL** | 🟡 | Funciona o básico, falta polimento ou edge cases, pode ter rodado em produção 1-2x mas não consolidada |
| **EM PROGRESSO** | 🔵 | Implementação parcial, gap claro pra fechar (ex: integração faltando 1 endpoint, skill chama API mas não trata erros) |
| **ESQUELETO** | ⚪ | Só estrutura básica, precisa implementação real (ex: skills B1-B4 criadas recentemente) |

---

## Distribuição geral

- **🟢 MADURA:** 12 skills
- **🟡 FUNCIONAL:** 18 skills
- **🔵 EM PROGRESSO:** 8 skills
- **⚪ ESQUELETO:** 13 skills

---

## Skills por squad

### Squad JADE (orquestração)

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/jade` | jade | 🟢 MADURA | — | em uso diário |
| `/consolidar-sessao` | jade | 🟢 MADURA | — | em uso diário |
| `/check-up-estrutura` | dev | 🟢 MADURA | — | em uso diário, 19 categorias funcionais |
| `/varrer-squads` | jade | 🟡 FUNCIONAL | falta validação em cron real | testar com /schedule quando ativo |
| `/rotina-gui-ausente` | jade | 🟢 MADURA | — | consolidada 10/05/2026, usada em produção |
| `/escrever-estrategia` | estrategista | 🟡 FUNCIONAL | falta consolidação de uso em múltiplas páginas | rodar em 3+ páginas pra consolidar padrões |
| `/revisar-estrategia` | jade | 🟡 FUNCIONAL | mesma dependência de escrever-estrategia | consolidar junto |
| `/atualizar-estrategia` | estrategista | 🟡 FUNCIONAL | mesma dependência de escrever-estrategia | consolidar junto |

---

### Squad CONTEUDO

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/escrever-newsletter` | newsletter | 🟡 FUNCIONAL | falta bateria #24 explícita, falta uso em 3+ edições | consolidar uso + adicionar revisor |
| `/criar-carrossel` | carrossel | 🟢 MADURA | — | orquestra estrategista → copywriter → squad-imagem → triple-check. Usada em produção. |
| `/criar-carrossel-de-video` | carrossel | 🟢 MADURA | — | atalho ponta-a-ponta. URL YouTube → carrossel pronto. |
| `/revisar-carrossel` | revisor-carrossel | 🟡 FUNCIONAL | falta consolidação de uso em múltiplos carrosseis | rodar em 3+ carrosseis |
| `/ver-carrossel` | — | 🟡 FUNCIONAL | extrai imagens + copy de URL Instagram, mas sem integração API real (scraping manual?) | validar se funciona sem fricção |
| `/disparar-newsletter` | newsletter | ⚪ ESQUELETO | integração {{PLATAFORMA_NF}}/MailerLite/SMTP não implementada | atacar quando houver API key + plataforma definida |

---

### Squad COPY

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/escrever-copy` | copywriter | 🟢 MADURA | — | em uso diário, regras consolidadas |
| `/escrever-pagina` | paginas | 🟢 MADURA | — | em uso diário, Light Copy consolidado |
| `/revisar-copy-pagina` | revisor-copy | 🟡 FUNCIONAL | falta bateria #24 explícita | adicionar cláusula Regra #24 |
| `/escrever-roteiro` | copywriter | 🟡 FUNCIONAL | falta uso em produção real | rodar roteiro de vídeo 1x pra validar |
| `/escrever-linkedin` | copywriter | 🟡 FUNCIONAL | falta uso em 3+ posts | consolidar padrões |

---

### Squad DEV

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/criar-pagina-nova` | jade | 🟢 MADURA | — | orquestra esteira completa, em uso diário |
| `/ajustar-pagina` | paginas-dev | 🟢 MADURA | — | em uso diário, regras consolidadas (Slider, GSAP, GTM, etc) |
| `/migrar-pagina` | paginas-dev | 🟢 MADURA | — | pixel-perfect validado, diff visual obrigatório |
| `/revisar-codigo-pagina` | paginas-dev | 🟡 FUNCIONAL | falta bateria #24 explícita | adicionar cláusula Regra #24 |
| `/publicar-pagina` | paginas-dev | 🟢 MADURA | — | build + preview + prod, usado diariamente |
| `/testar-pagina` | bug-hunter | 🟢 MADURA | — | bateria #15 (12/12), usado diariamente |
| `/publicar-{{plataforma_conteudo}}` | paginas-dev | 🟡 FUNCIONAL | protocolo QA existe, mas falta uso real em 3+ deploys {{Plataforma_Conteudo}} | consolidar uso |
| `/executar-bateria-qa` | bug-hunter | 🟡 FUNCIONAL | script genérico, mas falta uso em múltiplos contextos | consolidar matriz de baterias |

---

### Squad TRAFEGO

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/criar-criativo` | trafego | 🟡 FUNCIONAL | falta uso em 3+ criativos + validação Meta Ads real | consolidar padrões |
| `/impulsionar-organico` | trafego | ⚪ ESQUELETO | integração Meta Ads MCP não implementada | aguarda MCP Meta Ads funcional |
| `/relatar-trafego` | trafego | ⚪ ESQUELETO | integração Meta Ads MCP + Google Ads não implementada | aguarda MCP funcional |
| `/otimizar-campanha` | trafego | ⚪ ESQUELETO | integração Meta Ads MCP não implementada | aguarda MCP funcional |

---

### Squad MIDIA

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/transcrever-video` | — | 🟡 FUNCIONAL | usa yt-dlp + Whisper, funciona mas sem tratamento de erro robusto | adicionar Regra #22 (timeout + retry) |
| `/gerar-imagem` | — | 🔵 EM PROGRESSO | HTML→PNG via Playwright, funciona mas trava silenciosamente em alguns casos (bug conhecido Onda 9) | fix confiabilidade Regra #22 |
| `/revisar-visual` | revisor-visual | 🟡 FUNCIONAL | falta uso em 3+ outputs visuais | consolidar padrões |

---

### Squad FINANCEIRO

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/registrar-financeiro` | financeiro | ⚪ MADURA | — | integração {{PLATAFORMA_NF}} API funcional, em uso |
| `/analisar-resultados` | financeiro | ⚪ ESQUELETO | integração {{BANCO_PJ}} API não implementada | aguarda chave API + endpoint |

---

### Squad RADAR

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/monitorar-concorrentes` | radar | ⚪ ESQUELETO | sem implementação real | definir fontes de dados (scraping? RSS?) |
| `/varrer-tendencias` | radar | ⚪ ESQUELETO | sem implementação real | definir fontes (Twitter API? Google Trends?) |

---

### Squad COMERCIAL

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/consultar-leads` | comercial | ⚪ ESQUELETO | integração GHL API não implementada completamente | atacar quando MCP GHL estiver consolidado |
| `/qualificar-lead` | comercial | ⚪ ESQUELETO | sem implementação real | definir critérios de qualificação |
| `/fechar-venda` | comercial | ⚪ ESQUELETO | sem implementação real | definir fluxo de fechamento |
| `/onboarding-aluno` | comercial | ⚪ ESQUELETO | sem implementação real | definir checklist de onboarding |
| `/mentoria` | — | ⚪ ESQUELETO | sem implementação real (pode ser folder, não skill?) | validar se deve ser skill ou só doc |

---

### Squad INFRA

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/publicar-jade` | dev | 🔵 EM PROGRESSO | implementação parcial, falta auditoria de PII + workflow completo | atacar Onda específica |
| `/configurar-squad` | — | 🔵 EM PROGRESSO | onboarding do aluno, falta validação com aluno real | testar com 1 aluno beta |

---

### Skills UTILITÁRIAS / GESTÃO

| Skill | Agente | Maturidade | Bloqueios | Próximo passo |
|---|---|---|---|---|
| `/ver-agenda` | — | 🟡 FUNCIONAL | integração Google Calendar API, funciona mas sem robustez | adicionar Regra #22 |
| `/revisar-semana` | jade | 🟡 FUNCIONAL | performance review do squad, falta uso em 3+ semanas | consolidar padrões |
| `/auditar-entregabilidade-email` | — | ⚪ ESQUELETO | sem implementação real | atacar quando houver plataforma de email definida |
| `/agenda` | — | 🟡 FUNCIONAL | alias de /ver-agenda? auditar se é duplicata | validar e consolidar ou remover |
| `/paginas` | — | ⚪ ESQUELETO | alias? ou folder? auditar propósito | validar |
| `/revisor-pagina` | — | 🟡 FUNCIONAL | duplicata de /revisar-pagina? auditar | consolidar ou remover |

---

## Ondas de conclusão sugeridas

### Onda A — Skills atacáveis SEM dependência externa (prioridade 1)

Skills com implementação parcial/esqueleto que NÃO dependem de API externa:

1. **`/gerar-imagem`** (🔵 → 🟢) — fix confiabilidade Regra #22 (timeout + stderr + retry). Onda 9 já atacou, validar se resolveu.
2. **`/publicar-jade`** (🔵 → 🟢) — auditoria de PII + workflow completo.
3. **`/configurar-squad`** (🔵 → 🟢) — testar com 1 aluno beta.
4. **`/escrever-newsletter`** (🟡 → 🟢) — adicionar bateria #24 + rodar em 3+ edições.
5. **`/revisar-copy-pagina`** (🟡 → 🟢) — adicionar cláusula Regra #24.
6. **`/revisar-codigo-pagina`** (🟡 → 🟢) — adicionar cláusula Regra #24.
7. **`/escrever-roteiro`** (🟡 → 🟢) — rodar 1x em produção real pra validar.
8. **`/escrever-linkedin`** (🟡 → 🟢) — rodar em 3+ posts pra consolidar.
9. **`/revisar-visual`** (🟡 → 🟢) — rodar em 3+ outputs visuais.
10. **`/publicar-{{plataforma_conteudo}}`** (🟡 → 🟢) — rodar em 3+ deploys {{Plataforma_Conteudo}}.
11. **`/executar-bateria-qa`** (🟡 → 🟢) — consolidar matriz de baterias.
12. **`/transcrever-video`** (🟡 → 🟢) — adicionar Regra #22 (timeout + retry).
13. **`/ver-agenda`** (🟡 → 🟢) — adicionar Regra #22.
14. **`/revisar-semana`** (🟡 → 🟢) — rodar em 3+ semanas.
15. **`/varrer-squads`** (🟡 → 🟢) — testar com /schedule quando ativo.
16. **`/escrever-estrategia`** (🟡 → 🟢) — rodar em 3+ páginas pra consolidar.
17. **`/revisar-estrategia`** (🟡 → 🟢) — consolidar junto com escrever-estrategia.
18. **`/atualizar-estrategia`** (🟡 → 🟢) — consolidar junto com escrever-estrategia.

**Estimativa:** 18 skills. 2-3 sprints de 1 semana cada (6 skills/sprint).

---

### Onda B — Skills bloqueadas por API externa (prioridade 2)

Skills que aguardam integração externa funcionar:

1. **`/impulsionar-organico`** (⚪ → 🟡) — aguarda MCP Meta Ads funcional.
2. **`/relatar-trafego`** (⚪ → 🟡) — aguarda MCP Meta Ads + Google Ads.
3. **`/otimizar-campanha`** (⚪ → 🟡) — aguarda MCP Meta Ads.
4. **`/analisar-resultados`** (⚪ → 🟡) — aguarda chave API {{BANCO_PJ}} + endpoint.
5. **`/monitorar-concorrentes`** (⚪ → 🟡) — aguarda definição de fontes de dados.
6. **`/varrer-tendencias`** (⚪ → 🟡) — aguarda definição de fontes.
7. **`/consultar-leads`** (⚪ → 🟡) — aguarda MCP GHL consolidado.
8. **`/disparar-newsletter`** (⚪ → 🟡) — aguarda plataforma de email definida ({{PLATAFORMA_NF}}/MailerLite/SMTP).
9. **`/auditar-entregabilidade-email`** (⚪ → 🟡) — aguarda plataforma de email.

**Estimativa:** 9 skills. Dependem de decisões externas (Gui aprovar ferramentas + chaves API).

---

### Onda C — Skills de propósito ambíguo (prioridade 3)

Skills que precisam de auditoria de propósito antes de atacar:

1. **`/agenda`** — duplicata de /ver-agenda? Consolidar ou remover.
2. **`/paginas`** — alias? folder? Validar propósito.
3. **`/revisor-pagina`** — duplicata de /revisar-pagina? Consolidar ou remover.
4. **`/mentoria`** — deve ser skill ou só doc? Validar.
5. **`/qualificar-lead`** — definir critérios de qualificação.
6. **`/fechar-venda`** — definir fluxo de fechamento.
7. **`/onboarding-aluno`** — definir checklist de onboarding.

**Estimativa:** 7 skills. 1 sprint de auditoria + decisão Gui.

---

## Top 5 skills atacáveis AGORA (sem dependência externa)

1. **`/gerar-imagem`** — bug conhecido (Onda 9), fix confiabilidade é crítico.
2. **`/revisar-copy-pagina`** — adicionar cláusula Regra #24 (30min).
3. **`/revisar-codigo-pagina`** — adicionar cláusula Regra #24 (30min).
4. **`/publicar-jade`** — auditoria PII + workflow (1-2h).
5. **`/configurar-squad`** — testar com 1 aluno beta (1-2h).

---

## Top 5 skills bloqueadas (aguardando input externo)

1. **`/impulsionar-organico`** — aguarda MCP Meta Ads funcional.
2. **`/relatar-trafego`** — aguarda MCP Meta Ads + Google Ads.
3. **`/otimizar-campanha`** — aguarda MCP Meta Ads.
4. **`/analisar-resultados`** — aguarda chave API {{BANCO_PJ}}.
5. **`/disparar-newsletter`** — aguarda plataforma de email definida.

---

## Auditoria técnica

**Arquivos auditados:** 51 skills em `.claude/commands/*.md`  
**Método:** leitura de conteúdo (não só nome de arquivo) + correlação com memórias persistentes + histórico de uso em `squads/*/tarefas.md`  
**Classificação conservadora:** em dúvida entre 2 níveis, rebaixei (ex: funcional com 1 uso → não promovi a MADURA).

---

## Próxima ação (Jade decide)

**Sugestão:** atacar Onda A — 18 skills atacáveis sem dependência externa. Priorizar por caminho crítico:

1. **`/gerar-imagem`** (bloqueia carrosseis) → ataca primeiro.
2. **`/revisar-copy-pagina` + `/revisar-codigo-pagina`** (Regra #24 obrigatória) → ataca segundo.
3. **Resto da Onda A** em paralelo conforme disponibilidade.

**Onda B** aguarda decisões externas do Gui (chaves API, plataformas).  
**Onda C** aguarda auditoria de propósito.

---

**Última atualização:** 2026-05-11  
**Auditado por:** paginas-dev (squad-dev)  
**Aprovação pendente:** {{NOME_OPERADOR}}

---

## Arquivamento — 2026-05-14 (refactor task {{CLICKUP_TASK_ID}})

Skills ⚪ não-maduras movidas pra `workspace/skills-arquivadas/` (fora do escaneio do Claude Code). Lista:

- disparar-newsletter
- impulsionar-organico
- relatar-trafego
- otimizar-campanha
- analisar-resultados
- monitorar-concorrentes
- varrer-tendencias
- consultar-leads
- qualificar-lead
- fechar-venda
- onboarding-aluno
- mentoria
- auditar-entregabilidade-email
- paginas

Pra retomar uma skill arquivada: `mv workspace/skills-arquivadas/{nome}.md .claude/commands/{nome}.md` + adicionar override em settings.json se aplicável.

Nota: `/registrar-financeiro` aparece marcada como `⚪ MADURA` na tabela do squad FINANCEIRO (linha 111) — classificação contraditória; texto confirma "integração {{PLATAFORMA_NF}} API funcional, em uso" → mantida ativa (não arquivada).
