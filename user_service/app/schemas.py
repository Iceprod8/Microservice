from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserPreferenceCreate(BaseModel):
    id_genre: int

class User(BaseModel):
    uid: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
