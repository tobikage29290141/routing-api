# routers/ai.py 

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.ai_service import AIService
from utils.security import require_api_key
from config.settings import settings

router = APIRouter(
    prefix="/ai",          # main.py 側の prefix="/api/routing" と組み合わせて
    tags=["ai"],           # → /api/routing/ai/analyze になる
    dependencies=[Depends(require_api_key)],
)


class OcrTextRequest(BaseModel):
    raw_text: str
    doc_type: Optional[str] = None   # "invoice", "receipt" など
    company_hint: Optional[str] = None


class StructuredResponse(BaseModel):
    issue_date: Optional[str]
    total_amount: Optional[int]
    company_name: Optional[str]
    raw_text: str


@router.post("/analyze", response_model=StructuredResponse)
async def analyze_ocr_text(payload: OcrTextRequest) -> StructuredResponse:
    """
    OCR 済みテキストを受け取り、
    AI で「発行日・合計金額・会社名」を抜き出して構造化する。
    """
    service = AIService(engine=settings.AI_DEFAULT_ENGINE)

    prompt = f"""
あなたは日本の中小企業の経理担当のアシスタントです。
以下は OCR で読み取ったテキストです。請求書・領収書・見積書などが含まれます。

---
{payload.raw_text}
---

ここから、可能な範囲で以下の情報を抽出してください。

- issue_date: 発行日 (YYYY-MM-DD形式。推定でもよいが、分からなければ null)
- total_amount: 税込合計金額 (数字のみ。カンマなし。分からなければ null)
- company_name: 請求元・発行元の会社名（分からなければ null）

出力は、余計な文章やコードブロックなしで、**次の JSON だけ** にしてください。

{{
  "issue_date": "YYYY-MM-DD または null",
  "total_amount": 金額 または null,
  "company_name": "会社名 または null"
}}
"""

    answer = await service.ask(prompt)

    # LLM が ```json ... ``` で返してくる可能性もあるので簡易クリーン
    import json
    cleaned = answer.strip()

    # ```json や ``` を削る
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="AI response is not valid JSON")

    return StructuredResponse(
        issue_date=data.get("issue_date"),
        total_amount=data.get("total_amount"),
        company_name=data.get("company_name"),
        raw_text=payload.raw_text,
    )