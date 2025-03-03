from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.brand import Brand
from app.models.campaign import Campaign
from app.services.budget_service import BudgetService


class CampaignService:
    @classmethod
    async def update_campaign_spend(
        cls, brand_id: int, campaign_id: int, amount: float, db: AsyncSession
    ):
        campaign = await Campaign.get(campaign_id, db)
        if not campaign:
            return {"success": False, "message": "Campaign not found"}

        brand = await Brand.get(campaign.brand_id, db)
        if not brand:
            return {"success": False, "message": "Brand not found"}

        if campaign.brand_id != brand_id:
            return {
                "success": False,
                "message": "Unauthorized: This campaign does not belong to the brand.",
            }

        if not cls.is_within_active_hours(campaign):
            return {
                "success": False,
                "message": "Campaign is not available at this time.",
            }

        if brand.monthly_spent + amount > brand.monthly_budget:
            return {
                "success": False,
                "message": "Amount provided is greater than available monthly limit.",
            }

        if brand.daily_spent + amount > brand.daily_budget:
            return {
                "success": False,
                "message": "Amount provided is greater than available daily limit.",
            }

        brand.daily_spent += amount
        brand.monthly_spent += amount
        await BudgetService.pause_campaigns_if_budget_exceeded(brand.id, db)

        await db.commit()
        return {
            "success": True,
            "message": "Spend updated successfully.",
        }

    def is_within_active_hours(campaign) -> bool:
        """Check if the campaign is within its allowed time window."""
        if campaign.dayparting_start is None or campaign.dayparting_end is None:
            return True
        current_hour = datetime.now().hour
        return campaign.dayparting_start <= current_hour < campaign.dayparting_end
