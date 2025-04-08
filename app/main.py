# 1. On importe FastAPI et les routes
from fastapi import FastAPI
from app.api import audience, reco, full  
from fastapi.middleware.cors import CORSMiddleware


# 2. Création de l'application
app = FastAPI(
    title="Affichage Dynamique Intelligent",
    description="API pour analyser les visiteurs et adapter l’affichage",
    version="1.0.0",
    docs_url="/docs",           # URL Swagger UI
    redoc_url="/redoc",         # URL ReDoc
    openapi_url="/openapi.json" # Spéc OpenAPI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en dev, on autorise tout
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Inclusion des routes agents
app.include_router(audience.router, prefix="/audience", tags=["Audience"])
app.include_router(reco.router, prefix="/reco", tags=["Recommandation"])
app.include_router(full.router, prefix="/full", tags=["Full Workflow"])

# 4. Route racine pour tester le serveur
@app.get("/")
def home():
    return {"message": "Système Multi-Agents d’Affichage Dynamique actif"}
