<!-- Modelo recomendado: claude-sonnet-4-6 -->

# /transcrever-video

Skill de transcrição de vídeo (YouTube ou arquivo local) com timestamps por parágrafo e **verificação obrigatória de completude** (a transcrição só é aprovada se cobrir até o fim do vídeo dentro da tolerância).

## Quando usar

- {{NOME_OPERADOR}} manda URL de YouTube ou path de arquivo de vídeo/áudio e quer o conteúdo em texto.
- Outras skills (`/escrever-roteiro`, `/escrever-linkedin`, `/criar-carrossel`) recebem URL de YouTube e precisam transcrever antes de processar.
- Captura de aulas, lives, reuniões, podcasts.

Não usa: para legendar vídeo (timing por palavra) — isso é outro fluxo.

## Pré-requisitos (validar antes de rodar)

- `yt-dlp` (`brew install yt-dlp` ou `pip install -U yt-dlp`)
- `ffmpeg` + `ffprobe` (`brew install ffmpeg`)
- Para fallback offline (Whisper): `whisper` (`pip install -U openai-whisper`) **OU** `whisper-cpp` (`brew install whisper-cpp`)
- Para limpeza Claude (auto-sub apenas): `anthropic` Python SDK (`pip install anthropic`) + variável `ANTHROPIC_API_KEY` (procurada em env, `.env` na raiz, ou `app/.env.local`)

Se prerequisito faltar: ABORTAR com mensagem clara dizendo o que instalar.

## Input

Argumento posicional após o slash command:

```
/transcrever-video <URL_ou_path> [--whisper]
```

Exemplos:
- `/transcrever-video https://youtu.be/1U0g08yDg7M`
- `/transcrever-video https://www.youtube.com/watch?v=abc123`
- `/transcrever-video /Users/{{USERNAME_MAC}}/Downloads/aula.mp4`
- `/transcrever-video https://youtu.be/abc --whisper` → força Whisper e PULA a limpeza Claude (Whisper já é alta qualidade)

Se invocada sem argumento, a Jade pede a URL/path antes de rodar.

Aceita:
- URL do YouTube (qualquer formato: `youtu.be/X`, `youtube.com/watch?v=X`, com ou sem parâmetros)
- OU path absoluto para arquivo local de vídeo/áudio (`.mp4`, `.mov`, `.mp3`, `.wav`, `.m4a`...)

## Pipeline

### Passo 1 — Detectar fonte e duração total

- Se URL YouTube:
  ```bash
  yt-dlp --print "%(title)s|%(duration)s|%(id)s" URL
  ```
  Salvar `TITULO`, `DURACAO_TOTAL_SEGUNDOS`, `VIDEO_ID`.
- Se arquivo local:
  ```bash
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 PATH
  ```
  `TITULO` = nome do arquivo sem extensão.

### Passo 2 — Fast path: legenda automática do YouTube

```bash
yt-dlp --write-auto-sub --sub-lang "pt-orig,pt,pt-BR,en" \
  --sub-format vtt --skip-download \
  -o "/tmp/transcribe-%(id)s.%(ext)s" URL
```

Procurar nesta ordem o primeiro VTT existente: `/tmp/transcribe-{id}.pt.vtt` → `pt-orig.vtt` → `pt-BR.vtt` → `en.vtt`.

Se obteve VTT: `metodo = youtube-auto-sub`. Pular Passo 3.

### Passo 3 — Slow path: Whisper (fallback)

Só rodar se Passo 2 falhou OU input é arquivo local.

1. Verificar `which whisper` (ou `which whisper-cpp`). Se nenhum disponível: ABORTAR.
2. Se YouTube, baixar áudio:
   ```bash
   yt-dlp -x --audio-format mp3 -o "/tmp/audio-%(id)s.%(ext)s" URL
   ```
3. Rodar Whisper:
   ```bash
   whisper "/tmp/audio-{id}.mp3" \
     --model medium --language pt \
     --output_format vtt --output_dir /tmp/
   ```
   `metodo = whisper-medium` (ou `whisper-cpp` se for o caso).

### Passo 5 — Parser do VTT (cuidado com rolling captions)

VTT do YouTube vem com **rolling captions**: cada cue contém a linha anterior + uma linha nova (a com tags `<00:00:00.000>`). O parser deve:

- Quando o cue tem múltiplas linhas e alguma delas contém tag inline `<\d{2}:\d{2}:\d{2}\.\d{3}>`, **manter apenas as linhas com tag** (a linha "fresca"). Caso contrário, manter todas.
- Remover tags inline `<...>` e `<c>...</c>`.
- Se a primeira linha do cue atual é igual à última linha do cue anterior, descartar (caso de borda).
- Pular cues vazios.

