#!/usr/bin/env python3
"""
transcrever-video pipeline executor.
Usage:
    python3 transcribe_video.py <URL_or_path> <repo_root> [--whisper]

Flags:
    --whisper   Força o uso do Whisper (slow path, alta qualidade) e PULA a
                limpeza Claude. Útil quando auto-sub não existe ou quando se
                quer áudio direto.
"""
import sys
import os
import re
import subprocess
import json
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ARGS = sys.argv[1:]
FORCE_WHISPER = "--whisper" in ARGS
ARGS = [a for a in ARGS if a != "--whisper"]
URL_OR_PATH = ARGS[0]
REPO_ROOT = Path(ARGS[1])
OUTPUT_DIR = REPO_ROOT / "workspace/output/transcricoes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CLEANUP_MODEL = "claude-haiku-4-5-20251001"
CLEANUP_BATCH_SIZE = 10
CLEANUP_MAX_WORKERS = 4
# Pricing (USD per 1M tokens) for claude-haiku-4-5 at time of writing.
HAIKU_INPUT_USD_PER_MTOK = 1.0
HAIKU_OUTPUT_USD_PER_MTOK = 5.0
HAIKU_CACHE_WRITE_USD_PER_MTOK = 1.25
HAIKU_CACHE_READ_USD_PER_MTOK = 0.10

CLEANUP_SYSTEM_PROMPT = (
    "Você corrige erros de reconhecimento automático de fala em transcrições do "
    "YouTube em português brasileiro.\n\n"
    "Regras invioláveis:\n"
    "1. NÃO reformule, NÃO resuma, NÃO mude o estilo. Mantenha exatamente o conteúdo "
    "e o jeito de falar do narrador.\n"
    "2. NÃO traduza. Se está em PT-BR, fica em PT-BR.\n"
    "3. Corrija APENAS:\n"
    "   - Termos técnicos mal reconhecidos: \"Cloud Code\"→\"Claude Code\", "
    "\"squats\"→\"squads\", \"anrópico\"→\"Anthropic\", \"open AI\"→\"OpenAI\", etc.\n"
    "   - Palavras com clara troca de letra: \"Turmar\"→\"Turma\", "
    "\"carroçel\"→\"carrossel\"\n"
    "   - Nomes próprios óbvios mal grafados (quando contexto permite identificar)\n"
    "   - Erros de concordância gramatical evidentes\n"
    "4. Mantenha marcações como [música], [risadas], \"tá vendo, ó\", \"né\", "
    "interjeições — são parte do estilo falado.\n"
    "5. NÃO adicione pontuação inventada. Mantenha a pontuação que tem.\n"
    "6. Preserve EXATAMENTE os timestamps no formato [mm:ss] ou [hh:mm:ss] no início "
    "de cada parágrafo.\n"
    "7. Preserve a numeração de parágrafos quando fornecida.\n\n"
    "Quando em dúvida, NÃO mude. Erro de não corrigir é menos grave que erro de "
    "mudar conteúdo."
)


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-")


def fmt_ts(seconds: float, force_h: bool = False) -> str:
    s = int(seconds)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h > 0 or force_h:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"


