from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    """
    Учебный предмет (дисциплина)
    """
    SUBJECT_TYPE_CHOICES = [
        ('basic', 'Базовый'),
        ('profile', 'Профильный'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название предмета'
    )
    subject_type = models.CharField(
        max_length=10,
        choices=SUBJECT_TYPE_CHOICES,
        default='basic',
        verbose_name='Тип предмета'
    )
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Classroom(models.Model):
    """
    Учебный кабинет
    """
    CLASSROOM_TYPE_CHOICES = [
        ('basic', 'Для базовых дисциплин'),
        ('profile', 'Для профильных дисциплин'),
    ]
    
    number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Номер кабинета'
    )
    classroom_type = models.CharField(
        max_length=10,
        choices=CLASSROOM_TYPE_CHOICES,
        default='basic',
        verbose_name='Тип кабинета'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ['number']
    
    def __str__(self):
        return f'Кабинет {self.number}'


class Teacher(models.Model):
    """
    Учитель школы
    """
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Отчество'
    )
    classroom = models.OneToOneField(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_teacher',
        verbose_name='Закрепленный кабинет'
    )
    subjects = models.ManyToManyField(
        Subject,
        through='TeacherSubject',
        related_name='teachers',
        verbose_name='Преподаваемые предметы'
    )
    
    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.patronymic:
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        return f'{self.last_name} {self.first_name}'
    
    @property
    def full_name(self):
        if self.patronymic:
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        return f'{self.last_name} {self.first_name}'


class TeacherSubject(models.Model):
    """
    Связь учителя с предметом (какие предметы преподает учитель)
    """
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name='Учитель'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    
    class Meta:
        verbose_name = 'Преподаваемый предмет'
        verbose_name_plural = 'Преподаваемые предметы'
        unique_together = ['teacher', 'subject']
    
    def __str__(self):
        return f'{self.teacher} - {self.subject}'


class SchoolClass(models.Model):
    """
    Школьный класс
    """
    CLASS_NUMBER_CHOICES = [(i, str(i)) for i in range(1, 12)]
    CLASS_LETTER_CHOICES = [
        ('А', 'А'),
        ('Б', 'Б'),
        ('В', 'В'),
        ('Г', 'Г'),
        ('Д', 'Д'),
    ]
    
    number = models.PositiveSmallIntegerField(
        choices=CLASS_NUMBER_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(11)],
        verbose_name='Номер класса'
    )
    letter = models.CharField(
        max_length=1,
        choices=CLASS_LETTER_CHOICES,
        verbose_name='Буква класса'
    )
    class_teacher = models.OneToOneField(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_class',
        verbose_name='Классный руководитель'
    )
    
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        unique_together = ['number', 'letter']
        ordering = ['number', 'letter']
    
    def __str__(self):
        return f'{self.number}{self.letter}'


class Student(models.Model):
    """
    Ученик школы
    """
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Пол'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='Класс'
    )
    
    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.school_class})'


class Quarter(models.Model):
    """
    Учебная четверть
    """
    QUARTER_CHOICES = [
        (1, 'I четверть'),
        (2, 'II четверть'),
        (3, 'III четверть'),
        (4, 'IV четверть'),
    ]
    
    number = models.PositiveSmallIntegerField(
        choices=QUARTER_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name='Номер четверти'
    )
    academic_year = models.CharField(
        max_length=9,
        verbose_name='Учебный год',
        help_text='Например: 2024-2025'
    )
    start_date = models.DateField(
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        verbose_name='Дата окончания'
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name='Текущая четверть'
    )
    
    class Meta:
        verbose_name = 'Четверть'
        verbose_name_plural = 'Четверти'
        unique_together = ['number', 'academic_year']
        ordering = ['academic_year', 'number']
    
    def __str__(self):
        return f'{self.get_number_display()} ({self.academic_year})'


class TeachingAssignment(models.Model):
    """
    Назначение преподавания - какой учитель какой предмет ведет в каком классе
    """
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='teaching_assignments',
        verbose_name='Учитель'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='teaching_assignments',
        verbose_name='Предмет'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='teaching_assignments',
        verbose_name='Класс'
    )
    quarter = models.ForeignKey(
        Quarter,
        on_delete=models.CASCADE,
        related_name='teaching_assignments',
        verbose_name='Четверть'
    )
    
    class Meta:
        verbose_name = 'Назначение преподавания'
        verbose_name_plural = 'Назначения преподавания'
        unique_together = ['teacher', 'subject', 'school_class', 'quarter']
    
    def __str__(self):
        return f'{self.teacher} - {self.subject} - {self.school_class}'


class Schedule(models.Model):
    """
    Расписание занятий
    """
    DAY_CHOICES = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    ]
    
    LESSON_CHOICES = [(i, f'{i} урок') for i in range(1, 9)]
    
    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.CASCADE,
        related_name='schedule_entries',
        verbose_name='Назначение'
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name='День недели'
    )
    lesson_number = models.PositiveSmallIntegerField(
        choices=LESSON_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name='Номер урока'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='schedule_entries',
        verbose_name='Кабинет'
    )
    
    class Meta:
        verbose_name = 'Запись расписания'
        verbose_name_plural = 'Расписание'
        # В одном классе не может быть двух уроков одновременно
        unique_together = ['teaching_assignment', 'day_of_week', 'lesson_number']
        ordering = ['day_of_week', 'lesson_number']
    
    def __str__(self):
        return (f'{self.get_day_of_week_display()}, {self.lesson_number} урок - '
                f'{self.teaching_assignment.subject} ({self.teaching_assignment.school_class})')


class Grade(models.Model):
    """
    Четвертная оценка ученика по предмету
    """
    GRADE_CHOICES = [
        (2, 'Неудовлетворительно (2)'),
        (3, 'Удовлетворительно (3)'),
        (4, 'Хорошо (4)'),
        (5, 'Отлично (5)'),
    ]
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Ученик'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Предмет'
    )
    quarter = models.ForeignKey(
        Quarter,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Четверть'
    )
    value = models.PositiveSmallIntegerField(
        choices=GRADE_CHOICES,
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ['student', 'subject', 'quarter']
        ordering = ['student', 'subject']
    
    def __str__(self):
        return f'{self.student} - {self.subject}: {self.value}'
