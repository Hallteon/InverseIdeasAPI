from rest_framework import permissions


class IsHead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_type == 'head'