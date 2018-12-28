from django.db.models import Q

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Item
from api.serializers import ItemListCreateSerializer, ItemDetailSerializer, ItemEstimationSerializer, ItemReplySerializer
from api.filters import ItemOrderingFilter

from utils.pagination import StandardResultsSetPagination


class ItemMixin(object):
    serializer_class = ItemListCreateSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (ItemOrderingFilter, filters.SearchFilter)
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
    serializer_class = ItemDetailSerializer


class ItemListCreateView(ItemMixin, generics.ListCreateAPIView):
    pass


class ItemEstimationView(ItemMixin, generics.CreateAPIView):
    serializer_class = ItemEstimationSerializer


class ItemReplyView(ItemMixin, generics.CreateAPIView):
    serializer_class = ItemReplySerializer
