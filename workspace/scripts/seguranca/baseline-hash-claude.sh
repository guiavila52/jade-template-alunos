#!/usr/bin/env bash
# baseline-hash-claude.sh
# Item 0.2 — Fase 0 Hardening Segurança (Regra §16, vetor R1)
# Fecha vetor: Mini Shai-Hulud worm (TeamPCP) + CVE-2025-59536
# Pendência mãe: ClickUp 86ahha462
#
# Modos:
#   init   — gera baseline de hashes dos arquivos críticos Claude
#   check  — recalcula e compara com baseline. exit 1 se divergente.
#
set -uo pipefail

PROJECT_ROOT="/Users/guiavila/Documents/Projetos IA Gui Ávila/Squad Empresa Gui Ávila"
BASELINE_JSON="$PROJECT_ROOT/workspace/output/seguranca/baseline-hashes.json"
LAST_STATUS="$PROJECT_ROOT/workspace/output/seguranca/last-check-status.txt"
LOG_FILE="$PROJECT_ROOT/workspace/output/seguranca/hash-check.log"

MODE="${1:-}"

if [[ "$MODE" != "init" && "$MODE" != "check" ]]; then
  echo "Uso: $0 {init|check}" >&2
  exit 2
fi

# ---- coleta lista de arquivos críticos ----
collect_files() {
  local files=()

  # Arquivos pontuais (só existem alguns)
  for f in "$HOME/.claude.json" "$HOME/.claude/mcp.json" "$HOME/.claude/settings.json" \
           "$PROJECT_ROOT/.claude/settings.json" "$PROJECT_ROOT/.claude/settings.local.json"; do
    [[ -f "$f" ]] && files+=("$f")
  done

  # Hooks project
  if [[ -d "$PROJECT_ROOT/.claude/hooks" ]]; then
    while IFS= read -r -d '' f; do files+=("$f"); done < <(find "$PROJECT_ROOT/.claude/hooks" -maxdepth 1 -type f -name '*.sh' -print0)
  fi

  # Commands project
  if [[ -d "$PROJECT_ROOT/.claude/commands" ]]; then
    while IFS= read -r -d '' f; do files+=("$f"); done < <(find "$PROJECT_ROOT/.claude/commands" -maxdepth 1 -type f -name '*.md' -print0)
  fi

  # Agents project
  if [[ -d "$PROJECT_ROOT/.claude/agents" ]]; then
    while IFS= read -r -d '' f; do files+=("$f"); done < <(find "$PROJECT_ROOT/.claude/agents" -type f -name '*.md' -print0)
  fi

  # Hooks global
  if [[ -d "$HOME/.claude/hooks" ]]; then
    while IFS= read -r -d '' f; do files+=("$f"); done < <(find "$HOME/.claude/hooks" -maxdepth 1 -type f -name '*.sh' -print0)
  fi

  printf '%s\n' "${files[@]}"
}

# ---- calcula sha256 (macOS) ----
sha256_of() {
  shasum -a 256 "$1" 2>/dev/null | awk '{print $1}'
}

size_of() {
  stat -f '%z' "$1" 2>/dev/null
}

mtime_iso() {
  # macOS stat → epoch → ISO8601 UTC
  local epoch
  epoch=$(stat -f '%m' "$1" 2>/dev/null)
  [[ -z "$epoch" ]] && { echo ""; return; }
  date -u -r "$epoch" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null
}

now_iso() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# ---- build JSON via python3 (dependência mínima) ----
build_json() {
  local mode_label="$1"
  python3 - "$mode_label" <<'PYEOF'
import json, sys, os, subprocess, hashlib

mode_label = sys.argv[1]

# Reproduz collect_files em Python pra evitar parsing frágil de bash array
PROJECT_ROOT = "/Users/guiavila/Documents/Projetos IA Gui Ávila/Squad Empresa Gui Ávila"
HOME = os.path.expanduser("~")

candidates = [
    f"{HOME}/.claude.json",
    f"{HOME}/.claude/mcp.json",
    f"{HOME}/.claude/settings.json",
    f"{PROJECT_ROOT}/.claude/settings.json",
    f"{PROJECT_ROOT}/.claude/settings.local.json",
]

def add_glob(base, pattern, recursive=False):
    if not os.path.isdir(base):
        return []
    found = []
    if recursive:
        for root, _, files in os.walk(base):
            for fn in files:
                if pattern == "*.md" and fn.endswith(".md"):
                    found.append(os.path.join(root, fn))
                elif pattern == "*.sh" and fn.endswith(".sh"):
                    found.append(os.path.join(root, fn))
    else:
        for fn in os.listdir(base):
            full = os.path.join(base, fn)
            if not os.path.isfile(full): continue
            if pattern == "*.sh" and fn.endswith(".sh"): found.append(full)
            elif pattern == "*.md" and fn.endswith(".md"): found.append(full)
    return found

candidates += add_glob(f"{PROJECT_ROOT}/.claude/hooks", "*.sh")
candidates += add_glob(f"{PROJECT_ROOT}/.claude/commands", "*.md")
candidates += add_glob(f"{PROJECT_ROOT}/.claude/agents", "*.md", recursive=True)
candidates += add_glob(f"{HOME}/.claude/hooks", "*.sh")

import datetime
def iso(epoch):
    return datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

files = {}
for f in sorted(set(candidates)):
    if not os.path.isfile(f): continue
    try:
        with open(f, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        st = os.stat(f)
        files[f] = {"sha256": h, "size_bytes": st.st_size, "mtime": iso(st.st_mtime)}
    except Exception as e:
        files[f] = {"error": str(e)}

out = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "generated_by": f"baseline-hash-claude.sh {mode_label}",
    "files": files,
}
print(json.dumps(out, indent=2, ensure_ascii=False))
PYEOF
}

