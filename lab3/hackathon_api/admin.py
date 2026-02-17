from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    CustomUser, Task, TaskFile, TaskLink,
    Team, TeamMember, Solution, Evaluation
)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Админка для пользователей"""
    list_display = ['username', 'email', 'role', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Дополнительная информация'), {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Дополнительная информация'), {'fields': ('email', 'role')}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для задач"""
    list_display = ['title', 'created_by', 'curator', 'created_at']
    list_filter = ['created_at', 'curator']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    """Админка для файлов задач"""
    list_display = ['name', 'task', 'uploaded_at']
    list_filter = ['uploaded_at', 'task']
    search_fields = ['name', 'task__title']


@admin.register(TaskLink)
class TaskLinkAdmin(admin.ModelAdmin):
    """Админка для ссылок задач"""
    list_display = ['title', 'task', 'created_at']
    list_filter = ['created_at', 'task']
    search_fields = ['title', 'url', 'task__title']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Админка для команд"""
    list_display = ['name', 'captain', 'selected_task', 'created_at']
    list_filter = ['created_at', 'selected_task']
    search_fields = ['name', 'captain__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Админка для участников команд"""
    list_display = ['first_name', 'last_name', 'team', 'email', 'created_at']
    list_filter = ['created_at', 'team']
    search_fields = ['first_name', 'last_name', 'email', 'team__name']


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    """Админка для решений"""
    list_display = ['team', 'task', 'published_at']
    list_filter = ['published_at', 'task']
    search_fields = ['team__name', 'task__title', 'description']
    readonly_fields = ['published_at', 'updated_at']


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    """Админка для оценок"""
    list_display = ['solution', 'jury', 'score', 'created_at']
    list_filter = ['created_at', 'score', 'jury']
    search_fields = ['solution__team__name', 'jury__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
