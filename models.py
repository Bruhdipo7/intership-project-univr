from pydantic import BaseModel, EmailStr
from typing import Optional

# Questo modello definisce cosa ci aspettiamo di trovare nel JSON
class User(BaseModel):
    name: str
    surname: str
    username: str
    # email: Optional[EmailStr] = None
    hashed_password: str
    # is_active: bool = True