from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StockPriceSerializer
from .services import fetch_stock_price


class StockPriceView(APIView):
    def get(self, request, stock_symbol):
        stock_symbol = stock_symbol.upper()
        result = fetch_stock_price(stock_symbol)

        if result is None:
            raise NotFound(f"Price not found for {stock_symbol}.")

        serializer = StockPriceSerializer({"stock_symbol": stock_symbol, "price": result["price"], "last_updated": result["last_updated"]})
        return Response(serializer.data, status=200)
