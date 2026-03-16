# Практическая работа №2.2

## Практическое задание 1

Правильно настроить связь между автомобилем, владением и владельцем.

### Выполнение задания 1

Чтобы реализовать связь "многие-ко-многим" между владельцем и автомобилем через владение, воспользуемся полем `ManyToManyField`:

```python title="django_project_klimenkov/project_first_app/models.py"
class Owner(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    # Добавим это поле для реализации связи "многие-ко-многим"
    cars = models.ManyToManyField('Car', through='Ownership')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
```

Теперь связь между владельцем и автомобилем стала более полной, что даёт возможность в перспективе обращаться к автомобилям через их владельца и к владельцам через автомобиль, которым они обладали или обладают.

Чтобы применить эти изменения нужно будет сделать миграцию:

```
python3 manage.py makemigrations project_first_app
python3 manage.py migrate
```

## Практическое задание 2

1. Реализовать вывод всех владельцев функционально. Добавить данные минимум от трех владельцах. Должны быть реализованы контроллер (views) и шаблоны (templates).
2. Реализовать вывод всех автомобилей, вывод автомобиля по id, обновления на основе классов. Добавить данные минимум о трёх автомобилях. Должны быть реализованы контроллер (views) и шаблоны (templates).

### Выполнение задания 2

Для начала реализуем вывод всех владельцев в виде списка с помощью представления на основе функции.

Создадим представление для вывода списка всех владельцев:

```python title="django_project_klimenkov/project_first_app/views.py"
def owners_list(request):
    """
    Представление для отображения списка всех владельцев автомобилей.
    """
    # Получаем всех владельцев и передаём их в html-шаблон
    owners = Owner.objects.all()
    return render(request, 'owners/owners_list.html', {'owners': owners})
```

Также создадим соответствующий html-шаблон:

```html title="django_project_klimenkov/templates/owners/owners_list.html"
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список автовладельцев</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>

    <h1>Список автовладельцев</h1>
    
    {% if owners %}
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Фамилия</th>
                </tr>
            </thead>
            <tbody>
                {% for owner in owners %}
                <tr>
                    <td>{{ owner.id }}</td>
                    <td>{{ owner.first_name }}</td>
                    <td>{{ owner.last_name }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Автовладельцы не найдены.</p>
    {% endif %}
</body>
</html>
```

В шаблоне перебираем всех владельцев и выводим основную информацию о них. Также подключаем CSS-стили, чтобы список выглядел более красиво.

Чтобы к странице можно было получить доступ по url-запросу, зарегистрируем созданное выше представление в `urls.py`:

```python title="django_project_klimenkov/project_first_app/urls.py"
urlpatterns = [
    path('owner/<int:id>/', views.owner_detail, name='owner_detail'),

    # Даём доступ к представлению по url-запросу
    path('owner/list/', views.owners_list, name='owners_list'),
]
```

Теперь при переходе по адресу `http://127.0.0.1:8000/owner/list/` видим таблицу со всеми владельцами:

![1](../img/lab_2/pw_2/1.png)

Чтобы упростить навигацию по веб-приложению, сделаем переадресацию с адреса `http://127.0.0.1:8000/` на `http://127.0.0.1:8000/owner/list/`, чтобы по умолчанию открывался именно список владельцев:

```python title="django_project_klimenkov/project_first_app/views.py"
# Добавим представление для переадресация в owners_list
def root_redirect(request):
    return redirect('owners_list')
```

```python title="django_project_klimenkov/project_first_app/urls.py"
urlpatterns = [
    # Привяжем root_redirect к корневому адресу
    path('', views.root_redirect),

    path('owner/<int:id>/', views.owner_detail, name='owner_detail'),
    path('owner/list/', views.owners_list, name='owners_list'),
]
```

Также дадим пользователю возможность перейти со страницы списка владельцев к странице с детальной информацией о владельце и обратно.

