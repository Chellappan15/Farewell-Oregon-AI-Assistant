import logging

from core.config import settings

from google.genai import types

from ai.tools.compare_weapons import compare_weapons
from ai.tools.zombie_types import zombie_details

logger = logging.getLogger(__name__)
_MAX_TOOL_CALLS = 5

def handlers(function_call, history, response, config, prompt, client):
    for _ in range(_MAX_TOOL_CALLS):
        if function_call.name == "compare_weapons":
            result = compare_weapons(
                function_call.args.get("first"),
                function_call.args.get("second"),
            )
        elif function_call.name == "zombie_details":
            result = zombie_details(function_call.args.get("zombie_name"))
        else:
            raise ValueError(f"Unsupported Gemini tool: {function_call.name}")

        function_response = types.Part.from_function_response(
            name=function_call.name,
            response={"content": result if result is not None else ""},
        )
        content = [
            *history,
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
            response.candidates[0].content,
            types.Content(
                role="tool",
                parts=[function_response],
            ),
        ]
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=content,
            config=config,
        )
        parts = response.candidates[0].content.parts
        logger.info("Gemini tool response received with %d content parts", len(parts))
        function_call = getattr(parts[0], "function_call", None)
        if not function_call:
            return response.text

    raise RuntimeError("Gemini exceeded the maximum tool-call limit.")
