from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name}"
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Название задания")
    description = models.TextField(verbose_name="Текст задания")
    issued_date = models.DateField(verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    penalty_info = models.TextField(blank=True, verbose_name="Информация о штрафах")
    
    def __str__(self):
        return f"{self.subject} - {self.title}"
    
    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name="Студент")
    submission_text = models.TextField(verbose_name="Текст решения")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    grade = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    feedback = models.TextField(blank=True, verbose_name="Комментарий преподавателя")
    
    def __str__(self):
        return f"{self.student} - {self.homework}"
    
    class Meta:
        verbose_name = "Сданное задание"
        verbose_name_plural = "Сданные задания"
        unique_together = ['homework', 'student']