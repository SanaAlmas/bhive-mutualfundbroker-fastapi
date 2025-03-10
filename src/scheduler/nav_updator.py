from celery.schedules import crontab
from celery import Celery
import requests
from config import config_obj

c_app = Celery("celery", broker=config_obj.REDIS_URL, backend=config_obj.REDIS_URL, broker_connection_retry_on_startup=True)
c_app.config_from_object(config_obj)

# celery beat config
c_app.conf.beat_schedule = {
    "update-nav-hourly": {
        "task": "src.scheduler.nav_updator.fetch_investments",
        "schedule": crontab(minute=0, hour="*"),  # Runs every 1 hour
    },
}

c_app.conf.timezone = "UTC"

# API URL for NAV updates
API_URL = f"http://localhost:8000/mfb/investment/update-all-navs"

@c_app.task(name="src.scheduler.nav_updator.fetch_investments", autoretry_for=(requests.RequestException,), retry_kwargs={"max_retries": 3, "countdown": 60})
def fetch_investments():
    try:
        response = requests.post(API_URL, timeout=15)
        response.raise_for_status()
        nav_data = response.json()
        return nav_data
    except requests.RequestException as req_err:
        raise fetch_investments.retry(exc=req_err)
    except Exception as unexpected_err:
        raise unexpected_err