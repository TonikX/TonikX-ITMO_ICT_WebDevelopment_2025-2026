from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subject(models.Model):
    """Модель для предмета"""
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
    
    def __str__(self):
        return self.name


class Homework(models.Model):
    """Модель для домашнего задания"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Название задания")
    description = models.TextField(verbose_name="Текст задания")
    issued_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    due_date = models.DateTimeField(verbose_name="Крайний срок выполнения")
    penalty_info = models.TextField(blank=True, verbose_name="Информация о штрафах")
    
    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['-issued_date']
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    def is_overdue(self):
        return timezone.now() > self.due_date


class StudentSubmission(models.Model):
    """Модель для сдачи домашнего задания студентом"""
    GRADE_CHOICES = [
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    text = models.TextField(verbose_name="Текст решения")
    grade = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True, verbose_name="Оценка")
    is_late = models.BooleanField(default=False, verbose_name="Сдано с опозданием")
    
    class Meta:
        verbose_name = "Сдача домашнего задания"
        verbose_name_plural = "Сдачи домашних заданий"
        unique_together = ('homework', 'student')
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk and self.submission_date:
            self.is_late = self.submission_date > self.homework.due_date
        super().save(*args, **kwargs)
