from typing import ClassVar

from rest_framework import serializers

from .models import WatchlistItem


class WatchlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistItem
        fields: ClassVar[list] = ["id", "stock_symbol", "date_added"]
        read_only_fields: ClassVar[list] = ["id", "date_added"]


class AddWatchlistItemSerializer(serializers.Serializer):
    stock_symbol = serializers.CharField(max_length=10)

    def validate_stock_symbol(self, value):
        return value.upper().strip()
