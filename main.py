## main.py

from fastapi import FastAPI
from routers import health, ocr

app = FastAPI(
    title="Routing API",
    version="0.1.0",
)

# ルーター登録
app.include_router(health.router, prefix="/api/routing")
app.include_router(ocr.router, prefix="/api/routing")    # ← ここは「Cloud OCR プロキシ」用に
app.include_router(ai.router,prefix="/api/routing")      #/api/routing/ai/analyze