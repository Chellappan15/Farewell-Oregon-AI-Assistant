import os
from functools import lru_cache

import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY must be configured in the environment.")
    return genai.Client(api_key=api_key)
