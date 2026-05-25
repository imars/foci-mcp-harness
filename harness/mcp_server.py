from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys
sys.path.append('.')
from src.foci.loki import Loki

app = FastAPI(title='Foci MCP Harness Server (Secure Public)', version='0.2.1')

# Security: API Key (set via env)
API_KEY = os.getenv('API_KEY', 'dev-only-insecure-key')
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)

loki = Loki()

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Invalid or missing API key')
    return True

class GoalCreate(BaseModel):
    description: str
    success_criteria: List[str]
    version: str = 'v1.0'

class SwarmSpawn(BaseModel):
    goal_id: str
    num_agents: int = 3
    focus: str = 'task'

@app.get('/health')
def health_check():
    return {'status': 'healthy', 'service': 'foci-mcp-harness', 'secure': True, 'version': '0.2.1'}

# Public manifest endpoint for Grok custom connector installation
# This allows Grok to discover and validate the connector without requiring API key
@app.get('/')
@app.get('/manifest')
def connector_manifest():
    return {
        "name": "Foci MCP Harness",
        "version": "0.2.1",
        "description": "MCP server exposing Foci agent library, goal orchestration, and Git collaboration workflows for Grok/Loki testing.",
        "endpoints": {
            "health": "/health",
            "goals": "/goals (requires X-API-Key)",
            "swarms": "/swarms (requires X-API-Key)",
            "metrics": "/metrics/{goal_id} (requires X-API-Key)",
            "git_pr": "/git/pr (requires X-API-Key)"
        },
        "auth": "X-API-Key header required for all functional endpoints except /health and /manifest",
        "docs": "/docs"
    }

@app.post('/goals', dependencies=[Depends(verify_api_key)])
def create_goal(g: GoalCreate):
    goal = loki.create_goal(g.description, g.success_criteria, g.version)
    return goal.to_dict()

@app.post('/swarms', dependencies=[Depends(verify_api_key)])
def spawn_swarm(s: SwarmSpawn):
    try:
        swarm = loki.spawn_swarm(s.goal_id, s.num_agents, s.focus)
        return {'swarm_id': swarm.id, 'num_agents': len(swarm.agents), 'status': swarm.status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get('/metrics/{goal_id}', dependencies=[Depends(verify_api_key)])
def get_metrics(goal_id: str):
    try:
        return loki.measure_progress(goal_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post('/git/pr', dependencies=[Depends(verify_api_key)])
def create_pr(goal_id: str, branch: str = 'feature/test'):
    pr = loki.simulate_git_pr(goal_id, branch)
    if 'error' in pr:
        raise HTTPException(status_code=404, detail=pr['error'])
    return pr

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 8000)))
