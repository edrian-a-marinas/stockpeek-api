import logging

from celery import shared_task

from watchlist.models import WatchlistItem

from .services import fetch_stock_price

logger = logging.getLogger(__name__)


@shared_task
def refresh_watchlisted_stock_prices():
    symbols = WatchlistItem.objects.values_list("stock_symbol", flat=True).distinct()

    if not symbols:
        logger.info("STOCK_REFRESH | status=skipped | reason=no watchlisted symbols")
        return

    for symbol in symbols:
        fetch_stock_price(symbol, force=True)

    logger.info(f"STOCK_REFRESH | count={len(symbols)} | status=success")
