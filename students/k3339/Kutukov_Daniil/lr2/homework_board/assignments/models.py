from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    """Расширенная модель пользователя для системы домашних заданий"""
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Студент'),
        (TEACHER, 'Преподаватель'),
        (ADMIN, 'Администратор'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
        verbose_name="Роль"
    )
    student_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Студенческий билет",
        help_text="Номер студенческого билета"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subject(models.Model):
    """Модель предмета"""
    name = models.CharField(
        max_length=100,
        verbose_name="Название предмета",
        unique=True
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание предмета"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ['name']


class Assignment(models.Model):
    """Модель домашнего задания"""
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет"
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_assignments',
        verbose_name="Преподаватель"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название задания"
    )
    description = models.TextField(
        verbose_name="Описание задания"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата выдачи"
    )
    due_date = models.DateTimeField(
        verbose_name="Срок выполнения"
    )
    penalty_info = models.TextField(
        blank=True,
        null=True,
        verbose_name="Информация о штрафах",
        help_text="Описание штрафов за несвоевременную сдачу"
    )
    max_points = models.PositiveIntegerField(
        default=100,
        verbose_name="Максимальный балл",
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно"
    )
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"
    
    def is_overdue(self):
        """Проверяет, просрочено ли задание"""
        return timezone.now() > self.due_date
    
    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['-created_at']


class Submission(models.Model):
    """Модель сдачи домашнего задания"""
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Задание"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Студент"
    )
    content = models.TextField(
        verbose_name="Текст сдачи"
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата сдачи"
    )
    is_late = models.BooleanField(
        default=False,
        verbose_name="Сдано с опозданием"
    )
    
    def save(self, *args, **kwargs):
        # Проверяем, сдано ли задание с опозданием
        if self.assignment.due_date < timezone.now():
            self.is_late = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
    
    class Meta:
        verbose_name = "Сдача задания"
        verbose_name_plural = "Сдачи заданий"
        ordering = ['-submitted_at']
        unique_together = ['assignment', 'student']


class Grade(models.Model):
    """Модель оценки за задание"""
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade',
        verbose_name="Сдача"
    )
    points = models.PositiveIntegerField(
        verbose_name="Полученные баллы",
        validators=[MinValueValidator(0)]
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий преподавателя"
    )
    graded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='graded_assignments',
        verbose_name="Оценил"
    )
    graded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оценки"
    )
    
    def __str__(self):
        return f"{self.submission.student} - {self.points}/{self.submission.assignment.max_points}"
    
    def get_percentage(self):
        """Возвращает процент от максимального балла"""
        return round((self.points / self.submission.assignment.max_points) * 100, 2)
    
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-graded_at']