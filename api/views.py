from django.db.models import Q

from rest_framework import filters, mixins, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


from utils.pagination import StandardResultsSetPagination

from .models import Item, Category

from .serializers import (
    ItemSerializer,
    CategorySerializer,
    ImageSerializer,
)

from .filters import ItemOrderingFilter


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = (MultiPartParser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (ItemOrderingFilter,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (ItemOrderingFilter, filters.SearchFilter)
    search_fields = ('name', 'details')
    ordering_fields = ('id', 'name', 'details', 'date')

    def get_queryset(self):
        item = self.kwargs.get('item')
        return Item.objects.filter(Q(category__path__iexact=item) | Q(category__path__contains='%s.' % item))


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, item):
        category = self.get_queryset().get(slug=item)
        serializer = self.get_serializer(category)

        return Response(serializer.data.get('children'))
