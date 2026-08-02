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


def check_db_connection() -> str:
    try:
        connections["default"].cursor()
        return "connected"
    except OperationalError:
        return "unreachable"


def log_startup():
    logger.info(f"APP | debug={settings.DEBUG} | env loaded")
    logger.info(f"DB  | env={get_db_label()} | status={check_db_connection()}")