def parse_vtt(path: Path):
    """Parse VTT into deduped [(start_s, end_s, text)].

    YouTube auto-sub uses rolling captions: each cue contains the previous
    line plus a new line with inline timing tags. The strategy here:
    - For cues with inline timing tags <00:00:00.000>, only take the line(s)
      that contain those tags (the new content), not the repeated old line.
    - Strip the tags after extracting.
    """
    raw = path.read_text(encoding="utf-8", errors="replace")
    blocks = re.split(r"\n\n+", raw)
    cues = []
    ts_re = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
    )
    inline_ts_re = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")
    seen_lines = []  # last line of previous cue, to suppress repeats

    def clean(s: str) -> str:
        s = inline_ts_re.sub("", s)
        s = re.sub(r"</?c[^>]*>", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    for block in blocks:
        m = ts_re.search(block)
        if not m:
            continue
        sh, sm, ss, sms, eh, em, es, ems = [int(x) for x in m.groups()]
        start = sh * 3600 + sm * 60 + ss + sms / 1000.0
        end = eh * 3600 + em * 60 + es + ems / 1000.0
        lines = block.splitlines()
        ti = next(i for i, ln in enumerate(lines) if ts_re.search(ln))
        text_lines = [ln for ln in lines[ti + 1:] if ln.strip()]
        if not text_lines:
            continue
        # Prefer lines that contain inline timing tags (the "fresh" line in
        # rolling captions). If none has tags, take all lines.
        tagged = [ln for ln in text_lines if inline_ts_re.search(ln)]
        chosen = tagged if tagged else text_lines
        cleaned = [clean(ln) for ln in chosen]
        cleaned = [c for c in cleaned if c]
        if not cleaned:
            continue
        # Drop a leading line that exactly matches what we already emitted.
        if seen_lines and cleaned and cleaned[0] == seen_lines[-1]:
            cleaned = cleaned[1:]
        if not cleaned:
            continue
        text = " ".join(cleaned)
        # Skip pure noise like "[música]" alone? Keep it — could be useful.
        cues.append((start, end, text))
        seen_lines.append(cleaned[-1])
    return cues


def dedupe_cues(cues):
    """Already deduped in parse_vtt; pass through."""
    return cues


def cues_to_paragraphs(cues, min_seconds=30, max_seconds=60):
    """Group cues into paragraphs of roughly min..max seconds."""
    paragraphs = []
    if not cues:
        return paragraphs
    cur_start = cues[0][0]
    cur_end = cues[0][1]
    cur_texts = [cues[0][2]]
    for start, end, text in cues[1:]:
        dur = end - cur_start
        if dur >= min_seconds and (
            dur >= max_seconds or re.search(r"[.!?]\s*$", cur_texts[-1])
        ):
            paragraphs.append((cur_start, cur_end, " ".join(cur_texts)))
            cur_start = start
            cur_end = end
            cur_texts = [text]
        else:
            cur_end = end
            cur_texts.append(text)
    paragraphs.append((cur_start, cur_end, " ".join(cur_texts)))
    # final cleanup of paragraph text
    cleaned = []
    for s, e, t in paragraphs:
        t = re.sub(r"\s+", " ", t).strip()
        # collapse repeated adjacent words ("agora agora que vocês")
        t = re.sub(r"\b(\w+)( \1\b)+", r"\1", t, flags=re.IGNORECASE)
        cleaned.append((s, e, t))
    return cleaned


def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url


def get_youtube_meta(url: str):
    out = subprocess.check_output(
        ["yt-dlp", "--print", "%(title)s|%(duration)s|%(id)s", url],
        text=True,
    ).strip().splitlines()[-1]
    title, duration, vid = out.split("|", 2)
    return title, int(duration), vid


def download_auto_sub(url: str, vid: str):
    out_template = f"/tmp/transcribe-%(id)s.%(ext)s"
    # try once, ignore HTTP 429 on extra languages — we just need pt
    subprocess.run(
        [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang",
            "pt-orig,pt,pt-BR,en",
            "--sub-format",
            "vtt",
            "--skip-download",
            "-o",
            out_template,
            url,
        ],
        capture_output=True,
        text=True,
    )
    candidates = [
        Path(f"/tmp/transcribe-{vid}.pt.vtt"),
        Path(f"/tmp/transcribe-{vid}.pt-orig.vtt"),
        Path(f"/tmp/transcribe-{vid}.pt-BR.vtt"),
        Path(f"/tmp/transcribe-{vid}.en.vtt"),
    ]
    for p in candidates:
        if p.exists() and p.stat().st_size > 0:
            return p
    return None


def get_local_duration(path: str) -> int:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        text=True,
    ).strip()
    return int(float(out))


def whisper_transcribe(media_path: str, vid: str) -> Path:
    out_dir = "/tmp"
    subprocess.check_call(
        [
            "whisper",
            media_path,
            "--model",
            "medium",
            "--language",
            "pt",
            "--output_format",
            "vtt",
            "--output_dir",
            out_dir,
            "--verbose",
            "False",
        ]
    )
    base = Path(media_path).stem
    return Path(f"{out_dir}/{base}.vtt")


def download_audio(url: str, vid: str) -> Path:
    out = f"/tmp/audio-{vid}.%(ext)s"
    subprocess.check_call(
        ["yt-dlp", "-x", "--audio-format", "mp3", "-o", out, url]
    )
    return Path(f"/tmp/audio-{vid}.mp3")


def fmt_elapsed_human(elapsed: float) -> str:
    """Format elapsed seconds: '7.4s' < 60s, '2m 15s' < 1h, '1h 5m 30s' >= 1h."""
    if elapsed < 60:
        return f"{elapsed:.1f}s"
    total = int(round(elapsed))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h > 0:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"


