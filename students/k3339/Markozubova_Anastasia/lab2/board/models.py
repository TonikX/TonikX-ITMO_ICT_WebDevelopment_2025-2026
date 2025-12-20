from django.db import models
from django.contrib.auth.models import User


# Модель для учебных предметов
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


# Модель для преподавателей
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предмет")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


# Модель для домашних заданий
class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Тема задания")
    task_text = models.TextField(verbose_name="Текст задания")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    penalty_info = models.TextField(blank=True, null=True, verbose_name="Информация о штрафах")

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['-due_date']


# Модель для сданных студентами работ
class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions',
                                 verbose_name="Домашнее задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    submission_text = models.TextField(verbose_name="Текст ответа")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"Ответ от {self.student.username} на {self.homework.title}"

    class Meta:
        verbose_name = "Сданное задание"
        verbose_name_plural = "Сданные задания"
        unique_together = ('homework', 'student')
