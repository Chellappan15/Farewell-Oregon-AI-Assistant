from typing import Any

from google.genai import types

from ai.gemini_client import get_gemini_client
from core.config import settings
from LLM.prompt_renderer import render_gemini_prompt


def generate_answer(question: str, chunks: list[dict[str, Any]], game_name: str = "Days Gone") -> str:
    """Answer with the same prompt template as the chat (no history, no tools)."""
    prompt = render_gemini_prompt(query=question, context=chunks, history=[], game_name=game_name)

    response = get_gemini_client().models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0),
    )
    return (response.text or "").strip()