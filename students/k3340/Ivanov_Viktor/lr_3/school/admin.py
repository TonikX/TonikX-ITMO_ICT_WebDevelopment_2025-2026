from django.contrib import admin

from school import models


class TeacherSubjectInline(admin.TabularInline):
    model = models.TeacherSubject
    extra = 1


class TeachingAssignmentInline(admin.TabularInline):
    model = models.TeachingAssignment
    extra = 1


class GradeInline(admin.TabularInline):
    model = models.Grade
    extra = 1


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "assigned_room", "hired_at")
    list_filter = ("assigned_room__category",)
    search_fields = ("last_name", "first_name", "middle_name", "email")
    inlines = (TeacherSubjectInline, TeachingAssignmentInline)


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "school_class", "gender", "is_active")
    list_filter = ("gender", "school_class")
    search_fields = ("last_name", "first_name", "middle_name")
    inlines = (GradeInline,)


@admin.register(models.SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("title", "grade_level", "profile", "homeroom_teacher")
    search_fields = ("title",)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category")
    search_fields = ("name", "code")
    list_filter = ("category",)


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "category", "capacity")
    list_filter = ("category",)
    search_fields = ("number", "title")


@admin.register(models.TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ("teacher", "subject", "period_start", "period_end")
    list_filter = ("subject",)


@admin.register(models.TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = ("school_class", "subject", "teacher", "period_start", "period_end")
    list_filter = ("school_class", "subject")


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "quarter", "value", "graded_by")
    list_filter = ("quarter", "subject")
    search_fields = ("student__last_name",)


@admin.register(models.ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = (
        "school_class",
        "weekday",
        "lesson_number",
        "subject",
        "teacher",
        "room",
    )
    list_filter = ("weekday", "school_class")