```html title="django_project_klimenkov/templates/owners/owners_list.html"
{% if owners %}
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Имя</th>
                <th>Фамилия</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {% for owner in owners %}
            <tr>
                <td>{{ owner.id }}</td>
                <td>{{ owner.first_name }}</td>
                <td>{{ owner.last_name }}</td>
                <td>

                    <!-- Добавляем ссылку на страницу с информацией о владельце -->
                    <a href="{% url 'owner_detail' owner.id %}">
                        Подробнее
                    </a>

                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% else %}
    <p>Автовладельцы не найдены.</p>
{% endif %}
```

```html title=""
<body>

    <!-- Добавляем ссылку на список владельцев -->
    <a href="{% url 'owners_list' %}" class="back-button">← Назад к списку автовладельцев</a>

    <h1>Информация об автовладельце</h1>
    <div class="detail-card">
        <p><strong>ID:</strong> {{ owner.id }}</p>
        <p><strong>Фамилия:</strong> {{ owner.last_name }}</p>
        <p><strong>Имя:</strong> {{ owner.first_name }}</p>
        <p><strong>Дата рождения:</strong> {{ owner.birth_date }}</p>
    </div>
</body>
```

Теперь между этими страницами можно переключаться:

![2](../img/lab_2/pw_2/2.png)

![3](../img/lab_2/pw_2/3.png)

Реализуем аналогичный функционал и для автомобилей, но в этот раз с помощью представлений на основе классов.

```python title="django_project_klimenkov/project_first_app/views.py"
from django.views.generic import ListView, DetailView
from .models import Owner, Car


# Представление для вывода списка автомобилей
class CarsListView(ListView):
    model = Car
    template_name = 'cars/cars_list.html'
    context_object_name = 'cars'


# Представление для вывода детальной информации об автомобиле
class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'
```

Создаём соответствующие html-шаблоны:

```html title="django_project_klimenkov/templates/cars/car_detail.html"
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Информация об автомобиле</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>
    <a href="{% url 'cars_list' %}" class="back-button">← Назад к списку автомобилей</a>

    <h1>Информация об автомобиле</h1>
    
    <div class="detail-card">
        <p><strong>ID:</strong> {{ car.car_id }}</p>
        <p><strong>Модель:</strong> {{ car.model }}</p>
        <p><strong>Государственный номер:</strong> {{ car.license_plate }}</p>
        <p><strong>Цвет:</strong> {{ car.color|default:"Не указан" }}</p>
    </div>
</body>
</html>
```

```html title="django_project_klimenkov/templates/cars/cars_list.html"
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список автомобилей</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>
    <h1>Список автомобилей</h1>
    
    {% if cars %}
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Модель</th>
                    <th>Гос. номер</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {% for car in cars %}
                <tr>
                    <td>{{ car.car_id }}</td>
                    <td>{{ car.model }}</td>
                    <td>{{ car.license_plate }}</td>
                    <td>
                        <a href="{% url 'car_detail' car.car_id %}">
                            Подробнее
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Автомобили не найдены.</p>
    {% endif %}
</body>
</html>
```

Регистрируем url-адреса:

```python title="django_project_klimenkov/project_first_app/urls.py"
urlpatterns = [
    path('', views.root_redirect),

    # Владельцы
    path('owner/list/', views.owners_list, name='owners_list'),
    path('owner/<int:id>/', views.owner_detail, name='owner_detail'),

    # Автомобили
    path('car/list/', views.CarsListView.as_view(), name='cars_list'),
    path('car/<int:car_id>/', views.CarDetailView.as_view(), name='car_detail'),
]
```

Также добавим в `owners_list.html` и `cars_list.html` меню для переключения между списками и доступом к админ-панели:

```html title="django_project_klimenkov/templates/owners/owners_list.html"
<body>

    <!-- Добавленное меню -->
    <div class="nav-menu">
        <p><strong>Список автовладельцев</strong></p>
        <a href="{% url 'cars_list' %}">Список автомобилей</a><br>
        <a href="/admin">Админ-панель</a>
    </div>

    <h1>Список автовладельцев</h1>
```

```html title="django_project_klimenkov/templates/cars/cars_list.html"
<body>
    <div class="nav-menu">
        <a href="{% url 'owners_list' %}">Список автовладельцев</a>
        <p><strong>Список автомобилей</strong></p>
        <a href="/admin">Админ-панель</a>
    </div>

    <h1>Список автомобилей</h1>
```

