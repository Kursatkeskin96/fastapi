from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel): 
    firstname: str
    lastname: str
    email: EmailStr
    conference_name: str
    conference_location: str
    conference_detail: str
    conference_date: str
    status: str

class PostCreate(PostBase):
    pass 

# response
class Post(BaseModel):
    id: int
    firstname: str
    lastname: str
    conference_name: str
    conference_location: str
    conference_detail: str
    conference_date: str
    status: str
    created_at: datetime

    class Config:
        from_attributes=True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes=True

# response
class UserOut(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime
    class Config:
        from_attributes=True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
