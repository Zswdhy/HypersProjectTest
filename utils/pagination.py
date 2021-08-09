from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector
from rest_framework.pagination import (
    PageNumberPagination as BasePageNumberPagination,
)
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    """分页list."""
    page_size_query_param = "pageSize"

    def get_paginated_response(self, data):
        """分页list."""
        if "format" in self.request.query_params:
            return Response(data)
        else:
            return Response(
                OrderedDict(
                    [
                        (
                            "page",
                            {
                                "current": (self.page.number - 1)
                                           * self.page.paginator.per_page,
                                "size": self.page.paginator.per_page,
                                "total": self.page.paginator.count,
                            },
                        ),
                        ("records", data),
                    ]
                )
            )

# class RestResponsePagination(PaginatorInspector):
#     def get_paginated_response(self, paginator, response_schema):
#         paged_schema = openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties=OrderedDict(
#                 (
#                     (
#                         "page",
#                         openapi.Schema(
#                             type=openapi.TYPE_OBJECT,
#                             properties=OrderedDict(
#                                 (
#                                     (
#                                         "current",
#                                         openapi.Schema(
#                                             type=openapi.TYPE_INTEGER,
#                                             format=openapi.TYPE_INTEGER,
#                                         ),
#                                     ),
#                                     (
#                                         "size",
#                                         openapi.Schema(
#                                             type=openapi.TYPE_INTEGER,
#                                             format=openapi.TYPE_INTEGER,
#                                         ),
#                                     ),
#                                     (
#                                         "total",
#                                         openapi.Schema(
#                                             type=openapi.TYPE_INTEGER,
#                                             format=openapi.TYPE_INTEGER,
#                                         ),
#                                     ),
#                                 )
#                             ),
#                         ),
#                     ),
#                     ("records", response_schema),
#                 )
#             ),
#             required=["records"],
#         )
#         return paged_schema
