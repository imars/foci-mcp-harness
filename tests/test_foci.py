import pytest
import sys
sys.path.append('.')
from src.foci.loki import Loki

def test_create_goal():
    loki = Loki()
    goal = loki.create_goal('Test MCP harness', ['endpoint works', 'metrics reported'])
    assert goal.id.startswith('goal-')
    assert goal.progress == 0.0

def test_spawn_and_measure():
    loki = Loki()
    goal = loki.create_goal('Swarm test', ['complete'])
    swarm = loki.spawn_swarm(goal.id, 3)
    result = loki.measure_progress(goal.id)
    assert result['goal']['progress'] > 0
    assert result['swarm_metrics'] is not None

def test_git_pr():
    loki = Loki()
    goal = loki.create_goal('PR goal', ['merge'])
    pr = loki.simulate_git_pr(goal.id, 'feature/mcp')
    assert pr['status'] == 'open'
    assert goal.progress > 0.4
