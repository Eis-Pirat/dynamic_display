from fastapi import APIRouter
from app.agents.agent_audience import get_live_visitors
from app.agents.agent_reco import recommander_contenu

router = APIRouter(prefix="/full", tags=["Full Workflow"])

@router.get("/recommandation")
def full_reco():
    result = get_live_visitors()
    if not result["visitors"]:
        return {"error": "Aucun visiteur détecté"}

    visiteur = result["visitors"][0]
    genre = visiteur.get("genre", "Inconnu")
    age = visiteur.get("âge_estimé", 0)
    emotion = visiteur.get("émotion", "neutral")

    reco = recommander_contenu(genre, age, emotion)

    return {
        "profil": visiteur,
        "recommandation": reco["recommandation"],
        "images": reco["images"]  # 👉 Très important pour ton front
    }

