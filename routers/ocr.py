## routers/ocr.py

from fastapi import APIRouter, UploadFile, File, Depends
from utils.security import require_api_key
from services.ocr_service import call_cloud_ocr

router = APIRouter()

@router.post("/ocr", dependencies=[Depends(require_api_key)])
async def ocr_proxy(file: UploadFile = File(...)):
    result = await call_cloud_ocr(file)
    return result
