from rest_framework import generics
from api.views import ItemListCreateSerializer
from utils.pagination import StandardResultsSetPagination


class MyListingsView(generics.ListAPIView, generics.GenericAPIView):
    serializer_class = ItemListCreateSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.request.user.items.all()
