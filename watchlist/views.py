from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AddWatchlistItemSerializer, WatchlistItemSerializer
from .services import add_to_watchlist, list_watchlist, remove_from_watchlist


class WatchlistView(APIView):
    def get(self, request):
        items = list_watchlist(request.user)
        serializer = WatchlistItemSerializer(items, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = AddWatchlistItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = add_to_watchlist(request.user, serializer.validated_data["stock_symbol"], request)
        return Response(WatchlistItemSerializer(item).data, status=201)


class WatchlistDetailView(APIView):
    def delete(self, request, stock_symbol):
        remove_from_watchlist(request.user, stock_symbol.upper(), request)
        return Response(status=204)
