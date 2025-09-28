from django.contrib import admin
from .models import Subject, Homework, Submission, Penalty

class PenaltyInline(admin.TabularInline):
    model = Penalty
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'issue_date', 'due_date', 'max_score')
    list_filter = ('subject', 'teacher', 'issue_date', 'due_date')
    search_fields = ('title', 'description')
    inlines = [PenaltyInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submission_date', 'score')
    list_filter = ('homework__subject', 'student', 'submission_date')
    search_fields = ('homework__title', 'student__username')

@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('homework', 'penalty_type', 'days_after_due', 'penalty_value')
    list_filter = ('homework__subject', 'penalty_type')