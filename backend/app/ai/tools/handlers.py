import logging
from typing import Any

from google.genai import types

from core.config import settings
from ai.tools.compare_weapons import compare_weapons
from ai.tools.zombie_types import zombie_details
from ai.tools.gta6_tools import compare_editions, get_character, get_game_facts, get_region

logger = logging.getLogger(__name__)

# Max model round-trips that request tools before we give up.
_MAX_TOOL_ROUNDS = 5

# Tool name -> function taking the call's args. Names are unique across games.
_TOOLS = {
    # Days Gone
    "compare_weapons": lambda a: compare_weapons(a.get("first"), a.get("second")),
    "zombie_details": lambda a: zombie_details(a.get("zombie_name")),
    # GTA 6
    "get_character": lambda a: get_character(a.get("name")),
    "get_region": lambda a: get_region(a.get("name")),
    "compare_editions": lambda a: compare_editions(),
    "get_game_facts": lambda a: get_game_facts(a.get("topic")),
}


def _dispatch(call) -> dict[str, Any]:
    """Run one tool call. Errors go back to the model instead of crashing the request."""
    args = call.args or {}
    tool = _TOOLS.get(call.name)
    if tool is None:
        logger.warning("Gemini requested unknown tool: %s", call.name)
        return {"error": f"Unknown tool: {call.name}"}
    try:
        result = tool(args)
    except Exception:
        logger.exception("Tool %s failed with args %s", call.name, args)
        return {"error": f"The {call.name} tool failed. Answer without it if possible."}

    return {"content": result if result is not None else ""}


def _function_calls(content: types.Content | None) -> list:
    return [part.function_call for part in (content.parts or []) if part.function_call] if content else []


def _text(content: types.Content | None) -> str:
    if not content:
        return ""
    return "".join(
        part.text for part in (content.parts or []) if part.text and not getattr(part, "thought", False)
    )


def run_tools(
    model_content: types.Content,
    history: list,
    prompt: str,
    client,
    config: types.GenerateContentConfig,
    stats: dict | None = None,
) -> str:
    """Resolve tool calls until the model returns a plain answer.

    model_content is the model turn that requested the tools (all of its parts,
    kept as-is so thought signatures are preserved). Every round's calls and
    results are appended to one running conversation, so later rounds still see
    earlier tool results, and parallel calls in one turn are all answered together.
    """
    contents = [
        *history,
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)]),
    ]

    for round_number in range(1, _MAX_TOOL_ROUNDS + 1):
        calls = _function_calls(model_content)
        if not calls:
            return _text(model_content)
        if stats is not None:
            stats["tool_rounds"] = round_number

        logger.info("Tool round %d: %s", round_number, [call.name for call in calls])
        contents.append(model_content)
        contents.append(
            types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(name=call.name, response=_dispatch(call))
                    for call in calls
                ],
            )
        )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=config,
        )
        model_content = response.candidates[0].content if response.candidates else None

    raise RuntimeError("Gemini exceeded the maximum tool-call limit.")
