# Отчёт по лабораторной работе №2  
## Тема: Веб-приложение «Доска домашних заданий» на Django 

В ходе лабораторной работы был разработан и оформлен полноценный веб-сервис **«Доска домашних заданий»**, реализованный на фреймворке **Django**.  
Приложение предназначено для взаимодействия преподавателя и студентов: оно позволяет создавать, публиковать, просматривать и сдавать домашние задания, а также выставлять оценки и анализировать успеваемость.  

## Цель, задачи и результат

**Цель:**  
Создать минимально жизнеспособную систему управления домашними заданиями, запускаемую локально без Docker и сторонних контейнеров.

**Задачи:**  
- спроектировать модели данных для хранения информации о заданиях, преподавателях и ответах студентов;  
- реализовать систему регистрации и аутентификации пользователей;  
- разграничить доступ по ролям: преподаватель (администратор) и студент;  
- реализовать основные пользовательские сценарии — создание, просмотр, фильтрация и сдача заданий;  
- разработать визуально аккуратный интерфейс в едином цветовом стиле.

**Результат:**  
Готовый Django-проект с приложением `board`, панелью администратора и страницами для студентов и преподавателей.  
Добавлена кнопка **«Добавить домашку»** для преподавателя, ведущая в админ-панель, а также реализована страница **«Успеваемость»**, отображающая все сданные работы и оценки.


## Архитектура и структура проекта
```bash
homework_project/
│
├── homework_project/
│   ├── settings.py            # настройки Django
│   ├── urls.py                # маршрутизация
│   └── wsgi.py / asgi.py      # конфигурация сервера приложения
│
├── board/
│   ├── models.py              # модели данных
│   ├── views.py               # представления (CBV)
│   ├── forms.py               # формы регистрации, фильтрации и сдачи
│   ├── admin.py               # регистрация моделей в админ-панели
│   ├── urls.py                # маршруты приложения
├── templates/                 # HTML-шаблоны (клиентская часть)
│   ├── base.html              # базовый шаблон (меню, шапка, подключение стилей)
│   │
│   ├── board/                 # страницы, связанные с заданиями
│   │   ├── homework_list.html     # список домашних заданий (с фильтром и пагинацией)
│   │   ├── homework_detail.html   # детальная страница конкретного задания и форма сдачи
│   │   └── gradebook.html         # таблица успеваемости преподавателя
│   │
│   └── registration/          # шаблоны аутентификации и регистрации
│       ├── login.html             # форма входа пользователя
│       └── signup.html            # форма регистрации нового пользователя
│
├── db.sqlite3                 # локальная база данных 
├── manage.py                  # точка входа в Django-приложение
└── requirements.txt           # зависимости проекта

```
База данных создаётся автоматически при выполнении миграций, проект полностью автономен и не требует Docker-окружения.


## Модель данных

### Основные модели:

```python
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предмет")


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    title = models.CharField(max_length=200, verbose_name="Тема задания")
    task_text = models.TextField(verbose_name="Текст задания")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    penalty_info = models.TextField(blank=True, null=True, verbose_name="Информация о штрафах")


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions', verbose_name="Домашнее задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    submission_text = models.TextField(verbose_name="Текст ответа")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")

    class Meta:
        unique_together = ('homework', 'student')

```

Модель Homework хранит всю необходимую информацию по условию задания: предмет, преподаватель, дата выдачи, срок сдачи, текст задания и сведения о штрафах.
Модель Submission фиксирует сдачу студентом и обеспечивает уникальность каждой попытки.

## Роли и пользовательские сценарии

Студент может:
зарегистрироваться и войти в систему;
просматривать все доступные задания;
фильтровать их по предмету;
открыть детальную страницу с описанием задания;
отправить решение в текстовом виде;
видеть отметку о сдаче и оценку после проверки.

Преподаватель может:
добавлять, редактировать и удалять задания через админ-панель /admin/;
выставлять оценки студентам в разделе «Сданные работы»;
просматривать таблицу успеваемости /gradebook/;
создавать задания с помощью кнопки «Добавить домашку» на клиентской части.

Представления (Views)

В проекте реализованы классовые представления Django (CBV):

```python
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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


class GradebookView(UserPassesTestMixin, ListView):
    model = Submission
    template_name = 'board/gradebook.html'
    context_object_name = 'submissions'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Submission.objects.select_related('homework', 'student').order_by('homework__title', 'student__username')

```
Используется пагинация и фильтрация по предметам.
Администратор видит все сдачи студентов в таблице, студенты — только свои работы.


## Визуальное оформление
Интерфейс сайта выполнен в фирменных цветах — оранжево-жёлто-красных, символизирующих энергию и активность.
Навигационная панель оформлена плавным градиентом, карточки заданий имеют белый фон и мягкие тени, а кнопки при наведении подсвечиваются и меняют оттенок.

```css
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(90deg, #fb8500, #ffb703);
  padding: 15px 25px;
  border-radius: 14px;
  color: white;
  box-shadow: 0 3px 8px rgba(255, 100, 0, 0.25);
}

button {
  background: linear-gradient(90deg, #fb8500, #ffb703);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 18px;
  cursor: pointer;
}
```

## Запуск проекта

```python
# Установка Django
pip install django

# Применение миграций
python manage.py makemigrations
python manage.py migrate

# Создание администратора
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```
## Вывод
В результате работы создан законченный веб-сервис на Django, позволяющий преподавателю управлять домашними заданиями, а студентам — просматривать и сдавать их онлайн.
Приложение обладает продуманной архитектурой, лаконичным интерфейсом и реализует все обязательные и дополнительные функции, включая фильтрацию, пагинацию и систему оценок.
