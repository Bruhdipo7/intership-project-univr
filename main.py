from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from config import templates

from routers import user, org, guest

app = FastAPI()

# Setting static materials (CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Linking routers to main file
app.include_router(user.router)
app.include_router(org.router)
app.include_router(guest.router)

### --- Root --- ###
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

### --- Logout --- ###
@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    # Delete current session
    response.set_cookie(key="session_token", value="", path="/", httponly=True, max_age=0)
    return response