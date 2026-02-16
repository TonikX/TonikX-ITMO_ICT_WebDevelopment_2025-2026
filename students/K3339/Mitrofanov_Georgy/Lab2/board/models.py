from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Homework(models.Model):
    subject = models.CharField(max_length=200)       # предмет
    teacher = models.CharField(max_length=200)       # преподаватель
    issued_date = models.DateField()                 # дата выдачи
    start_date = models.DateField()                  # начало периода выполнения
    due_date = models.DateField()                    # дедлайн
    task_text = models.TextField()                   # текст задания
    penalties = models.TextField(blank=True)         # штрафы

    def __str__(self):
        return f"{self.subject} — до {self.due_date}"

class Submission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="submissions")
    answer_text = models.TextField()                 # текст сдачи
    submitted_at = models.DateTimeField(auto_now_add=True)

    # оценка ставится учителем через админку
    grade = models.IntegerField(null=True, blank=True,
                                validators=[MinValueValidator(1), MaxValueValidator(10)])
    teacher_comment = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "homework")

    def __str__(self):
        return f"{self.student.username} -> {self.homework} ({self.grade})"
