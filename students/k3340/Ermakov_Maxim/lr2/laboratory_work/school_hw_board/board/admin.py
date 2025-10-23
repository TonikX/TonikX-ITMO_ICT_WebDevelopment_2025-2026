from django.contrib import admin
from .models import Subject, Homework, Submission

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'issued_at', 'due_date')
    list_filter = ('subject', 'teacher')
    search_fields = ('text', 'penalty_info')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'created_at', 'grade', 'graded_by')
    list_filter = ('homework__subject', 'grade')
    search_fields = ('student__username', 'content')
