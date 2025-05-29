from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.agent_reco import recommend_ad

router = APIRouter(
    prefix="/reco",
    tags=["Ad Recommendation"],
    responses={404: {"description": "Not found"}},
)

# ✅ Input schema
class AudienceProfile(BaseModel):
    genre: str        # "Homme" or "Femme"
    âge_estimé: int   # Integer age
    émotion: str      # "joy", "neutral", "sad", etc.

# ✅ Endpoint: /reco/ad
@router.post("/ad", summary="Recommender: Predict best ad", response_description="Predicted ad class")
async def get_ad_recommendation(profile: AudienceProfile):
    ad = recommend_ad(profile.genre, profile.âge_estimé, profile.émotion)
    return {"recommandation": ad}
