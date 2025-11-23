## config/settings.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings:
    CLOUD_OCR_ENDPOINT = os.getenv("CLOUD_OCR_ENDPOINT")
    CLOUD_OCR_API_KEY  = os.getenv("CLOUD_OCR_API_KEY")

    ROUTING_API_KEY = os.getenv("ROUTING_API_KEY")

    AI_DEFAULT_ENGINE: str = "ollama"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "gpt-oss:latest"
    OPENAI_MODEL: str = "gpt-4.1-mini"

    class Config:
        env_file = ".env"
settings = Settings()
