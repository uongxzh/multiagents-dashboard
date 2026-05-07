from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.agent import Agent
from app.models.task import Task
from app.schemas.agent import AgentResponse, AgentUpdate
from app.schemas.common import err, ok
from app.schemas.task import TaskResponse

router = APIRouter(tags=["agents"])


@router.get("/api/agents")
def list_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).order_by(Agent.name).all()
    return ok([AgentResponse.model_validate(a) for a in agents])


@router.get("/api/agents/{agent_id}")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        return err("NOT_FOUND", "Agent not found", 404)
    return ok(AgentResponse.model_validate(agent))


@router.put("/api/agents/{agent_id}")
def update_agent(agent_id: str, data: AgentUpdate, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        return err("NOT_FOUND", "Agent not found", 404)
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(agent, key, val)
    db.commit()
    db.refresh(agent)
    return ok(AgentResponse.model_validate(agent))


@router.get("/api/agents/{agent_id}/tasks")
def get_agent_tasks(agent_id: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.assignee_agent_id == agent_id).all()
    return ok([TaskResponse.model_validate(t) for t in tasks])
