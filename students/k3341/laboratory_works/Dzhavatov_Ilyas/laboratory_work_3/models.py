from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    # Для различения базовых и профильных дисциплин добавим поле типа
    SUBJECT_TYPE_CHOICES = [
        ('base', 'Базовая дисциплина'),
        ('profile', 'Профильная дисциплина'),
    ]
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE_CHOICES, default='base')

    def __str__(self):
        return f"Каб. {self.room_number} ({self.get_subject_type_display()})"

class Subject(models.Model):
    name = models.CharField(max_length=160)  # Из midpairs.name

    def __str__(self):
        return self.name

class SchoolClass(models.Model):
    name = models.CharField(max_length=10)  # Например, "10А"
    # Классный руководитель - это учитель
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_classes')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Закрепленный кабинет (может быть NULL)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    # Предметы, которые учитель может преподавать (Many-to-Many)
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мальчик'),
        ('F', 'Девочка'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='students')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.school_class})"

class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Может быть открытым

    class Meta:
        unique_together = ('teacher', 'subject', 'school_class', 'start_date')

    def __str__(self):
        return f"{self.teacher} -> {self.subject} в {self.school_class}"

class Grade(models.Model):
    QUARTER_CHOICES = [
        (1, 'I четверть'),
        (2, 'II четверть'),
        (3, 'III четверть'),
        (4, 'IV четверть'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField()  # Например, от 2 до 5
    quarter = models.PositiveSmallIntegerField(choices=QUARTER_CHOICES)
    school_year = models.CharField(max_length=9)  # Например, "2023-2024"

    class Meta:
        unique_together = ('student', 'subject', 'quarter', 'school_year')

    def __str__(self):
        return f"{self.student}: {self.subject} - {self.grade} (Q{self.quarter})"

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    ]
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='schedule')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Кто ведет урок
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    lesson_number = models.PositiveSmallIntegerField()  # Номер урока по порядку

    class Meta:
        unique_together = ('school_class', 'day_of_week', 'lesson_number')
        ordering = ['day_of_week', 'lesson_number']

    def __str__(self):
        return f"{self.school_class} - {self.get_day_of_week_display()}, {self.lesson_number} урок: {self.subject}"