##  routers/ocr.py

from fastapi import APIRouter, UploadFile, File
from services.ocr_service import call_cloud_ocr

router = APIRouter()

@router.post("/ocr")
async def ocr_proxy(file: UploadFile = File(...)):
    result = await call_cloud_ocr(file)
    return result
