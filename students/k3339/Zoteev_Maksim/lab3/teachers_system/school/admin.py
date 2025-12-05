from django.contrib import admin
from .models import (
    Subject, Classroom, Teacher, TeacherSubject, SchoolClass,
    Student, Quarter, TeachingAssignment, Schedule, Grade
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_type']
    list_filter = ['subject_type']
    search_fields = ['name']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['number', 'classroom_type', 'description']
    list_filter = ['classroom_type']
    search_fields = ['number', 'description']


class TeacherSubjectInline(admin.TabularInline):
    model = TeacherSubject
    extra = 1


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'classroom']
    list_filter = ['subjects']
    search_fields = ['last_name', 'first_name', 'patronymic']
    inlines = [TeacherSubjectInline]


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject']
    list_filter = ['subject']
    search_fields = ['teacher__last_name', 'subject__name']


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'number', 'letter', 'class_teacher']
    list_filter = ['number', 'letter']
    search_fields = ['class_teacher__last_name']
    inlines = [StudentInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'gender', 'school_class']
    list_filter = ['school_class', 'gender']
    search_fields = ['last_name', 'first_name']


@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'academic_year', 'start_date', 'end_date', 'is_current']
    list_filter = ['academic_year', 'is_current']


@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'school_class', 'quarter']
    list_filter = ['subject', 'school_class', 'quarter']
    search_fields = ['teacher__last_name', 'subject__name']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['teaching_assignment', 'day_of_week', 'lesson_number', 'classroom']
    list_filter = ['day_of_week', 'lesson_number', 'teaching_assignment__school_class']
    search_fields = ['teaching_assignment__subject__name', 'teaching_assignment__teacher__last_name']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'quarter', 'value']
    list_filter = ['subject', 'quarter', 'value', 'student__school_class']
    search_fields = ['student__last_name', 'subject__name']
