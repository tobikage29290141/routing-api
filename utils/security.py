# utils/security.py

from fastapi import Header, HTTPException, status
from config.settings import settings

async def require_api_key(x_api_key: str = Header(None)):
    """
    共通APIキー認証。
    ヘッダ x-api-key の一致を確認。
    """

    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key missing",
        )

    if x_api_key != settings.ROUTING_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return True
