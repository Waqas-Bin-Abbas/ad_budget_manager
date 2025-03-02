from fastapi import APIRouter

from .brand_routes import brands_bp
from .campaign_routes import campaign_bp

router = APIRouter()

router.include_router(brands_bp)
router.include_router(campaign_bp)


@router.get("/")
def root():
    return {"message": "Hello, World!"}
