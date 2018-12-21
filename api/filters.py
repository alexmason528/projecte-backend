from django.db.models import Count

from rest_framework import filters


class ItemOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)

        if params:
            if '-estimation' in request.query_params[self.ordering_param]:
                queryset = queryset.annotate(estimation_counts=Count('estimations')).order_by('-estimation_counts')
            elif 'estimation' in request.query_params[self.ordering_param]:
                queryset = queryset.annotate(estimation_counts=Count('estimations')).order_by('estimation_counts')

        return super(ItemOrderingFilter, self).filter_queryset(request, queryset, view)
