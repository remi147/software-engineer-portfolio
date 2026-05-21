# 🌐 REST API Uptime Monitor

## User Story
> *As a DevOps engineer, I want an automated API monitor so that I am alerted when any endpoint goes down or responds too slowly.*

## Sprint Delivery (Kanban)
| Column | Story | Status |
|--------|-------|--------|
| Done | Endpoint config model | ✅ |
| Done | HTTP checker with timeout | ✅ |
| Done | Concurrent thread monitoring | ✅ |
| Done | YAML config loader | ✅ |
| Done | GitHub Actions CI | ✅ |

## Usage
```bash
pip install requests pyyaml
python monitor.py --config endpoints.yaml
```

## Features
- Configurable via `endpoints.yaml` — no code changes needed
- Concurrent monitoring using `threading`
- Response time alerts (configurable `alert_on_slow_ms`)
- Detects HTTP errors, timeouts, and connection failures
