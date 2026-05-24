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
```

## Getting Started

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
# Create a goal
curl -X POST http://localhost:8000/goals \
  -H "Content-Type: application/json" \
  -d '{"description": "Build reliable agent swarm for code review", "success_criteria": ["All PRs reviewed", "Coverage > 90%"], "version": "v1.0"}'

# Spawn swarm
curl -X POST http://localhost:8000/swarms \
  -H "Content-Type: application/json" \
  -d '{"goal_id": "goal-123", "num_agents": 5, "focus": "code_review"}'

# Get metrics
curl http://localhost:8000/metrics/goal-123

# Trigger Git PR simulation
curl -X POST http://localhost:8000/git/pr \
  -H "Content-Type: application/json" \
  -d '{"goal_id": "goal-123", "branch": "feature/agent-swarm"}'
```

## Foci Project Instructions Compliance

This harness was built following strict Foci workflow:
- Created feature branch `feature/full-foci-mcp-harness` from `main`
- All changes via push + PR (no direct main edits)
- Full paper trail with reviewable PR
- Concise, actionable, versioned deliverables

## Next Steps
- Deploy to live environment
- Integrate real GitHub API for Git collaboration endpoints
- Expand agent capabilities in Foci library
- Add WebSocket support for real-time swarm monitoring

---
*Built by Grok following Foci Project Instructions. All updates via PR.*