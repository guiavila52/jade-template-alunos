---
name: cortar-youtube
description: Corta primeiro minuto de video YouTube, converte pra 9:16 vertical (1080x1920) e adiciona gancho de texto nos ultimos 5s.
type: skill
---

<!-- Modelo recomendado: claude-sonnet-4-5 -->

# /cortar-youtube — Vídeo YouTube → Reel vertical 9:16 com gancho

Skill canônica do squad-midia. Pega URL YouTube, extrai primeiro minuto (ou duração custom), converte pra 9:16 vertical (1080×1920) e adiciona gancho de texto nos últimos ~5s. Output em `workspace/output/videos-verticais/`.

Disparo: pega URL do {{NOME_OPERADOR_CURTO}}, escolhe defaults se {{NOME_OPERADOR_CURTO}} não passou parâmetros, executa, abre o resultado.

## Parâmetros

| Parâmetro | Default | Descrição |
|---|---|---|
| `--url` | (obrigatório) | URL completa do YouTube |
| `--duracao` | `60` | Segundos a cortar do início |
| `--gancho-texto` | `"Curtiu? Vídeo completo no YouTube — link na bio"` | Texto overlay últimos 5s |
| `--output-name` | timestamp | Nome do arquivo final (sem extensão) |

## Dependências do sistema

- `yt-dlp` → `brew install yt-dlp`
- `ffmpeg` + `ffprobe` → `brew install ffmpeg`

Skill valida instalação antes de processar (Regra #22 confiabilidade).

## Fluxo

```
URL YouTube
    ↓
[1] check_dependencies (yt-dlp, ffmpeg, ffprobe)
    ↓
[2] download_video — primeiro minuto via --download-sections (retry 2x, timeout 300s)
    ↓
[3] crop_to_vertical — ffmpeg filter_complex:
    - crop centrado horizontal (de 16:9/4:3 → 9:16)
    - scale 1080×1920
    - drawtext últimos ~5s (gancho)
    ↓
[4] validate_output — dimensões + duração via ffprobe
    ↓
[5] open no QuickTime (macOS)
    ↓
workspace/output/videos-verticais/{nome|timestamp}.mp4
```

## Confiabilidade (Regra #22)

- Timeout 300s no download + 300s no ffmpeg
- Retry 2x no yt-dlp (vídeos longos podem falhar primeira tentativa)
- Stderr capturado e printado em falhas
- Exit code propagado
- Cleanup temp files no `finally` (mesmo se crashar)
- Validação dimensões pós-encoding (warn se ≠ 1080×1920)

## Como invocar

```bash
python3 "scripts/video/cortar-youtube.py" \
  --url "https://www.youtube.com/watch?v=ID" \
  --duracao 60 \
  --gancho-texto "Aprenda squad de IA — {{DOMINIO}}/youtube"
```

Output:
```
🔽 Baixando primeiros 60s do vídeo...
✅ Download concluído: downloaded.mp4
🎬 Processando vídeo (crop vertical + gancho)...
✅ Vídeo processado: workspace/output/videos-verticais/vertical-2026-05-13-1015.mp4
📐 Dimensões: 1080x1920
⏱️ Duração: 60.0s
🎉 Concluído: workspace/output/videos-verticais/vertical-2026-05-13-1015.mp4
```

## Casos de uso

1. **Repurpose Reel/Shorts/TikTok** — pega vídeo YouTube longo, gera versão vertical com gancho
2. **Teaser pra Instagram** — primeiro minuto como gancho pra ver completo no YouTube
3. **Variações múltiplas** — rodar várias vezes com `--gancho-texto` diferente

## Limitações conhecidas

- Crop sempre **centrado horizontal** — se conteúdo importante está nas laterais, vai cortar
- Drawtext usa Helvetica do sistema macOS — em Linux requer ajuste de fontfile
- Não baixa vídeos com paywall/region-lock (yt-dlp limit)
- Gancho fixo nos últimos ~5s assumindo 30fps — vídeos 60fps mudam um pouco

## Output canônico

`workspace/output/videos-verticais/{nome|YYYY-MM-DD-HHMMSS}.mp4`

## Cross-reference

- Script: [scripts/video/cortar-youtube.py](../../scripts/video/cortar-youtube.py)
- Task ClickUp: `{{CLICKUP_TASK_EXEMPLO}}` — tag `{{TAG_EXEMPLO}}`
- Regra #22 confiabilidade — timeout/stderr/exit code

---

## Aprendizado + pendência (Regras §1 §5)

- Antes de executar trabalho estrutural, registrar pendência no ClickUp via `/criar-pendencia`
- Ao concluir, comentar via `/comentar-pendencia` e fechar via `/fechar-pendencia`
- Aprendizado real (correção do {{NOME_OPERADOR_CURTO}}, padrão descoberto) → registrar em `squads/{squad}/agentes/{agente}/aprendizados.md` (Regra §5)
- Reincidência = falha de processo, escalar imediatamente