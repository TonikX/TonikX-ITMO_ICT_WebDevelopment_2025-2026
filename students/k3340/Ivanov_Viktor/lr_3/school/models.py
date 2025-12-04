from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """Абстрактная модель с базовыми временными полями."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gender(models.TextChoices):
    MALE = "male", "Мальчик"
    FEMALE = "female", "Девочка"


class RoomCategory(models.TextChoices):
    BASIC = "basic", "Базовый"
    PROFILE = "profile", "Профильный"


class SubjectCategory(models.TextChoices):
    BASIC = "basic", "Общая"
    PROFILE = "profile", "Профильная"


class WeekDay(models.IntegerChoices):
    MONDAY = 1, "Понедельник"
    TUESDAY = 2, "Вторник"
    WEDNESDAY = 3, "Среда"
    THURSDAY = 4, "Четверг"
    FRIDAY = 5, "Пятница"
    SATURDAY = 6, "Суббота"


class Quarter(models.IntegerChoices):
    Q1 = 1, "I четверть"
    Q2 = 2, "II четверть"
    Q3 = 3, "III четверть"
    Q4 = 4, "IV четверть"


class Classroom(TimestampedModel):
    """Кабинет школы."""

    number = models.CharField("Номер", max_length=10, unique=True)
    title = models.CharField("Название", max_length=64, blank=True)
    category = models.CharField(
        "Тип кабинета",
        max_length=16,
        choices=RoomCategory.choices,
        default=RoomCategory.BASIC,
    )
    capacity = models.PositiveSmallIntegerField("Вместимость", default=25)

    class Meta:
        ordering = ("number",)
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"

    def __str__(self) -> str:
        return self.title or f"Кабинет {self.number}"


class Subject(TimestampedModel):
    """Учебная дисциплина."""

    code = models.CharField("Код", max_length=32, unique=True)
    name = models.CharField("Название", max_length=128)
    category = models.CharField(
        "Категория",
        max_length=16,
        choices=SubjectCategory.choices,
        default=SubjectCategory.BASIC,
    )
    description = models.TextField("Описание", blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self) -> str:
        return self.name


class SchoolClass(TimestampedModel):
    """Класс (например, 10А)."""

    title = models.CharField("Обозначение", max_length=32, unique=True)
    grade_level = models.PositiveSmallIntegerField(
        "Класс", validators=[MinValueValidator(1), MaxValueValidator(11)]
    )
    profile = models.CharField(
        "Профиль",
        max_length=16,
        choices=SubjectCategory.choices,
        default=SubjectCategory.BASIC,
    )
    homeroom_teacher = models.OneToOneField(
        "school.Teacher",
        related_name="homeroom_class",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("grade_level", "title")
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self) -> str:
        return self.title


class Teacher(TimestampedModel):
    """Сведения об учителе."""

    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    middle_name = models.CharField("Отчество", max_length=64, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    hired_at = models.DateField("Дата приема", default=timezone.now)
    assigned_room = models.ForeignKey(
        Classroom,
        verbose_name="Закрепленный кабинет",
        related_name="teachers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    subjects = models.ManyToManyField(
        Subject,
        through="TeacherSubject",
        related_name="teachers",
        blank=True,
    )

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(part for part in parts if part)


class TeacherSubject(TimestampedModel):
    """Связь учителя и предмета."""

    teacher = models.ForeignKey(
        Teacher, related_name="subject_links", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="teacher_links", on_delete=models.CASCADE
    )
    period_start = models.DateField("Начало периода", null=True, blank=True)
    period_end = models.DateField("Конец периода", null=True, blank=True)
    hours_per_week = models.PositiveSmallIntegerField("Часов в неделю", default=1)

    class Meta:
        verbose_name = "Преподавание предмета"
        verbose_name_plural = "Преподавания предметов"
        constraints = [
            models.UniqueConstraint(
                fields=("teacher", "subject", "period_start", "period_end"),
                name="unique_teacher_subject_period",
            )
        ]

    def __str__(self) -> str:
        return f"{self.teacher.full_name} → {self.subject.name}"


class TeachingAssignment(TimestampedModel):
    """Связь учителя, предмета и класса."""

    teacher = models.ForeignKey(
        Teacher, related_name="class_assignments", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="class_assignments", on_delete=models.CASCADE
    )
    school_class = models.ForeignKey(
        SchoolClass, related_name="teaching_assignments", on_delete=models.CASCADE
    )
    period_start = models.DateField("Начало периода", null=True, blank=True)
    period_end = models.DateField("Конец периода", null=True, blank=True)
    notes = models.TextField("Примечание", blank=True)

    class Meta:
        verbose_name = "Назначение преподавателя"
        verbose_name_plural = "Назначения преподавателей"
        constraints = [
            models.UniqueConstraint(
                fields=("teacher", "subject", "school_class", "period_start", "period_end"),
                name="unique_class_assignment_period",
            )
        ]

    def __str__(self) -> str:
        return f"{self.school_class}: {self.subject} ({self.teacher})"


class Student(TimestampedModel):
    """Информация об ученике."""

    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    middle_name = models.CharField("Отчество", max_length=64, blank=True)
    gender = models.CharField("Пол", max_length=6, choices=Gender.choices)
    school_class = models.ForeignKey(
        SchoolClass, related_name="students", on_delete=models.PROTECT
    )
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    enrollment_date = models.DateField("Дата зачисления", default=timezone.now)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(part for part in parts if part)


class Grade(TimestampedModel):
    """Четвертная оценка по предмету."""

    student = models.ForeignKey(
        Student, related_name="grades", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="grades", on_delete=models.PROTECT
    )
    quarter = models.PositiveSmallIntegerField(
        "Четверть",
        choices=Quarter.choices,
    )
    value = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[MinValueValidator(2), MaxValueValidator(5)],
    )
    comment = models.TextField("Комментарий", blank=True)
    graded_by = models.ForeignKey(
        Teacher,
        related_name="issued_grades",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        constraints = [
            models.UniqueConstraint(
                fields=("student", "subject", "quarter"),
                name="unique_grade_per_quarter",
            )
        ]

    def __str__(self) -> str:
        return f"{self.student} – {self.subject}: {self.value}"


class ScheduleEntry(TimestampedModel):
    """Элемент расписания."""

    school_class = models.ForeignKey(
        SchoolClass, related_name="schedule", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="schedule", on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        Teacher, related_name="schedule", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Classroom,
        related_name="lessons",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    weekday = models.PositiveSmallIntegerField(
        "День недели",
        choices=WeekDay.choices,
    )
    lesson_number = models.PositiveSmallIntegerField(
        "Номер урока",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    starts_at = models.TimeField("Начало", null=True, blank=True)
    ends_at = models.TimeField("Окончание", null=True, blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Расписание"
        constraints = [
            models.UniqueConstraint(
                fields=("school_class", "weekday", "lesson_number"),
                name="unique_lesson_slot_per_class",
            ),
            models.UniqueConstraint(
                fields=("teacher", "weekday", "lesson_number"),
                name="unique_lesson_slot_per_teacher",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.school_class} – {self.subject} (урок {self.lesson_number})"
