from fastapi import FastAPI
from app.api import audience, reco

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Affichage Dynamique Intelligent",
    description="API pour analyser les visiteurs et adapter l’affichage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 🎯 Fichiers statiques pour les images recommandées
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 📦 Inclusion des routes
app.include_router(audience.router)
app.include_router(reco.router)


@app.get("/")
def home():
    return {"message": "✅ Backend FastAPI opérationnel pour l’analyse d’audience"}
