import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("stockpeek")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "refresh-watchlisted-stock-prices": {
        "task": "stocks.tasks.refresh_watchlisted_stock_prices",
        "schedule": settings.CACHE_TTL_STOCK_PRICE,
    },
    "refresh-stale-insights": {
        "task": "stocks.tasks.refresh_stale_insights",
        "schedule": settings.INSIGHT_REFRESH_INTERVAL,
    },
    "record-daily-stock-price-snapshot": {
        "task": "stocks.tasks.record_daily_stock_price_snapshot",
        "schedule": settings.PRICE_SNAPSHOT_INTERVAL,
    },
    "detect-monthly-drops": {
        "task": "stocks.tasks.detect_monthly_drops",
        "schedule": settings.PRICE_SNAPSHOT_INTERVAL,
    },
}
