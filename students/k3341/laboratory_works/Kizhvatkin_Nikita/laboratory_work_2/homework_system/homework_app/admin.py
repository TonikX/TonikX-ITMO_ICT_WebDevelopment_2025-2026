from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Subject, Homework, HomeworkSubmission

admin.site.unregister(User)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['subject', 'title', 'teacher', 'issued_date', 'due_date']
    list_filter = ['subject', 'teacher', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'due_date'


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework', 'submission_date', 'grade']
    list_filter = ['grade', 'homework__subject', 'student']
    search_fields = ['student__username', 'homework__title']
    readonly_fields = ['submission_date']
    list_editable = ['grade']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(homework__teacher=request.user)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'groups']
