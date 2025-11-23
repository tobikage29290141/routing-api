## routers/ocr.py

# routers/ai.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.ai_service import AIService

router = APIRouter(prefix="/api/ai", tags=["ai"])

class OcrTextRequest(BaseModel):
    raw_text: str
    doc_type: str | None = None  # "invoice", "receipt" など
    company_hint: str | None = None

class StructuredResponse(BaseModel):
    issue_date: str | None
    total_amount: int | None
    company_name: str | None
    raw_text: str

@router.post("/analyze", response_model=StructuredResponse)
async def analyze_ocr_text(payload: OcrTextRequest):
    service = AIService()

    prompt = f"""
あなたは会計事務のアシスタントです。
以下はOCRで読み取った日本語の請求書・領収書などのテキストです。

---
{payload.raw_text}
---

ここから、可能な範囲で以下をJSONで返してください。

- issue_date: 発行日 (YYYY-MM-DD形式でできる限り正規化)
- total_amount: 税込合計金額 (数値のみ、カンマなし)
- company_name: 請求元・発行元の会社名（分かれば）

出力は必ず次のJSON形式のみとします：

{{
  "issue_date": "...",
  "total_amount": 123456,
  "company_name": "..."
}}
"""

    answer = await service.ask(prompt)
    # TODO: answerをjson.loadsしてStructuredResponseに詰める
    # まずはLLM側を strict JSON に寄せる方針で

    import json
    data = json.loads(answer)
    return StructuredResponse(
        issue_date=data.get("issue_date"),
        total_amount=data.get("total_amount"),
        company_name=data.get("company_name"),
        raw_text=payload.raw_text,
    )