from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    status: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    party_size: int
    party_level: int


class CampaignCreate(CampaignBase):
    pass


class Campaign(CampaignBase):
    id: int
    gm_user_id: int

    class Config:
        from_attributes = True


# @trace TASK-007
# @trace TASK-008
# @trace TASK-012
