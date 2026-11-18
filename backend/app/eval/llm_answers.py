from google.genai import types

from ai.gemini_client import get_gemini_client
from core.config import settings

def generate_answer(question: str, contexts: list[str]) -> str:
    context_block = "\n\n".join(
        f"[Source {i}]\n{text}" for i, text in enumerate(contexts, start=1)
    ) or "No context provided."

    prompt = (
        "You are a Days Gone game assistant.\n"
        "Answer the question using ONLY the context below. "
        "If the context does not contain the answer, say you do not have enough information.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question:\n{question}"
    )

    response = get_gemini_client().models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0),
    )
    return (response.text or "").strip()