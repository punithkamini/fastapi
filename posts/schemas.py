from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr
from typing import Optional, List
from enum import Enum

class Posts(BaseModel):
    title: str
    content: str
    created_at: datetime = datetime.now()
    published: Optional[bool] = True


class ShowPosts(Posts):
    id: int
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Posts: Posts
    votes: int
    class Config:
        orm_mode=True

class OwnerPost(Posts):
    owner_id: int
    class Config:
        orm_mode=True


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    name: str
    class Config:
        orm_mode=True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None


class dir_vote(int, Enum):
    like= 1
    dislike= 0

class Votes(BaseModel):
    post_id: int
    dir: dir_vote
