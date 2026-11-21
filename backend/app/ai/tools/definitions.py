from google.genai import types

# Days Gone tools (MySQL: weapon_info, zombie_details)
days_gone_tool = types.Tool(
    function_declarations=[
        {
            "name": "compare_weapons",
            "description": "Compares between 2 guns from the game.",
            "parameters": {
                "type": "object",
                "properties": {
                    "first": {"type": "string", "description": "The first weapon."},
                    "second": {"type": "string", "description": "The second weapon."},
                },
                "required": ["first", "second"],
            },
        },
        {
            "name": "zombie_details",
            "description": (
                "Use this function whenever the user asks about a zombie/freaker "
                "in Days Gone, including its characteristics, behavior, "
                "weaknesses, or how to kill it."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "zombie_name": {
                        "type": "string",
                        "description": (
                            "The specific zombie/freaker type the user is asking "
                            "about and available values are Swarmers, Newts, "
                            "Bleachers, Screamers, Breakers, Reachers, Runners, "
                            "Ragers, Criers, Marauders, Rippers, Anarchists, "
                            "Wolves, Bears, Cougars."
                        ),
                    }
                },
                "required": ["zombie_name"],
            },
        },
    ]
)

# GTA 6 tools (MySQL: gta6_characters, gta6_regions, gta6_editions, gta6_facts)
gta6_tool = types.Tool(
    function_declarations=[
        {
            "name": "get_character",
            "description": (
                "Use this whenever the user asks who a GTA 6 character is: their role, "
                "background, relationships or story details."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": (
                            "Character name, full or partial. Available characters: Jason Duval, "
                            "Lucia Caminos, Cal Hampton, Boobie Ike, Dre'Quan Priest, Real Dimez "
                            "(Bae-Luxe and Roxy), Raul Bautista, Brian Heder, Lori."
                        ),
                    }
                },
                "required": ["name"],
            },
        },
        {
            "name": "get_region",
            "description": (
                "Use this whenever the user asks about a region of Leonida, the GTA 6 map: "
                "its real-world inspiration, location, landmarks or activities."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": (
                            "Region name. Available regions: Vice City, Leonida Keys, Grassrivers, "
                            "Port Gellhorn, Ambrosia, Mount Kalaga National Park."
                        ),
                    }
                },
                "required": ["name"],
            },
        },
        {
            "name": "compare_editions",
            "description": (
                "Use this when the user asks about GTA 6 editions, prices, what the Ultimate "
                "Edition includes, or the pre-order bonus. Returns the Standard and Ultimate "
                "editions side by side plus the Vintage Vice City Pack."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
        {
            "name": "get_game_facts",
            "description": (
                "Use this for factual questions about GTA 6 as a product: release date, platforms, "
                "delays, performance and frame rate, review scores, sales, online mode, "
                "pre-order bonus or trailers and marketing."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "enum": [
                            "release", "platforms", "delays", "performance", "reviews",
                            "sales", "online", "preorder_bonus", "marketing",
                        ],
                        "description": "The fact category to look up.",
                    }
                },
                "required": ["topic"],
            },
        },
    ]
)

_TOOL_CONFIGS = {
    "days_gone": types.GenerateContentConfig(tools=[days_gone_tool]),
    "gta6": types.GenerateContentConfig(tools=[gta6_tool]),
}


def get_tool_config(game: str) -> types.GenerateContentConfig:
    """Each game only sees its own tools."""
    return _TOOL_CONFIGS[game]
