from rest_framework import generics, status
from rest_framework.response import Response

from api.serializers import ImageUploadSerializer

from utils.pagination import StandardResultsSetPagination


class ImageUploadView(generics.CreateAPIView, generics.GenericAPIView):
    serializer_class = ImageUploadSerializer
