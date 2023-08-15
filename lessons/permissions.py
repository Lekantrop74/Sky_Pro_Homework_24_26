from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.groups.filter(name='Модераторы').exists():
            return True

        return request.method in permissions.SAFE_METHODS


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.groups.filter(name='Модераторы').exists():
            return True

        return obj.owner == request.user