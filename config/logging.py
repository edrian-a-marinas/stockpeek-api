import logging

from django.conf import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(name)s - %(message)s",
)
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger("config.startup")


def get_db_label() -> str:
    db_host = settings.DATABASES["default"].get("HOST", "")
    if "localhost" in db_host or "127.0.0.1" in db_host or not db_host:
        return "DEV"
    return "PROD"


def get_frontend_label() -> str:
    if "localhost" in settings.ALLOWED_ORIGINS or "127.0.0.1" in settings.ALLOWED_ORIGINS:
        return "DEV"
    return "PROD"


def get_celery_label() -> str:
    if "localhost" in settings.REDIS_URL or "127.0.0.1" in settings.REDIS_URL:
        return "DEV"
    return "PROD"


def get_mongo_label() -> str:
    mongo_url = settings.MONGO_URL
    if "localhost" in mongo_url or "127.0.0.1" in mongo_url:
        return "DEV"
    return "PROD"


def check_connections() -> dict:
    results = {}

    try:
        connections["default"].cursor()
        results["db"] = "connected"
    except OperationalError:
        results["db"] = "unreachable"

    try:
        from config.mongo import client

        client.admin.command("ping")
        results["mongo"] = "connected"
    except Exception:
        results["mongo"] = "unreachable"

    try:
        import redis

        redis.from_url(settings.REDIS_CACHE_URL).ping()
        results["cache"] = "connected"
    except Exception:
        results["cache"] = "unreachable"

    try:
        import redis

        redis.from_url(settings.REDIS_URL).ping()
        results["broker"] = "connected"
    except Exception:
        results["broker"] = "unreachable"

    try:
        from config.celery import app as celery_app

        with celery_app.connection() as conn:
            conn.ensure_connection(max_retries=1)
        results["celery"] = "connected"
    except Exception:
        results["celery"] = "unreachable"

    return results


def log_startup():
    logger.info(f"APP    | ratelimit_enabled={settings.RATELIMIT_ENABLED} | debug={settings.DEBUG} | env loaded")
    logger.info(
        f"Server | DB={get_db_label()} | frontend={get_frontend_label()} | celery={get_celery_label()} | mongo={get_mongo_label()} | env loaded"
    )
    conns = check_connections()
    logger.info(f"Conn   | db={conns['db']} | broker={conns['broker']} | cache={conns['cache']} | celery={conns['celery']} | mongo={conns['mongo']}")
