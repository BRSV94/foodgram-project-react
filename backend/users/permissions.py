from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)


class IsOwnerProfile(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.user == request.user)


class IsAuthenticatedOrNotMe(BasePermission):
    def has_permission(self, request, view):
        print('lol'*29)
        print(request)
        print(request.kwargs)
        print(request.kwargs.get('pk'))

        return (request.user.is_authenticated
                or request.kwargs.get('pk'))
