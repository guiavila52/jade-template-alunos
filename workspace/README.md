# Squad de Agentes — Gui Ávila

Agentes especializados nos gargalos do negócio. Cada agente conhece o Cérebro (tom de voz, produtos, contexto) e opera com checkpoints de aprovação antes de qualquer entrega.

---

## Agentes disponíveis

| Comando | Agente | Função |
|---------|--------|--------|
| `/estrategista` | Estrategista | Analisa o negócio, prioriza ações, delega para outros agentes |
| `/escrever-copy` | Copywriter | Escreve qualquer copy no tom do Gui — agente base do squad |
| `/escrever-newsletter` | Newsletter | Escreve a newsletter semanal completa |
| `/mentoria` | Mentoria | Estrutura e executa o lançamento da mentoria |
| `/criar-criativo` | Tráfego | Estratégia de campanhas e briefings de criativos |
| `/criar-carrossel` | Carrossel | Transforma vídeos do YouTube em carrosséis para Instagram/LinkedIn |
| `/escrever-pagina` | Páginas | Cria e melhora landing pages para sites.{{DOMINIO}} |

---

## Como usar

1. Abra o Claude Code na raiz do projeto (`Squad Empresa Gui Ávila/`)
2. Digite o slash command do agente (ex: `/escrever-newsletter`)
3. O agente lê o Cérebro e inicia o workflow
4. Aprove ou redirecione em cada checkpoint

---

## Arquitetura do squad

```
Estrategista
    ↓ (orquestra)
    ├── Newsletter ──→ Copywriter (redige o texto)
    ├── Mentoria ────→ Copywriter (redige materiais)
    ├── Tráfego ─────→ Copywriter (redige copies dos anúncios)
    ├── Carrossel ───→ Copywriter (redige os slides)
    └── Páginas ─────→ Copywriter (redige a copy da página)
```

O **Copywriter** é o agente base — todos os outros chamam ele para redigir. A memória de correções (`workspace/memory/escrever-copy.md`) é centralizada e compartilhada por todos.

---

## Sistema de memória (aprendizado)

O Copywriter aprende com cada correção do Gui:

1. Entrega a copy
2. Pergunta: "Tem algo que você mudaria?"
3. Se sim: extrai o padrão, apresenta a regra, salva em `workspace/memory/escrever-copy.md`
4. Na próxima sessão, lê a memória e começa mais calibrado

Quanto mais sessões, menos correções necessárias.

---

## Outputs

| Agente | Pasta |
|--------|-------|
| Newsletter | `workspace/output/newsletter/` |
| Mentoria | `workspace/output/mentoria/` |
| Tráfego | `workspace/output/criativos/` |
| Carrossel | `workspace/output/carrossel/` |
| Páginas | `workspace/output/paginas/` |

---

## Conexão com {{Plataforma_Conteudo}}

Integração via API REST do {{Plataforma_Conteudo}} (Bearer `sk-sq-*`, endpoints em `segundo-cerebro/03-operacao/{{plataforma_conteudo}}-historico.md`):
- Carrossel empurra direto para a fila de produção do {{Plataforma_Conteudo}}
- Newsletter envia rascunho para aprovação no {{Plataforma_Conteudo}}
- Status visível no painel visual em tempo real

**Nota histórica [DEPRECATED 2026-05-14]:** antes existia plano de expor MCP server; MCP descontinuado em 12/05/2026 (retorna 401). API REST direta é o caminho canônico.

---

## Estrutura de arquivos

```
workspace/
├── README.md              ← este arquivo
├── agents/                ← definições e personas dos agentes
│   ├── copywriter.md
│   ├── estrategista.md
│   ├── newsletter.md
│   ├── mentoria.md
│   ├── trafego.md
│   ├── carrossel.md
│   └── paginas.md
├── memory/
│   └── copywriter.md      ← memória que cresce com correções
└── output/                ← outputs gerados pelos agentes
    ├── newsletter/
    ├── mentoria/
    ├── criativos/
    ├── carrossel/
    └── paginas/
```
