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

## Making It Public & Secure (for Grok Access)

Grok cannot access private networks. This update makes the MCP server **publicly deployable and secure**:

- **API Key Authentication**: All endpoints (except /health) require `X-API-Key` header.
- **CORS**: Restricted origins via env var (set to Grok domains or your frontend).
- **Production Ready**: Dockerized, env-configured, no hardcoded secrets.

### Quick Secure Deploy (Recommended: Render or Railway)

1. Fork/clone this repo
2. Set env vars on your platform:
   - `API_KEY` = strong random key (share securely with Grok only)
   - `ALLOWED_ORIGINS` = `https://grok.x.ai,https://yourapp.com`
3. Deploy (free tier works):
   - Render: Connect GitHub repo → Web Service → Python 3.11 → Build: `pip install -r requirements.txt` → Start: `uvicorn harness.mcp_server:app --host 0.0.0.0 --port $PORT`
   - Or use the included `Dockerfile`
4. Public URL e.g. `https://foci-mcp-harness.onrender.com`
5. Test with Grok: Include header `X-API-Key: your-key`

**Security Notes**:
- Never commit real keys (.env is gitignored)
- Rotate keys regularly
- Rate limiting can be added via slowapi if needed
- HTTPS enforced by platform

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
├── Dockerfile
├── .env.example
```

## Getting Started (Local)

### Prerequisites
- Python 3.10+
- pip install -r requirements.txt

### Run the MCP Server

```bash
uvicorn harness.mcp_server:app --reload --host 0.0.0.0 --port 8000
```

Server runs at http://localhost:8000

### Example API Usage (for Grok testing)

```bash
# Create a goal (with auth)
curl -X POST https://your-public-url/goals \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"description": "Build reliable agent swarm for code review", "success_criteria": ["All PRs reviewed", "Coverage > 90%"], "version": "v1.0"}'

# ... other endpoints same (add X-API-Key header)
```

## Foci Project Instructions Compliance

This harness was built following strict Foci workflow:
- Created feature branch `feature/public-secure-deployment` from latest `main`
- All changes via push + PR (no direct main edits)
- Full paper trail with reviewable PR
- Concise, actionable, versioned deliverables
- Upstream checked before work

## Next Steps
- Deploy to live environment (public + secure)
- Integrate real GitHub API for Git collaboration endpoints
- Expand agent capabilities in Foci library
- Add rate limiting + logging

---
*Built by Grok following Foci Project Instructions. All updates via PR.*