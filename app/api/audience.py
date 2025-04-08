from fastapi import APIRouter
from app.agents.agent_audience import detect_visitors

router = APIRouter(prefix="/audience")

@router.get("/scan")
def scan_audience():
    result = detect_visitors(display=False)  # Ne pas afficher l’image
    return result

