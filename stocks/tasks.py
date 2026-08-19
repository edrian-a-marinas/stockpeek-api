import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from notifications.choices import NotificationType
from notifications.services import create_notification
from watchlist.models import WatchlistItem

from .ai import generate_insight_text, parse_insight_sections
from .models import StockInsight, StockPriceHistory
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
def record_daily_stock_price_snapshot():
    symbols = WatchlistItem.objects.values_list("stock_symbol", flat=True).distinct()
    if not symbols:
        logger.info("PRICE_SNAPSHOT | status=skipped | reason=no watchlisted symbols")
        return
    today = timezone.now().date()
    count = 0
    for symbol in symbols:
        result = fetch_stock_price(symbol)
        if result is None:
            logger.warning(f"PRICE_SNAPSHOT | symbol={symbol} | status=failed | reason=no price returned")
            continue
        StockPriceHistory.objects.update_or_create(
            stock_symbol=symbol,
            recorded_at=today,
            defaults={"price": result["price"]},
        )
        count += 1
    logger.info(f"PRICE_SNAPSHOT | date={today} | count={count} | status=success")


@shared_task
def generate_insight_for_stock(stock_symbol):
    existing = StockInsight.objects.filter(stock_symbol=stock_symbol).first()

    if existing:
        stale_cutoff = timezone.now() - timedelta(days=settings.INSIGHT_STALE_DAYS)
        if existing.generated_at > stale_cutoff:
            logger.info(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=skipped | reason=not stale yet")
            return

    content = generate_insight_text(stock_symbol)
    if content is None:
        logger.warning(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=failed | reason=no content returned")
        return

    sections = parse_insight_sections(content)

    if existing:
        existing.long_term_relevance = sections["relevance"]
        existing.risks = sections["risks"]
        existing.save()
        logger.info(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=success | action=refreshed")
    else:
        StockInsight.objects.create(
            stock_symbol=stock_symbol,
            company_overview=sections["overview"],
            long_term_relevance=sections["relevance"],
            risks=sections["risks"],
        )
        logger.info(f"INSIGHT_GENERATE | symbol={stock_symbol} | status=success | action=created")


@shared_task
def refresh_stale_insights():
    symbols = StockInsight.objects.values_list("stock_symbol", flat=True)
    for symbol in symbols:
        generate_insight_for_stock(symbol)


def _get_price_30_days_ago(symbol, cutoff_date):
    return StockPriceHistory.objects.filter(stock_symbol=symbol, recorded_at__lte=cutoff_date).order_by("-recorded_at").first()


def _calculate_drop_percent(old_price, current_price):
    return (float(old_price) - float(current_price)) / float(old_price) * 100


def _notify_watchers(symbol, drop_percent):
    watchers = WatchlistItem.objects.filter(stock_symbol=symbol).select_related("user")
    for item in watchers:
        message = f"{symbol} dropped {drop_percent:.1f}% over the past 30 days."
        create_notification(
            user_id=item.user.id,
            email=item.user.email,
            notification_type=NotificationType.DROP_ALERT,
            stock_symbol=symbol,
            message=message,
        )
    return watchers.count()


@shared_task
def detect_monthly_drops():
    cutoff_date = timezone.now().date() - timedelta(days=30)
    symbols = WatchlistItem.objects.values_list("stock_symbol", flat=True).distinct()
    if not symbols:
        logger.info("DROP_DETECT | status=skipped | reason=no watchlisted symbols")
        return
    alerted_count = 0
    for symbol in symbols:
        old_snapshot = _get_price_30_days_ago(symbol, cutoff_date)
        if old_snapshot is None:
            logger.info(f"DROP_DETECT | symbol={symbol} | status=skipped | reason=no snapshot 30 days ago")
            continue
        current = fetch_stock_price(symbol)
        if current is None:
            logger.warning(f"DROP_DETECT | symbol={symbol} | status=failed | reason=no current price")
            continue
        drop_percent = _calculate_drop_percent(old_snapshot.price, current["price"])
        if drop_percent < settings.MONTHLY_DROP_THRESHOLD_PERCENT:
            continue
        watcher_count = _notify_watchers(symbol, drop_percent)
        alerted_count += 1
        logger.info(f"DROP_DETECT | symbol={symbol} | drop_percent={drop_percent:.1f} | watchers={watcher_count} | status=alerted")
    logger.info(f"DROP_DETECT | symbols_checked={len(symbols)} | symbols_alerted={alerted_count} | status=success")
