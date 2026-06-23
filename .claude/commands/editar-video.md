# /editar-video

Skill de edição autônoma de vídeos YouTube gravados em múltiplos clips.

Detecta e corta: retomadas explícitas ("Peraí", "Ops", "retomando"), sentenças truncadas em "...", hesitações e repetições nos finais/inícios de clips. Exporta um único `.mp4` por vídeo.

## Fluxo

1. Detectar clips na pasta (`yt NNN - 1.mp4`, `yt NNN - 2.mp4`...)
2. Transcrever cada clip com mlx-whisper (Apple Silicon, GPU)
3. Detectar erros em cada clip: retomadas, truncamentos, hesitações, repetições
4. Calcular cortes precisos (timestamps) para cada erro detectado
5. Aplicar cortes via ffmpeg (sem reencoding no áudio limpo)
6. Juntar clips em um único vídeo
7. Exportar `yt NNN_FINAL.mp4` na pasta do Drive
8. Salvar relatório de cortes realizados

## Quando usar

operador gravou um vídeo em múltiplos clips (pasta `yt NNN` com arquivos `yt NNN - 1.mp4`, `yt NNN - 2.mp4`...) e quer juntar + cortar erros + exportar.

## Pré-requisitos

- `ffmpeg` (`brew install ffmpeg`)
- `mlx-whisper` (`pip3 install mlx-whisper --break-system-packages`) — usa Apple Silicon GPU, 10-20x mais rápido que whisper padrão
- Clips nomeados no padrão `yt NNN - N.mp4` na pasta do Google Drive

## Input

```
/editar-video <pasta_ou_numero>
```

Exemplos:
- `/editar-video 178` → procura pasta `yt 178` no path canônico
- `/editar-video "/caminho/completo/yt 178"` → path direto

**Path canônico dos clips:**
```
/Users/{{USERNAME_MAC}}/Library/CloudStorage/GoogleDrive-{{USERNAME_MAC}}@{{DOMINIO}}/Meu Drive/{{NOME_OPERADOR}} - Business/Videos Youtube - arquivos de gravação/yt NNN/
```

**Output:** `/Users/{{USERNAME_MAC}}/Desktop/yt-editados/ytNNN/ytNNN_FINAL.mp4`

## Pipeline

### Passo 1 — Detectar clips

Listar todos os `.mp4` da pasta em ordem numérica. Registrar duração de cada clip (ffprobe). Calcular offsets cumulativos no concat.

### Passo 2 — Extrair áudio (WAV 16kHz mono)

```bash
ffmpeg -i "clip_N.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "clipN.wav" -y
```

Concatenar todos os WAVs com concat demuxer.

### Passo 3 — Transcrever com mlx-whisper

```bash
mlx_whisper "audio_concat.wav" \
  --model mlx-community/whisper-medium-mlx \
  --language pt \
  --output-format json \
  --output-dir "pasta_output/" \
  --word-timestamps True
```

**Importante:** mlx-whisper é 10-20x mais rápido que `whisper` padrão no Apple Silicon. Nunca usar `whisper` padrão para arquivos >5min.

### Passo 4 — Análise de cortes (camadas)

Para cada boundary entre clips, analisar os últimos **20s antes** e primeiros **10s depois**:

**CAMADA 1 — Retomadas explícitas no início do próximo clip:**
- `peraí`, `ops,`, `retomando`, `vamos recomeçar`, `gaguej`
- → Skip N segundos do início do próximo clip até passar o marcador

**CAMADA 2 — Sentenças truncadas no final do clip atual:**
- Termina em `...` (ex: "você vai ver..." / "é só você...")
- Padrão regex: `\.\.\.$` ou `é só\s+\w+` ou `conta\.\.\.`
- → Trim clip atual antes da frase truncada (voltar à última frase com pontuação final `.!?,`)

**CAMADA 3 — Repetição de conteúdo:**
- Mesma frase aparece nos últimos 5s do clip atual E nos primeiros 5s do próximo
- → Cortar a versão truncada, manter a versão completa

**CAMADA 4 — Verificação de pontuação:**
- Se o último segmento do clip não termina com `.!?,` e tem >5 palavras → investigar se é truncamento

