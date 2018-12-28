from django.conf.urls import url
from rest_framework import routers

from .views import ItemListCreateView, ItemRetriveUpdateDestroyView, ItemEstimationView, ItemReplyView, CategoryView

router = routers.SimpleRouter()

urlpatterns = [
    url(r'category/(?P<item>(.+))/$', CategoryView.as_view()),
    url(r'item/(?P<type>(.+))/(?P<pk>(\w+))/reply/$', ItemReplyView.as_view()),
    url(r'item/(?P<type>(.+))/(?P<pk>(\w+))/estimation/$', ItemEstimationView.as_view()),
    url(r'item/(?P<type>(.+))/(?P<pk>(\w+))/$', ItemRetriveUpdateDestroyView.as_view()),
    url(r'item/(?P<type>(.+))/$', ItemListCreateView.as_view()),
]

urlpatterns += router.urls
