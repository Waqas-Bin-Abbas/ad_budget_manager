from datetime import time
from typing import List, Optional

from pydantic import BaseModel
from pydantic import Field


class CampaignBase(BaseModel):
    name: str = Field(..., example="Campaign")
    brand_id: int
    start_hour: Optional[time] = None
    end_hour: Optional[time] = None
    is_active: bool = True


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    is_active: Optional[bool] = None
    start_hour: Optional[time] = None
    end_hour: Optional[time] = None


class CampaignResponse(CampaignBase):
    id: int

    class Config:
        from_attributes = True
