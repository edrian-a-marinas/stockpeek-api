import logging

from celery import shared_task

from watchlist.models import WatchlistItem

from .ai import generate_insight_text, parse_insight_sections
from .models import StockInsight
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


@shared_task
def generate_insight_for_stock(stock_symbol):
    if StockInsight.objects.filter(stock_symbol=stock_symbol).exists():
        logger.info(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=skipped | reason=already exists")
        return

    content = generate_insight_text(stock_symbol)
    if content is None:
        logger.warning(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=failed | reason=no content returned")
        return

    sections = parse_insight_sections(content)

    StockInsight.objects.create(
        stock_symbol=stock_symbol,
        company_overview=sections["overview"],
        long_term_relevance=sections["relevance"],
        risks=sections["risks"],
    )
    logger.info(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=success")
