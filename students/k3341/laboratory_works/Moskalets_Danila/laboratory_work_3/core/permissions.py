from rest_framework import permissions


class IsCompanyOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу компании.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Для Service проверяем связь через security_company.user
        if hasattr(obj, 'security_company'):
            return obj.security_company.user == request.user
        return False


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только владельцам компаний. Чтение разрешено всем.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для создания нужно быть авторизованным
        if view.action == 'create':
            return request.user.is_authenticated

        # Для остальных действий проверка на уровне объекта
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Редактирование/удаление: только владелец компании
        # Проверяем разные возможные связи
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'security_company') and hasattr(obj.security_company, 'user'):
            return obj.security_company.user == request.user
        return False



class IsRequestOwnerOrCompanyOwner(permissions.BasePermission):
    """
    Разрешает доступ:
    - Любому авторизованному для создания заявок
    - Пользователю, создавшему заявку (для чтения/обновления)
    - Владельцу компании, к которой относится услуга
    - Администраторам
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated
        if view.action == 'list':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.user == request.user:
            return True
        if hasattr(obj, 'service') and hasattr(obj.service, 'security_company'):
            return obj.service.security_company.user == request.user

        return False


class IsServiceOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование услуги только владельцу компании.
    Чтение разрешено всем.
    """

    def has_permission(self, request, view):
        # Безопасные методы разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для создания нужно быть авторизованным
        if view.action == 'create':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, что пользователь - владелец компании услуги
        if hasattr(obj, 'security_company') and hasattr(obj.security_company, 'user'):
            return obj.security_company.user == request.user

        return False


# permissions.py
class IsDiscountOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает:
    - Всем авторизованным просматривать активные скидки
    - Владельцам компаний редактировать свои скидки
    - Администраторам все
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS разрешены всем (или всем авторизованным)
        if request.method in permissions.SAFE_METHODS:
            # Если хотим, чтобы скидки видели все, включая неавторизованных:
            # return True
            # Если только авторизованные:
            return request.user.is_authenticated

        # Для создания/редактирования нужно быть авторизованным
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Безопасные методы разрешены всем (или авторизованным)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Редактирование: только владелец компании или администратор
        if request.user.is_staff:
            return True

        if hasattr(obj, 'service') and hasattr(obj.service, 'security_company'):
            return obj.service.security_company.user == request.user

        return False