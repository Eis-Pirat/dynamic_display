from fastapi import APIRouter
from app.agents.agent_audience import detect_visitors
from app.agents.agent_reco import recommander_contenu

router = APIRouter(prefix="/full", tags=["Full Workflow"])

@router.get("/recommandation")
def full_reco():
    # 🧠 On récupère un seul visiteur via détection
    result = detect_visitors(display=False)
    if not result["visitors"]:
        return {"error": "Aucun visiteur détecté"}

    visiteur = result["visitors"][0]
    genre = visiteur["genre"]
    age = visiteur["âge_estimé"]

    # 📡 On appelle la logique de recommandation
    reco = recommander_contenu(genre, age)

    return {
        "profil": visiteur,
        "recommandation": reco["recommandation"]
    }
