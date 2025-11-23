# config/settings.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env を先に読む（なくても Settings が env_file で拾うが、開発時はあっても良い）
load_dotenv()


class Settings(BaseSettings):
    # Cloud OCR API (Nextcloud 側)
    CLOUD_OCR_ENDPOINT: str = "https://cloud.sunamura-llc.com/api/ocr/pdf"
    CLOUD_OCR_API_KEY: str | None = None

    # Routing-API 自身の API キー
    ROUTING_API_KEY: str | None = None

    # AI エンジン関連
    AI_DEFAULT_ENGINE: str = "ollama"
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "gpt-oss:latest"
    OPENAI_MODEL: str = "gpt-4.1-mini"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()