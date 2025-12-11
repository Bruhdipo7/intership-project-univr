from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from pydantic import EmailStr

import crud
from models import User

app = FastAPI()

# Monta la cartella "static" per servire CSS e immagini
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura la cartella dei template
templates = Jinja2Templates(directory="templates")

# Sicurezza password
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    error_message = request.cookies.get("flash_error")

    response = templates.TemplateResponse("authentication.html", {
        "request": request,
        "error": error_message
    })
    
    if request.cookies.get("session_token"):
        response.delete_cookie("session_token", path="/", httponly=True)
    if error_message:
        response.delete_cookie("flash_error")

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

### --- Authentication Endpoints --- ###
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = crud.get_user(username)

    if not user or not pwd_context.verify(password, user.hashed_password):
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
        response.set_cookie(key="flash_error", value="Invalid credentials. Please try again.")
        return response

    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

    response.set_cookie(key="session_token", value=username, path="/", httponly=True)

    return response

### --- Home Endpoints --- ###
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    cookie_username = request.cookies.get("session_token")
    if not cookie_username:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    current_user = crud.get_user(cookie_username)
    # If logged in, show home page
    response = templates.TemplateResponse("home.html", {"request": request, "user": current_user}) 

    return response

@app.get("/guest_home", response_class=HTMLResponse)
async def gust_home(request: Request):
    return templates.TemplateResponse("guest_home.html", {"request": request})

### --- Registration Endpoints --- ###
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request, 
    name: str = Form(...),
    surname: str = Form(...),
    email: EmailStr = Form(...), 
    username: str = Form(...), 
    password: str = Form(...)
):
    hashed_pw = pwd_context.hash(password)
    new_user = User(name=name, surname=surname, email=email, username=username, hashed_password=hashed_pw)
    try:
        crud.create_user(new_user)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username already exists. Please choose another."
        })

### --- Logout Endpoint --- ###
@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    # Delete current session
    response.delete_cookie(key="session_token", path="/", httponly=True)
    
    # Not allow cahing of logged in pages
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response