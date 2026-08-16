import logging

from config.mongo import db

from .schema import build_activity_log

logger = logging.getLogger(__name__)


def log_activity(user_id, email, action, stock_symbol):
    try:
        document = build_activity_log(user_id, email, action, stock_symbol)
        db.activity_logs.insert_one(document)
        logger.info(f"ACTIVITY_LOG | email={email} | action={action} | symbol={stock_symbol} | status=success")
    except Exception as e:
        logger.error(f"ACTIVITY_LOG | email={email} | action={action} | symbol={stock_symbol} | status=failed | reason={e!s}")
