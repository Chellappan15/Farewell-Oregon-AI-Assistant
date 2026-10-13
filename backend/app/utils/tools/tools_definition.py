from google.genai import types

tool = types.Tool(
    function_declarations=[
        {
            "name": "compare_weapons",
            "description": "Compares between 2 guns from the game.",
            "parameters": {
                "type": "object",
                "properties": {
                    "first": {
                        "type": "string",
                        "description": "The first weapon."
                    },
                    "second": {
                        "type": "string",
                        "description": "The second weapon."
                    }
                },
                "required": ["first", "second"]
            }
        },
        {
            "name": "zombie_details",
            "description": "Use this function whenever the user asks about a zombie/freaker in Days Gone, including its characteristics, behavior, weaknesses, or how to kill it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zombie_name": {
                        "type": "string",
                        "description": "The specific zombie/freaker type the user is asking about and available values are Swarmers, Newts, Screamers, Breakers, Reachers, Runners, Ragers, Criers, Marauders, Rippers, Wolves, Bears, Cougars."
                    }
                },
                "required": ["zombie_name"]
            },
        }
    ]
)

config = types.GenerateContentConfig(
    tools=[tool]
)