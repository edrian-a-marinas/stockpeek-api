from rest_framework import serializers


class StockPriceSerializer(serializers.Serializer):
    stock_symbol = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=6)
