from django.contrib import admin
from .models import Subject, Homework, Submission


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'given_at', 'due_from', 'due_to')
    list_filter = ('subject',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submitted_at', 'grade')
    list_filter = ('homework', 'student', 'grade')
