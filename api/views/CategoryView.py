from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Category

from api.serializers import CategorySerializer


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, item):
        category = self.get_queryset().get(slug=item)
        serializer = self.get_serializer(category)

        return Response(serializer.data.get('children'))
