from celery.schedules import crontab
from tasks import celery, run_daily_reset, run_monthly_reset, run_campaign_reset

celery.conf.beat_schedule = {
    "reset-daily-budgets": {
        "task": "tasks.run_campaign_reset",
        "schedule": crontab(hour=0, minute=0),  # Runs every midnight
    },
    "reset-daily-budgets": {
        "task": "tasks.run_daily_reset",
        "schedule": crontab(hour=0, minute=0),  # Runs every midnight
    },
    "reset-monthly-budgets": {
        "task": "tasks.run_monthly_reset",
        "schedule": crontab(
            day_of_month=1, hour=0, minute=0
        ),  # Runs on 1st day of the month
    },
}

celery.conf.timezone = "UTC"
