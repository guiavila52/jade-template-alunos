# Style guide — squad

Convenções de output. Não são regras invioláveis (essas vivem em `AGENTS.md`) — são padrões de qualidade que toda skill, agente e a Jade seguem em copy, markdown, naming, citação e formatação.

## URLs

Toda URL mencionada em qualquer resposta, doc, comentário ou mensagem **vira link clicável** no formato markdown `[texto](https://url)`. Sem URL "crua". Sub-regra: quando pedir pro Gui abrir / clicar / verificar / validar / conferir qualquer coisa que tenha URL (task ClickUp, newsletter no {{Plataforma_Conteudo}}, página, pasta Drive), o link clicável DEVE estar na MESMA frase do pedido, com URL completa. Sem mandar só ID/nome/caminho esperando que Gui monte.

- ✅ `[a newsletter](https://{{DOMINIO_NEWSLETTER}}/guiavila/conteudos/62bec9ff-1abd-4190-be01-f79f64a5b9fc)`
- ❌ `Confere a newsletter 62bec9ff`

## Citações

Falas literais do Gui em itálico ou bloco quote: *"frase exata"* ou `> frase exata`. Sempre datadas quando importam pra história (ex.: "06/05/2026 ~21h"). Memória `feedback_jade_comportamento.md` agrega o padrão.

## Naming de arquivos

- Datas em prefixo: `YYYY-MM-DD-slug.md` (ex.: `2026-05-14-refactor-arquitetura.md`).
- Sem versões no nome (`v1`, `v2`, `final`, `CORRETO`) — git é o versionamento. Memória `feedback_naming_assets_descritivo_sem_versao.md`.
- Slug descritivo, kebab-case, sem acento, sem espaço.
- Assets visuais: `tipo-pessoa-descricao-formato.ext` (ex.: `foto-gui-quadrada-800x800.png`).

## Acentuação

Português correto, sem omitir acentos. Bash heredoc preserva UTF-8 nativamente — falta de acento é falha humana. Vale pra copy, newsletter, post, carrossel, tweet, email, README público, comentários ClickUp. Memória `feedback_acentuacao_obrigatoria.md`.

## Hiperlinks padrão `{{DOMINIO}}/[slug]`

Toda menção a empresa/produto/parceiro do Gui vira link `{{DOMINIO}}/[slug]` (WordPress redirector). Slugs conhecidos: `{{produto_slug}}`, `manychat`, `clickup`, `clickup8x`, `level`, `automacoes`, `reverso`, `youtube`. Memória `project_hiperlinks_padrao.md`.

## Tom

Sem jargão inventado. Termos novos = perguntar antes (memória `feedback_sem_jargao.md`). "Onda" foi aprovada = lote de tarefas coeso.
