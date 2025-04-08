from fastapi import APIRouter
from app.agents.agent_audience import get_live_visitors

router = APIRouter(prefix="/audience")

@router.get("/live")
def live_audience():
    return get_live_visitors()