Resultado: lista `[(start_s, end_s, text)]` sem repetição.

### Passo 6 — Agrupar em parágrafos

- Janela: `min_seconds=30`, `max_seconds=60`.
- Encerra parágrafo quando `dur >= 30` E (`dur >= 60` OU último texto termina com `.`/`!`/`?`).
- Cada parágrafo recebe o timestamp do **início** no formato:
  - `[mm:ss]` se vídeo total < 1h
  - `[hh:mm:ss]` se vídeo >= 1h
- Após montar parágrafos, rodar limpezas:
  - Colapsar palavras adjacentes repetidas: `\b(\w+)( \1\b)+` → `\1` (case-insensitive).
  - Normalizar espaços.

### Passo 7 — Limpeza via Claude (auto-sub apenas)

Só roda quando `metodo == youtube-auto-sub` e a flag `--whisper` NÃO foi passada (Whisper já produz texto limpo).

**Pré-requisitos:**
- `ANTHROPIC_API_KEY` resolvido na seguinte ordem:
  1. `os.environ["ANTHROPIC_API_KEY"]`
  2. Linha `ANTHROPIC_API_KEY=...` em `.env` na raiz do repo
  3. Linha `ANTHROPIC_API_KEY=...` em `app/.env.local` (ou `app/.env`)
- SDK `anthropic` instalado. Se não estiver, o script tenta `pip install -q anthropic` (com fallback `--user --break-system-packages`).

Se nenhum dos dois disponível: PULAR a limpeza com warning. Não abortar — gravar versão sem limpeza e marcar `limpeza_claude: false` no frontmatter + razão na linha final.

**Implementação:**
- Modelo: `claude-haiku-4-5-20251001` (barato e rápido).
- Prompt caching: `cache_control: ephemeral` no system prompt.
- Lotes de até **10 parágrafos** por chamada, **4 chamadas paralelas** via `ThreadPoolExecutor`.
- Cada lote: numeração `#1 [mm:ss] texto`, devolvida no mesmo formato.
- Se o parser da resposta falhar para um lote: manter os parágrafos originais desse lote, registrar warning, continuar.

**Regras invioláveis no system prompt:** corrigir só termos técnicos mal reconhecidos (ex: "Cloud Code"→"Claude Code", "squats"→"squads"), trocas de letra ("Turmar"→"Turma"), nomes próprios óbvios e concordância. **Não** reformular, não traduzir, não inventar pontuação. Preservar timestamps `[mm:ss]` e marcações `[música]`/`[risadas]`/etc.


### Passo 8 — Salvar output

Path: `squad/output/transcricoes/YYYY-MM-DD-{slug}.md`

`slug`: lowercase, sem acentos, espaços/pontuação → hifens, máximo 60 chars, sem hifens nas pontas.

Frontmatter:
```yaml
---
fonte: {URL ou path}
titulo: {título}
duracao: {hh:mm:ss}
duracao_segundos: {N}
metodo: youtube-auto-sub | whisper-medium | whisper-cpp
tempo_execucao_segundos: {N.N}
tempo_execucao_humano: {7.4s | 2m 15s | 1h 5m 30s}
limpeza_claude: true | false
modelo_limpeza: claude-haiku-4-5-20251001   # só se aplicada
tempo_limpeza_segundos: {N.N}                # só se aplicada
data_transcricao: YYYY-MM-DD
---
```

Corpo:
```markdown
# {título}

[mm:ss] Parágrafo 1...

[mm:ss] Parágrafo 2...

...

_Transcrição completa — último timestamp [mm:ss], duração total [mm:ss], diff Xs (dentro da tolerância de Ys). Tempo de execução: 22.3s (auto-sub 7.4s + limpeza Claude 14.9s)._  
_Quando a limpeza não foi aplicada (Whisper, key faltando, etc.):_  
_Transcrição completa — ... Tempo de execução: 7.4s. ⚠️ Limpeza Claude não aplicada (motivo)._
```

### Passo 9 — Verificação de fim (CRÍTICA, não pode pular)

Skill SÓ retorna sucesso se passar.

```
ULTIMO_TS = timestamp de fim do último parágrafo (segundos)
DIFF = DURACAO_TOTAL_SEGUNDOS - ULTIMO_TS
TOLERANCIA = max(15, 0.02 * DURACAO_TOTAL_SEGUNDOS)
```

