from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.campaign import Campaign
from app.services.campaign_service import CampaignService

campaign_bp = APIRouter()


@campaign_bp.get("/campaigns/")
async def get_campaigns(db: Session = Depends(get_db)):
    try:
        campaigns = await Campaign.get_all(db)
        return campaigns
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching campaign: {str(e)}"
        )


@campaign_bp.post("/campaigns/")
async def create_campaign(
    name: str,
    brand_id: int,
    dayparting_start_hour: int = None,
    dayparting_end_hour: int = None,
    db: Session = Depends(get_db),
):
    if not dayparting_end_hour >= dayparting_start_hour:
        return JSONResponse(
            status_code=400,
            content={"detail": f"Error creating campaign: Invalid dayparting hours."},
        )
    campaign = Campaign(
        name=name,
        brand_id=brand_id,
        dayparting_start=dayparting_start_hour,
        dayparting_end=dayparting_end_hour,
    )
    try:
        await campaign.save(db)

        return campaign

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error creating campaign: {str(e)}"
        )


class CampaignSpendRequest(BaseModel):
    brand_id: int
    amount: float


@campaign_bp.post("/campaigns/{campaign_id}/spend")
async def campaign_spend(
    campaign_id: int, request: CampaignSpendRequest, db: Session = Depends(get_db)
):
    result = await CampaignService.update_campaign_spend(
        request.brand_id, campaign_id, request.amount, db
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
