from rest_framework import permissions

from core.models import TypeChoicesUser


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, views):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return request.user.type_user in [TypeChoicesUser.ADMIN]
