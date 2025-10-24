from django.contrib import admin

from .models import *

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'assigned_date', 'due_date']
    list_filter = ['subject', 'teacher', 'assigned_date']

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ['homework', 'student', 'submitted_date']
    list_filter = ['homework__subject', 'student']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['submission', 'grade', 'graded_by', 'graded_date']
    list_filter = ['grade', 'graded_by']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_class']

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
