import httpx
from config.settings import settings

async def call_cloud_ocr(file):
    async with httpx.AsyncClient(timeout=60.0) as client:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        headers = {"x-api-key": settings.CLOUD_OCR_API_KEY}

        response = await client.post(
            settings.CLOUD_OCR_ENDPOINT,
            files=files,
            headers=headers
        )

        return response.json()
