from db.compare_weapons_queries import get_weapon_statistics

def compare_weapons(weapon_1: str, weapon_2: str) -> dict:
    result = get_weapon_statistics(weapon_1, weapon_2)

    print(result)

    # Check if both weapons were returned in the result list
    has_both_weapons = isinstance(result, (list, tuple)) and len(result) >= 2

    return {
        "weapon_1": result[0] if has_both_weapons else {},
        "weapon_2": result[1] if has_both_weapons else {}
    }