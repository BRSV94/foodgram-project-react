from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)


class IsOwnerProfile(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.user == request.user)


class IsAuthenticatedOrNotMe(BasePermission):
    def has_permission(self, request, view):
        return ('users/me' not in request.META['PATH_INFO']
                or request.user.is_authenticated)
