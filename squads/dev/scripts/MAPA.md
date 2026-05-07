# MAPA — squads/dev/scripts/

**Propósito:** scripts utilitários do squad-dev usados por skills. Reutilizáveis, idempotentes, sem efeitos colaterais fora dos paths de output declarados.

## Arquivos

| Arquivo | Skill que usa | O que faz |
|---------|---------------|-----------|
| `transcribe_video.py` | `/transcrever-video` | Pipeline completo: detecta fonte (YouTube ou arquivo), tenta auto-sub do YouTube, faz fallback Whisper, parseia VTT lidando com rolling captions, agrupa em parágrafos de 30-60s com timestamps, salva em `squad/output/transcricoes/`, verifica completude (diff ≤ max(15s, 2%) da duração) com 1 retry automático. |

**Uso:**
```bash
python3 squads/dev/scripts/transcribe_video.py "URL_OU_PATH" "$(pwd)"
```

**Última atualização:** 2026-05-06 — pasta criada com `transcribe_video.py` (skill `/transcrever-video`).
