from django.contrib import admin
from .models import User
from .models import SchoolClass
from .models import Student
from .models import Teacher
from .models import Subject
from .models import Homework
from .models import HomeworkSubmission
# Register your models here.

admin.site.register(User)
admin.site.register(SchoolClass)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
