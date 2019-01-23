from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from api.models import WatchItem, Item

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
    lookup_field = 'slug'

    def delete(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        watchitem = get_object_or_404(WatchItem, item=item)
        watchitem.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
