from typing import Any
from core.config import settings


def estimator(text: str) -> int:
    return len(text) // 4

def chunk_selection(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected_chunks = []

    token_count = 0

    for chunk in chunks:
        chunk_tokens = estimator(chunk["text"])

        if token_count + chunk_tokens > settings.tokens:
            break

        selected_chunks.append(chunk)
        token_count += chunk_tokens

    return selected_chunks

def history_selection(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    history_token = 0
    selected = []

    if history and history[-1].get("role") == "user":
        history = history[:-1]

    for i in range(len(history) - 1, -1, -1):
        message_tokens = history[i].get("token", 0)

        if history_token + message_tokens > settings.chat_history:
            break

        history_token += message_tokens

        selected.insert(
            0,
            {
                "role": history[i].get("role", "user"),
                "parts": [
                    {"text": part.get("text", "")}
                    for part in history[i].get("parts", [])
                ],
            },
        )

    return selected