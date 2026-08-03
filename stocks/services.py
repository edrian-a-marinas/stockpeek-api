import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def fetch_stock_price(stock_symbol):
    try:
        response = requests.get(
            f"{settings.TWELVE_DATA_BASE_URL}/price",
            params={"symbol": stock_symbol, "apikey": settings.TWELVE_DATA_API_KEY},
            timeout=5,
        )
        data = response.json()

        if "price" not in data:
            logger.warning(f"STOCK_FETCH | symbol={stock_symbol} | status=failed | reason={data.get('message', 'unknown error')}")
            return None

        logger.info(f"STOCK_FETCH | symbol={stock_symbol} | price={data['price']} | status=success")
        return data["price"]
    except requests.RequestException as e:
        logger.error(f"STOCK_FETCH | symbol={stock_symbol} | status=failed | reason={e!s}")
        return None
