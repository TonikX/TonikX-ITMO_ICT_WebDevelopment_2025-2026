from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с ролями"""
    ROLE_CHOICES = [
        ('captain', 'Капитан команды'),
        ('curator', 'Куратор задачи'),
        ('jury', 'Член жюри'),
        ('admin', 'Главный администратор'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='captain',
        verbose_name='Роль'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_captain(self):
        return self.role == 'captain'
    
    def is_curator(self):
        return self.role == 'curator'
    
    def is_jury(self):
        return self.role == 'jury'
    
    def is_main_admin(self):
        return self.role == 'admin'


class Task(models.Model):
    """Модель задачи хакатона"""
    title = models.CharField(max_length=200, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Создатель',
        limit_choices_to={'role': 'admin'}
    )
    curator = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='curated_task',
        verbose_name='Куратор',
        limit_choices_to={'role': 'curator'}
    )
    consultation_link = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на консультацию'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TaskFile(models.Model):
    """Модель файла задачи"""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Задача'
    )
    file = models.FileField(upload_to='task_files/', verbose_name='Файл')
    name = models.CharField(max_length=200, verbose_name='Название файла')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        verbose_name = 'Файл задачи'
        verbose_name_plural = 'Файлы задач'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} ({self.task.title})"


class TaskLink(models.Model):
    """Модель ссылки задачи"""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='links',
        verbose_name='Задача'
    )
    url = models.URLField(verbose_name='URL')
    title = models.CharField(max_length=200, verbose_name='Название ссылки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Ссылка задачи'
        verbose_name_plural = 'Ссылки задач'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.task.title})"


class Team(models.Model):
    """Модель команды"""
    name = models.CharField(max_length=200, verbose_name='Название команды')
    captain = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='team',
        verbose_name='Капитан',
        limit_choices_to={'role': 'captain'}
    )
    motto = models.TextField(blank=True, null=True, verbose_name='Девиз/Описание')
    selected_task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams',
        verbose_name='Выбранная задача'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """Модель участника команды"""
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Команда'
    )
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команд'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team.name})"


class Solution(models.Model):
    """Модель решения команды"""
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='solutions',
        verbose_name='Команда'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='solutions',
        verbose_name='Задача'
    )
    description = models.TextField(verbose_name='Описание решения')
    file = models.FileField(
        upload_to='solutions/',
        blank=True,
        null=True,
        verbose_name='Файл решения'
    )
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'
        ordering = ['-published_at']
        unique_together = ['team', 'task']
    
    def __str__(self):
        return f"{self.team.name} - {self.task.title}"


class Evaluation(models.Model):
    """Модель оценки решения жюри"""
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='Решение'
    )
    jury = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='Член жюри',
        limit_choices_to={'role': 'jury'}
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка (1-10)'
    )
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оценки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-created_at']
        unique_together = ['solution', 'jury']
    
    def __str__(self):
        return f"{self.jury.username} - {self.solution.team.name} ({self.score}/10)"
