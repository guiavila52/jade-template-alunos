# workspace/infra/

## Propósito

Infraestrutura local de observabilidade, monitoramento e ferramentas operacionais self-hosted do squad. Pasta criada em 2026-05-16 (Item 0.4 / Fase 0 hardening, pendência mãe ClickUp 86ahha462).

## Estrutura

- `signoz/` — SigNoz self-hosted (OpenTelemetry backend). Recebe traces/logs/métricas do Claude Code (env vars `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`). Status atual: docker-compose baixado, NÃO subido (Docker não instalado no laptop).

## Como operar

### SigNoz

Pré-requisito: Docker Desktop instalado (decisão pendente Gui).

```bash
cd workspace/infra/signoz
docker compose up -d   # subir
docker compose ps      # verificar
docker compose down    # parar
```

Dashboard local: http://localhost:3301 (default SigNoz).
Portas OTLP: 4317 (gRPC) / 4318 (HTTP).

Dados ClickHouse ficam em `workspace/infra/signoz/data/` (gitignored).

## Última atualização

2026-05-16 — criação inicial via Item 0.4 hardening (pendência ClickUp 86ahha462).