**Decisão de corte:**
```
Para cada clip i:
  trim_at = None  # segundos dentro do clip onde cortar o fim
  skip_at = None  # segundos do início do clip i+1 a pular

Se detectou CAMADA 2 em clip i:
  trim_at = posição_após_última_frase_completa - offset[i]

Se detectou CAMADA 1 em clip i+1:
  skip_at = timestamp_após_marcador - offset[i]
```

### Passo 5 — Recodificação dos clips com cortes

Para cada clip, gerar segmento com os cortes aplicados:

```bash
# Clip sem corte:
ffmpeg -y -i "clip_N.mp4" \
  -c:v libx264 -preset fast -crf 22 \
  -c:a aac -b:a 192k \
  "sNN.mp4"

# Clip com trim no fim:
ffmpeg -y -i "clip_N.mp4" -t TRIM_AT \
  -c:v libx264 -preset fast -crf 22 \
  -c:a aac -b:a 192k \
  "sNN.mp4"

# Clip com skip no início:
ffmpeg -y -i "clip_N.mp4" -ss SKIP_AT \
  -c:v libx264 -preset fast -crf 22 \
  -c:a aac -b:a 192k \
  "sNN.mp4"
```

**Parâmetros de qualidade:** `-crf 22` (boa qualidade) + `-preset fast` (velocidade razoável). Nunca usar `-crf` acima de 28.

### Passo 6 — Concatenar final

```bash
# Gerar lista de segmentos
ffmpeg -y -f concat -safe 0 -i concat_list.txt \
  -c copy "ytNNN_FINAL.mp4"
```

### Passo 7 — Verificação pós-export

Rodar o verificador de camadas novamente contra o transcript para confirmar que nenhum padrão de alto risco está dentro da janela efetiva de cada emenda. Reportar tabela de timestamps para operador verificar manualmente no QuickTime.

## Output para operador

Após gerar o FINAL:

1. `open /Users/{{USERNAME_MAC}}/Desktop/yt-editados/ytNNN/` — abre Finder
2. Reportar tabela:

```
| Emenda | Timestamp no final | O que foi cortado |
|--------|-------------------|-------------------|
| Clip 1→2 | 3:44 | "Peraí, peraí que eu dei uma gaguejada" |
| Clip 4→5 | 6:54 | "Versailles..." (truncado) |
```

3. Pedir para operador conferir cada timestamp no QuickTime

## Aprendizados acumulados (atualizar a cada uso)

- **mlx-whisper é obrigatório** para Apple Silicon. `whisper medium` padrão leva 1h+ em 20min de áudio. mlx leva ~2min.
- **Whisper limpa disfluências** no texto mas o áudio original tem o gagueio — não confiar só no transcript para detectar stutters.
- **Sentenças truncadas em "..."** são sempre problemáticas — prioridade alta de corte.
- **"já já"** é filler natural do operador, não stutter. Não cortar.
- **Clips com pouca duração** (< 30s) geralmente são retomadas de clips anteriores — verificar início com atenção extra.
- **Verificação final obrigatória:** sempre rodar o checker de alto risco nos offsets efetivos pós-corte, não nos originais.
- **Output path:** nunca salvar no Google Drive (lento, pode corromper). Sempre `/Users/{{USERNAME_MAC}}/Desktop/yt-editados/`.
- **Padrões de retomada do operador:** "Peraí", "Ops, retomando então", "baixa retomando então", "vamos lá, retomando", "Então vamos lá, retomando."
- **Padrões de truncamento:** "é só você...", "dá uma olhada nos outros...", "Versailles...", "conta...", "e...", "aqui e..."

## Regra de margem de timestamp (10/06/2026)

Whisper word timestamps têm margem de erro de ~0.2-0.4s — o timestamp reportado pode estar atrasado em relação ao início real da pronúncia.

**Regra obrigatória ao definir início de seg2:**
```python
# NUNCA usar o timestamp bruto como corte
# SEMPRE anticicar 0.15s
seg2_start = word_start_whisper - 0.15  # captura o início real da palavra
```

Para palavras importantes (nome próprio, URL, número) no início do seg2: extrair 2s antes do timestamp e transcrever isolado para confirmar.

**Histórico:** yt175 re-editado 10/06/2026 — "{{NOME_OPERADOR}}" foi cortado para ".com" porque Whisper reportou start 0.4s atrasado.

## Histórico

