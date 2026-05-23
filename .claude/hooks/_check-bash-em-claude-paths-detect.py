#!/usr/bin/env python3
"""Auxiliar do hook check-bash-em-claude-paths.sh.
Lê JSON do Claude Code via stdin, emite PASS ou BLOCK|path|op|cmd_b64."""
import sys, json, re, base64

try:
    data = json.load(sys.stdin)
except Exception:
    print("PASS"); sys.exit(0)

if data.get("tool_name", "") != "Bash":
    print("PASS"); sys.exit(0)

cmd = data.get("tool_input", {}).get("command", "")
if not cmd:
    print("PASS"); sys.exit(0)

protected_patterns = [
    r'\.claude/settings\.json',
    r'\.claude/settings\.local\.json',
    r'\.claude/hooks/',
    r'\.claude/commands/',
    r'\.claude/agents/',
    r'~/\.claude/settings\.json',
    r'\$HOME/\.claude/settings\.json',
    r'/Users/[^/]+/\.claude/settings\.json',
    r'~/\.claude\.json',
    r'\$HOME/\.claude\.json',
    r'/Users/[^/]+/\.claude\.json',
    r'~/\.claude/mcp\.json',
    r'\$HOME/\.claude/mcp\.json',
    r'/Users/[^/]+/\.claude/mcp\.json',
]

protected_hit = None
for pat in protected_patterns:
    m = re.search(pat, cmd)
    if m:
        protected_hit = m.group(0); break

if not protected_hit:
    print("PASS"); sys.exit(0)

esc = re.escape(protected_hit)
write_patterns = [
    (r'>\s*[\'"]?[^|&;<>\s]*' + esc, 'redirect >'),
    (r'>>\s*[\'"]?[^|&;<>\s]*' + esc, 'redirect >>'),
    (r'\btee\s+(-a\s+)?[\'"]?[^|&;<>\s]*' + esc, 'tee'),
    (r"\bsed\s+-i(\s+''|\s+'[^']*')?\s+[^|&;]*?" + esc, 'sed -i'),
    (r'\bcat\s+[^|&;]*>\s*[\'"]?[^|&;<>\s]*' + esc, 'cat >'),
    (r'\becho\s+[^|&;]*>\s*[\'"]?[^|&;<>\s]*' + esc, 'echo >'),
    (r'\bprintf\s+[^|&;]*>\s*[\'"]?[^|&;<>\s]*' + esc, 'printf >'),
    (r'\bpython3?\s+-c\s+[\'"][^\'"]*(write|w\+|open)[^\'"]*' + esc, 'python -c write'),
    (r'\bmv\s+[^|&;]*' + esc, 'mv -> protected'),
    (r'\bcp\s+[^|&;]*' + esc, 'cp -> protected'),
    (r'\brm\s+[^|&;]*' + esc, 'rm protected'),
    (r'\btruncate\s+[^|&;]*' + esc, 'truncate'),
    (r'\bdd\s+[^|&;]*of=[\'"]?[^|&;<>\s]*' + esc, 'dd of='),
]

op = None
for pat, name in write_patterns:
    if re.search(pat, cmd):
        op = name; break

if not op:
    print("PASS"); sys.exit(0)

cmd_b64 = base64.b64encode(cmd.encode("utf-8")).decode("ascii")
print("BLOCK|" + protected_hit + "|" + op + "|" + cmd_b64)
