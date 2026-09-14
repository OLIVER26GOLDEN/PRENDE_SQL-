from pydantic import BaseModel, EmailStr, Field
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ProgressOut(BaseModel):
    xp: int
    streak: int
    completed_levels: List[int]

    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    xp: int
    streak: int
    completed_levels: List[int]
