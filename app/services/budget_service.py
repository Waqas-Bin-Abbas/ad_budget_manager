from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.brand import Brand


class BudgetService:

    @classmethod
    async def pause_campaigns_if_budget_exceeded(cls, brand_id: int, db: AsyncSession):
        """Pauses all campaigns if the daily or monthly budget for a specific brand has been exceeded."""
        result = await db.execute(
            select(Brand)
            .options(selectinload(Brand.campaigns))
            .filter(Brand.id == brand_id)
        )
        brand = result.scalar_one()
        if (
            brand.daily_spent >= brand.daily_budget
            or brand.monthly_spent >= brand.monthly_budget
        ):
            campaigns = brand.campaigns
            for campaign in campaigns:
                campaign.is_active = False
            await db.commit()

    @classmethod
    async def activate_campaigns(cls, db: AsyncSession):
        """Activate all campaigns if the daily or monthly budget for a specific brand is available."""
        result = await db.execute(select(Brand).options(selectinload(Brand.campaigns)))

        brands = result.scalars().all()

        for brand in brands:
            if (
                brand.daily_budget > brand.daily_spent
                and brand.monthly_budget > brand.monthly_spent
            ):
                for campaign in brand.campaigns:
                    campaign.is_active = True

                await db.commit()
            else:
                print(
                    f"Brand {brand.id} has exceeded its budget, campaigns not activated."
                )

    @classmethod
    async def reset_daily_budgets(cls, db: AsyncSession):
        """
        Resets the daily spend of all brands at the start of a new day.
        """
        brands = await Brand.get_all(db)
        for brand in brands:
            brand.daily_spent = 0
        await db.commit()
        print(f"[{datetime.now()}] Daily budgets have been reset.")

    @classmethod
    async def reset_monthly_budgets(cls, db: AsyncSession):
        """
        Resets the monthly spend of all brands at the start of a new month.
        """
        brands = await Brand.get_all()
        for brand in brands:
            brand.monthly_spent = 0
        await db.commit()
        print(f"[{datetime.now()}] Monthly budgets have been reset.")