В результате получился следующий функционал для автомобилей (аналогичный таковому для владельцев, но на основе классов):

![4](../img/lab_2/pw_2/4.png)

![5](../img/lab_2/pw_2/5.png)

## Практическое задание 3

1. Реализовать форму ввода всех владельцев функционально. Добавить данные минимум о ещё трёх владельцах. Должны быть реализованы форма (Form), контроллер (views) и шаблоны (templates).
2. Реализовать форму ввода, обновления и удаления всех автомобилей на основе классов. Добавить данные минимум о ещё трех автомобилях. Должны быть реализованы форма (Form), контроллер (views) и шаблоны (templates).

### Выполнение задания 3

Реализуем механизмы добавления, изменения и удаления владельцев функционально.

Создадим файл `django_project_klimenkov/project_first_app/forms.py`, в который добавим форму владельца:

```python title="django_project_klimenkov/project_first_app/forms.py"
from django import forms
from .models import Owner


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['username', 'password', 'first_name', 'last_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }
```

(Добавим в форму также поля `username` и `password`, так как они обязательны для модели пользователя, коим как раз и является владелец.)

Теперь эту форму можно будет использовать для реализации механизмов добавления и редактирования владельцев.

Создадим соответствующие представления:

```python title="django_project_klimenkov/project_first_app/views.py"
# Представление для создания владельца
def create_owner(request):
    # Если приходит форма, то проверяем её на корректность и сохраняем
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owners_list')
    # Если иной запрос (запрос на получение формы), то создаём и возвращаем форму
    else:
        form = OwnerForm()
    return render(request, 'owners/create_owner.html', {'form': form})


# Представление для редактирования владельца
def edit_owner(request, id):
    owner = get_object_or_404(Owner, id=id)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owners_list')
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'owners/edit_owner.html', {'form': form, 'owner': owner})


# Представление для удаления владельца
def delete_owner(request, id):
    owner = get_object_or_404(Owner, id=id)
    if request.method == 'POST':
        owner.delete()
        return redirect('owners_list')
    return render(request, 'owners/confirm_delete_owner.html', {'owner': owner})
```

Для представлений создадим html-шаблоны:

```html title="django_project_klimenkov/templates/owners/create_owner.html"
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>Добавить автовладельца</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>

    <h1>Добавить автовладельца</h1>
    
    <form method="post" class="form">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="buttons">
            <button type="submit">Добавить</button>
            <a href="{% url 'owners_list' %}">Отмена</a>
        </div>
    </form>
</body>
</html>
```

```html title="django_project_klimenkov/templates/owners/edit_owner.html"
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>Изменить автовладельца</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>
    
    <h1>Изменить автовладельца: {{ owner.first_name }} {{ owner.last_name }} (ID: {{ owner.id }})</h1>
    
    <form method="post" class="form">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="buttons">
            <button type="submit">Сохранить</button>
            <a href="{% url 'owners_list' %}">Отмена</a>
        </div>
    </form>
</body>
</html>
```

```html title="django_project_klimenkov/templates/owners/confirm_delete_owner.html"
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Подтверждение удаления</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>
    <h1>Подтверждение удаления</h1>

    <div class="form">
        <p>Вы уверены, что хотите удалить автовладельца:</p>
        <p><strong>{{ owner.first_name }} {{ owner.last_name }} (ID: {{ owner.id }})</strong>?</p>
        
        <form method="post">
            {% csrf_token %}
            <div class="buttons">
                <button type="submit" class="delete">Да, удалить</button>
                <a href="{% url 'owners_list' %}">Отмена</a>
            </div>
        </form>
    </div>
</body>
</html>
```

Зарегистрируем представления в `urls.py`:

