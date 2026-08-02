from django.urls import path

from .views import WatchlistDetailView, WatchlistView

urlpatterns = [
    path("", WatchlistView.as_view(), name="watchlist-list"),
    path("<str:stock_symbol>/", WatchlistDetailView.as_view(), name="watchlist-detail"),
]
