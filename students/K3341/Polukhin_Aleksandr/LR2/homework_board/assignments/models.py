from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subject(models.Model):
    """Предмет (например, Математика, Физика)"""
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Профиль преподавателя (связан с User)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subjects = models.ManyToManyField(Subject, verbose_name="Преподаваемые предметы")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Student(models.Model):
    """Профиль студента (связан с User)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Homework(models.Model):
    """Домашнее задание"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Название задания")
    description = models.TextField(verbose_name="Текст задания")
    issued_at = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи")
    due_date = models.DateTimeField(verbose_name="Срок сдачи")
    penalty_info = models.TextField(blank=True, null=True, verbose_name="Информация о штрафах")

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['-issued_at']  # новые — первыми

    def __str__(self):
        return f"{self.subject} — {self.title}"


class Submission(models.Model):
    """Сданная работа студента"""
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name="Домашнее задание")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Дата отправки")
    text = models.TextField(verbose_name="Текст решения")
    grade = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name="Оценка"
    )
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата выставления оценки")

    class Meta:
        verbose_name = "Работа студента"
        verbose_name_plural = "Работы студентов"
        unique_together = ('homework', 'student')  # один студент — одна сдача на задание

    def __str__(self):
        return f"{self.student} → {self.homework.title} [{self.grade or '—'}]"