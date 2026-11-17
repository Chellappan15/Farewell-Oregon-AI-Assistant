from functools import lru_cache

import google.genai as genai

from core.config import settings


@lru_cache(maxsize=1)
def get_gemini_client():
    return genai.Client(api_key=settings.gemini_api_key)
