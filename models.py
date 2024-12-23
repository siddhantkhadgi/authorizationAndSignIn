from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class InputTokenRequest(BaseModel):
    token: str
