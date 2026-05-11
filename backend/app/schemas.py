# @trace TASK-011
# @trace TASK-012
from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    message: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserDetail(BaseModel):
    id: int
    username: str
    email: str
    status: str
    role: str

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserDetail]

class UserStatusUpdate(BaseModel):
    status: str

class UserStatusResponse(BaseModel):
    user_id: str
    status: str
