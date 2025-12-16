import json
import os
import pandas as pd
from models import User, Organization

DATA_DIR_USERS = "data/users"
os.makedirs(DATA_DIR_USERS, exist_ok=True)

DATA_DIR_ORGS = "data/organizations"
os.makedirs(DATA_DIR_ORGS, exist_ok=True)

### --- User CRUD operations --- ###
def get_json_path(username: str) -> str:
    safe_name = username.lower().strip()
    return os.path.join(DATA_DIR_USERS, f"{safe_name}.json")

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

### --- Organization CRUD operations --- ###
def get_json_path_org(username: str) -> str:
    safe_name = username.lower().strip()
    return os.path.join(DATA_DIR_ORGS, f"{safe_name}.json")

def get_organization(username: str) -> Organization | None:
    path = get_json_path_org(username)
    if not os.path.exists(path):
        return None
    
    with open(path, "r") as f:
        data = json.load(f)
        return Organization(**data)

def create_organization(org: Organization):
    path = get_json_path_org(org.username)
    if os.path.exists(path):
        raise ValueError("Organization already exists")
    
    with open(path, "w") as f:
        json.dump(org.model_dump(), f, indent=4) # model_dump() transforms the Pydantic model to a dict for JSON file

### --- Extract skills by user input --- ###
def extracting_skills(target_role: str) -> dict[str:str] | None:
    # reading Excel file, only columns C (function title) and E (Required skills)
    try: 
        df = pd.read_excel("data/ISCO-08 EN Structure and definitions.xlsx", usecols="C,D")

        col_title = df.columns[0]
        col_definition = df.columns[1]

        # filtering rows, converting to string, case insensitive search
        filter = df[col_title].astype(str).str.contains(target_role, case=False, na=False)
        results = df[filter]

        if not results.empty:
            roles_dict = dict(zip(results[col_title], results[col_definition]))
            return roles_dict
        else:
            return None
    except Exception as e:
        print(f"Error extracting skills: {e}")
        return None