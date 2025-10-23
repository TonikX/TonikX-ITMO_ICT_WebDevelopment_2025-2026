from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='given_homeworks',
        limit_choices_to={'role': 'teacher'}
    )
    issued_at = models.DateField()               # дата выдачи
    due_date = models.DateField()                # срок сдачи
    text = models.TextField()                    # текст задания
    penalty_info = models.TextField(blank=True)  # инфо о штрафах

    def __str__(self):
        return f"{self.subject} — до {self.due_date}"

class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='submissions',
        limit_choices_to={'role': 'student'}
    )
    content = models.TextField()                 # сдача в текстовом виде
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # оценка через админку
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    graded_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='graded_submissions', limit_choices_to={'role': 'teacher'}
    )

    class Meta:
        unique_together = ('homework', 'student')  # один студент -> одна сдача

    def __str__(self):
        g = self.grade if self.grade is not None else '—'
        return f"{self.student} -> {self.homework} ({g})"
