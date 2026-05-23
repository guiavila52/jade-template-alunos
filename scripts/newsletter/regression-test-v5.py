#!/usr/bin/env python3
"""
Regression test — Newsletter HTML rendering vs v5 canonical baseline.

Roda renderizar-html.py com cadc4df0-config.json e compara byte-a-byte
contra o HTML da v5 aprovada pelo Gui em 13/05/2026.

Falha = bug ou mudança intencional não aprovada. Em caso de mudança
intencional: aprovar nova versão (v6+) e atualizar baseline path.

Uso:
    python3 scripts/newsletter/regression-test-v5.py

Exit codes:
    0 — diff zero (template íntegro)
    1 — diff detectado (REGRESSÃO ou mudança não aprovada)
    2 — erro de execução
"""

import subprocess
import sys
import tempfile
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_RENDER = ROOT / "scripts" / "newsletter" / "renderizar-html.py"
CONFIG_V5 = ROOT / "squad-fisico" / "output" / "newsletter" / "cadc4df0-config.json"
BASELINE_V5 = ROOT / "squad-fisico" / "output" / "newsletter" / "2026-05-13-cadc4df0-v5.html"

def main():
    # Sanidade
    for f in [SCRIPT_RENDER, CONFIG_V5, BASELINE_V5]:
        if not f.exists():
            print(f"ERRO: arquivo ausente: {f}", file=sys.stderr)
            sys.exit(2)

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        proc = subprocess.run(
            ["python3", str(SCRIPT_RENDER),
             "--input", str(CONFIG_V5),
             "--output", str(tmp_path)],
            capture_output=True, text=True, timeout=30
        )
        if proc.returncode != 0:
            print(f"ERRO: renderizar-html.py falhou (exit {proc.returncode})", file=sys.stderr)
            print(proc.stderr, file=sys.stderr)
            sys.exit(2)

        baseline = BASELINE_V5.read_text(encoding="utf-8")
        rendered = tmp_path.read_text(encoding="utf-8")

        if baseline == rendered:
            print("OK — Newsletter v5 regression PASS (diff zero, template canônico íntegro)")
            sys.exit(0)
        else:
            print("FALHA — Diff detectado vs v5 baseline:", file=sys.stderr)
            diff = difflib.unified_diff(
                baseline.splitlines(keepends=True),
                rendered.splitlines(keepends=True),
                fromfile=str(BASELINE_V5),
                tofile="rerender (atual)",
                n=3,
            )
            sys.stderr.writelines(diff)
            sys.exit(1)
    finally:
        tmp_path.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
