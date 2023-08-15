from rest_framework import permissions
from rest_framework.permissions import BasePermission

from lessons.models import Lesson, Course


class IsModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.groups.filter(name='Модераторы').exists():
            return True

        return request.method in permissions.SAFE_METHODS


class IsModeratorEditOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.groups.filter(name='Модераторы').exists():
            return False

        return True
