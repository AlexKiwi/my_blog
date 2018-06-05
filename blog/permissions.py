from rest_framework.permissions import BasePermission

# Create your models here.


class IsSuperUser(BasePermission):
    """
    超级用户权限
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser