from fastapi import APIRouter
from app.agents.agent_audience import get_live_visitors  # ✅ remplacer l'import
from app.agents.agent_reco import recommander_contenu

router = APIRouter(prefix="/full", tags=["Full Workflow"])

@router.get("/recommandation")
def full_reco():
    # 📡 Récupération live des visiteurs déjà analysés
    result = get_live_visitors()
    if not result["visitors"]:
        return {"error": "Aucun visiteur détecté"}

    visiteur = result["visitors"][0]  # prend le 1er
    genre = visiteur["genre"]
    age = visiteur["âge_estimé"]

    reco = recommander_contenu(genre, age)

    return {
        "profil": visiteur,
        "recommandation": reco["recommandation"]
    }
