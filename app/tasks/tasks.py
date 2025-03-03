from celery import Celery
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.budget_service import BudgetService

from app.core.config import settings

celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)


@celery.task
def run_campaign_reset(db: Session = Depends(get_db)):
    """Trigger daily budget reset using Celery"""
    BudgetService.activate_campaigns(db)
    db.close()
    print("[Celery] Daily reset executed.")


@celery.task
def run_daily_reset(db: Session = Depends(get_db)):
    """Trigger daily budget reset using Celery"""
    BudgetService.reset_daily_budgets(db)
    db.close()
    print("[Celery] Daily reset executed.")


@celery.task
def run_monthly_reset(db: Session = Depends(get_db)):
    """Trigger monthly budget reset using Celery"""
    BudgetService.reset_monthly_budgets(db)
    db.close()
    print("[Celery] Monthly reset executed.")
