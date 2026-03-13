from django.contrib import admin
from .models import Homework, Submission

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "teacher", "issued_date", "start_date", "due_date")
    search_fields = ("subject", "teacher")
    list_filter = ("subject", "teacher")

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "homework", "student", "submitted_at", "grade")
    list_filter = ("grade", "homework__subject")
    search_fields = ("student__username", "homework__subject")
    fields = ("homework", "student", "answer_text", "submitted_at", "grade", "teacher_comment")
    readonly_fields = ("submitted_at",)
