import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from config.mongo import db

from .schema import build_notification

logger = logging.getLogger(__name__)


def _push_to_websocket(user_id, document):
    try:
        channel_layer = get_channel_layer()
        document_copy = {**document, "_id": str(document.get("_id", "")), "created_at": document["created_at"].isoformat()}

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {"type": "notify", "data": document_copy},
        )
        logger.info(f"WS_PUSH | user_id={user_id} | status=success")
    except Exception as e:
        logger.error(f"WS_PUSH | user_id={user_id} | status=failed | reason={e!s}")


def create_notification(user_id, email, notification_type, stock_symbol, message):
    try:
        document = build_notification(user_id, email, notification_type, stock_symbol, message)
        db.notifications.insert_one(document)
        logger.info(f"NOTIFICATION_CREATE | email={email} | type={notification_type} | symbol={stock_symbol} | status=success")

        _push_to_websocket(user_id, document)

        return document
    except Exception as e:
        logger.error(f"NOTIFICATION_CREATE | email={email} | type={notification_type} | symbol={stock_symbol} | status=failed | reason={e!s}")
        return None
