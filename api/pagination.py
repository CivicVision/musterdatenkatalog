from rest_framework import pagination
from rest_framework.response import Response

from catalog import settings


class CustomPagination(pagination.PageNumberPagination):
    
    page_size_query_param = 'per_page'
    
    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'data': data
        })
