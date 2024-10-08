from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsOwnerProfile(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.user == request.user)
