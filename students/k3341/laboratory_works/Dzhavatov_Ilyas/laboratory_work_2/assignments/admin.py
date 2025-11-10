from django.contrib import admin
from .models import Subject, Assignment, Submission

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'assigned_date', 'due_date']
    list_filter = ['subject', 'assigned_date', 'due_date']
    search_fields = ['title', 'description']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_date', 'grade']
    list_filter = ['grade', 'submitted_date']
    search_fields = ['assignment__title', 'student__username']
    readonly_fields = ['submitted_date']