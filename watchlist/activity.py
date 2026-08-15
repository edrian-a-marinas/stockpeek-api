import logging

from django.utils import timezone

from config.mongo import db

logger = logging.getLogger(__name__)


def log_activity(user_id, email, action, stock_symbol):
    try:
        db.activity_logs.insert_one(
            {
                "user_id": user_id,
                "email": email,
                "action": action,
                "stock_symbol": stock_symbol,
                "timestamp": timezone.now(),
            }
        )
        logger.info(f"ACTIVITY_LOG | email={email} | action={action} | symbol={stock_symbol} | status=success")
    except Exception as e:
        logger.error(f"ACTIVITY_LOG | email={email} | action={action} | symbol={stock_symbol} | status=failed | reason={e!s}")
