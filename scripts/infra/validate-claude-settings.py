#!/usr/bin/env python3
"""
Valida ~/.claude/settings.json no formato canônico.
Exit 0 = OK. Exit 1 = formato quebrado, com diagnóstico.

Uso:
    python3 scripts/infra/validate-claude-settings.py
    python3 scripts/infra/validate-claude-settings.py --fix  # tenta normalizar
"""
import json, sys, shutil, os
from pathlib import Path
from datetime import datetime

SETTINGS = Path.home() / ".claude" / "settings.json"

def validate(data):
    errors = []
    hooks = data.get("hooks", {})
    for event_name, items in hooks.items():
        if not isinstance(items, list):
            errors.append(f"hooks.{event_name}: deveria ser array, é {type(items).__name__}")
            continue
        for i, item in enumerate(items, 1):
            if not isinstance(item, dict):
                errors.append(f"hooks.{event_name}[{i}]: deveria ser object")
                continue
            if "matcher" not in item:
                errors.append(f"hooks.{event_name}[{i}]: falta chave 'matcher' (formato antigo 'hook' detectado?)")
            if "hooks" not in item or not isinstance(item.get("hooks"), list):
                errors.append(f"hooks.{event_name}[{i}]: chave 'hooks' faltando ou não é array (formato antigo 'matchers' plural?)")
                continue
            for j, h in enumerate(item["hooks"], 1):
                if h.get("type") != "command":
                    errors.append(f"hooks.{event_name}[{i}].hooks[{j}]: 'type' deve ser 'command', achei {h.get('type')!r}")
                if not h.get("command"):
                    errors.append(f"hooks.{event_name}[{i}].hooks[{j}]: 'command' obrigatório")
    return errors

def backup():
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    dst = SETTINGS.with_suffix(f".json.bak-validate-{ts}")
    shutil.copy(SETTINGS, dst)
    return dst

def normalize_old_format(data):
    fixed = 0
    for event, items in data.get("hooks", {}).items():
        if not isinstance(items, list): continue
        new = []
        for item in items:
            if "matcher" in item and "hooks" in item:
                new.append(item); continue
            if "hook" in item and "matchers" in item:
                hook_path = item["hook"]
                if not hook_path.startswith("/"):
                    hook_path = f"{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}/{hook_path}"
                new.append({
                    "matcher": "|".join(item["matchers"]),
                    "hooks": [{
                        "type": "command",
                        "command": hook_path,
                        "description": "auto-normalized from legacy {hook, matchers} format"
                    }]
                })
                fixed += 1
            else:
                new.append(item)
        data["hooks"][event] = new
    return fixed

def main():
    if not SETTINGS.exists():
        print(f"❌ {SETTINGS} não existe", file=sys.stderr); return 1
    try:
        with SETTINGS.open() as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}", file=sys.stderr); return 1

    errors = validate(data)
    if not errors:
        print(f"✅ settings.json OK ({len(data.get('hooks', {}).get('PreToolUse', []))} PreToolUse hooks no formato canônico)")
        return 0

    print(f"❌ {len(errors)} problema(s) em settings.json:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)

    if "--fix" in sys.argv:
        b = backup()
        print(f"📦 Backup: {b}", file=sys.stderr)
        fixed = normalize_old_format(data)
        with SETTINGS.open("w") as f:
            json.dump(data, f, indent=2)
        print(f"🔧 {fixed} hook(s) normalizados", file=sys.stderr)
        # revalida
        errors2 = validate(data)
        if errors2:
            print(f"❌ Ainda restam {len(errors2)} problemas após --fix:", file=sys.stderr)
            for e in errors2: print(f"  - {e}", file=sys.stderr)
            return 1
        print("✅ Após --fix: settings.json no formato canônico", file=sys.stderr)
        return 0

    print("\nPra corrigir automaticamente: rode com --fix", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main())
