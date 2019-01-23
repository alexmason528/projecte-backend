from django.db.models import Q

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Item
from api.serializers import ItemListCreateSerializer, ItemDetailSerializer, ItemDetailUpdateSerializer, ItemEstimationSerializer, ItemReplySerializer
from api.filters import ItemOrderingFilter, ItemCategoryFilter

from utils.pagination import StandardResultsSetPagination


class ItemMixin(object):
    serializer_class = ItemListCreateSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (ItemOrderingFilter, ItemCategoryFilter, filters.SearchFilter)
    search_fields = ('name', 'details')
    ordering_fields = ('id', 'name', 'details', 'date')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        type = self.kwargs.get('type')
        return Item.objects.filter(Q(category__path__iexact=type) | Q(category__path__contains='%s.' % type))


class ItemRetriveUpdateDestroyView(
    ItemMixin,
    generics.RetrieveUpdateDestroyAPIView,
    generics.GenericAPIView
):
    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.request.method in ['PATCH']:
            return ItemDetailUpdateSerializer
        return ItemDetailSerializer


class ItemListCreateView(ItemMixin, generics.ListCreateAPIView):
    pass


class ItemEstimationView(ItemMixin, generics.CreateAPIView):
    serializer_class = ItemEstimationSerializer


class ItemReplyView(ItemMixin, generics.CreateAPIView):
    serializer_class = ItemReplySerializer
