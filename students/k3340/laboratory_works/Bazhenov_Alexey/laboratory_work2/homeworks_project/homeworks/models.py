from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    """Модель для предметов/дисциплин"""
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Homework(models.Model):
    """Модель домашнего задания"""
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет"
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Преподаватель"
    )
    title = models.CharField(max_length=200, verbose_name="Название задания")
    description = models.TextField(verbose_name="Текст задания")
    assigned_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    due_date = models.DateTimeField(verbose_name="Срок выполнения")
    penalty_info = models.TextField(verbose_name="Информация о штрафах", blank=True)

    def __str__(self):
        return f"{self.subject} - {self.title}"

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['-assigned_date']


class HomeworkSubmission(models.Model):
    """Модель для сдачи домашних заданий"""
    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        verbose_name="Домашнее задание"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'students'},
        verbose_name="Студент"
    )
    submission_text = models.TextField(verbose_name="Текст решения")
    submitted_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    file_attachment = models.FileField(
        upload_to='homework_submissions/',
        blank=True,
        null=True,
        verbose_name="Файл с решением"
    )

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"

    class Meta:
        verbose_name = "Сданное задание"
        verbose_name_plural = "Сданные задания"
        unique_together = ['homework', 'student']
        ordering = ['-submitted_date']


class Grade(models.Model):
    """Модель для оценок"""
    submission = models.OneToOneField(
        HomeworkSubmission,
        on_delete=models.CASCADE,
        verbose_name="Сданное задание"
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка"
    )
    feedback = models.TextField(verbose_name="Комментарий преподавателя", blank=True)
    graded_date = models.DateTimeField(auto_now=True, verbose_name="Дата оценки")
    graded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Оценил"
    )

    def __str__(self):
        return f"{self.submission.student.username} - {self.grade}"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-graded_date']


class StudentProfile(models.Model):
    """Дополнительная информация о студенте"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    student_class = models.CharField(max_length=20, verbose_name="Класс/Группа")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_class}"

    class Meta:
        verbose_name = "Профиль студента"
        verbose_name_plural = "Профили студентов"


class TeacherProfile(models.Model):
    """Дополнительная информация о преподавателе"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subjects = models.ManyToManyField(Subject, verbose_name="Преподаваемые предметы")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Профиль преподавателя"
        verbose_name_plural = "Профили преподавателей"