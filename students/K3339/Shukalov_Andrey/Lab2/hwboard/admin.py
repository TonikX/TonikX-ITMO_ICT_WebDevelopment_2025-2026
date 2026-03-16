from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import *

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Subject)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
admin.site.register(Grade)