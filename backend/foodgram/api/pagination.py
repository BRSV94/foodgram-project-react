from rest_framework.pagination import LimitOffsetPagination, _positive_int


class CustomPagination(LimitOffsetPagination):

    offset_query_param = 'page'
    default_limit = 20
