from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Subject, Assignment, Submission, Grade


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Расширенная админка для пользователей"""
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('role', 'student_id', 'phone', 'birth_date')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('role', 'student_id', 'phone', 'birth_date')
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'student_id', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'student_id')
    ordering = ('username',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'created_at', 'due_date', 'max_points', 'is_active')
    list_filter = ('subject', 'teacher', 'is_active', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'subject__name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('subject', 'teacher')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'is_late', 'has_grade')
    list_filter = ('is_late', 'submitted_at', 'assignment__subject')
    search_fields = ('assignment__title', 'student__first_name', 'student__last_name', 'student__student_id')
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'
    
    def has_grade(self, obj):
        return obj.grade is not None
    has_grade.boolean = True
    has_grade.short_description = 'Оценено'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assignment', 'student')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('submission', 'points', 'get_max_points', 'get_percentage', 'graded_by', 'graded_at')
    list_filter = ('graded_at', 'graded_by')
    search_fields = ('submission__student__first_name', 'submission__student__last_name', 'submission__assignment__title')
    ordering = ('-graded_at',)
    date_hierarchy = 'graded_at'
    
    def get_max_points(self, obj):
        return obj.submission.assignment.max_points
    get_max_points.short_description = 'Макс. балл'
    
    def get_percentage(self, obj):
        return f"{obj.get_percentage()}%"
    get_percentage.short_description = 'Процент'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('submission__student', 'submission__assignment', 'graded_by')