# Foci MCP Harness

**Foci**: The agent library for reliable, efficient, and reviewable focused agent swarms.
**Loki**: AI personal assistant orchestrating versioned, measurable goals using Git collaboration.

## Overview

This repository contains the full Foci harness implemented as an **MCP (Measurement & Control Protocol) Server** for testing Foci by Grok.

The harness provides a REST API that allows Grok (acting as Loki) to exercise and validate all core Foci functionality in a controlled, versioned, and measurable way.

## Key Features

- **Versioned Goals**: Create, track, and version goals with measurable success criteria.
- **Agent Swarms**: Spawn and orchestrate focused agent swarms around specific goals.
- **Git Collaboration**: Simulate and trigger Git-based workflows (branch, PR, review, merge) as part of goal achievement.
- **Metrics & Measurement**: Real-time progress metrics, success scoring, and audit trails.
- **MCP Server**: FastAPI-powered server exposing all operations via clean JSON API.
- **Full Testability**: Designed for automated testing and live deployment preparation.

## Making It Public & Secure (for Grok Access) — No Docker

Grok cannot access private networks. This update makes the MCP server **publicly deployable and secure** (non-Docker path):

- **API Key Authentication**: All endpoints (except /health) require `X-API-Key` header.
- **CORS**: Restricted origins via env var (set to Grok domains).
- **Simple Deploy**: Direct uvicorn on platforms like Render or Railway (free tier).

### Quick Secure Deploy (Non-Docker)

1. Fork/clone this repo
2. Set env vars:
   - `API_KEY` = strong random key (share only with Grok)
   - `ALLOWED_ORIGINS` = `https://grok.x.ai`
3. Deploy on Render/Railway:
   - Connect GitHub → Python 3.11 → Build: `pip install -r requirements.txt`
   - Start command: `uvicorn harness.mcp_server:app --host 0.0.0.0 --port $PORT`
4. Public URL ready. Grok uses it with `X-API-Key` header.

**Security**: Never commit keys; rotate regularly; HTTPS by platform.

## Project Structure

```
foci-mcp-harness/
├── src/foci/
│   ├── __init__.py
│   ├── agent.py
│   ├── goal.py
│   ├── swarm.py
│   ├── loki.py
├── harness/
│   ├── mcp_server.py
├── tests/
│   ├── test_foci.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
```

## Getting Started (Local, No Docker)

pip install -r requirements.txt
uvicorn harness.mcp_server:app --reload --host 0.0.0.0 --port 8000

## Example API Usage (Grok with auth)

```bash
curl -X POST https://your-public-url/goals \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"description": "Test goal", "success_criteria": ["works securely"]}'
```

## Foci Project Instructions Compliance

- New branch `chore/remove-docker-support` from latest `main`
- All via PR (no main edits)
- Full paper trail
- Upstream checked (clean)

---
*Built by Grok following Foci Project Instructions.*