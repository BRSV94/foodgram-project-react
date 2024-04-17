from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


# class CustomPagination(LimitOffsetPagination):

#     offset_query_param = 'page'
#     default_limit = 20

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
