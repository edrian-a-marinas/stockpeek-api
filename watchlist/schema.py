from django.utils import timezone


def build_activity_log(user_id, email, action, stock_symbol):
    return {
        "user_id": user_id,
        "email": email,
        "action": action,
        "stock_symbol": stock_symbol,
        "timestamp": timezone.now(),
    }
