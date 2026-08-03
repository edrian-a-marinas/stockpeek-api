from django.urls import path

from .views import StockPriceView

urlpatterns = [
    path("<str:stock_symbol>/price/", StockPriceView.as_view(), name="stock-price"),
]
