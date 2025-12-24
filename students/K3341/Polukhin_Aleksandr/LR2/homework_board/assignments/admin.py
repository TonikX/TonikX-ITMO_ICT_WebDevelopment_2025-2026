from django.contrib import admin
from .models import Subject, Teacher, Student, Homework, Submission

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_subjects']
    def get_subjects(self, obj):
        return ", ".join([s.name for s in obj.subjects.all()])
    get_subjects.short_description = "Предметы"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'issued_at', 'due_date']
    list_filter = ['subject', 'teacher']
    search_fields = ['title', 'description']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework', 'submitted_at', 'grade', 'graded_at']
    list_filter = ['homework__subject', 'grade']
    search_fields = ['student__user__last_name', 'homwork__title']
    list_editable = ['grade']  # ← УЧИТЕЛЬ МОЖЕТ СТАВИТЬ ОЦЕНКУ ПРЯМО В СПИСКЕ!