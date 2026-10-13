from db.zombie_types_queries import get_zombie_details

def zombie_details(name: str):
    details = get_zombie_details(name)

    if isinstance(details, (list, tuple)):
        return {
            "zombie_details": details
        }

    else: 
        return {
            "zombie_details": "No details were able to be found for this zombie."
        } 