from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.brand import Brand

brands_bp = APIRouter()


@brands_bp.get("/brands/")
async def get_brands(db: AsyncSession = Depends(get_db)):
    try:
        brands = await Brand.get_all(db)
        return brands
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching brands: {str(e)}")


@brands_bp.post("/brands/")
async def create_brand(
    name: str,
    daily_budget: float,
    monthly_budget: float,
    db: AsyncSession = Depends(get_db),
):
    brand = Brand(name=name, daily_budget=daily_budget, monthly_budget=monthly_budget)

    try:
        await brand.save(db)

        return brand

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating brand: {str(e)}")
