from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """Право автора. Доступ, если автор объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    """Право администратора. Доступ, если пользователь с ролью администратора"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"
