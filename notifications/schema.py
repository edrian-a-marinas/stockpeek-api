from django.utils import timezone

from .choices import NotificationType


def build_notification(user_id, email, notification_type, stock_symbol, message):
    if notification_type not in NotificationType.values:
        raise ValueError(f"Invalid notification type: {notification_type}")

    return {
        "user_id": user_id,
        "email": email,
        "type": notification_type,
        "stock_symbol": stock_symbol,
        "message": message,
        "is_read": False,
        "created_at": timezone.now(),
    }
