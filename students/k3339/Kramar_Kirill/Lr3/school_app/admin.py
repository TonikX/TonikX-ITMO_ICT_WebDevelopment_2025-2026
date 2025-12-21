from django.contrib import admin
from .models import Klass, Teacher, Student, QuarterGrade, Classroom, Lesson, Subject

admin.site.register(Klass)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(QuarterGrade)
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(Subject)