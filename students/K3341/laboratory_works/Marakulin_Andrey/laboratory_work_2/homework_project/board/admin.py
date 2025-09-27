from django.contrib import admin
from .models import Subject, Teacher, Homework, Submission


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    fields = ('student', 'submission_text', 'submission_date', 'grade')
    readonly_fields = ('student', 'submission_text', 'submission_date')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date')
    list_filter = ('subject', 'teacher', 'due_date')
    search_fields = ('title', 'task_text')
    inlines = [SubmissionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submission_date', 'grade')
    list_filter = ('homework__subject', 'student', 'grade')
    search_fields = ('student__username', 'homework__title')
    list_editable = ('grade',)


admin.site.register(Subject)
admin.site.register(Teacher)
