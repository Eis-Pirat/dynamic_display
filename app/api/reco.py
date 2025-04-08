from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.agent_reco import recommander_contenu

router = APIRouter(prefix="/reco", tags=["Recommandation"])

class Profil(BaseModel):
    genre: str
    age: int

@router.post("/recommander")
def reco_api(profil: Profil):
    return recommander_contenu(profil.genre, profil.age)
