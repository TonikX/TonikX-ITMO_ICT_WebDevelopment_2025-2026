from django.contrib import admin
from .models import Subject, Homework, Submission

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'issue_date', 'due_date')
    list_filter = ('subject',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'status', 'grade', 'submitted_at')
    list_filter = ('homework', 'grade', 'status')
    search_fields = ('student__username', 'student__first_name', 'student__last_name')
    list_editable = ('status', 'grade')
    actions = ['delete_old_submissions']

    def delete_old_submissions(self, request, queryset):
        """Удаляет все кроме последних сдач"""
        from django.db.models import Max

        # Находим ID последних сдач для каждого студента и задания
        latest_submissions = Submission.objects.values(
            'student', 'homework'
        ).annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)

        # Удаляем все кроме последних
        deleted_count = Submission.objects.exclude(
            id__in=latest_submissions
        ).delete()[0]

        self.message_user(request, f"Удалено {deleted_count} старых сдач")

    delete_old_submissions.short_description = "Удалить все кроме последних сдач"