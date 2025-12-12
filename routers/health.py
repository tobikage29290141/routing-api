# routers/health.py

from fastapi import APIRouter, Depends
from utils.security import require_api_key

router = APIRouter()

@router.get("/health", dependencies=[Depends(require_api_key)])
def health():
    return {"status": "ok","message":"health check Success"}
