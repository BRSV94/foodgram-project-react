from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):

    offset_query_param = 'page'
    default_limit = 20
