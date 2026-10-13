from pydantic import BaseModel
from typing import Literal
from google.genai import types

class HistoryItem(BaseModel):
    role: Literal["user", "model", "tool"]
    timestamp: str
    parts: list[dict[str, str]]

def history_data_transform_object(
    data: list[HistoryItem]
) -> list[dict]:
    return [types.Content(role=item["role"], parts=item["parts"]) for item in data]