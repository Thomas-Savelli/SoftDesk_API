from rest_framework import permissions


class IsContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name='Contributor').exists()
        return False
