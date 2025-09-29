from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """Право автора"""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    """Право администратора"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"
