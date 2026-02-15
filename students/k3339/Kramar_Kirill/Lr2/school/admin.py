from django.contrib import admin
from .models import Subject, Homework, Submission, Review

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'given_at', 'due_from', 'due_to')
    list_filter = ('subject', 'teacher', 'given_at')
    search_fields = ('text',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'score', 'created_at')
    list_filter = ('homework__subject', 'score')
    search_fields = ('student__username', 'body')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('homework', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'homework__subject')
    search_fields = ('text',)