- Se `DIFF <= TOLERANCIA`: SUCESSO. Adicionar a linha de validação no fim do arquivo.
- Se `DIFF > TOLERANCIA`: FALHA.
  - Mensagem: `Transcrição parou em mm:ss mas vídeo tem hh:mm:ss (faltam Xs / Y%). Re-rodando...`
  - Tentar re-execução automática (1 retry — limpar VTTs `/tmp/transcribe-{id}*` e refazer Passos 2-5).
  - Se retry também falhar: salvar arquivo como `YYYY-MM-DD-{slug}-INCOMPLETA.md` e reportar erro destacado.

### Passo 10 — Reportar

Imprimir JSON com:
```json
{
  "ok": true|false,
  "method": "...",
  "title": "...",
  "duration_s": N,
  "last_ts_s": N,
  "diff_s": N,
  "tolerance_s": N,
  "output_path": "...",
  "paragraphs": N
}
```

Mostrar ao {{NOME_OPERADOR}}: path do arquivo, duração, último timestamp, diff, e SUCESSO/FALHA.

## Implementação

A pipeline está implementada em Python. O script de referência fica em `/tmp/transcribe_video.py` durante a sessão. Para uso permanente, copie para `squads/dev/scripts/transcribe_video.py` e chame:

```bash
python3 squads/dev/scripts/transcribe_video.py "URL_OU_PATH" "$(pwd)"
```

## Output

`squad/output/transcricoes/YYYY-MM-DD-{slug}.md` — atualizar `MAPA.md` da pasta a cada transcrição.

## Verificação de fim (resumo)

- Tolerância = `max(15s, 2% da duração)`.
- 1 retry automático em caso de falha.
- Arquivo marcado `[INCOMPLETA]` no nome se o retry também falhar.

## Quem chama

- {{NOME_OPERADOR}} direto: `/transcrever-video URL` ou `/transcrever-video /path/file.mp4`
- Outras skills (futuras):
  - `/escrever-roteiro` → recebe URL → chama `/transcrever-video` antes
  - `/escrever-linkedin` → recebe URL → chama `/transcrever-video` antes
  - `/criar-carrossel` → recebe URL → chama `/transcrever-video` antes

## Saída pra Jade

Ao terminar, sempre reportar:
- Path da transcrição gerada
- Método usado
- Diff/tolerância
- Tempo total de execução
- N° de parágrafos

## Fluxo

```
[ /transcrever-video <URL_ou_path> [--whisper] ]
        ↓
[ 1. Validar pré-requisitos ] → @transcrever-video
   yt-dlp, ffmpeg/ffprobe; (whisper se --whisper);
   anthropic + ANTHROPIC_API_KEY se auto-sub
        ↓
[ 2. Detectar fonte + duração total ] → @transcrever-video
   yt-dlp --print  OU  ffprobe duration
        ↓
   ┌─────────────────────────────────────┐
   ↓ (URL YT, sem --whisper)        (--whisper OU arquivo local)
[ 3a. Fast path: yt-dlp           [ 3b. Slow path: Whisper
   --write-auto-sub VTT ]            yt-dlp -x audio + whisper medium pt ]
        ↓                                       ↓
        └────────────┬──────────────────────────┘
                     ↓
[ 4. Parser VTT ] → @transcrever-video
   trata rolling captions (mantém linha com tag inline)
   remove tags <...>, dedup, pula vazios
        ↓
[ 5. Agrupar parágrafos 30-60s ] → @transcrever-video
   timestamp [mm:ss] ou [hh:mm:ss]
   colapsa palavras repetidas
        ↓
   ┌─────────────────────────────────────┐
   ↓ (auto-sub + sem --whisper)    (--whisper OU sem API key)
[ 6a. Limpeza Claude haiku-4-5     [ 6b. Pular limpeza
   - lotes de 10, 4 paralelos        (registra warning) ]
   - prompt caching ephemeral
   - corrige só termos técnicos ]
        ↓                                       ↓
        └────────────┬──────────────────────────┘
                     ↓
[ 7. Salvar output + frontmatter ] → @transcrever-video
   squad/output/transcricoes/YYYY-MM-DD-{slug}.md
        ↓
[ 8. Verificação de fim (CRÍTICA) ] → @transcrever-video
   tolerancia = max(15s, 2% duração)
   diff = duração - último_ts
        ↓
   ┌─────────────────────────────────────┐
   ↓ (diff <= tol)                (diff > tol)
[ ✅ SUCESSO                        [ ❌ FALHA
   - linha de validação no fim         - 1 retry automático
   - reporta JSON ao {{NOME_OPERADOR}} ]             - se retry falhar:
                                        salva [INCOMPLETA].md
                                        + alerta destacado ]
        ↓                                       ↓
        └────────────┬──────────────────────────┘
                     ↓
[ 9. Atualizar MAPA.md da pasta transcricoes ]
        ↓
   ⟶ FIM (path + método + diff/tol + tempo + paragraphs)
```
