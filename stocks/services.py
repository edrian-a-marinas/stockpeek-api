import logging

import requests
from django.conf import settings

from config.cache import get_cache, set_cache

logger = logging.getLogger(__name__)


def fetch_stock_price(stock_symbol):
    cache_key = f"stock_price:{stock_symbol}"
    cached_price = get_cache(cache_key)
    if cached_price is not None:
        logger.info(f"STOCK_FETCH | symbol={stock_symbol} | price={cached_price} | source=cache | status=success")
        return cached_price

    try:
        response = requests.get(
            f"{settings.TWELVE_DATA_BASE_URL}/price",
            params={"symbol": stock_symbol, "apikey": settings.TWELVE_DATA_API_KEY},
            timeout=5,
        )
        data = response.json()

        if "price" not in data:
            logger.warning(f"STOCK_FETCH | symbol={stock_symbol} | source=api | status=failed | reason={data.get('message', 'unknown error')}")
            return None

        price = data["price"]
        set_cache(cache_key, price, settings.CACHE_TTL_STOCK_PRICE)
        logger.info(f"STOCK_FETCH | symbol={stock_symbol} | price={price} | source=api | status=success")
        return price
    except requests.RequestException as e:
        logger.error(f"STOCK_FETCH | symbol={stock_symbol} | source=api | status=failed | reason={e!s}")
        return None