- 29/05/2026: pipeline criado e validado em yt 175 (20 clips, 22min), yt 176 (8 clips, 20min), yt 177 (23 clips, 39min)
- Doc de referência: `segundo-cerebro/03-operacao/edicao-video-historico.md`

## QA Pós-Export (OBRIGATÓRIO após gerar o FINAL)

Após gerar o `*_FINAL.mp4`, rodar QA no próprio vídeo editado:

```bash
# 1. Extrair áudio do FINAL
ffmpeg -i "ytNNN_FINAL.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "final_audio.wav" -y

# 2. Transcrever o FINAL com mlx-whisper
mlx_whisper "final_audio.wav" --model mlx-community/whisper-medium-mlx \
  --language pt --output-format json --output-dir "./" --word-timestamps True

# 3. Ler transcrição em cada ponto de corte (±15s ao redor)
# Verificar: (a) sentença termina com pontuação, (b) próxima sentença continua coerentemente
# Flag "FIM SEM PONTUAÇÃO" pode ser FALSO POSITIVO se a sentença continua no próximo clip
```

**Regra de ouro do QA:** ler as últimas 2 linhas ANTES + primeiras 2 linhas DEPOIS de cada corte
como se fosse um único parágrafo. Se o texto fizer sentido semântico, a emenda está OK.

**Falsos positivos confirmados (30/05/2026):**
- Sentença que continua naturalmente entre clips (ex: "...na comunidade [corte] pra ajudar as pessoas")
- Artigo separado do substantivo (ex: "usa o [corte] chat GPT") — flui perfeitamente em áudio
- Continuação de lista (ex: "o Haiku não [corte] surgiram") — padrão normal de fala
- "faz uma... por exemplo, [corte] você manda fazer" — padrão de fala natural com trail-off

**Problemas reais (que devem ser fixados):**
- Frase explicitamente truncada: "Versailles...", "é só você...", "dá uma olhada nos outros..."
- Marcadores verbais: "Peraí, peraí que eu dei uma gaguejada", "Ops, retomando então"
- Sentença sem continuação possível no próximo clip (verifica o que vem depois)

## Trim do início (OBRIGATÓRIO)

Após gerar o FINAL, sempre cortar o início para remover respiração/silêncio antes da primeira fala:

```bash
# 1. Extrair primeiros 10s e transcrever com word_timestamps
ffmpeg -i "ytNNN_FINAL.mp4" -t 10 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/start.wav -y
mlx_whisper /tmp/start.wav --model mlx-community/whisper-medium-mlx \
  --language pt --output-format json --output-dir /tmp/ --word-timestamps True

# 2. Ler timestamp da primeira palavra
# primeiro_word_start = segments[0]['words'][0]['start']

# 3. Trim: começar 0.15s antes da primeira palavra
# ss = max(0, primeiro_word_start - 0.15)
ffmpeg -y -i "ytNNN_FINAL.mp4" -ss {ss} -c copy "ytNNN_FINAL.mp4"
```

**Regra:** nunca deixar o vídeo começar no frame 0 bruto — sempre tem respiração/silêncio antes da primeira fala.

## Regras de precisão de corte (aprendizados 05/06/2026)

### Silêncio em emendas entre takes (OBRIGATÓRIO verificar)

Quando dois segmentos de takes diferentes são emendados, o gap entre eles pode deixar uma pausa audível. Após gerar o FINAL, verificar via transcript:

```python
# Para cada ponto de emenda, checar o gap
for i in range(len(segments)-1):
    gap = segments[i+1]['start'] - segments[i]['end']
    if gap > 0.3:  # >300ms é audível
        print(f"GAP AUDÍVEL em {segments[i]['end']:.2f}s → {segments[i+1]['start']:.2f}s ({gap:.2f}s)")
```

Se gap > 0.3s na junção de takes diferentes: re-segmentar removendo o gap. Nunca deixar pausa orphan entre emendas.

### Fim do vídeo: sempre cortar antes de desligar a câmera

Após transcrição do FINAL, identificar o timestamp da última palavra e cortar 0.5s depois:

```python
ultimo_seg = segments[-1]
ultimo_word_end = ultimo_seg['words'][-1]['end']  # timestamp da última palavra
trim_end = ultimo_word_end + 0.5  # 0.5s de margem natural
# Re-encode: -t {trim_end}
```

