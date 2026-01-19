from django.contrib import admin
from .models import Classroom, Subject, Teacher, Group, Student, Grade, Schedule


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ["number", "capacity"]
    list_filter = ["capacity"]
    search_fields = ["number"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "hours_per_semester"]
    list_filter = ["hours_per_semester"]
    search_fields = ["name"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "middle_name", "classroom"]
    search_fields = ["last_name", "first_name", "middle_name"]
    filter_horizontal = ["subjects"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "specialty"]
    list_filter = ["course"]
    search_fields = ["name", "specialty"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "last_name",
        "first_name",
        "middle_name",
        "group",
        "enrollment_date",
    ]
    list_filter = ["group", "enrollment_date"]
    search_fields = ["last_name", "first_name", "middle_name"]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "grade", "semester", "date"]
    list_filter = ["grade", "semester", "date", "subject"]
    search_fields = ["student__last_name", "student__first_name"]
    date_hierarchy = "date"


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "group",
        "subject",
        "teacher",
        "day_of_week",
        "lesson_number",
        "classroom",
        "start_time",
    ]
    list_filter = ["day_of_week", "lesson_number", "group"]
    search_fields = ["group__name", "subject__name", "teacher__last_name"]
