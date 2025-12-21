from django.db import models
from .base_models import *
from accounts.models import *

class Subject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    classname = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    penalty_info = models.CharField(max_length=128)
    module = models.IntegerField()
    date_of_issue = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.name[:16]

class Solution(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField(null=True, blank=True)
    link_to_file = models.CharField(max_length=128, null=True, blank=True)
    def __str__(self):
        return self.assignment.name