**Regra:** vídeo NUNCA pode terminar com câmera desligando, silêncio longo ou ruído de encerramento. O fim é sempre 0.3-0.5s após a última palavra.

### Revisão de QA pós-emenda: 3 checks obrigatórios

1. **Gaps audíveis** — checar todos os pontos de corte para gap > 0.3s
2. **Fim limpo** — vídeo termina 0.3-0.5s após última palavra (sem câmera desligando)
3. **Início limpo** — vídeo começa 0.15s antes da primeira palavra (sem silêncio/respiração)

### CAMADA 5 — Repetição de frases (varredura no FINAL — obrigatório)

Após gerar o FINAL, varrer o transcript em busca de segmentos consecutivos com >70% de palavras em comum:

```python
for i in range(len(segments)-1):
    words1 = set(segments[i]['text'].strip().lower().split())
    words2 = set(segments[i+1]['text'].strip().lower().split())
    if not words1 or not words2:
        continue
    overlap = len(words1 & words2) / max(len(words1), len(words2))
    if overlap > 0.7:
        # REPETIÇÃO — remover a primeira instância, manter a segunda (tem continuação)
        # cut_end = segments[i]['start']  → keep até aqui
        # resume_at = segments[i+1]['start']  → retomar daqui
```

**Regra:** sempre remover a PRIMEIRA instância e manter a segunda — ela é a que tem continuação natural. Reconstruir o FINAL com ffmpeg (2 segmentos + concat). Rodar a varredura de novo para confirmar zero repetições.

**Histórico:** 05/06/2026 — `video_FINAL.mp4` passou pelo QA de emendas mas frase "Você pode ter o seu próprio aplicativo." apareceu 2x (overlap 86%). Causa: QA anterior verificava apenas gaps e pontuação, não identidade semântica entre segmentos consecutivos.

## REGRA DE OURO — QA sempre do vídeo FINAL editado (05/06/2026)

**O QA pós-export É FEITO SOBRE O ARQUIVO FINAL GERADO, não sobre o áudio concatenado dos clips originais.**

Fluxo obrigatório:
1. Gerar o `*_FINAL.mp4`
2. Extrair áudio DO FINAL: `ffmpeg -i ytNNN_FINAL.mp4 -vn ... final_audio.wav`
3. Transcrever o FINAL: `mlx_whisper final_audio.wav ...`
4. Rodar as 5 camadas sobre a transcrição do FINAL:
   - CAMADA 5: repetições de frases (>70% overlap entre segmentos consecutivos)
   - Retomadas remanescentes (peraí, ops, retomando, etc.)
   - Gaps audíveis > 0.3s nos pontos de corte
   - Fim limpo (0.3-0.5s após última palavra)
   - Início limpo (0.15s antes da primeira palavra)
5. Corrigir tudo que for encontrado
6. Re-transcrever e confirmar ZERO problemas
7. SÓ ENTÃO reportar o vídeo como pronto para o operador

**Nunca reportar como pronto sem ter passado por esse ciclo completo.**

## BUG CRÍTICO CORRIGIDO — gaps entre palavras (05/06/2026)

O checker de gaps anterior verificava apenas gaps ENTRE SEGMENTOS do Whisper. Bug: gaps grandes podem existir DENTRO de um mesmo segmento, entre palavras — especialmente nas emendas entre clips.

**Check correto — verificar gaps entre PALAVRAS, não entre segmentos:**

```python
# Extrair todas as palavras do transcript em ordem
all_words = []
for s in segments:
    for w in s.get('words', []):
        all_words.append(w)

# Verificar gaps entre palavras consecutivas
for i in range(len(all_words)-1):
    gap = all_words[i+1]['start'] - all_words[i]['end']
    if gap > 0.5:
        print(f"GAP {gap:.2f}s após '{all_words[i]['word']}' @ {all_words[i]['end']:.2f}s → '{all_words[i+1]['word']}' @ {all_words[i+1]['start']:.2f}s")
```

**Ação:** para cada gap > 0.5s detectado, avaliar se é pausa natural de fala (entre frases/seções) ou gap de emenda que precisa ser fechado. Gaps em pontos de corte entre clips são sempre candidatos a fechar.

**Histórico:** 05/06/2026 — yt175 tinha gap 2.76s na emenda Clip1→2 que passou pelo QA porque estava dentro do mesmo segmento Whisper. operador encontrou no min 1:37.
