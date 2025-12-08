# Модели данных - Homework Board

## 📋 Обзор

В проекте Homework Board используются 5 основных моделей данных:

1. **User** - пользователи системы
2. **Subject** - учебные предметы
3. **Assignment** - домашние задания
4. **Submission** - сдачи заданий студентами
5. **Grade** - оценки за задания

## 👤 User (Пользователь)

Расширенная модель пользователя на основе `AbstractUser`.

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Студент'),
        (TEACHER, 'Преподаватель'),
        (ADMIN, 'Администратор'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
        verbose_name="Роль"
    )
    student_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Студенческий билет"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `username` | CharField | Уникальное имя пользователя (наследуется) |
| `email` | EmailField | Email адрес (наследуется) |
| `first_name` | CharField | Имя (наследуется) |
| `last_name` | CharField | Фамилия (наследуется) |
| `role` | CharField | Роль в системе (student/teacher/admin) |
| `student_id` | CharField | Номер студенческого билета |
| `phone` | CharField | Контактный телефон |
| `birth_date` | DateField | Дата рождения |

### Методы

```python
def __str__(self):
    return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
```

### Связи

- `created_assignments` - задания, созданные преподавателем (reverse ForeignKey)
- `submissions` - сдачи студента (reverse ForeignKey)
- `graded_assignments` - оценки, выставленные преподавателем (reverse ForeignKey)

## 📚 Subject (Предмет)

Модель для хранения информации об учебных предметах.

```python
class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название предмета",
        unique=True
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание предмета"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | CharField | Уникальное название предмета |
| `description` | TextField | Описание предмета (опционально) |
| `created_at` | DateTimeField | Дата создания записи |

### Meta опции

```python
class Meta:
    verbose_name = "Предмет"
    verbose_name_plural = "Предметы"
    ordering = ['name']
```

## 📝 Assignment (Домашнее задание)

Основная модель для хранения домашних заданий.

```python
class Assignment(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет"
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_assignments',
        verbose_name="Преподаватель"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название задания"
    )
    description = models.TextField(
        verbose_name="Описание задания"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата выдачи"
    )
    due_date = models.DateTimeField(
        verbose_name="Срок выполнения"
    )
    penalty_info = models.TextField(
        blank=True,
        null=True,
        verbose_name="Информация о штрафах"
    )
    max_points = models.PositiveIntegerField(
        default=100,
        verbose_name="Максимальный балл",
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно"
    )
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `subject` | ForeignKey(Subject) | Связь с предметом |
| `teacher` | ForeignKey(User) | Преподаватель-автор |
| `title` | CharField | Название задания |
| `description` | TextField | Полное описание задания |
| `created_at` | DateTimeField | Дата создания |
| `due_date` | DateTimeField | Срок сдачи |
| `penalty_info` | TextField | Информация о штрафах |
| `max_points` | PositiveIntegerField | Максимальный балл (1-1000) |
| `is_active` | BooleanField | Флаг активности |

### Методы

```python
def __str__(self):
    return f"{self.subject.name} - {self.title}"

def is_overdue(self):
    """Проверяет, просрочено ли задание"""
    return timezone.now() > self.due_date
```

### Связи

- `submissions` - сдачи этого задания (reverse ForeignKey)

## 📤 Submission (Сдача задания)

Модель для хранения сдач заданий студентами.

```python
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Задание"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Студент"
    )
    content = models.TextField(
        verbose_name="Текст сдачи"
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата сдачи"
    )
    is_late = models.BooleanField(
        default=False,
        verbose_name="Сдано с опозданием"
    )
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `assignment` | ForeignKey(Assignment) | Связь с заданием |
| `student` | ForeignKey(User) | Студент |
| `content` | TextField | Текст/описание сдачи |
| `submitted_at` | DateTimeField | Дата и время сдачи |
| `is_late` | BooleanField | Флаг опоздания |

### Методы

```python
def save(self, *args, **kwargs):
    # Проверяем, сдано ли задание с опозданием
    if self.assignment.due_date < timezone.now():
        self.is_late = True
    super().save(*args, **kwargs)

def __str__(self):
    return f"{self.student} - {self.assignment.title}"
```

### Meta опции

```python
class Meta:
    verbose_name = "Сдача задания"
    verbose_name_plural = "Сдачи заданий"
    ordering = ['-submitted_at']
    unique_together = ['assignment', 'student']  # Студент может сдать задание только один раз
```

## ⭐ Grade (Оценка)

Модель для хранения оценок за сдачи.

```python
class Grade(models.Model):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade',
        verbose_name="Сдача"
    )
    points = models.PositiveIntegerField(
        verbose_name="Полученные баллы",
        validators=[MinValueValidator(0)]
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий преподавателя"
    )
    graded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='graded_assignments',
        verbose_name="Оценил"
    )
    graded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оценки"
    )
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `submission` | OneToOneField(Submission) | Связь со сдачей (1:1) |
| `points` | PositiveIntegerField | Полученные баллы |
| `feedback` | TextField | Комментарий преподавателя |
| `graded_by` | ForeignKey(User) | Преподаватель, выставивший оценку |
| `graded_at` | DateTimeField | Дата выставления оценки |

### Методы

```python
def __str__(self):
    return f"{self.submission.student} - {self.points}/{self.submission.assignment.max_points}"

def get_percentage(self):
    """Возвращает процент от максимального балла"""
    return round((self.points / self.submission.assignment.max_points) * 100, 2)
```

## 🔗 Связи между моделями

### Диаграмма связей

```
User (Teacher) ─┬─ creates ──→ Assignment
                │
User (Student) ─┼─ submits ──→ Submission ──→ Grade
                │
User (Teacher) ─┴─ grades ───→ Grade

Subject ──→ Assignment
```

### Типы связей

1. **User → Assignment** (ForeignKey)
   - Один преподаватель может создать много заданий
   - Каждое задание создано одним преподавателем

2. **Subject → Assignment** (ForeignKey)
   - Один предмет может иметь много заданий
   - Каждое задание относится к одному предмету

3. **User → Submission** (ForeignKey)
   - Один студент может сдать много заданий
   - Каждая сдача принадлежит одному студенту

4. **Assignment → Submission** (ForeignKey)
   - Одно задание может иметь много сдач
   - Каждая сдача относится к одному заданию

5. **Submission → Grade** (OneToOneField)
   - У одной сдачи может быть только одна оценка
   - Каждая оценка относится к одной сдаче

6. **User → Grade** (ForeignKey)
   - Один преподаватель может выставить много оценок
   - Каждая оценка выставлена одним преподавателем

## 💾 Миграции

Для создания таблиц в базе данных выполните:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔍 Примеры запросов

### Получить все задания по предмету

```python
subject = Subject.objects.get(name="Математика")
assignments = Assignment.objects.filter(subject=subject)
```

### Получить сдачи студента

```python
student = User.objects.get(username="ivanov")
submissions = Submission.objects.filter(student=student)
```

### Получить непроверенные сдачи

```python
ungraded = Submission.objects.filter(grade__isnull=True)
```

### Средний балл студента

```python
from django.db.models import Avg

avg_grade = Grade.objects.filter(
    submission__student=student
).aggregate(Avg('points'))
```

---

!!! tip "Совет"
    Используйте `select_related()` и `prefetch_related()` для оптимизации запросов с связями!
