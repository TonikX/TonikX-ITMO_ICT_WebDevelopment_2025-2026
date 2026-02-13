from django.contrib import admin

from .models import User
from django.contrib.auth.models import Group

admin.site.register(User)

user_group, created = Group.objects.get_or_create(name='Пользователь')
admin_group, created = Group.objects.get_or_create(name='Администратор')
