from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import lmstudio as lms

app = FastAPI(title="LM Studio Model Control API")


class ModelRequest(BaseModel):
    model_path: str  # GGUF-Pfad oder Model-Alias


@app.post("/load")
def load_model(payload: ModelRequest):
    """
    Lädt ein Modell in LM Studio (über die Python-API, NICHT über CLI).
    """
    try:
        lms.llm(payload.model_path)
        return {"status": "ok", "message": f"Model '{payload.model_path}' loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/unload")
def unload_model():
    """
    Entlädt das aktuell geladene Modell.
    """
    try:
        lms.llm().unload()
        return {"status": "ok", "message": "Model unloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    """
    Zeigt Status + geladenes Modell an.
    """
    try:
        info = lms.llm()
        return {"status": "ok", "current_model": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