def load_anthropic_api_key() -> tuple[str | None, str | None]:
    """Resolve ANTHROPIC_API_KEY. Returns (key, source) or (None, None)."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key, "env"
    candidates = [
        REPO_ROOT / ".env",
        REPO_ROOT / "app" / ".env.local",
        REPO_ROOT / "app" / ".env",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if line.startswith("ANTHROPIC_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val, str(path)
        except Exception:
            continue
    return None, None


def ensure_anthropic_sdk() -> bool:
    try:
        import anthropic  # noqa: F401
        return True
    except ImportError:
        pass
    # try to install
    for cmd in (
        [sys.executable, "-m", "pip", "install", "-q", "anthropic"],
        [sys.executable, "-m", "pip", "install", "--user", "--break-system-packages",
         "-q", "anthropic"],
    ):
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            try:
                import anthropic  # noqa: F401
                return True
            except ImportError:
                continue
        except Exception:
            continue
    return False


def _build_batch_user_message(batch: list[tuple[int, str, str]]) -> str:
    """batch: list of (idx, ts_str, text). Returns user message string."""
    lines = [
        "Corrija os parágrafos abaixo seguindo as regras. Devolva no MESMO "
        "formato, com a mesma numeração:\n"
    ]
    for idx, ts, text in batch:
        lines.append(f"#{idx} [{ts}] {text}")
    return "\n".join(lines)


def _parse_batch_response(text: str) -> dict[int, str]:
    """Parse Claude response into {idx: cleaned_text}. ts is dropped here —
    we re-attach the original ts when writing the final paragraph."""
    out: dict[int, str] = {}
    line_re = re.compile(r"^#(\d+)\s*(?:\[[^\]]+\])?\s*(.*)$")
    for raw in text.splitlines():
        ln = raw.strip()
        if not ln:
            continue
        m = line_re.match(ln)
        if not m:
            continue
        idx = int(m.group(1))
        body = m.group(2).strip()
        out[idx] = body
    return out


def _call_cleanup_batch(client, batch: list[tuple[int, str, str]]):
    """Call Claude on a batch. Returns (mapping, usage_dict)."""
    user_msg = _build_batch_user_message(batch)
    resp = client.messages.create(
        model=CLEANUP_MODEL,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": CLEANUP_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    mapping = _parse_batch_response(text)
    usage = {
        "input_tokens": getattr(resp.usage, "input_tokens", 0) or 0,
        "output_tokens": getattr(resp.usage, "output_tokens", 0) or 0,
        "cache_creation_input_tokens": getattr(
            resp.usage, "cache_creation_input_tokens", 0
        ) or 0,
        "cache_read_input_tokens": getattr(
            resp.usage, "cache_read_input_tokens", 0
        ) or 0,
    }
    return mapping, usage


def cleanup_paragraphs_with_claude(paragraphs, api_key: str, use_h: bool):
    """Run cleanup over paragraphs in batches. Returns (cleaned_paragraphs,
    elapsed_seconds, usage_totals, n_batches, n_failed_batches)."""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    # Build numbered batches keyed by original paragraph index.
    indexed = []
    for i, (s, e, t) in enumerate(paragraphs):
        ts_str = fmt_ts(s, force_h=use_h)
        indexed.append((i, ts_str, t))

    batches: list[list[tuple[int, str, str]]] = []
    for i in range(0, len(indexed), CLEANUP_BATCH_SIZE):
        batches.append(indexed[i : i + CLEANUP_BATCH_SIZE])

    cleaned_map: dict[int, str] = {}
    failed_batches = 0
    usage_total = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }

    t0 = time.monotonic()
    with ThreadPoolExecutor(max_workers=CLEANUP_MAX_WORKERS) as pool:
        futures = [pool.submit(_call_cleanup_batch, client, b) for b in batches]
        for fut, batch in zip(futures, batches):
            try:
                mapping, usage = fut.result()
                # If the parser failed to recover any entry for this batch, treat
                # the whole batch as failed (fall back to originals).
                if not mapping:
                    failed_batches += 1
                    print(
                        f"⚠️  Limpeza Claude: batch sem matches, mantendo originais "
                        f"({len(batch)} parágrafos).",
                        file=sys.stderr,
                    )
                else:
                    for idx, _, _ in batch:
                        if idx in mapping and mapping[idx]:
                            cleaned_map[idx] = mapping[idx]
                    missing = [idx for idx, _, _ in batch if idx not in cleaned_map]
                    if missing:
                        print(
                            f"⚠️  Limpeza Claude: {len(missing)} parágrafos sem match "
                            f"no batch, mantendo originais.",
                            file=sys.stderr,
                        )
                for k in usage_total:
                    usage_total[k] += usage.get(k, 0)
            except Exception as exc:  # noqa: BLE001
                failed_batches += 1
                print(
                    f"⚠️  Limpeza Claude: batch falhou ({exc!r}), mantendo "
                    f"{len(batch)} parágrafos originais.",
                    file=sys.stderr,
                )
    elapsed = time.monotonic() - t0

    cleaned_paragraphs = []
    for i, (s, e, t) in enumerate(paragraphs):
        new_t = cleaned_map.get(i, t)
        cleaned_paragraphs.append((s, e, new_t))

    return cleaned_paragraphs, elapsed, usage_total, len(batches), failed_batches


def estimate_cost_usd(usage: dict) -> float:
    inp = usage.get("input_tokens", 0)
    out = usage.get("output_tokens", 0)
    cw = usage.get("cache_creation_input_tokens", 0)
    cr = usage.get("cache_read_input_tokens", 0)
    cost = (
        (inp / 1_000_000) * HAIKU_INPUT_USD_PER_MTOK
        + (out / 1_000_000) * HAIKU_OUTPUT_USD_PER_MTOK
        + (cw / 1_000_000) * HAIKU_CACHE_WRITE_USD_PER_MTOK
        + (cr / 1_000_000) * HAIKU_CACHE_READ_USD_PER_MTOK
    )
    return cost


def main():
    start_time = time.monotonic()
    method = None
    title = None
    duration_s = None
    fonte = URL_OR_PATH
    vtt_path = None

    if is_youtube(URL_OR_PATH):
        title, duration_s, vid = get_youtube_meta(URL_OR_PATH)
        if FORCE_WHISPER:
            # forced whisper path: skip auto-sub entirely
            if not subprocess.run(["which", "whisper"], capture_output=True).stdout.strip():
                print("ERRO: whisper não está instalado. Rode: pip install -U openai-whisper")
                sys.exit(2)
            audio = download_audio(URL_OR_PATH, vid)
            vtt_path = whisper_transcribe(str(audio), vid)
            method = "whisper-medium"
        else:
            # fast path
            vtt_path = download_auto_sub(URL_OR_PATH, vid)
            if vtt_path:
                method = "youtube-auto-sub"
            else:
                # whisper fallback
                if not subprocess.run(["which", "whisper"], capture_output=True).stdout.strip():
                    print("ERRO: whisper não está instalado. Rode: pip install -U openai-whisper")
                    sys.exit(2)
                audio = download_audio(URL_OR_PATH, vid)
                vtt_path = whisper_transcribe(str(audio), vid)
                method = "whisper-medium"
    else:
        local = Path(URL_OR_PATH).expanduser().resolve()
        if not local.exists():
            print(f"ERRO: arquivo não encontrado: {local}")
            sys.exit(2)
        title = local.stem
        duration_s = get_local_duration(str(local))
        if not subprocess.run(["which", "whisper"], capture_output=True).stdout.strip():
            print("ERRO: whisper não está instalado.")
            sys.exit(2)
        vtt_path = whisper_transcribe(str(local), title)
        method = "whisper-medium"

    cues = parse_vtt(vtt_path)
    cues = dedupe_cues(cues)
    paragraphs = cues_to_paragraphs(cues)

    use_h = duration_s >= 3600

    # ---- Cleanup via Claude (auto-sub only, unless --whisper) ----
    cleanup_applied = False
    cleanup_skip_reason = None
    cleanup_elapsed = 0.0
    cleanup_usage = None
    cleanup_cost_usd = 0.0
    cleanup_batches = 0
    cleanup_failed_batches = 0

    transcription_only_elapsed = time.monotonic() - start_time

    should_clean = (method == "youtube-auto-sub") and not FORCE_WHISPER and bool(paragraphs)
    if FORCE_WHISPER:
        cleanup_skip_reason = "flag --whisper desabilita limpeza Claude (Whisper já é alta qualidade)"
    elif method != "youtube-auto-sub":
        cleanup_skip_reason = f"método {method} não precisa de limpeza Claude"

    if should_clean:
        api_key, key_source = load_anthropic_api_key()
        if not api_key:
            cleanup_skip_reason = (
                "ANTHROPIC_API_KEY não encontrada (env, .env, app/.env.local). "
                "Defina a key e re-rode."
            )
            print(f"⚠️  Limpeza Claude pulada — {cleanup_skip_reason}", file=sys.stderr)
        elif not ensure_anthropic_sdk():
            cleanup_skip_reason = (
                "SDK anthropic não instalado e instalação automática falhou. "
                "Rode: pip install anthropic"
            )
            print(f"⚠️  Limpeza Claude pulada — {cleanup_skip_reason}", file=sys.stderr)
        else:
            print(
                f"→ Aplicando limpeza Claude ({CLEANUP_MODEL}) sobre "
                f"{len(paragraphs)} parágrafos (key: {key_source})...",
                file=sys.stderr,
            )
            try:
                paragraphs, cleanup_elapsed, cleanup_usage, cleanup_batches, cleanup_failed_batches = (
                    cleanup_paragraphs_with_claude(paragraphs, api_key, use_h)
                )
                cleanup_applied = True
                cleanup_cost_usd = estimate_cost_usd(cleanup_usage)
            except Exception as exc:  # noqa: BLE001
                cleanup_skip_reason = f"erro inesperado na limpeza Claude: {exc!r}"
                print(f"⚠️  {cleanup_skip_reason}", file=sys.stderr)

    last_ts = paragraphs[-1][1] if paragraphs else 0
    diff = duration_s - last_ts
    tolerance = max(15, 0.02 * duration_s)
    ok = diff <= tolerance

    slug = slugify(title)
    today = date.today().isoformat()
    out_path = OUTPUT_DIR / f"{today}-{slug}.md"
    if not ok:
        out_path = OUTPUT_DIR / f"{today}-{slug}-INCOMPLETA.md"

    elapsed = time.monotonic() - start_time
    elapsed_human = fmt_elapsed_human(elapsed)
    transcription_only_human = fmt_elapsed_human(transcription_only_elapsed)
    cleanup_human = fmt_elapsed_human(cleanup_elapsed) if cleanup_applied else None

    fm_lines = [
        "---",
        f"fonte: {fonte}",
        f"titulo: {title}",
        f"duracao: {fmt_ts(duration_s, force_h=True)}",
        f"duracao_segundos: {duration_s}",
        f"metodo: {method}",
        f"tempo_execucao_segundos: {elapsed:.1f}",
        f"tempo_execucao_humano: {elapsed_human}",
        f"limpeza_claude: {'true' if cleanup_applied else 'false'}",
    ]
    if cleanup_applied:
        fm_lines.append(f"modelo_limpeza: {CLEANUP_MODEL}")
        fm_lines.append(f"tempo_limpeza_segundos: {cleanup_elapsed:.1f}")
    fm_lines.append(f"data_transcricao: {today}")
    fm_lines.append("---\n")
    fm = "\n".join(fm_lines) + "\n"

    body_lines = [f"# {title}\n"]
    for s, e, t in paragraphs:
        ts = fmt_ts(s, force_h=use_h)
        body_lines.append(f"[{ts}] {t}\n")
    last_human = fmt_ts(last_ts, force_h=use_h)
    total_human = fmt_ts(duration_s, force_h=use_h)

    if ok:
        if cleanup_applied:
            footer = (
                f"\n_Transcrição completa — último timestamp [{last_human}], "
                f"duração total [{total_human}], diff {int(diff)}s "
                f"(dentro da tolerância de {int(tolerance)}s). "
                f"Tempo de execução: {elapsed_human} "
                f"(auto-sub {transcription_only_human} + limpeza Claude {cleanup_human})._\n"
            )
        else:
            footer = (
                f"\n_Transcrição completa — último timestamp [{last_human}], "
                f"duração total [{total_human}], diff {int(diff)}s "
                f"(dentro da tolerância de {int(tolerance)}s). "
                f"Tempo de execução: {elapsed_human}._"
            )
            if cleanup_skip_reason:
                footer += f" ⚠️ Limpeza Claude não aplicada ({cleanup_skip_reason})._\n"
            else:
                footer += "\n"
        body_lines.append(footer)
    else:
        body_lines.append(
            f"\n_⚠️ Transcrição INCOMPLETA — último timestamp [{last_human}], "
            f"duração total [{total_human}], diff {int(diff)}s "
            f"(tolerância {int(tolerance)}s). "
            f"Tempo de execução: {elapsed_human}._\n"
        )

    out_path.write_text(fm + "\n".join(body_lines), encoding="utf-8")

    result = {
        "ok": ok,
        "method": method,
        "title": title,
        "duration_s": duration_s,
        "last_ts_s": last_ts,
        "diff_s": diff,
        "tolerance_s": tolerance,
        "output_path": str(out_path),
        "paragraphs": len(paragraphs),
        "elapsed_s": round(elapsed, 1),
        "elapsed_human": elapsed_human,
        "cleanup": {
            "applied": cleanup_applied,
            "model": CLEANUP_MODEL if cleanup_applied else None,
            "elapsed_s": round(cleanup_elapsed, 1) if cleanup_applied else 0,
            "batches": cleanup_batches,
            "failed_batches": cleanup_failed_batches,
            "usage": cleanup_usage,
            "cost_usd": round(cleanup_cost_usd, 6) if cleanup_applied else 0,
            "skip_reason": cleanup_skip_reason,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
