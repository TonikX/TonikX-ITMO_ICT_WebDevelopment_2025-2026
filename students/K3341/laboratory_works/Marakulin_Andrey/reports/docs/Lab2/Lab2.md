# Отчет по лабораторной работе №2
### Тема: Доска домашних заданий

### Структура проекта

Проект представляет собой веб-приложение на Django, использующее PostgreSQL в качестве базы данных, запущенной в Docker-контейнере.

1.  **Проект `homework_project`**
    * `homework_project/settings.py` — основной файл настроек, включая подключение к БД PostgreSQL, регистрацию приложений и URL для редиректов.
    * `homework_project/urls.py` — главный файл URL-маршрутизации, подключающий маршруты приложения `board`.

2.  **Приложение `board`**
    * `models.py` — определяет структуру базы данных: модели `Subject`, `Teacher`, `Homework`, `Submission`.
    * `views.py` — содержит всю логику отображения страниц: регистрация, список заданий, детальная страница, сдача работы и панель успеваемости для учителя.
    * `forms.py` — определяет формы для регистрации (`SignUpForm`), сдачи работы (`SubmissionForm`) и фильтрации (`HomeworkFilterForm`).
    * `admin.py` — настраивает отображение моделей в административной панели Django для удобного управления контентом.
    * `urls.py` — определяет маршруты для всех страниц приложения `board`.
    * `templates/` — папка с HTML-шаблонами:
        * `base.html` — базовый шаблон с навигацией и стилями.
        * `board/homework_list.html` — страница со списком всех заданий.
        * `board/homework_detail.html` — страница с детальной информацией о задании и формой сдачи.
        * `board/gradebook.html` — страница с таблицей успеваемости для учителя.
        * `registration/` — шаблоны для регистрации и входа.
    * `static/` — папка со статическими файлами:
        * `board/style.css` — внешний файл стилей для всего сайта.

3.  **Конфигурация окружения**
    * `docker-compose.yml` — файл для запуска и управления контейнером с базой данных PostgreSQL.

---

## 1. Настройка проекта и Модель данных

Для хранения данных СУБД PostgreSQL запущенна в Docker-контейнере для изоляции и переносимости окружения. Модель данных спроектирована для отражения всех сущностей предметной области.

- **`Subject`**: Модель для учебных предметов.
- **`Teacher`**: Модель для преподавателей, связанная с пользователем Django.
- **`Homework`**: Основная модель для домашних заданий со связями `ForeignKey` к предметам и учителям.
- **`Submission`**: Модель для хранения ответов студентов, связывающая конкретного пользователя с конкретным заданием.

**Код:**

*docker-compose.yml:*
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=homework_db
      - POSTGRES_USER=hw_user
      - POSTGRES_PASSWORD=a_strong_password
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

*board/models.py:*
```python
from django.db import models
from django.contrib.auth.models import User


# Модель для учебных предметов
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


# Модель для преподавателей
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предмет")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


# Модель для домашних заданий
class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Тема задания")
    task_text = models.TextField(verbose_name="Текст задания")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    penalty_info = models.TextField(blank=True, null=True, verbose_name="Информация о штрафах")

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['-due_date']


# Модель для сданных студентами работ
class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions',
                                 verbose_name="Домашнее задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    submission_text = models.TextField(verbose_name="Текст ответа")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"Ответ от {self.student.username} на {self.homework.title}"

    class Meta:
        verbose_name = "Сданное задание"
        verbose_name_plural = "Сданные задания"
        # Уникальность: один студент может сдать одно задание только один раз
        unique_together = ('homework', 'student')
```

---
## 2. Аутентификация и Регистрация пользователей

Реализован стандартный для Django функционал регистрации, входа и выхода пользователей. Для регистрации используется кастомная форма `SignUpForm`, наследуемая от `UserCreationForm`, для добавления полей имени, фамилии и email. Представления (`Views`) используют встроенные в Django классы `CreateView`, `LoginView` и `LogoutView`.

**Код:**

*board/views.py (фрагмент):*
```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
```

*board/forms.py (фрагмент):*
```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
```

---
## 3. Функционал студента

Студент после авторизации может выполнять следующие действия:
- **Просматривать список** всех домашних заданий на главной странице. Список поддерживает пагинацию.
- **Открывать детальную страницу** каждого задания для просмотра полного текста.
- **Сдавать работу**, отправляя текстовый ответ через форму. Реализована проверка, запрещающая повторную сдачу одного и того же задания.

