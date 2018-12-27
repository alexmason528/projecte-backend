from django.db.models import Q

from rest_framework import filters, mixins, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from utils.pagination import StandardResultsSetPagination

from .models import Item, Category

from .serializers import (
    ItemSerializer,
    ItemEstimationSerializer,
    CategorySerializer,
    ImageSerializer,
)

from .filters import ItemOrderingFilter


class ItemMixin(object):
    serializer_class = ItemSerializer
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
    pass


class ItemListCreateView(ItemMixin, generics.ListCreateAPIView):
    pass


class ItemEstimationView(ItemMixin, generics.CreateAPIView):
    serializer_class = ItemEstimationSerializer


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, item):
        category = self.get_queryset().get(slug=item)
        serializer = self.get_serializer(category)

        return Response(serializer.data.get('children'))
