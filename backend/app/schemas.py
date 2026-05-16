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

# @trace TASK-016
from datetime import datetime
from typing import Optional

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    party_size: int
    party_level: int

class CampaignCreate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    id: int
    gm_user_id: int
    share_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CampaignShareResponse(BaseModel):
    share_url: str

# @trace TASK-021
from typing import Any

class AssetBase(BaseModel):
    asset_type: str
    name: str
    description: Optional[str] = None
    traits: Optional[list[str]] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    tick_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class EncounterBase(BaseModel):
    mechanical_data: dict[str, Any]
    gm_narrative: Optional[str] = None

class EncounterCreate(EncounterBase):
    pass

class EncounterResponse(EncounterBase):
    id: int
    asset_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class TickBase(BaseModel):
    narrative: Optional[str] = None

# @trace TASK-022
class TickCreate(TickBase):
    campaign_id: int

class TickResponse(TickBase):
    id: int
    campaign_id: int
    tick_number: int
    created_at: datetime
    updated_at: datetime
    assets: List[AssetResponse] = []
    
    model_config = {"from_attributes": True}

class TimelineData(BaseModel):
    campaign_id: int
    is_owner: bool = False
    ticks: List[TickResponse]

