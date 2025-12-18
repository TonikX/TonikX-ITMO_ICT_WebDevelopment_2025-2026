from django.db import models

class Klass(models.Model):
    id = models.AutoField(primary_key=True)
    parallel = models.IntegerField()
    class_number = models.CharField(max_length=10)
    class_teacher = models.OneToOneField(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f"{self.parallel}-{self.class_number}"

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ManyToManyField('Subject')
    class_lead = models.OneToOneField(
        Klass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Student(models.Model):
    GENDERS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDERS)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class QuarterGrade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.student}: {self.subject}-{self.grade}"

class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.type}-{self.number}"

class Lesson(models.Model):
    WEEKDAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    lesson_number = models.IntegerField()

    class Meta:
        unique_together = ('klass', 'weekday', 'lesson_number')

    def __str__(self):
        return f"{self.subject} ({self.weekday} - Lesson {self.lesson_number})"

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    subject_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"