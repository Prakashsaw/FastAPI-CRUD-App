def individual_user_data(data) -> dict:
    return {
        "user_id": data["user_id"],
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
    }

def all_user_data(all_data) -> list:
    return [individual_user_data(data) for data in all_data]