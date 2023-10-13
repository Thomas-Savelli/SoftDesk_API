from rest_framework import permissions
from .models import Contributor


class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj, contributor=request.user).exists()


class IsProjectCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
