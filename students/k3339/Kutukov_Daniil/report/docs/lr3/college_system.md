# Система управления колледжем

## Обзор

Комплексная система управления образовательным процессом в колледже, построенная на Django REST Framework.

## Модели данных

### Classroom (Кабинет)
```python
class Classroom(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=30)
```

### Subject (Дисциплина)
```python
class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    hours_per_semester = models.IntegerField(default=36)
```

### Teacher (Преподаватель)
```python
class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    subjects = models.ManyToManyField(Subject)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
```

### Student (Студент)
```python
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    group = models.CharField(max_length=20)
    enrollment_year = models.IntegerField()
```

### Grade (Оценка)
```python
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)])
    date = models.DateField(auto_now_add=True)
    semester = models.IntegerField()
```

## API Endpoints

- `GET/POST /api/classrooms/` - Управление кабинетами
- `GET/POST /api/subjects/` - Управление дисциплинами
- `GET/POST /api/teachers/` - Управление преподавателями
- `GET/POST /api/students/` - Управление студентами
- `GET/POST /api/grades/` - Управление оценками

## Технологии

- Django REST Framework для API
- Djoser для аутентификации
- CORS headers для кросс-доменных запросов
- SQLite база данных