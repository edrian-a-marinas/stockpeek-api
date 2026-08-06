from django.contrib import admin

from .models import StockNote, WatchlistItem

admin.site.register(WatchlistItem)
admin.site.register(StockNote)
