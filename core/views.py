from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "p"

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "data": data,
                "message": "Retrived list data",
            },
            status=status.HTTP_200_OK,
        )
