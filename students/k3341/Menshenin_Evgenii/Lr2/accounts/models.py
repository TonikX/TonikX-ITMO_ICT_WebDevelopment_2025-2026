from django.db import models
from django.contrib.auth.models import User


class Classroom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    USER_GROUPS = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.CASCADE)
    group = models.CharField(max_length=10, default='student', choices=USER_GROUPS)

    def __str__(self):
        return f"{self.user.username} - {self.group}"
