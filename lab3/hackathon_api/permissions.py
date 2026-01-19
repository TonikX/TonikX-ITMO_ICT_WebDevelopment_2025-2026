from rest_framework import permissions


class IsCaptain(permissions.BasePermission):
    """Проверка, что пользователь является капитаном"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_captain()


class IsCurator(permissions.BasePermission):
    """Проверка, что пользователь является куратором"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_curator()


class IsJury(permissions.BasePermission):
    """Проверка, что пользователь является членом жюри"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_jury()


class IsMainAdmin(permissions.BasePermission):
    """Проверка, что пользователь является главным администратором"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_main_admin()


class IsCaptainOrReadOnly(permissions.BasePermission):
    """Капитан может редактировать, остальные только читать"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_captain()


class IsTeamCaptain(permissions.BasePermission):
    """Проверка, что пользователь является капитаном конкретной команды"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_captain()
    
    def has_object_permission(self, request, view, obj):
        # Для Team
        if hasattr(obj, 'captain'):
            return obj.captain == request.user
        # Для Solution
        if hasattr(obj, 'team'):
            return obj.team.captain == request.user
        # Для TeamMember
        if hasattr(obj, 'team') and hasattr(obj.team, 'captain'):
            return obj.team.captain == request.user
        return False


class IsTaskCurator(permissions.BasePermission):
    """Проверка, что пользователь является куратором задачи"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_curator()
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'task'):
            return obj.task.curator == request.user
        if hasattr(obj, 'curator'):
            return obj.curator == request.user
        return False


class IsJuryOrReadOnly(permissions.BasePermission):
    """Жюри может оценивать, остальные только читать"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_jury()


class CanViewSolution(permissions.BasePermission):
    """Проверка прав на просмотр решения"""
    def has_object_permission(self, request, view, obj):
        # Капитан команды может видеть свое решение
        if hasattr(obj, 'team') and obj.team.captain == request.user:
            return True
        # Куратор задачи может видеть решения по своей задаче
        if request.user.is_curator() and obj.task.curator == request.user:
            return True
        # Жюри может видеть все решения
        if request.user.is_jury():
            return True
        # Главный админ может видеть все решения
        if request.user.is_main_admin():
            return True
        return False


class CanEvaluateSolution(permissions.BasePermission):
    """Проверка прав на оценку решения (только жюри)"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_jury()
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'solution'):
            # Для Evaluation - проверяем, что решение существует
            return True
        # Для Solution
        return True


class CanCreateTask(permissions.BasePermission):
    """Проверка прав на создание задачи (только главный админ)"""
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.is_main_admin()
        return True


class CanAssignCurator(permissions.BasePermission):
    """Проверка прав на назначение куратора (только главный админ)"""
    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT']:
            return request.user.is_main_admin()
        return True
