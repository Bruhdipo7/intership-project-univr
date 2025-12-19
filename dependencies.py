from fastapi import Request
import crud

# get current user
async def get_current_user(request: Request):
    token = request.cookies.get("session_token")

    if not token:
        return None
    
    user = crud.get_user(token)
    return user

# get current org
async def get_current_org(request: Request):
    token = request.cookies.get("session_token")

    if not token:
        return None
    
    org = crud.get_organization(token)
    return org