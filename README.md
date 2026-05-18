# Squad Jade — Time de Agentes IA pra teu negócio

Este é o template público do squad da **Jade** — uma COO virtual que orquestra um time de agentes de IA pra tocar operação do teu negócio (conteúdo, copy, dev, tráfego, financeiro, comercial).

## O que tu ganha

- **24 agentes** especializados em 8 squads funcionais
- **56 skills** prontas pra produção (newsletter, carrossel, copy de página, criativos Meta Ads, etc)
- **Jade COO** — agente orquestrador que despacha tudo
- **Hooks de segurança** (DCG bloqueia comandos destrutivos)
- **Atualização contínua** via `/atualizar-jade` (puxa updates preservando tua customização)

## Pré-requisitos

- macOS ou Linux
- [Claude Code](https://claude.com/claude-code) instalado
- Git + GitHub CLI (opcional)

## Como começar (5 minutos)

### 1. Pegue o template

Clique em **"Use this template"** no canto superior direito desta página → cria fork pessoal limpo na tua conta.

OU clone direto:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO
```

### 2. Abra no Claude Code

```bash
claude
```

### 3. Rode a configuração inicial

Dentro do Claude Code:

```
/configurar-jade
```

A Jade vai te fazer 7 perguntas (nome, empresa, domínio, etc) e substituir todos os placeholders pela tua identidade.

### 4. Inicie a primeira sessão

```
/jade-iniciar
```

Pronto — a Jade da TUA empresa tá rodando.

## Estrutura

```
.
├── CLAUDE.md           orquestrador principal
├── AGENTS.md           regras invioláveis do squad
├── IDENTIDADE.md       teus dados (preenchido por /configurar-jade)
├── MEMORY.md           memória persistente entre sessões
├── workspace/          estado operacional (memory, output, scripts)
├── squads/             8 squads funcionais (24 agentes total)
├── segundo-cerebro/    knowledge atemporal (preenche conforme uso)
└── .claude/
    ├── commands/       56 skills prontas
    ├── agents/         24 definições de agentes
    └── hooks/          guardas de segurança
```

## Squads inclusos

| Squad | Agentes | Skills macro |
|---|---|---|
| **gestao** | jade (COO) | `/jade`, `/listar-pendencias` |
| **conteudo** | 6 agentes | `/escrever-newsletter`, `/criar-carrossel`, `/cortar-youtube` |
| **copy** | 2 agentes | `/escrever-copy`, `/escrever-pagina` |
| **dev** | 5 agentes | `/criar-pagina-nova`, `/publicar-pagina` |
| **trafego** | 3 agentes | `/criar-criativo`, `/relatar-trafego-diario` |
| **financeiro** | 2 agentes | (skills dedicadas opcionais) |
| **comercial** | 3 agentes | (skills dedicadas opcionais) |
| **radar** | 2 agentes | `/monitorar-concorrentes`, `/varrer-tendencias` |

## Recebendo atualizações

Quando este template ganhar melhorias (skills novas, agentes novos), tu roda:

```
/atualizar-jade
```

A Jade puxa as novidades sem tocar nos teus dados pessoais (IDENTIDADE.md, memórias, aprendizados acumulados).

## Segurança

- **DCG Hook** — bloqueia comandos destrutivos (`rm -rf /`, `git push --force`, etc) automaticamente
- **Gitleaks + detect-secrets** — pré-commit varre segredos antes de commitar
- **Convenções claras** — segredos vão em `.env.local` (gitignored), nunca commitado

## Licença

MIT — usa, modifica, vende.

## Como contribuir

Issues e PRs bem-vindos. Mantenha a sanitização (zero info pessoal sua) ao propor mudanças.
