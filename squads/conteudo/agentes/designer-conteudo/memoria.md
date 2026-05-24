# memoria.md — Agente Carrossel

> Memória específica do agente carrossel. Padrões, preferências e estado de execução.

---

## Contexto

Squad: conteudo
Função: produzir carrosséis para redes sociais (Instagram, LinkedIn).

---

## Padrões de entrega

- Estilo: "print de tweet" — leitura rápida, visual limpo
- Slide 1: gancho forte, promessa clara
- Slides intermediários: uma ideia por slide, sem texto longo
- Último slide: CTA direto

---

## Briefing esperado do estrategista — schema

Quando o agente carrossel é despachado pela Jade dentro do fluxo `/criar-carrossel` ou `/criar-carrossel-de-video`, ele recebe briefing do estrategista no formato:

| Campo | Descrição | Exemplo |
|---|---|---|
| `tema` | tema principal | "Por que 80% dos squads de IA falham" |
| `angulo_unico` | recorte único pro Gui | "Maioria erra na orquestração, não na IA" |
| `payoff` | conclusão que o último slide entrega | "Squad bom = orquestração + memória + revisão" |
| `qtd_laminas` | número de slides | 7 |
| `estrutura` | sequência lógica | "hook (1) → problema (2-3) → diagnóstico (4-5) → método (6) → CTA (7)" |
| `tom` | tom específico | "didático+irônico" ou "técnico+sério" |
| `referencias_segundo_cerebro` | arquivos relevantes | ["banco-de-historias.md", "tom-de-voz.md", "produtos-servicos.md"] |
| `transcricao` (se vídeo) | texto bruto da transcrição | "..." |

Output esperado do agente carrossel:
- `roteiro.md` — copy slide-a-slide com Light Copy
- `briefing-visual.md` — pra cada slide: template recomendado (default/quote/lista/antes-depois/story), texto exato, autor, handle, número (1/N)
- Salvar em `workspace/output/carrosseis/YYYY-MM-DD-[slug]/`

---

## Cadeia de despacho

```
estrategista → carrossel (você) → squad-imagem (HTML→PNG via gerar-imagem.mjs) → revisor-visual + revisor-carrossel
```

---

## Regras invioláveis pra carrossel

- **Light Copy obrigatório** (frase curta, premissa única por slide)
- **Slide 1 = Setup+Punch ou Escalada de Atenção** (sem 3 Ps)
- **CTA SÓ no último slide**
- **Cormorant Garamond NUNCA em dígitos** (Regra #188 absoluta)
- **Banco de histórias do segundo-cerebro = fonte de exemplos reais**

---

## Dependências

- ~~Aguarda método de acesso a transcrições do YouTube para gerar carrosséis a partir de vídeos~~ **RESOLVIDO** (08/05/2026 — `/transcrever-video` operacional)
