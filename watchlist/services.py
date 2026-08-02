import logging

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from config import settings

from .models import StockNote, WatchlistItem

logger = logging.getLogger(__name__)

MAX_WATCHLIST_ITEMS = settings.MAX_WATCHLIST_ITEMS


def list_watchlist(user):
    return WatchlistItem.objects.filter(user=user).order_by("-date_added")


def add_to_watchlist(user, stock_symbol, request):
    ip = request.META.get("REMOTE_ADDR")
    count = WatchlistItem.objects.filter(user=user).count()

    if count >= MAX_WATCHLIST_ITEMS:
        logger.warning(f"WATCHLIST_ADD | email={user.email} | ip={ip} | symbol={stock_symbol} | status=failed | reason=max limit reached")
        raise ValidationError(f"Watchlist limit reached (max {MAX_WATCHLIST_ITEMS}).")

    try:
        item = WatchlistItem.objects.create(user=user, stock_symbol=stock_symbol)
        logger.info(f"WATCHLIST_ADD | email={user.email} | ip={ip} | symbol={stock_symbol} | status=success")
        return item
    except IntegrityError:
        logger.warning(f"WATCHLIST_ADD | email={user.email} | ip={ip} | symbol={stock_symbol} | status=failed | reason=already in watchlist")
        raise ValidationError("Stock already in your watchlist.")


def remove_from_watchlist(user, stock_symbol, request):
    ip = request.META.get("REMOTE_ADDR")
    deleted, _ = WatchlistItem.objects.filter(user=user, stock_symbol=stock_symbol).delete()

    if deleted == 0:
        logger.warning(f"WATCHLIST_REMOVE | email={user.email} | ip={ip} | symbol={stock_symbol} | status=failed | reason=not found")
        raise ValidationError("Stock not found in your watchlist.")

    logger.info(f"WATCHLIST_REMOVE | email={user.email} | ip={ip} | symbol={stock_symbol} | status=success")


def save_note(user, stock_symbol, note_text, request):
    ip = request.META.get("REMOTE_ADDR")
    try:
        item = WatchlistItem.objects.get(user=user, stock_symbol=stock_symbol)
    except WatchlistItem.DoesNotExist:
        logger.warning(f"NOTE_SAVE | email={user.email} | ip={ip} | symbol={stock_symbol} | status=failed | reason=not in watchlist")
        raise ValidationError("Stock not found in your watchlist.")

    note, created = StockNote.objects.update_or_create(watchlist_item=item, defaults={"note_text": note_text})
    action = "created" if created else "updated"
    logger.info(f"NOTE_SAVE | email={user.email} | ip={ip} | symbol={stock_symbol} | action={action} | status=success")
    return note
