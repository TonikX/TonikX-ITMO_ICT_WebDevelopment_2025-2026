from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='given_assignments')
    date_issued = models.DateField()
    period_days = models.PositiveIntegerField(help_text='Период выполнения в днях')
    penalties_info = models.TextField(blank=True, help_text='Информация о штрафах')

    class Meta:
        ordering = ['-date_issued']

    def __str__(self):
        return f"{self.subject} — {self.title}"

    def due_date(self):
        from datetime import timedelta
        return self.date_issued + timedelta(days=self.period_days)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.assignment} — {self.student.username}"
