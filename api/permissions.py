from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user.is_authenticated
                                                  and request.user.is_admin)


class IsOwnerAdminModerator(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_moderator or request.user.is_admin
                or obj.author == request.user)
