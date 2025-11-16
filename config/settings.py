## config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CLOUD_OCR_ENDPOINT = os.getenv("CLOUD_OCR_ENDPOINT")
    CLOUD_OCR_API_KEY  = os.getenv("CLOUD_OCR_API_KEY")

    ROUTING_API_KEY = os.getenv("ROUTING_API_KEY")

settings = Settings()
