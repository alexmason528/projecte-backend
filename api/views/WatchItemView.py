from rest_framework import generics

from api.models import WatchItem

from api.serializers import WatchItemListSerializer, WatchItemCreateSerializer

from utils.pagination import StandardResultsSetPagination


class WatchItemView(generics.ListCreateAPIView, generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return WatchItemCreateSerializer
        return WatchItemListSerializer

    def get_queryset(self):
        if self.request.method in ['POST']:
            return WatchItem.objects.filter(user=self.request.user)
        return self.request.user.watchlist.select_related('item').all()


class WatchItemDestroyView(generics.DestroyAPIView, generics.GenericAPIView):
    lookup_field = 'item'

    def get_queryset(self):
        return WatchItem.objects.filter(user=self.request.user)
