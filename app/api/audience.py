from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.agents.agent_analyse import analyse_visage

router = APIRouter(prefix="/audience", tags=["Analyse d’audience"])

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = analyse_visage(content)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Échec de l’analyse", "details": str(e)}
        )
