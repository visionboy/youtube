from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.settings_service import settings_service

router = APIRouter(prefix="/api/settings", tags=["settings"])

class ApiKeyRequest(BaseModel):
    apiKey: str

@router.get("/api-key")
async def get_api_key_status():
    """
    Check if API key is configured
    """
    try:
        return settings_service.get_api_key_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api-key")
async def save_api_key(request: ApiKeyRequest):
    """
    Save or update YouTube API key
    """
    try:
        result = settings_service.save_api_key(request.apiKey)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api-key")
async def delete_api_key():
    """
    Delete YouTube API key
    """
    try:
        result = settings_service.delete_api_key()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
