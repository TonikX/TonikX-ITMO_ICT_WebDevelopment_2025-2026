from rest_framework.permissions import BasePermission

class IsDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='director').exists()

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['employee', 'director']).exists()