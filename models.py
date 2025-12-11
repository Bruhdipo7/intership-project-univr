from pydantic import BaseModel, EmailStr
from typing import Optional

# Questo modello definisce cosa ci aspettiamo di trovare nel JSON
class User(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    hashed_password: str