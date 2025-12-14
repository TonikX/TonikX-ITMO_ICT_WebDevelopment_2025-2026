from django.contrib import admin
from .models import Subject, Assignment, Submission

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'date_issued', 'period_days', 'due_date_display')
    list_filter = ('subject', 'teacher')
    search_fields = ('title', 'description', 'teacher__username')

    def due_date_display(self, obj):
        return obj.due_date()
    due_date_display.short_description = 'Срок выполнения'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade', 'graded_by')
    list_filter = ('grade', 'assignment__subject')
    search_fields = ('student__username', 'assignment__title', 'feedback')
    readonly_fields = ('submitted_at',)
