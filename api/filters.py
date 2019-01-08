from django.db.models import Count, Avg

from rest_framework import filters

from .models import Category


class ItemOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)

        if params:
            if '-price' in params:
                queryset = queryset.annotate(price=Avg('estimations__value')).order_by('-price')
            elif 'price' in params:
                queryset = queryset.annotate(price=Avg('estimations__value')).order_by('price')

            if '-estimation' in params:
                queryset = queryset.annotate(estimation_counts=Count('estimations')).order_by('-estimation_counts')
            elif 'estimation' in params:
                queryset = queryset.annotate(estimation_counts=Count('estimations')).order_by('estimation_counts')

        return super(ItemOrderingFilter, self).filter_queryset(request, queryset, view)


class ItemCategoryFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        cid = request.query_params.get('cid')

        if cid:
            category = Category.objects.get(pk=cid)
            queryset = queryset.filter(category__path__contains=category.path)

        return queryset
