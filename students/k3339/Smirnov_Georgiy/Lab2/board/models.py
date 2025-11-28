from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)          # предмет
    teacher = models.CharField(max_length=100)       # преподаватель

    def __str__(self):
        return f"{self.name} ({self.teacher})"


class Homework(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='homeworks',
    )
    given_at = models.DateField()                    # дата выдачи
    due_from = models.DateField()                    # начало периода выполнения
    due_to = models.DateField()                      # конец периода выполнения
    text = models.TextField()                        # текст задания
    penalty_info = models.CharField(
        max_length=255,
        blank=True,
        help_text="Информация о штрафах",
    )

    def __str__(self):
        return f"{self.subject.name}: {self.text[:40]}..."


class Submission(models.Model):
    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    answer_text = models.TextField()                 # сдача ДЗ в текстовом виде
    grade = models.IntegerField(
        null=True,
        blank=True,
        help_text="Оценка ставится учителем в админке",
    )

    def __str__(self):
        return f"{self.student.username} -> {self.homework.id}"
