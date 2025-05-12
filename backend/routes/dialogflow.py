from fastapi import APIRouter, Body
from typing import Dict
from ..controllers import dialogflow

router = APIRouter(prefix="/dialogflow", tags=["Dialogflow"])

@router.post("")
async def detect_intent(data: Dict = Body(...)):
    text = data.get("text", "")
    session_id = data.get("session_id", "default")
    language_code = data.get("language_code", "vi")
    
    return await dialogflow.detect_intent(text, session_id, language_code)
