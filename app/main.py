from fastapi import FastAPI
from app.api import audience, reco, full  
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 👈 à ajouter

app = FastAPI(
    title="Affichage Dynamique Intelligent",
    description="API pour analyser les visiteurs et adapter l’affichage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 👇 Ajoute cette ligne ici pour servir les images statiques
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(audience.router, prefix="/audience", tags=["Audience"])
app.include_router(reco.router, prefix="/reco", tags=["Recommandation"])
app.include_router(full.router, prefix="/full", tags=["Full Workflow"])

@app.get("/")
def home():
    return {"message": "Système Multi-Agents d’Affichage Dynamique actif"}
