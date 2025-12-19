from rest_framework import permissions


class BaseCompanyPermission(permissions.BasePermission):

    def _is_company_owner(self, obj, user):
        """Проверяет, является ли пользователь владельцем компании объекта"""
        if hasattr(obj, 'user'):
            return obj.user == user
        if hasattr(obj, 'security_company'):
            return hasattr(obj.security_company, 'user') and obj.security_company.user == user
        return False

    def _is_service_company_owner(self, obj, user):
        """Проверяет владение через связь service -> security_company"""
        if hasattr(obj, 'service') and hasattr(obj.service, 'security_company'):
            return obj.service.security_company.user == user
        return False

    def _is_object_owner(self, obj, user):
        """Проверяет, является ли пользователь владельцем объекта"""
        return hasattr(obj, 'user') and obj.user == user

    def _check_safe_methods(self, request):
        """Проверяет безопасные методы HTTP"""
        return request.method in permissions.SAFE_METHODS


class IsCompanyOwner(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        return self._is_company_owner(obj, request.user)


class IsCompanyOwnerOrReadOnly(BaseCompanyPermission):
    def has_permission(self, request, view):
        if self._check_safe_methods(request):
            return True
        if view.action == 'create':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if self._check_safe_methods(request):
            return True
        return self._is_company_owner(obj, request.user)


class IsRequestOwnerOrCompanyOwner(BaseCompanyPermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'list']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if self._is_object_owner(obj, request.user):
            return True
        if self._is_service_company_owner(obj, request.user):
            return True
        return False


class IsServiceOwnerOrReadOnly(BaseCompanyPermission):
    def has_permission(self, request, view):
        if self._check_safe_methods(request):
            return True
        if view.action == 'create':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if self._check_safe_methods(request):
            return True
        return self._is_company_owner(obj, request.user)


class IsDiscountOwnerOrReadOnly(BaseCompanyPermission):
    def has_permission(self, request, view):
        if self._check_safe_methods(request):
            return request.user.is_authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if self._check_safe_methods(request):
            return True
        if request.user.is_staff:
            return True
        if self._is_service_company_owner(obj, request.user):
            return True
        return False


class IsCompanyOwnerOrAdmin(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return self._is_object_owner(obj, request.user)


class IsCompanyOwnerOnly(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        return self._is_object_owner(obj, request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsRequestOwnerOrCompanyOwnerOrAdmin(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        if obj.user == user:
            return True
        if hasattr(obj.service, 'security_company') and obj.service.security_company.user == user:
            return True
        return False


class IsRequestOwnerOrAdmin(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.user == user


class IsFavoriteOwnerOrAdmin(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        return hasattr(obj, 'user') and obj.user == user


class IsReviewOwnerOrAdmin(BaseCompanyPermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        return hasattr(obj, 'user') and obj.user == user