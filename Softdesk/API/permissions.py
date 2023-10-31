from rest_framework import permissions
from .models import Contributor


class IsContributor(permissions.BasePermission):
    # must be a contributor to the project
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj, contributor=request.user).exists()


class IsCreator(permissions.BasePermission):
    # must be the creator of the element
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
