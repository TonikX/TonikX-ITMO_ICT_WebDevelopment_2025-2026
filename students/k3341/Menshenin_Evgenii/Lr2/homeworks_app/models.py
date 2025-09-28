from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_homework')
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_date = models.DateField()
    due_date = models.DateField()
    max_score = models.IntegerField(default=100)
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"
    
    def clean(self):
        if self.due_date and self.issue_date and self.due_date < self.issue_date:
            raise ValidationError("Due date must be after issue date.")
    
    def is_overdue(self):
        return date.today() > self.due_date

class Penalty(models.Model):
    PENALTY_TYPES = (
        ('percentage', 'Percentage'),
        ('points', 'Points'),
    )
    
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='penalties')
    penalty_type = models.CharField(max_length=15, choices=PENALTY_TYPES)
    days_after_due = models.IntegerField()
    penalty_value = models.FloatField()
    
    def __str__(self):
        return f"Penalty for {self.homework.title} after {self.days_after_due} days"

class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_submissions')
    content = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(blank=True, null=True)
    teacher_comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
    
    def is_late(self):
        return self.submission_date.date() > self.homework.due_date
    
    def get_penalty(self):
        if not self.is_late():
            return 0
        
        days_late = (self.submission_date.date() - self.homework.due_date).days
        penalty = self.homework.penalties.filter(days_after_due__lte=days_late).order_by('-days_after_due').first()
        
        if penalty:
            if penalty.penalty_type == 'percentage':
                return self.homework.max_score * (penalty.penalty_value / 100)
            else:
                return penalty.penalty_value
        return 0
    
    def get_final_score(self):
        if self.score is None:
            return None
        penalty = self.get_penalty()
        final_score = self.score - penalty
        return max(0, final_score)