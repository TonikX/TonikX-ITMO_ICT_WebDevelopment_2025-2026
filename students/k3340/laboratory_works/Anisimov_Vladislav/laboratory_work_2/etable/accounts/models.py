from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from main.base_models import *

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('admin', 'Администратор'),
    )
    classname = models.ForeignKey(Class, on_delete=models.DO_NOTHING, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    username = models.CharField(max_length=32, unique=True, db_index=True)
    full_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username