from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 from typing import List, Dict, Any
 import sys
sys.path.append('.')
from src.foci.loki import Loki
app = FastAPI(title='Foci MCP Harness Server', version='0.1.0')
loki = Loki()
class GoalCreate(BaseModel):
    description: str
    success_criteria: List[str]
    version: str = 'v1.0'
class SwarmSpawn(BaseModel):
    goal_id: str
    num_agents: int = 3
    focus: str = 'task'
@app.get('/health')
def health_check(): return {'status': 'healthy', 'service': 'foci-mcp-harness'}
@app.post('/goals')
def create_goal(g: GoalCreate):
    goal = loki.create_goal(g.description, g.success_criteria, g.version)
    return goal.to_dict()
@app.post('/swarms')
def spawn_swarm(s: SwarmSpawn):
    try:
        swarm = loki.spawn_swarm(s.goal_id, s.num_agents, s.focus)
        return {'swarm_id': swarm.id, 'num_agents': len(swarm.agents), 'status': swarm.status}
    except Exception as e: raise HTTPException(status_code=404, detail=str(e))
@app.get('/metrics/{goal_id}')
def get_metrics(goal_id: str):
    try: return loki.measure_progress(goal_id)
    except Exception as e: raise HTTPException(status_code=404, detail=str(e))
@app.post('/git/pr')
def create_pr(goal_id: str, branch: str = 'feature/test'):
    pr = loki.simulate_git_pr(goal_id, branch)
    if 'error' in pr: raise HTTPException(404, pr['error'])
    return pr
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)