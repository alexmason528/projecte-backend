from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('totalItemsCount', self.page.paginator.count),
            ('itemsCountPerPage', self.page_size),
            ('activePage', self.page.number),
            ('results', data),
        ]))
