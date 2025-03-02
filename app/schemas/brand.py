from typing import List, Optional

from pydantic import BaseModel
from pydantic import Field

from .campaign import CampaignResponse


class BrandBase(BaseModel):
    name: str = Field(..., example="Nike")
    daily_budget: float = Field(..., gt=0, example=5000.0)
    monthly_budget: float = Field(..., gt=0, example=100000.0)


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    daily_budget: Optional[float] = Field(None, gt=0, example=6000.0)
    monthly_budget: Optional[float] = Field(None, gt=0, example=120000.0)


class BrandResponse(BrandBase):
    id: int
    daily_spent: float = 0.0
    monthly_spent: float = 0.0
    campaigns: List[CampaignResponse] = []

    class Config:
        from_attributes = True
