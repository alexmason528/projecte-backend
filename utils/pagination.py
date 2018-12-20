from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pageSize', self.page_size),
            ('currentPage', self.page.number),
            ('totalCount', self.page.paginator.count),
            ('results', data),
        ]))
