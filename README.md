# 🧠 Sistema Operacional da {{EMPRESA_HOLDING}}

Sistema interno de comando e controle da {{EMPRESA_HOLDING}}.

## Documentação do Projeto

| Arquivo | O que contém |
|---------|-------------|
| `CLAUDE.md` | Contexto principal para o Claude Code (stack, estrutura, regras) |
| `PRD.md` | Requisitos do produto com roadmap em 3 MVPs |
| `docs/integrations.md` | Detalhes técnicos de cada integração (APIs, endpoints, auth) |
| `docs/database.md` | Schema completo do banco de dados |
| `docs/business-rules.md` | Regras de negócio, cálculos, permissões |
| `.env.example` | Todas as variáveis de ambiente necessárias |

## Stack

- **Frontend:** Next.js 14+ (App Router)
- **UI:** shadcn/ui + Tailwind CSS + Recharts
- **Backend:** Next.js API Routes + Supabase Edge Functions
- **Banco:** PostgreSQL (Supabase)
- **Auth:** Supabase Auth (Magic Link)
- **IA:** Claude API (Anthropic)
- **Deploy:** Vercel
- **Cron:** Vercel Cron Jobs

## Como usar com o Claude Code

### Workflow recomendado (3 sessões)

**Sessão 1 — Setup do projeto**
```
Leia o CLAUDE.md e o PRD.md. Configure o projeto Next.js com a estrutura definida, 
instale as dependências, configure Supabase e crie as migrations do MVP 1 
baseado no docs/database.md.
```
Depois: `/clear`

**Sessão 2 — Layout e Auth**
```
Leia o CLAUDE.md. Implemente o layout base do dashboard (sidebar, header, dark mode), 
o sistema de auth com Magic Link e o middleware de permissões.
```
Depois: `/clear`

**Sessão 3+ — Features do MVP 1**
```
Leia o CLAUDE.md e o PRD.md (seção MVP 1). Implemente [feature específica].
Consulte docs/business-rules.md para regras de cálculo.
```

### Dica importante
Trabalhe feature por feature. Não peça para implementar tudo de uma vez. O Claude Code performa melhor com tarefas específicas e bem definidas.
