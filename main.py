## main.py

from fastapi import FastAPI
from routers import health, ocr

app = FastAPI()

# ルーター登録
app.include_router(health.router, prefix="/api/routing")
app.include_router(ocr.router, prefix="/api/routing")
