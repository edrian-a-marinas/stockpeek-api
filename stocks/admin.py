from django.contrib import admin

from .models import StockInsight, StockPrice

admin.site.register(StockPrice)
admin.site.register(StockInsight)
