import json
import os
from models import User

DATA_DIR = "data/users"
os.makedirs(DATA_DIR, exist_ok=True)

def get_json_path(username: str) -> str:
    safe_name = username.lower().strip()
    return os.path.join(DATA_DIR, f"{safe_name}.json")

def get_user(username: str) -> User | None:
    path = get_json_path(username)
    if not os.path.exists(path):
        return None
    
    with open(path, "r") as f:
        data = json.load(f)
        return User(**data)
    
def create_user(user: User):
    path = get_json_path(user.username)
    if os.path.exists(path):
        raise ValueError("User already exists")
    
    with open(path, "w") as f:
        json.dump(user.model_dump(), f, indent=4) # model_dump() transforms the Pydantic model to a dict for JSON file