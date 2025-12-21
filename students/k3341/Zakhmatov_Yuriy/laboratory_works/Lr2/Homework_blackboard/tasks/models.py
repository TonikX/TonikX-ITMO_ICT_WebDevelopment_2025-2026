from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.CharField(max_length=30)
    teacher_email = models.EmailField()

    def __str__(self):
        return self.name

class Homework(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    penalty_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name}: {self.description[:100]}"

    def get_last_submission(self, user):
        """Возвращает последнюю сдачу пользователя для этого задания"""
        return self.submission_set.filter(student=user).order_by('-submitted_at').first()


class Submission(models.Model):
    HOMEWORK_STATUS = [
        ('submitted', '📤 Сдано'),
        ('graded', '✅ Оценено'),
        ('late', '⚠️ Сдано с опозданием'),
        ('not_submitted', '⏳ Не сдано'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=HOMEWORK_STATUS,
        default='not_submitted'
    )

    def save(self, *args, **kwargs):
        # Сначала вызываем родительский save, чтобы установились auto_now_add поля
        super().save(*args, **kwargs)

        # Затем обновляем статус, если нужно
        if self.submitted_at and self.homework.due_date:
            if self.submitted_at.date() > self.homework.due_date:
                self.status = 'late'
            elif self.grade is not None:
                self.status = 'graded'
            elif self.text:
                self.status = 'submitted'
        elif self.grade is not None:
            self.status = 'graded'

        # Сохраняем снова, если статус изменился
        if self._state.adding is False:  # Если объект уже существует
            super().save(update_fields=['status'])

    def __str__(self):
        return f"{self.student.username} - {self.homework.subject.name} ({self.get_status_display()})"