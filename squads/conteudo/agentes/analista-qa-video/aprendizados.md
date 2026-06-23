# Aprendizados — analista-qa-video

Registro cronológico de lições do agente de QA de vídeo. Padrões de erro recorrentes em edições reais.

---

**Criado em:** 2026-06-10 — agente criado em 06/06/2026, pasta squad criada em 10/06/2026.

## Princípio fundador (06/06/2026)

Agente criado para fechar o ciclo de qualidade do conteúdo audiovisual. O editor (`editor-audiovisual`) produz, o `analista-qa-video` audita o arquivo final antes do upload.

**Regra:** nenhum arquivo `*_FINAL.mp4` vai para o YouTube sem passar pelo analista-qa-video via skill `/qa-video`.

---

## Checklist de detecção padrão

- Retomadas explícitas ("Peraí", "Ops", "vou refazer", "retomando")
- Sentenças truncadas no meio do pensamento
- Hesitações nos inícios de clips (respiro longo, "uh", "hmm")
- Gaps de silêncio acima de 1.5s fora de pausa intencional
- Repetição de conteúdo idêntico ou muito similar entre clips adjacentes
- Final abrupto (áudio cortado sem conclusão de frase)
- Início sujo (clique, ruído, fala cortada)

---
