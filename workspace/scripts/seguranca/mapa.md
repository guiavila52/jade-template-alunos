# workspace/scripts/seguranca/ — MAPA

Propósito: scripts de hardening de segurança do squad. Fecha vetores ativos (Mini Shai-Hulud, CVE Claude Code, supply chain). Pendência mãe ClickUp Fase 0 Hardening: 86ahha462.

## Arquivos

- `baseline-hash-claude.sh` — Item 0.2 Fase 0 (Regra §16, vetor R1). Gera/verifica baseline sha256 de arquivos críticos do Claude Code (~/.claude.json, ~/.claude/mcp.json, settings.json globais e project, hooks, commands, agents). Modos: `init` (gera baseline) e `check` (compara e alerta divergência). Disparado por hook PreToolUse `.claude/hooks/check-baseline-hash-claude.sh` em background + plist launchd a cada 30min (`~/Library/LaunchAgents/com.guiavila.squad.baseline-hash.plist`, ativar com `launchctl load`).
- `mcp-audit-mensal.sh` — Item 0.5 Fase 0 (Regra §16). Auditoria mensal dos MCP servers ativos via invariantlabs-ai/mcp-scan.
- `audit-claude-logs.py` — Item 0.4 LITE Fase 0 (Regra §16, vetor R7). Parsing de transcripts JSONL nativos do Claude Code em `~/.claude/projects/{slug}/*.jsonl`. Detecta Bash suspeito (curl-pipe-shell, base64 decode+exec, eval, netcat, git --no-verify em commit), edits em paths sensíveis (`.claude/`, `AGENTS.md`, `.env`), MCP novo fora de baseline, volume anômalo (>3x média). Secrets mascarados. Modos: `--days N`, `--since 7d|30d`, `--session ID`, `--tail`, `--alerts-only`, `--output PATH`. Exit code: 0 ok / 1 warn / 2 critical. Output em `workspace/output/seguranca/audit-claude-logs-YYYY-MM-DD.md`. Plist semanal opcional: `~/Library/LaunchAgents/com.guiavila.squad.audit-logs.plist` (NÃO carregada — `launchctl load` pra ativar).

## Última atualização

2026-05-16 — Item 0.4 LITE adicionado (audit-claude-logs.py + plist semanal + detecção suspicious_bash + volume spike + secrets masking). Doc auditoria: `workspace/output/auditorias/2026-05-16-audit-claude-logs-setup.md`.
