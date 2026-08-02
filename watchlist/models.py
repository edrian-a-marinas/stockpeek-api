from django.conf import settings
from django.db import models


class WatchlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist_items")
    stock_symbol = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "stock_symbol")

    def __str__(self):
        return f"{self.user} - {self.stock_symbol}"


class StockNote(models.Model):
    watchlist_item = models.OneToOneField(WatchlistItem, on_delete=models.CASCADE, related_name="note")
    note_text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.watchlist_item.stock_symbol}"
