from rest_framework.permissions import BasePermission
from users.models import USER_ROLE


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorImage(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.car.author == request.user


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_role == USER_ROLE.MANAGER
        )
