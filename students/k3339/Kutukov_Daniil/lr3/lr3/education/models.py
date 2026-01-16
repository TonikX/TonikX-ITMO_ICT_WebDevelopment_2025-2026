from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Classroom(models.Model):
    """Кабинет"""

    number = models.CharField(max_length=10, unique=True, verbose_name="Номер кабинета")
    capacity = models.IntegerField(verbose_name="Вместимость", default=30)

    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"
        ordering = ["number"]

    def __str__(self):
        return f"Кабинет {self.number}"


class Subject(models.Model):
    """Дисциплина"""

    name = models.CharField(
        max_length=200, unique=True, verbose_name="Название дисциплины"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    hours_per_semester = models.IntegerField(verbose_name="Часов в семестр", default=36)

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Преподаватель"""

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    subjects = models.ManyToManyField(
        Subject, related_name="teachers", verbose_name="Преподаваемые дисциплины"
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachers",
        verbose_name="Закрепленный кабинет",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"


class Group(models.Model):
    """Группа студентов"""

    name = models.CharField(max_length=20, unique=True, verbose_name="Название группы")
    course = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="Курс"
    )
    specialty = models.CharField(max_length=200, verbose_name="Специальность")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ["course", "name"]

    def __str__(self):
        return f"{self.name} ({self.course} курс)"


class Student(models.Model):
    """Студент"""

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="students", verbose_name="Группа"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    enrollment_date = models.DateField(verbose_name="Дата зачисления")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["group", "last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.group.name})"

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"


class Grade(models.Model):
    """Оценка студента по дисциплине"""

    GRADE_CHOICES = [
        (5, "5 (Отлично)"),
        (4, "4 (Хорошо)"),
        (3, "3 (Удовлетворительно)"),
        (2, "2 (Неудовлетворительно)"),
    ]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grades", verbose_name="Студент"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name="Дисциплина",
    )
    grade = models.IntegerField(
        choices=GRADE_CHOICES,
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name="Оценка",
    )
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)], verbose_name="Семестр"
    )
    date = models.DateField(verbose_name="Дата выставления")

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["-date"]
        unique_together = ["student", "subject", "semester"]

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"


class Schedule(models.Model):
    """Расписание занятий"""

    DAYS_OF_WEEK = [
        (1, "Понедельник"),
        (2, "Вторник"),
        (3, "Среда"),
        (4, "Четверг"),
        (5, "Пятница"),
        (6, "Суббота"),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="schedules", verbose_name="Группа"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Дисциплина",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Преподаватель",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Кабинет",
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name="День недели")
    lesson_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name="Номер урока",
    )
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        ordering = ["day_of_week", "lesson_number"]
        unique_together = [
            ["group", "day_of_week", "lesson_number"],
            ["teacher", "day_of_week", "lesson_number"],
            ["classroom", "day_of_week", "lesson_number"],
        ]

    def __str__(self):
        return f"{self.group} - {self.subject} ({self.get_day_of_week_display()}, урок {self.lesson_number})"