```python title="django_project_klimenkov/project_first_app/urls.py"
urlpatterns = [
    path('', views.root_redirect),

    # Владельцы
    path('owner/list/', views.owners_list, name='owners_list'),
    path('owner/<int:id>/', views.owner_detail, name='owner_detail'),

    # Зарегистрируем представления для создания, редактирования и удаления владельцев
    path('owner/create/', views.create_owner, name='create_owner'),
    path('owner/edit/<int:id>/', views.edit_owner, name='edit_owner'),
    path('owner/delete/<int:id>/', views.delete_owner, name='delete_owner'),

    # Автомобили
    path('car/list/', views.CarsListView.as_view(), name='cars_list'),
    path('car/<int:car_id>/', views.CarDetailView.as_view(), name='car_detail'),
]
```

Также добавим соответствующие кнопки в `owners_list.html`:

```html title="django_project_klimenkov/templates/owners/owners_list.html"
<h1>Список автовладельцев</h1>

    <!-- Кнопка для добавления владельца -->
    <a href="{% url 'create_owner' %}" class="create-button">Добавить автовладельца</a>
    
    {% if owners %}
        <table class="table">

<!-- ... -->

            <td>
                <a href="{% url 'owner_detail' owner.id %}">
                    Подробнее
                </a>
            </td>
            <td>
                <!-- Кнопка для изменения владельца -->
                <a href="{% url 'edit_owner' owner.id %}">
                    Изменить
                </a>
            </td>
            <td>
                <!-- Кнопка для удаления владельца -->
                <a href="{% url 'delete_owner' owner.id %}" class="delete">
                    Удалить
                </a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

В результате для автовладельцев был реализован функционал добавления, изменения и удаления:

![6](../img/lab_2/pw_2/6.png)

![7](../img/lab_2/pw_2/7.png)

![8](../img/lab_2/pw_2/8.png)

![9](../img/lab_2/pw_2/9.png)

![10](../img/lab_2/pw_2/10.png)

![11](../img/lab_2/pw_2/11.png)

![12](../img/lab_2/pw_2/12.png)

Теперь реализуем аналогичный функционал для автомобилей, но на основе классов.

Создадим соответствующие представления на основе классов:

```python title="django_project_klimenkov/project_first_app/views.py"
# Добавить автомобиль
class CarCreateView(CreateView):
    model = Car
    template_name = 'cars/create_car.html'
    fields = ['license_plate', 'model', 'color']
    success_url = reverse_lazy('cars_list')


# Изменить автомобиль
class CarUpdateView(UpdateView):
    model = Car
    template_name = 'cars/edit_car.html'
    fields = ['license_plate', 'model', 'color']
    success_url = reverse_lazy('cars_list')
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'


# Удалить автомобиль
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'cars/confirm_delete_car.html'
    success_url = reverse_lazy('cars_list')
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'
```

Добавим представления в `urls.py`:

```python title="django_project_klimenkov/project_first_app/urls.py"
# Автомобили
path('car/list/', views.CarsListView.as_view(), name='cars_list'),
path('car/<int:car_id>/', views.CarDetailView.as_view(), name='car_detail'),

# Добавим эти url-адреса
path('car/create/', views.CarCreateView.as_view(), name='create_car'),
path('car/edit/<int:car_id>/', views.CarUpdateView.as_view(), name='edit_car'),
path('car/delete/<int:car_id>/', views.CarDeleteView.as_view(), name='delete_car'),
```

Создадим html-шаблоны `django_project_klimenkov/templates/cars/create_car.html`, `django_project_klimenkov/templates/cars/edit_car.html` и `django_project_klimenkov/templates/cars/confirm_delete_car.html` аналогичные таковым для работы с владельцами.

Также добавим в html-шаблон `django_project_klimenkov/templates/cars/cars_list.html` кнопки для реализации соответствующего функционала (аналогично таковым в случае с владельцами).

В результате получаем аналогичный функционал для добавления, изменения и удаления автомобилей, но на основе классов:

![13](../img/lab_2/pw_2/13.png)

![14](../img/lab_2/pw_2/14.png)

![15](../img/lab_2/pw_2/15.png)

![16](../img/lab_2/pw_2/16.png)

![17](../img/lab_2/pw_2/17.png)

![18](../img/lab_2/pw_2/18.png)

![19](../img/lab_2/pw_2/19.png)
