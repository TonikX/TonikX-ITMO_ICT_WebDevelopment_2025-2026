from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, related_name='given_homeworks')
    given_at = models.DateField()
    due_from = models.DateField()
    due_to = models.DateField()
    text = models.TextField()
    penalty_info = models.CharField(max_length=255, blank=True)
    def __str__(self): return f'{self.subject} / {self.given_at}'

class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        unique_together = ('homework', 'student')
    def __str__(self): return f'{self.student} → {self.homework}'

class Review(models.Model):
    """Отзывы к заданиям (рейтинг 1–10 + текст, автор)"""
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_reviews')
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Review {self.rating}/10 by {self.author}'
