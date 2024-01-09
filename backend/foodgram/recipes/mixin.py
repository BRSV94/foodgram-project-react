from rest_framework import viewsets, mixins


class BaseRecipeMixin(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    pass
