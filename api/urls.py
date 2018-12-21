from django.conf.urls import url
from rest_framework import routers

from .views import ItemViewSet, ItemListView, CategoryView

router = routers.SimpleRouter()

router.register(r'item', ItemViewSet)

urlpatterns = [
    url(r'category/(?P<item>(.+))/$', CategoryView.as_view()),
    url(r'item-list/(?P<item>(.+))/$', ItemListView.as_view()),
]

urlpatterns += router.urls
