# aprendizados.md — Agente Carrossel

> Lições específicas do agente carrossel.

---

*(Preencher após primeiras entregas)*

### 2026-05-10 — Carrossel "7 Ferramentas" — esteira validada parcialmente

**Contexto:** Primeira execução real do fluxo `/criar-carrossel-de-video` com URL real do {{OPERADOR}} (https://youtu.be/hoSD2Bd4I2I).

**O que funcionou:**
- yt-dlp pegando autosub PT-BR (auto-tradução YouTube) em 1s
- Estrategista propôs 3 candidatos e escolheu B (tese forte "ferramentas conversando")
- Carrossel/copywriter produziu roteiro 7 slides com Light Copy
- Briefing visual mapeou 7 templates apropriados (2 quote + 1 default + 3 lista + 1 story)

**O que não funcionou:**
- Slide 1 PNG travou no Playwright (Mac sem `timeout` nativo, sem feedback de erro)

**Padrão identificado:** Esteira até `briefing-visual.md` funciona. Geração PNG via {{skill_imagem}}.mjs ainda é frágil em background.

**Como evitar/repetir:**
- Sempre testar geração PNG em foreground primeiro (1 slide)
- Se travar, capturar stderr completo
- Considerar gtimeout (brew) como dependência opcional

---

## 2026-05-11 — Base64 para imagens locais no Playwright

**Contexto:** Carrossel "7 ferramentas" estava sem foto do {{OPERADOR}} nos slides quote/default.

**Descoberta técnica:** Playwright bloqueia `file://` URLs por política de segurança CORS. Solução = converter imagens locais para base64 data URLs.

**Implementação:**
- Modificar `buildFotoHtml()` em `scripts.mjs`
- Detectar extensão (.png/.jpg/.webp) → mime type correto
- `fs.readFileSync()` → `buffer.toString('base64')` → `data:image/png;base64,{base64}`
- Fallback continua funcionando (inicial do nome)

**Teste funcional antes de aprovar:**
```bash
node scripts.mjs \
  --template quote \
  --texto "Teste" \
  --autor "{{NOME_OPERADOR}}" \
  --handle "@{{handle}}" \
  --foto "scripts/tweet-templates/assets/gui-perfil.png" \
  --numero "1/1" \
  --output "/tmp/test.png"
```
Abrir PNG → foto deve aparecer dentro do círculo dourado.

**Regra permanente:** TODA imagem local em templates Playwright = base64, nunca file:// URL.
# aprendizados.md — Agente Carrossel

> Lições específicas do agente carrossel.

---

*(Preencher após primeiras entregas)*


## Conteúdo absorvido de squads/conteudo/agentes/designer-conteudo (refactor 2026-05-14)

# aprendizados.md — Agente Carrossel

> Lições específicas do agente carrossel.

---

*(Preencher após primeiras entregas)*
