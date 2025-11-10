from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Название задания")
    description = models.TextField(verbose_name="Описание задания")
    assigned_date = models.DateField(default=timezone.now, verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    penalty_info = models.TextField(blank=True, verbose_name="Информация о штрафах")

    def __str__(self):
        return f"{self.subject} - {self.title}"

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"


class Submission(models.Model):
    GRADE_CHOICES = [
        (5, '5 - Отлично'),
        (4, '4 - Хорошо'),
        (3, '3 - Удовлетворительно'),
        (2, '2 - Неудовлетворительно'),
        (0, 'Не оценено'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    submission_text = models.TextField(verbose_name="Текст решения")
    submitted_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    grade = models.IntegerField(choices=GRADE_CHOICES, default=0, verbose_name="Оценка")
    teacher_comment = models.TextField(blank=True, verbose_name="Комментарий преподавателя")

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    class Meta:
        verbose_name = "Сдача задания"
        verbose_name_plural = "Сдачи заданий"
        unique_together = ['assignment', 'student']