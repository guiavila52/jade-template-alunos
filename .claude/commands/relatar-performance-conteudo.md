---
name: relatar-performance-conteudo
description: Relatório de performance do conteúdo orgânico — YouTube, Instagram, LinkedIn. Fecha o loop do funil orgânico sem abrir as plataformas manualmente.
type: skill
---

# /relatar-performance-conteudo

**Squad:** conteudo
**Agente:** @estrategista-marketing
**Status:** 🟢 MADURA (YouTube Data API v3 ativa com chave restrita; Instagram e LinkedIn via WebFetch)
**Trigger:** sob demanda | cron semanal sexta 17:00 BRT

---

## Contexto

operador publica no YouTube (motor principal do funil), Instagram e LinkedIn.
Esta skill responde: "O conteúdo está funcionando? O que está trazendo audiência? Qual vídeo/post converteu mais?"
Fecha o loop: tráfego pago + conteúdo orgânico = visão completa do funil.

---

## Fluxo

```
Input (período: semana | mês)
  ↓
1. YouTube: buscar últimos vídeos + métricas (views, CTR, watch time, inscritos ganhos)
2. Instagram: buscar posts recentes + alcance/engajamento (via WebFetch perfil público ou API)
3. LinkedIn: buscar posts recentes + impressões/engajamento
4. Identificar: qual conteúdo performou melhor? Qual tema ressoou?
5. Correlacionar: conteúdo com pico de views → aumento de leads naquele período?
6. Salvar output em workspace/output/conteudo/performance/{YYYY-MM-DD}.md
  ↓
Output (ranking de conteúdo + insight acionável)
```

---

## YouTube (principal)

### Com YouTube Analytics API (quando disponível)
```bash
python3 workspace/scripts/marketing/relatar-performance-youtube.py --periodo 7d
```
Requer: `YOUTUBE_API_KEY` e `YOUTUBE_CHANNEL_ID` em app/.env.local

### Fallback sem API (usando agora)
- WebFetch no canal do operador: `https://www.youtube.com/@{{GITHUB_USER}}`
- Capturar: títulos, views visíveis, data de publicação, thumbnails
- Identificar vídeos das últimas 4 semanas com mais tração

**Canal:** `https://www.youtube.com/@{{GITHUB_USER}}`

---

## Instagram

### Com API Graph (quando disponível)
Requer: `INSTAGRAM_ACCESS_TOKEN` em app/.env.local

### Fallback (usando agora)
- WebFetch no perfil público: `https://www.instagram.com/{{GITHUB_USER}}/`
- Capturar: últimos posts visíveis, tipo de conteúdo, engajamento aproximado

---

## LinkedIn

### Fallback (usando agora)
- WebFetch no perfil: `https://www.linkedin.com/in/{{HANDLE_OPERADOR}}/`
- Capturar: posts recentes, reações aproximadas

---

## O que entregar

### Ranking da semana
```
🏆 Top 3 conteúdos (por engajamento/alcance)
1. [Título/descrição] — [plataforma] — [views/alcance] — [data]
2. ...
3. ...
```

### Insight acionável (1 linha)
"O vídeo sobre X performou 3x acima da média → pauta similar para próxima semana."

### Correlação com leads (se disponível)
"Pico de views em [data] coincide com entrada de N leads no GHL."

---

## Output canônico

`workspace/output/conteudo/performance/{YYYY-MM-DD}.md`

---

## Credenciais necessárias (via operador)

| Variável | Status | Como obter |
|---|---|---|
| `YOUTUBE_API_KEY` | ❌ Pendente | Google Cloud Console → APIs → YouTube Data API v3 → Criar credencial |
| `YOUTUBE_CHANNEL_ID` | ❌ Pendente | operador confirmar ID do canal (UC...) |
| `INSTAGRAM_ACCESS_TOKEN` | ❌ Pendente | Meta for Developers → Graph API → token de página |

Enquanto não tiver API: executa via WebFetch (dados parciais mas úteis).

---

## Bateria de testes

- [x] Skill criada e documentada
- [ ] Teste WebFetch canal YouTube (dados parciais)
- [ ] Credenciais YouTube API configuradas
- [ ] Output salvo no path canônico

---

## Aprendizados + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
