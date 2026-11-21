from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

_TEMPLATE_DIRECTORY = Path(__file__).resolve().parent / "templates"
_environment = Environment(
    loader=FileSystemLoader(_TEMPLATE_DIRECTORY),
    undefined=StrictUndefined,
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

def render_gemini_prompt(
    query: str,
    context: Any,
    history: list[dict[str, Any]],
    game_name: str = "Days Gone",
) -> str:
    """Render the shared Gemini prompt for a chat request."""
    template = _environment.get_template("game_prompt.j2")

    return template.render(
        current_question=query,
        relevant_context=context,
        conversation_history=history,
        game_name=game_name,
    )
