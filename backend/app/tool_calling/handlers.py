from utils.compare_weapons import compare_weapons
from google.genai import types
from utils.zombie_types import zombie_details

def handlers(function_call, history, response, config, prompt, client):

    while function_call:

        if function_call.name == "compare_weapons":
            first_weapon = function_call.args.get("first")
            second_weapon = function_call.args.get("second")

            print("Comparing:", first_weapon, second_weapon)

            result = compare_weapons(first_weapon, second_weapon)

        elif function_call.name == "zombie_details":
            zombie_name = function_call.args.get("zombie_name")

            print("Fetching details:", zombie_name)

            result = zombie_details(zombie_name)
            print(result)

        else:
            break

        # Send tool result back to Gemini
        function_response = types.Part.from_function_response(
            name=function_call.name,
            response={
                "content": result if result is not None else ""
            }
        )

        content_history = history[:-2] if len(history) > 2 else []

        content = [
            *content_history,
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            ),
            response.candidates[0].content,
            types.Content(
                role="tool",
                parts=[function_response]
            )
        ]

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=content,
            config=config
        )

        # Check whether Gemini wants another tool
        part = response.candidates[0].content.parts[0]
        function_call = getattr(part, "function_call", None)
        print(response.candidates[0].content.parts)

        # No more function calls → final answer
        return response.text