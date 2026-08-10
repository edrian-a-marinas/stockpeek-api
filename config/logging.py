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

    return results


def log_startup():
    logger.info(f"APP    | debug={settings.DEBUG} | env loaded")
    logger.info(f"Server | DB={get_db_label()} | mongo={get_mongo_label()} | env loaded")
    conns = check_connections()
    logger.info(f"Conn   | db={conns['db']} | mongo={conns['mongo']}")
