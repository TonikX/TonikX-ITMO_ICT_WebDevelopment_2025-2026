from rest_framework import permissions


class IsResident(permissions.BasePermission):
    """Проверка роли 'Жилец'"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'resident'
        )


class IsMaster(permissions.BasePermission):
    """Проверка роли 'Мастер'"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'master'
        )


class IsDispatcher(permissions.BasePermission):
    """Проверка роли 'Диспетчер'"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'dispatcher'
        )


class IsOwnerOrDispatcher(permissions.BasePermission):
    """Владелец квартиры или диспетчер"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'dispatcher':
            return True
        
        # Проверка владения квартирой
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'apartment'):
            return obj.apartment.owner == request.user
        
        return False


class IsAssignedWorkerOrDispatcher(permissions.BasePermission):
    """Назначенный мастер или диспетчер"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'dispatcher':
            return True
        
        if hasattr(obj, 'worker'):
            return obj.worker == request.user
        
        return False


class IsRequesterOrWorkerOrDispatcher(permissions.BasePermission):
    """Создатель заявки, назначенный мастер или диспетчер"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'dispatcher':
            return True
        
        if hasattr(obj, 'requester') and obj.requester == request.user:
            return True
        
        if hasattr(obj, 'worker') and obj.worker == request.user:
            return True
        
        return False

