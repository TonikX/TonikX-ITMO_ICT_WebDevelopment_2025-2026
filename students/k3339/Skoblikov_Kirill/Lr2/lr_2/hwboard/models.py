from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'

    ROLE_CHOICES = [
        (STUDENT, 'Ученик'),
        (TEACHER, 'Преподаватель'),
    ]

    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default=STUDENT, verbose_name="Роль")
    email = models.EmailField(max_length=64, verbose_name="Электронная почта", unique=True)
    patronymic = models.CharField(max_length=32, blank=True, verbose_name="Отчество")

    def get_full_name_with_patronymic(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    class_name = models.CharField(max_length=10, verbose_name="Класс")
    admission_year = models.IntegerField(verbose_name="Год поступления")

    class Meta:
        verbose_name = "Профиль ученика"
        verbose_name_plural = "Профили учеников"

    def __str__(self):
        return f"Ученик: {self.user.get_full_name_with_patronymic()} ({self.class_name})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    education = models.CharField(max_length=100, verbose_name="Образование")
    experience = models.IntegerField(default=0, verbose_name="Стаж (лет)")
    teacher_code = models.CharField(max_length=20, unique=True, verbose_name="Код преподавателя")
    is_class_teacher = models.BooleanField(default=False, verbose_name="Классный руководитель")

    class Meta:
        verbose_name = "Профиль преподавателя"
        verbose_name_plural = "Профили преподавателей"

    def __str__(self):
        return f"Преподаватель: {self.user.get_full_name_with_patronymic()} ({self.subject})"


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    teachers = models.ManyToManyField(TeacherProfile, related_name='subjects', verbose_name="Преподаватели")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, verbose_name="Преподаватель")
    assigned_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    text = models.TextField(verbose_name="Текст задания")
    penalty_info = models.TextField(blank=True, verbose_name="Информация о штрафах")
    for_class = models.CharField(max_length=10, verbose_name="Для класса")  # 5А, 6Б и т.д.
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="Ученик")
    submission_text = models.TextField(verbose_name="Текст сдачи")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Время сдачи")

    STATUS_CHOICES = [
        ('submitted', 'Сдано'),
        ('late', 'Сдано с опозданием'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    class Meta:
        unique_together = ['homework', 'student']
        verbose_name = "Сдача задания"
        verbose_name_plural = "Сдача заданий"


class Grade(models.Model):
    submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, verbose_name="Сдача")
    grade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка",
        null=True,
        blank=True
    )
    teacher_feedback = models.TextField(blank=True, verbose_name="Комментарий преподавателя")
    graded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оценки")

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

