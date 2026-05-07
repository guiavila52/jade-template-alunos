# Squad Template — Sistema de Agentes de IA

Template para construir o seu próprio squad de agentes de IA com Claude Code.

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/guiavila52/squad-template.git meu-squad
   cd meu-squad
   ```

2. Edite `MEMORY.md` e `CLAUDE.md` substituindo todos os placeholders `{{...}}` pelos dados da sua empresa/operação.

3. Configure suas próprias memórias do operador (opcional):
   ```bash
   # As memórias persistem em ~/.claude/projects/{path-encoded}/memory/
   # Use `/consolidar-sessao` durante o uso pra Claude salvar feedback
   ```

4. Crie a estrutura do `Segundo Cérebro/` (não vem no template — é o conhecimento da sua empresa):
   ```
   Segundo Cérebro/
   ├── MAPA.md
   ├── 01-identidade/
   ├── 02-negocios/
   ├── 03-operacao/
   └── 04-decisoes/
   ```

5. Comece a sessão chamando a Jade:
   ```
   /jade
   ```

## Estrutura

| Arquivo / Pasta | O que contém |
|---|---|
| `CLAUDE.md` | Contexto principal do squad (sanitizado, com placeholders) |
| `MEMORY.md` | GPS do squad — foco atual, projetos, links |
| `AGENTS.md` | Regras invioláveis (não editar sem combinar) |
| `.claude/commands/` | Skills (verbo-primeiro, Regra #17) |
| `squads/` | Squad operacional (Jade COO + workers) |
| `squad/` | Memória + outputs do squad |

## Squads e agentes

- **squad-jade** — COO + estrategista (orquestração)
- **squad-conteudo** — newsletter + carrossel
- **squad-copy** — copywriter + páginas
- **squad-dev** — desenvolvedor de páginas
- **squad-trafego** — criativos pagos

Cada squad tem `memoria.md`, `aprendizados.md` e `tarefas.md` próprios.

## Skills incluídas

- Orquestração: `/jade`, `/consolidar-sessao`
- Páginas: `/criar-pagina`, `/escrever-pagina`, `/codar-pagina`, `/migrar-pagina`, `/publicar-pagina`, `/revisar-pagina`, `/revisar-codigo-pagina`, `/testar-pagina`
- Conteúdo: `/escrever-copy`, `/escrever-newsletter`, `/criar-carrossel`, `/revisar-carrossel`, `/escrever-roteiro`, `/escrever-linkedin`
- Tráfego: `/criar-criativo`
- Operação: `/ver-agenda`, `/revisar-semana`, `/transcrever-video`

## Regra de ouro

A pessoa fala **com a Jade** (COO). A Jade despacha pra os squads. Você não chama agentes diretamente — sempre via Jade. Isso preserva o briefing, a fila de tarefas e o registro.

## Origem

Template extraído do squad real do Gui Ávila ([@guiavila](https://www.youtube.com/@guiavila)). Sincronizado manualmente quando há marcos relevantes (skill nova, agente novo, regra nova).

## Licença

MIT — use, modifique, compartilhe.
