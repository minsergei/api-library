from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """Проверка на модератора."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="manager").exists()