**Код:**

*board/views.py (фрагмент):*
```python
class HomeworkListView(ListView):
    model = Homework
    template_name = 'board/homework_list.html'
    context_object_name = 'homeworks'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = HomeworkFilterForm(self.request.GET)
        return context

class HomeworkDetailView(DetailView):
    model = Homework
    template_name = 'board/homework_detail.html'
    context_object_name = 'homework'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            existing_submission = Submission.objects.filter(
                homework=self.get_object(),
                student=self.request.user
            ).first()

            if existing_submission:
                context['existing_submission'] = existing_submission
            else:
                context['submission_form'] = SubmissionForm()

        return context

    def post(self, request, *args, **kwargs):
        homework = self.get_object()
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = request.user
            submission.save()
            return redirect('homework_detail', pk=homework.pk)

        context = self.get_context_data()
        context['submission_form'] = form
        return self.render_to_response(context)
```

---
## 4. Функционал учителя

Учитель (пользователь со статусом `is_staff`) имеет расширенные права:
- **Управление контентом** через стандартную административную панель Django (`/admin/`). Там он может создавать, редактировать и удалять предметы, задания и т.д.
- **Выставление оценок** через админ-панель. На странице задания отображаются все сданные по нему работы, где можно проставить оценку.
- **Просмотр успеваемости** на специальной странице сайта (`/gradebook/`), доступной только ему. На этой странице отображается таблица со всеми сданными работами всех студентов.

**Код:**

*board/admin.py:*
```python
from django.contrib import admin
from .models import Subject, Teacher, Homework, Submission

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date')
    list_filter = ('subject', 'teacher', 'due_date')
    search_fields = ('title', 'task_text')
    inlines = [SubmissionInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submission_date', 'grade')
    list_filter = ('homework__subject', 'student', 'grade')
    search_fields = ('student__username', 'homework__title')
    list_editable = ('grade',)

admin.site.register(Subject)
admin.site.register(Teacher)
```

*board/views.py (фрагмент):*
```python
from django.contrib.auth.mixins import UserPassesTestMixin

class GradebookView(UserPassesTestMixin, ListView):
    model = Submission
    template_name = 'board/gradebook.html'
    context_object_name = 'submissions'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Submission.objects.select_related('homework', 'student').order_by('homework__title', 'student__username')
```

---
## 5. Фильтрация и Стилизация

Для получения максимальной оценки реализован дополнительный функционал:
- **Фильтрация** списка домашних заданий по предмету с помощью выпадающего списка.
- **Стилизация** интерфейса с использованием внешнего CSS-файла для придания приложению аккуратного и современного вида.

**Код:**

*board/forms.py (фрагмент):*
```python
class HomeworkFilterForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="Все предметы",
        label="Фильтр по предмету"
    )
```

*board/static/board/style.css:*
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 960px;
    margin: auto;
    padding: 20px;
    background-color: #f8f9fa;
    color: #343a40;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #fff;
    padding: 15px 20px;
    margin-bottom: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

nav .user-info {
    display: flex;
    align-items: center;
}

nav a, .link-button {
    margin-left: 15px;
    font-weight: 500;
}

.link-button {
    background: none;
    border: none;
    color: #007bff;
    cursor: pointer;
    font-size: inherit;
    padding: 0;
}

.link-button:hover {
    text-decoration: underline;
}

.homework-item, .homework-detail, .submission-section {
    background: #fff;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

button {
    background-color: #007bff;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
}

button:hover {
    background-color: #0056b3;
}

input[type="text"], input[type="password"], input[type="email"], textarea {
    width: 100%;
    padding: 8px;
    margin: 6px 0 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

th, td {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: left;
}

thead {
    background-color: #f2f2f2;
}
```

### Выводы
В ходе выполнения лабораторной работы был разработан полнофункциональный веб-сервис на фреймворке Django. Были освоены ключевые концепции Django:
- Работа с моделями и Django ORM.
- Создание представлений на основе классов (CBV).
- Система аутентификации и разграничения прав доступа.
- Использование Django Forms для обработки пользовательского ввода.
- Работа с шаблонизатором Django, включая наследование шаблонов.
- Подключение статических файлов (CSS).
- Настройка и использование административной панели Django.

Кроме того, был повторен цикл работы с СУБД PostgreSQL и системой контейнеризации Docker.