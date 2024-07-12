from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination,CursorPagination
)

class StandardPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StandardLimitOffSetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 10

class StandardCursorPagination(CursorPagination):
    page_size = 10
    cursor_query_param = 'cursor'
    ordering = '-created'