from django.db import models


class StockPrice(models.Model):
    stock_symbol = models.CharField(max_length=10, unique=True)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock_symbol}: {self.current_price}"


class StockPriceHistory(models.Model):
    stock_symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_at = models.DateField()

    class Meta:
        unique_together = ("stock_symbol", "recorded_at")

    def __str__(self):
        return f"{self.stock_symbol} @ {self.recorded_at}: {self.price}"


class StockInsight(models.Model):
    stock_symbol = models.CharField(max_length=10, unique=True)
    company_overview = models.TextField()
    long_term_relevance = models.TextField()
    risks = models.TextField()
    generated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insight for {self.stock_symbol}"