mkdir -p "$(dirname "$BASELINE_JSON")"

if [[ "$MODE" == "init" ]]; then
  build_json "init" > "$BASELINE_JSON"
  N=$(python3 -c "import json; print(len(json.load(open('$BASELINE_JSON'))['files']))")
  echo "$(now_iso) [init] baseline gerado: $N arquivos → $BASELINE_JSON" >> "$LOG_FILE"
  echo "0" > "$LAST_STATUS"
  echo "baseline-hash-claude: baseline gerado com $N arquivos."
  echo "Path: $BASELINE_JSON"
  exit 0
fi

# MODE == check
if [[ ! -f "$BASELINE_JSON" ]]; then
  echo "baseline-hash-claude: baseline não existe. Rode '$0 init' primeiro." >&2
  echo "$(now_iso) [check] ABORTADO — baseline ausente" >> "$LOG_FILE"
  echo "1" > "$LAST_STATUS"
  exit 2
fi

CURRENT_JSON=$(build_json "check")

# Compara via python3 — gera diff estruturado
DIFF_REPORT=$(python3 - "$BASELINE_JSON" <<PYEOF
import json, sys
baseline = json.load(open(sys.argv[1]))
current = json.loads("""$CURRENT_JSON""")

bf = baseline["files"]
cf = current["files"]

modified = []
added = []
removed = []

for path, meta in cf.items():
    if path not in bf:
        added.append((path, meta))
        continue
    if "sha256" in meta and "sha256" in bf[path]:
        if meta["sha256"] != bf[path]["sha256"]:
            modified.append((path, bf[path], meta))

for path, meta in bf.items():
    if path not in cf:
        removed.append((path, meta))

total_diff = len(modified) + len(added) + len(removed)

if total_diff == 0:
    print("OK")
else:
    print(f"DIFF:{len(modified)}:{len(added)}:{len(removed)}")
    for path, old, new in modified:
        print(f"MOD\t{path}\t{old.get('sha256','?')}\t{old.get('size_bytes','?')}\t{old.get('mtime','?')}\t{new.get('sha256','?')}\t{new.get('size_bytes','?')}\t{new.get('mtime','?')}")
    for path, meta in added:
        print(f"ADD\t{path}\t{meta.get('sha256','?')}\t{meta.get('size_bytes','?')}\t{meta.get('mtime','?')}")
    for path, meta in removed:
        print(f"DEL\t{path}\t{meta.get('sha256','?')}\t{meta.get('size_bytes','?')}\t{meta.get('mtime','?')}")
PYEOF
)

FIRST_LINE=$(echo "$DIFF_REPORT" | head -1)

if [[ "$FIRST_LINE" == "OK" ]]; then
  echo "$(now_iso) [check] OK — todos os hashes batem" >> "$LOG_FILE"
  echo "0" > "$LAST_STATUS"
  echo "baseline-hash-claude: todos os hashes batem."
  exit 0
fi

# Divergente
COUNTS=${FIRST_LINE#DIFF:}
N_MOD=$(echo "$COUNTS" | cut -d: -f1)
N_ADD=$(echo "$COUNTS" | cut -d: -f2)
N_DEL=$(echo "$COUNTS" | cut -d: -f3)
TOTAL=$((N_MOD + N_ADD + N_DEL))

{
  echo ""
  echo "🚨 ALERTA SEGURANÇA — BASELINE HASH DIVERGENTE (Regra §16, vetor R1)"
  echo ""
  echo "VETOR: R1 — Mini Shai-Hulud / CVE-2025-59536"
  echo "DESCRIÇÃO: arquivos críticos do Claude Code foram modificados desde o último baseline."
  echo ""
  echo "ARQUIVOS MODIFICADOS ($TOTAL): $N_MOD modificados, $N_ADD adicionados, $N_DEL removidos"
  echo ""
  echo "$DIFF_REPORT" | tail -n +2 | while IFS=$'\t' read -r kind path b_sha b_size b_mtime c_sha c_size c_mtime; do
    case "$kind" in
      MOD)
        echo "- [MOD] $path"
        echo "  baseline: $b_sha ($b_size bytes, $b_mtime)"
        echo "  atual:    $c_sha ($c_size bytes, $c_mtime)"
        ;;
      ADD)
        echo "- [ADD] $path"
        echo "  atual: $b_sha ($b_size bytes, $b_mtime)"
        ;;
      DEL)
        echo "- [DEL] $path"
        echo "  baseline: $b_sha ($b_size bytes, $b_mtime)"
        ;;
    esac
  done
  echo ""
  echo "AÇÃO RECOMENDADA:"
  echo "1. Verificar diff: git diff em paths versionados, comparação manual em ~/.claude.json"
  echo "2. Investigar: instalação de plugin novo? clone de repo terceiro? MCP server novo?"
  echo "3. Se modificação foi LEGÍTIMA: rodar 'baseline-hash-claude.sh init' pra refrescar baseline"
  echo "4. Se SUSPEITA: rodar /security-audit, isolar ambiente, alertar Gui"
  echo ""
  echo "Vetores ativos 2026:"
  echo "- Mini Shai-Hulud (TeamPCP) — worm npm/PyPI com persistência em ~/.claude.json"
  echo "- CVE-2025-59536 — RCE via hooks em settings.json"
  echo ""
  echo "Pendência mãe: ClickUp 86ahha462"
} >&2

echo "$(now_iso) [check] DIVERGENTE — $TOTAL arquivos ($N_MOD mod, $N_ADD add, $N_DEL del)" >> "$LOG_FILE"
echo "1" > "$LAST_STATUS"
exit 1
