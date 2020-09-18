from rest_framework import pagination
from rest_framework.response import Response

from catalog import settings


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'per_page': settings.REST_FRAMEWORK.get("PAGE_SIZE"),
            'data': data
        })
