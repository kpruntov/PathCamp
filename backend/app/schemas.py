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
    role: str

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


class TickBase(BaseModel):
    narrative: Optional[str] = None


class TickCreate(BaseModel):
    campaign_id: int
    narrative: Optional[str] = None


class Tick(TickBase):
    id: int
    campaign_id: int
    tick_number: int

    class Config:
        from_attributes = True


class AssetBase(BaseModel):
    asset_type: str
    name: str
    description: Optional[str] = None
    traits: Optional[dict] = None


class AssetCreate(AssetBase):
    tick_id: int


class Asset(AssetBase):
    id: int
    tick_id: int

    class Config:
        from_attributes = True


class ShareLink(BaseModel):
    share_url: str


class CampaignPublic(CampaignBase):
    id: int
    name: str
    description: Optional[str] = None
    party_size: int
    party_level: int

    class Config:
        from_attributes = True


# @trace TASK-007
# @trace TASK-008
# @trace TASK-012
# @trace TASK-014
# @trace TASK-013
# @trace TASK-010
