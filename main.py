from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

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
    return templates.TemplateResponse("authentication.html", {"request": request})

### --- Authentication Endpoints --- ###
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = crud.get_user(username)

    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse("authentication.html", {
            "request": request, 
            "error": "Invalid credentials. Please try again."
        })

    return RedirectResponse(url=f"/home?user={username}", status_code=status.HTTP_303_SEE_OTHER)

### --- Home Endpoints --- ###
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, user: str):
    return templates.TemplateResponse("home.html", {"request": request, "user": user})

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
    username: str = Form(...), 
    password: str = Form(...)
):
    hashed_pw = pwd_context.hash(password)
    new_user = User(name=name, surname=surname, username=username, hashed_password=hashed_pw)
    try:
        crud.create_user(new_user)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username already exists. Please choose another."
        })