from django.contrib import admin
from .models import Subject, Homework, StudentSubmission


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'issued_date', 'due_date']
    list_filter = ['subject', 'teacher', 'issued_date']
    search_fields = ['title', 'description']
    readonly_fields = ['issued_date']


@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['homework', 'student', 'submission_date', 'grade', 'is_late']
    list_filter = ['homework', 'grade', 'is_late', 'submission_date']
    search_fields = ['homework__title', 'student__username']
    readonly_fields = ['submission_date']
