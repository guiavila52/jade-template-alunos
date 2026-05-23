#!/usr/bin/env python3
"""
audit-claude-logs.py — Vetor R7 (observability) leve.

Processa transcripts JSONL nativos do Claude Code em
~/.claude/projects/{projeto}/*.jsonl e gera relatório markdown com:

- Bash commands (top 10, com timestamp, secret-masked)
- Edit/Write em paths sensíveis (.claude/, ~/.claude.json, mcp.json, .env*)
- MCP tool calls (qual MCP/qual tool, contagem)
- Hooks bloqueados (saídas "BLOQUEADO"/"BLOQUEIO"/"exit 2")
- WebFetch URLs (domínios)
- Erros e re-tentativas
- Anomalias: MCP fora da baseline, sensitive-path access, hook desabilitado,
  settings.json modificado, allow ampliado

Modos:
  --since 7d|30d   (default 7d)
  --session <id>   sessão específica
  --tail           apenas última sessão
  --anomalies-only só anomalias

Regra §16 — secrets mascarados (sk-*, AKIA*, ghp_*, github_pat_*, gho_*,
xoxb-*, eyJ JWT, hugo, bearer tokens etc).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

# ------------------------------------------------------------ paths

REPO = Path(__file__).resolve().parents[3]
PROJ_LOGS = Path.home() / ".claude" / "projects" / (
    "-Users-guiavila-Documents-Projetos-IA-Gui--vila-Squad-Empresa-Gui--vila"
)
OUT_DIR = REPO / "squad" / "output" / "seguranca"
BASELINE_PATH = OUT_DIR / "mcp-baseline.json"

# ------------------------------------------------------------ regex

SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{20,}"), "[REDACTED:sk]"),
    (re.compile(r"sk-sq-[A-Za-z0-9_\-]{10,}"), "[REDACTED:sk-sq]"),
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "[REDACTED:sk-ant]"),
    (re.compile(r"pk_[A-Za-z0-9_\-]{20,}"), "[REDACTED:pk]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED:aws-akid]"),
    (re.compile(r"ASIA[0-9A-Z]{16}"), "[REDACTED:aws-asid]"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "[REDACTED:ghp]"),
    (re.compile(r"gho_[A-Za-z0-9]{20,}"), "[REDACTED:gho]"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "[REDACTED:gh-pat]"),
    (re.compile(r"xox[abprs]-[A-Za-z0-9\-]{10,}"), "[REDACTED:slack]"),
    (re.compile(r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "[REDACTED:jwt]"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{30,}"), "[REDACTED:google]"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}"), "Bearer [REDACTED]"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*)['\"]?[A-Za-z0-9_\-\.]{20,}"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(api[_\-]?key\s*[:=]\s*)['\"]?[A-Za-z0-9_\-]{20,}"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(password\s*[:=]\s*)['\"]?[^'\"\s]{6,}"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(token\s*[:=]\s*)['\"]?[A-Za-z0-9_\-\.]{20,}"), r"\1[REDACTED]"),
]

SENSITIVE_PATH_PATTERNS = [
    re.compile(r"\.claude/(?:commands|agents|hooks)/"),
    re.compile(r"\.claude/settings(?:\.local)?\.json"),
    re.compile(r"~?/\.claude\.json"),
    re.compile(r"~?/\.claude/mcp\.json"),
    re.compile(r"\.env(?:\.local|\.example)?$"),
    re.compile(r"AGENTS\.md$"),
    re.compile(r"CLAUDE\.md$"),
]

HOOK_BLOCK_PATTERNS = [
    re.compile(r"BLOQUEAD[OA]", re.I),
    re.compile(r"BLOQUEIO", re.I),
    re.compile(r"hook (?:rejected|blocked|failed)", re.I),
    re.compile(r"PreToolUse:\w+ hook error", re.I),
    re.compile(r"exit code 2\b"),
]

# Padrões Bash suspeitos (RCE clássicos / supply chain / persistência)
SUSPICIOUS_BASH_PATTERNS = [
    # Restrito: curl/wget de URL http(s) imediatamente seguido de | bash/sh — sem outros comandos no meio
    (re.compile(r"\bcurl\s+(?:-[A-Za-z]\S*\s+)*(?:https?://)\S+\s*\|\s*(?:bash|sh|zsh)\b"), "curl-pipe-shell"),
    (re.compile(r"\bwget\s+(?:-[A-Za-z]\S*\s+)*(?:-[OqsS]\s+-\s+)?(?:https?://)\S+\s*\|\s*(?:bash|sh|zsh)\b"), "wget-pipe-shell"),
    (re.compile(r"chmod\s+\+x\s+\S+\s*(?:&&|;)\s*(?:\./|/tmp/|/var/tmp/)"), "chmod-then-exec"),
    (re.compile(r"\beval\s+\$\("), "eval-subshell"),
    (re.compile(r"\beval\s+[\"']?\$\{?[A-Z_]+"), "eval-envvar"),
    (re.compile(r"base64\s+(?:-d|--decode|-D)\b[^|]*\|\s*(?:bash|sh|zsh|python|perl)"), "base64-decode-exec"),
    (re.compile(r"echo\s+[A-Za-z0-9+/=]{40,}\s*\|\s*base64\s+(?:-d|--decode|-D)"), "base64-blob-decode"),
    (re.compile(r"nc\s+(?:-e|-c)\b"), "netcat-exec"),
    (re.compile(r"/dev/tcp/"), "bash-tcp-socket"),
    # Só alerta se há operação de escrita/modificação real (>, >>, tee, sed -i, rm)
    (re.compile(r"(?:>|>>|tee\s+|sed\s+-i|rm\s+|chmod\s+)\s*\"?~/\.claude\.json"), "write-claude-json"),
    (re.compile(r"(?:>|>>|tee\s+|sed\s+-i|rm\s+|chmod\s+)\s*\"?~/\.claude/mcp\.json"), "write-mcp-json"),
    # git --no-verify só conta se for git commit/push com a flag (não prosa)
    (re.compile(r"\bgit\s+(?:commit|push|merge|rebase)\b[^\n;|&]*--no-verify\b"), "git-no-verify"),
    (re.compile(r"\bgit\s+push\s+[^\n;|&]*(?:\s|=)(?:-f\b|--force\b)"), "git-force-push"),
    (re.compile(r"rm\s+-rf\s+(?:/|\$HOME|~)\s*$"), "rm-rf-home"),
]

# ------------------------------------------------------------ helpers

def mask_secrets(text: str) -> str:
    if not isinstance(text, str):
        return text
    for pat, repl in SECRET_PATTERNS:
        text = pat.sub(repl, text)
    return text


def parse_ts(ts: str | None):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def is_sensitive(path: str) -> bool:
    if not path:
        return False
    for pat in SENSITIVE_PATH_PATTERNS:
        if pat.search(path):
            return True
    return False


def load_baseline() -> dict:
    if BASELINE_PATH.exists():
        try:
            return json.loads(BASELINE_PATH.read_text())
        except Exception:
            pass
    return {"authorized_mcps": [], "authorized_hooks": [], "_note": "auto-seeded"}


def save_baseline(b: dict) -> None:
    BASELINE_PATH.write_text(json.dumps(b, indent=2, ensure_ascii=False))


# ------------------------------------------------------------ core parser

def iter_entries(jsonl_path: Path) -> Iterable[dict]:
    with jsonl_path.open() as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                d["_line"] = ln
                d["_file"] = jsonl_path.name
                yield d
            except json.JSONDecodeError:
                continue


def collect_sessions(
    since: timedelta | None,
    session_id: str | None,
    tail: bool,
) -> list[Path]:
    if not PROJ_LOGS.exists():
        return []
    files = sorted(PROJ_LOGS.glob("*.jsonl"), key=os.path.getmtime, reverse=True)
    if tail:
        return files[:1]
    if session_id:
        return [f for f in files if session_id in f.name]
    if since is None:
        return files
    cutoff = datetime.now(timezone.utc) - since
    keep: list[Path] = []
    for f in files:
        if datetime.fromtimestamp(os.path.getmtime(f), timezone.utc) >= cutoff:
            keep.append(f)
    return keep


def analyze(files: list[Path], baseline: dict) -> dict:
    stats = {
        "sessions": [],
        "total_entries": 0,
        "user_turns": 0,
        "assistant_turns": 0,
        "bash_commands": [],  # (ts, cmd_masked, session, line)
        "edits": [],          # (ts, tool, path, session, line)
        "mcp_calls": [],      # (ts, mcp_full_name, session, line)
        "webfetch": [],       # (ts, domain, session, line)
        "hook_blocks": [],    # (ts, snippet, session, line)
        "errors": [],         # (ts, snippet, session, line)
        "tool_use_count": Counter(),
        "anomalies": [],
        "time_range": (None, None),
        "subagents_dispatched": 0,
    }
    authorized = set(baseline.get("authorized_mcps", []))
    min_ts, max_ts = None, None

    for fp in files:
        sess = fp.stem
        stats["sessions"].append(sess)
        for d in iter_entries(fp):
            stats["total_entries"] += 1
            ts = parse_ts(d.get("timestamp"))
            if ts:
                if min_ts is None or ts < min_ts:
                    min_ts = ts
                if max_ts is None or ts > max_ts:
                    max_ts = ts
            typ = d.get("type")
            if typ == "user":
                stats["user_turns"] += 1
                # tool_result errors
                msg = d.get("message", {}) or {}
                content = msg.get("content") if isinstance(msg, dict) else None
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "tool_result":
                            if c.get("is_error"):
                                txt = c.get("content")
                                if isinstance(txt, list):
                                    txt = " ".join(
                                        x.get("text", "") for x in txt if isinstance(x, dict)
                                    )
                                snip = mask_secrets(str(txt))[:200]
                                stats["errors"].append((ts, snip, sess, d.get("_line")))
            elif typ == "assistant":
                stats["assistant_turns"] += 1
                msg = d.get("message", {}) or {}
                content = msg.get("content") if isinstance(msg, dict) else None
                if not isinstance(content, list):
                    continue
                for c in content:
                    if not (isinstance(c, dict) and c.get("type") == "tool_use"):
                        continue
                    name = c.get("name", "?")
                    stats["tool_use_count"][name] += 1
                    inp = c.get("input", {}) or {}
                    if name == "Bash":
                        raw_cmd = str(inp.get("command", ""))
                        cmd = mask_secrets(raw_cmd)[:300]
                        stats["bash_commands"].append((ts, cmd, sess, d.get("_line")))
                        # detectar padrões suspeitos (RCE/persistência/supply chain)
                        for pat, tag in SUSPICIOUS_BASH_PATTERNS:
                            if pat.search(raw_cmd):
                                stats["anomalies"].append({
                                    "kind": "suspicious_bash",
                                    "severity": "critical" if tag in (
                                        "curl-pipe-shell", "wget-pipe-shell",
                                        "base64-decode-exec", "eval-subshell",
                                        "netcat-exec", "bash-tcp-socket",
                                    ) else "warn",
                                    "pattern": tag,
                                    "ts": ts.isoformat() if ts else None,
                                    "cmd_snippet": cmd[:160],
                                    "session": sess,
                                    "line": d.get("_line"),
                                })
                    elif name in ("Edit", "Write", "NotebookEdit"):
                        path = str(inp.get("file_path", inp.get("notebook_path", "")))
                        stats["edits"].append((ts, name, path, sess, d.get("_line")))
                        if is_sensitive(path):
                            stats["anomalies"].append({
                                "kind": "sensitive_path_edit",
                                "severity": "warn",
                                "ts": ts.isoformat() if ts else None,
                                "tool": name,
                                "path": path,
                                "session": sess,
                                "line": d.get("_line"),
                            })
                    elif name == "WebFetch":
                        url = str(inp.get("url", ""))
                        m = re.match(r"https?://([^/]+)", url)
                        domain = m.group(1) if m else url[:60]
                        stats["webfetch"].append((ts, domain, sess, d.get("_line")))
                    elif name == "Agent" or name == "Task":
                        stats["subagents_dispatched"] += 1
                    elif name.startswith("mcp__"):
                        stats["mcp_calls"].append((ts, name, sess, d.get("_line")))
                        # baseline check: parse MCP server name (mcp__<server>__<tool>)
                        parts = name.split("__", 2)
                        server = parts[1] if len(parts) >= 2 else name
                        if authorized and server not in authorized:
                            stats["anomalies"].append({
                                "kind": "mcp_unknown",
                                "severity": "critical",
                                "ts": ts.isoformat() if ts else None,
                                "mcp_server": server,
                                "tool": name,
                                "session": sess,
                                "line": d.get("_line"),
                            })

            # check user tool_result outputs for hook-block patterns
            if typ == "user":
                msg = d.get("message", {}) or {}
                content = msg.get("content") if isinstance(msg, dict) else None
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "tool_result":
                            txt = c.get("content")
                            if isinstance(txt, list):
                                txt = " ".join(
                                    x.get("text", "") for x in txt if isinstance(x, dict)
                                )
                            if not isinstance(txt, str):
                                continue
                            for pat in HOOK_BLOCK_PATTERNS:
                                if pat.search(txt):
                                    snip = mask_secrets(txt)[:200].replace("\n", " ")
                                    stats["hook_blocks"].append(
                                        (ts, snip, sess, d.get("_line"))
                                    )
                                    break

    stats["time_range"] = (min_ts, max_ts)

    # Análise de volume Bash por dia + detecção de anomalia (>3x média)
    by_day: dict[str, int] = defaultdict(int)
    for ts, *_ in stats["bash_commands"]:
        if ts:
            by_day[ts.date().isoformat()] += 1
    stats["bash_per_day"] = dict(sorted(by_day.items()))
    if len(by_day) >= 3:
        avg = sum(by_day.values()) / len(by_day)
        for day, n in by_day.items():
            if avg > 0 and n > 3 * avg and n >= 50:
                stats["anomalies"].append({
                    "kind": "volume_spike_bash",
                    "severity": "warn",
                    "day": day,
                    "count": n,
                    "avg_period": round(avg, 1),
                    "ratio": round(n / avg, 2),
                })

    return stats


# ------------------------------------------------------------ report

def fmt_ts(ts) -> str:
    if not ts:
        return "(no-ts)"
    if isinstance(ts, str):
        return ts
    return ts.isoformat()


def build_report(stats: dict, args, files: list[Path]) -> str:
    out: list[str] = []
    today = datetime.now().strftime("%Y-%m-%d")
    mn, mx = stats["time_range"]
    out.append(f"# Audit Claude Logs — {today}")
    out.append("")
    out.append(f"_gerado por `workspace/scripts/seguranca/audit-claude-logs.py` em {datetime.now().isoformat(timespec='seconds')}_")
    out.append("")
    out.append("## Resumo executivo")
    out.append("")
    out.append(f"- **Sessões analisadas:** {len(stats['sessions'])}")
    out.append(f"- **Arquivos JSONL:** {len(files)}")
    out.append(f"- **Janela temporal:** {fmt_ts(mn)} → {fmt_ts(mx)}")
    out.append(f"- **Entradas totais:** {stats['total_entries']}")
    out.append(f"- **Turns user:** {stats['user_turns']}")
    out.append(f"- **Turns assistant:** {stats['assistant_turns']}")
    out.append(f"- **Bash commands:** {len(stats['bash_commands'])}")
    out.append(f"- **Edits/Writes:** {len(stats['edits'])}")
    out.append(f"- **MCP tool calls:** {len(stats['mcp_calls'])}")
    out.append(f"- **WebFetch:** {len(stats['webfetch'])}")
    out.append(f"- **Subagents despachados (Agent/Task):** {stats['subagents_dispatched']}")
    out.append(f"- **Hook-blocks detectados:** {len(stats['hook_blocks'])}")
    out.append(f"- **Erros (tool_result.is_error):** {len(stats['errors'])}")
    out.append(f"- **Anomalias:** {len(stats['anomalies'])}")
    out.append("")

    if args.anomalies_only:
        out.append("## Anomalias (modo --anomalies-only)")
        out.append("")
        if not stats["anomalies"]:
            out.append("_nenhuma anomalia detectada._")
        else:
            for a in stats["anomalies"]:
                out.append(f"- **[{a['severity'].upper()}]** {a['kind']} — {json.dumps({k:v for k,v in a.items() if k not in ('severity','kind')}, ensure_ascii=False)}")
        return "\n".join(out)

    # Anomalias
    out.append("## Anomalias")
    out.append("")
    if not stats["anomalies"]:
        out.append("_nenhuma anomalia detectada._")
    else:
        for a in stats["anomalies"][:50]:
            sev = a["severity"].upper()
            kind = a["kind"]
            extra = {k: v for k, v in a.items() if k not in ("severity", "kind")}
            out.append(f"- **[{sev}]** {kind} — `{a.get('session','')}:{a.get('line','')}` → {json.dumps(extra, ensure_ascii=False)}")
        if len(stats["anomalies"]) > 50:
            out.append(f"- _… mais {len(stats['anomalies'])-50} omitidas_")
    out.append("")

    # Volume Bash por dia
    out.append("## Volume Bash por dia")
    out.append("")
    bpd = stats.get("bash_per_day", {})
    if not bpd:
        out.append("_sem Bash commands no período._")
    else:
        out.append("| Dia | Bash calls |")
        out.append("|---|---|")
        for day, n in bpd.items():
            out.append(f"| {day} | {n} |")
    out.append("")

    # Top Bash
    out.append("## Top 10 Bash commands (por frequência)")
    out.append("")
    bash_counter = Counter(b[1].split()[0] if b[1] else "(empty)" for b in stats["bash_commands"])
    for cmd, n in bash_counter.most_common(10):
        out.append(f"- `{cmd}` — {n}x")
    out.append("")

    # Sensitive path access timeline
    out.append("## Sensitive-path access timeline")
    out.append("")
    sens = [e for e in stats["edits"] if is_sensitive(e[2])]
    if not sens:
        out.append("_sem acessos a paths sensíveis no período._")
    else:
        for ts, tool, path, sess, line in sens[:30]:
            out.append(f"- {fmt_ts(ts)} — **{tool}** `{path}` (`{sess}:{line}`)")
        if len(sens) > 30:
            out.append(f"- _… mais {len(sens)-30} omitidos_")
    out.append("")

    # MCP servers
    out.append("## MCPs invocados")
    out.append("")
    mcp_counter = Counter(m[1] for m in stats["mcp_calls"])
    if not mcp_counter:
        out.append("_nenhum MCP invocado no período._")
    else:
        for name, n in mcp_counter.most_common():
            out.append(f"- `{name}` — {n}x")
    out.append("")

    # WebFetch domains
    out.append("## WebFetch domains")
    out.append("")
    wf_counter = Counter(w[1] for w in stats["webfetch"])
    if not wf_counter:
        out.append("_nenhum WebFetch._")
    else:
        for dom, n in wf_counter.most_common(15):
            out.append(f"- `{dom}` — {n}x")
    out.append("")

    # Hook blocks
    out.append("## Hook-blocks detectados")
    out.append("")
    if not stats["hook_blocks"]:
        out.append("_nenhum hook bloqueou no período._")
    else:
        for ts, snip, sess, line in stats["hook_blocks"][:20]:
            out.append(f"- {fmt_ts(ts)} (`{sess}:{line}`) — {snip}")
        if len(stats["hook_blocks"]) > 20:
            out.append(f"- _… mais {len(stats['hook_blocks'])-20} omitidos_")
    out.append("")

    # Erros
    out.append("## Erros tool_result")
    out.append("")
    if not stats["errors"]:
        out.append("_sem erros tool_result.is_error._")
    else:
        for ts, snip, sess, line in stats["errors"][:20]:
            out.append(f"- {fmt_ts(ts)} (`{sess}:{line}`) — {snip}")
        if len(stats["errors"]) > 20:
            out.append(f"- _… mais {len(stats['errors'])-20} omitidos_")
    out.append("")

    # Tendência: comparar com relatório anterior
    out.append("## Tendência (comparação com relatório anterior)")
    out.append("")
    prev = find_previous_report(today)
    if prev:
        out.append(f"_relatório anterior: `{prev.name}`_")
        # parse só números do resumo
        try:
            prev_text = prev.read_text()
            for label in ["Bash commands", "MCP tool calls", "Anomalias", "Hook-blocks detectados"]:
                m = re.search(rf"\*\*{re.escape(label)}:\*\* (\d+)", prev_text)
                if m:
                    out.append(f"- {label}: anterior {m.group(1)} → atual (ver resumo executivo)")
        except Exception:
            pass
    else:
        out.append("_sem relatório anterior pra comparar (baseline desta semana)._")
    out.append("")

    out.append("---")
    out.append("")
    out.append("_Regra §16: secrets mascarados (sk-*, AKIA*, ghp_*, JWT, bearer etc) substituídos por `[REDACTED:*]`._")
    return "\n".join(out)


def find_previous_report(today: str) -> Path | None:
    candidates = sorted(
        OUT_DIR.glob("audit-claude-logs-*.md"),
        key=os.path.getmtime,
        reverse=True,
    )
    for c in candidates:
        if today not in c.name:
            return c
    return None


# ------------------------------------------------------------ baseline seeding

def maybe_seed_baseline(stats: dict, baseline: dict) -> dict:
    """Se baseline vazia, semeia com MCPs vistos historicamente."""
    if baseline.get("authorized_mcps"):
        return baseline
    seen = set()
    for _, name, _, _ in stats["mcp_calls"]:
        parts = name.split("__", 2)
        if len(parts) >= 2:
            seen.add(parts[1])
    baseline["authorized_mcps"] = sorted(seen)
    baseline["_seeded_at"] = datetime.now().isoformat()
    save_baseline(baseline)
    return baseline


# ------------------------------------------------------------ main

def parse_since(s: str) -> timedelta:
    s = s.strip().lower()
    m = re.match(r"^(\d+)([dhwm])$", s)
    if not m:
        raise ValueError(f"--since inválido: {s} (use ex 7d, 30d, 12h)")
    n, unit = int(m.group(1)), m.group(2)
    return {
        "h": timedelta(hours=n),
        "d": timedelta(days=n),
        "w": timedelta(weeks=n),
        "m": timedelta(days=30 * n),
    }[unit]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Audit Claude Code transcripts (R7 leve).")
    ap.add_argument("--since", default=None, help="Janela (ex 7d, 30d, 12h). Default 7d.")
    ap.add_argument("--days", type=int, default=None, help="Atalho: --days 7 == --since 7d.")
    ap.add_argument("--session", help="Apenas uma sessão específica (substring do filename).")
    ap.add_argument("--tail", action="store_true", help="Apenas última sessão.")
    ap.add_argument("--anomalies-only", action="store_true", help="Só anomalias.")
    ap.add_argument("--alerts-only", dest="anomalies_only", action="store_true",
                    help="Alias de --anomalies-only.")
    ap.add_argument("--out", "--output", dest="out",
                    help="Path do relatório (default auto em workspace/output/seguranca/).")
    ap.add_argument("--print", action="store_true", help="Imprime relatório no stdout além de salvar.")
    args = ap.parse_args(argv)

    # resolver --days vs --since
    if args.days is not None and args.since is not None:
        print("[audit-claude-logs] use --days OU --since, não ambos", file=sys.stderr)
        return 1
    if args.days is not None:
        args.since = f"{args.days}d"
    if args.since is None:
        args.since = "7d"

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    since_td: timedelta | None
    if args.session or args.tail:
        since_td = None
    else:
        since_td = parse_since(args.since)

    files = collect_sessions(since_td, args.session, args.tail)
    if not files:
        print(f"[audit-claude-logs] nenhum JSONL encontrado em {PROJ_LOGS}", file=sys.stderr)
        return 1

    baseline = load_baseline()
    stats = analyze(files, baseline)
    baseline = maybe_seed_baseline(stats, baseline)
    # Re-analyze after seeding so authorized_mcps takes effect (no false positives on 1st run)
    if "_seeded_at" in baseline:
        stats["anomalies"] = [a for a in stats["anomalies"] if a["kind"] != "mcp_unknown"]

    report = build_report(stats, args, files)

    today = datetime.now().strftime("%Y-%m-%d")
    suffix = ""
    if args.tail:
        suffix = "-tail"
    elif args.session:
        suffix = f"-sess-{args.session[:8]}"
    elif args.anomalies_only:
        suffix = "-anomalies"
    out_path = Path(args.out) if args.out else OUT_DIR / f"audit-claude-logs-{today}{suffix}.md"
    out_path.write_text(report)

    print(f"[audit-claude-logs] relatório salvo em: {out_path}")
    print(f"[audit-claude-logs] sessões={len(stats['sessions'])} bash={len(stats['bash_commands'])} mcp={len(stats['mcp_calls'])} edits={len(stats['edits'])} anomalies={len(stats['anomalies'])}")
    if args.print:
        print()
        print(report)

    # exit code: 0=ok, 1=warn (volume/sensitive), 2=critical (mcp novo, suspicious bash crítico)
    has_critical = any(a.get("severity") == "critical" for a in stats["anomalies"])
    has_warn = any(a.get("severity") == "warn" for a in stats["anomalies"])
    if has_critical:
        print("[audit-claude-logs] EXIT 2 — anomalia CRÍTICA detectada", file=sys.stderr)
        return 2
    if has_warn:
        print("[audit-claude-logs] EXIT 1 — anomalia WARN detectada", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
