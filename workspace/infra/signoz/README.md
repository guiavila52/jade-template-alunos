# SigNoz Self-Hosted — Observability backend pro Claude Code

Recebe traces/logs/métricas exportados via OpenTelemetry pelo Claude Code (env vars `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`).

Fecha vetor de risco R7 (sem audit log / observability) da auditoria de segurança 2026-05-16.

## Pré-requisito

Docker Desktop instalado e rodando. **Status atual (2026-05-16): Docker NÃO instalado no laptop do Gui.** Setup parado aguardando decisão.

## Subir

```bash
cd workspace/infra/signoz
docker compose up -d
# Aguardar ~60s pra healthchecks subirem
docker compose ps
```

## Dashboard

http://localhost:3301 (login default: `admin@signoz.io` / definido no primeiro acesso).

## Portas

- `3301` — frontend SigNoz
- `4317` — OTLP gRPC (Claude Code exporta aqui)
- `4318` — OTLP HTTP

## Parar / limpar

```bash
docker compose down       # parar (preserva dados)
docker compose down -v    # parar + deletar volumes (perde dados)
```

## Dados

ClickHouse persiste em volumes Docker. Pasta `data/` (se criada) está gitignored.

## Ativar telemetria no Claude Code

Após SigNoz rodando, adicionar em `.claude/settings.json` (via Bash heredoc/jq, Regra §11):

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_SERVICE_NAME": "claude-code-squad-gui"
  }
}
```

Telemetria começa a fluir na PRÓXIMA sessão (reload settings.json).

**Importante:** não ativar essas env vars sem SigNoz rodando, ou Claude vai tentar exportar pra endpoint morto a cada call (logs ruidosos).

## Versão do docker-compose

Baixado de `https://raw.githubusercontent.com/SigNoz/signoz/develop/deploy/docker/clickhouse-setup/docker-compose-minimal.yaml` em 2026-05-16. Branch `develop` (não pinned em tag — TODO: pinar em release stable quando ativar).
