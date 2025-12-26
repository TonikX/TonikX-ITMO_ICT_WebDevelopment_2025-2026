# Бизнес-логика

## Введение

Бизнес-логика - это правила и алгоритмы, которые определяют, как работает приложение. В этом разделе я опишу основные процессы и проверки, которые реализованы в проекте.

## Регистрация и профили пользователей

### Создание нового пользователя

Когда кто-то регистрируется на сайте, происходит следующее:

1. Пользователь заполняет форму регистрации (имя пользователя, email, пароль)
2. Django создает объект `User` в базе данных
3. Автоматически срабатывает сигнал `post_save`
4. Создается пустой профиль `DriverProfile` с пустым полем `full_name`
5. Пользователь перенаправляется на страницу заполнения профиля

**Код сигнала:**

```python
@receiver(post_save, sender=User)
def create_or_update_driver_profile(sender, instance, created, **kwargs):
    if created:
        DriverProfile.objects.create(user=instance, full_name='')
```

### Обязательное заполнение профиля

Пользователь не может участвовать в гонках, пока не заполнит профиль. Проверка происходит в нескольких местах:

**1. При попытке зарегистрироваться на гонку:**

```python
if not driver_profile.full_name or driver_profile.full_name.strip() == '':
    messages.warning(request, 'Для регистрации на гонку сначала заполните свой профиль')
    return redirect('driverprofile_update')
```

**2. При попытке добавить комментарий:**

```python
if not request.user.driver_profile.full_name:
    messages.warning(request, 'Для добавления комментария сначала заполните свой профиль')
    return redirect('driverprofile_update')
```

**3. При просмотре профиля:**

Если `full_name` пустой, пользователя сразу перенаправляют на редактирование:

```python
def get(self, request, *args, **kwargs):
    profile = self.get_object()
    if not profile.full_name or profile.full_name.strip() == '':
        messages.info(request, 'Пожалуйста, заполните свой профиль')
        return redirect('driverprofile_update')
    return super().get(request, *args, **kwargs)
```

## Управление гонками

### Видимость гонок

Обычные пользователи видят только опубликованные гонки:

```python
def get_queryset(self):
    queryset = Race.objects.filter(is_published=True)
    # ...
```

Администраторы через админ-панель видят все гонки и могут их публиковать или скрывать.

### Поиск и фильтрация гонок

Пользователи могут искать гонки по:

- Названию
- Месту проведения
- Описанию

```python
search_query = self.request.GET.get('search', '').strip()
if search_query:
    queryset = queryset.filter(
        Q(title__icontains=search_query) |
        Q(location__icontains=search_query) |
        Q(description__icontains=search_query)
    )
```

`Q` объекты позволяют делать сложные запросы с условием "ИЛИ".

### Сортировка

Доступны варианты сортировки:

- По дате (новые/старые)
- По названию (А-Я / Я-А)
- По месту проведения

```python
sort_by = self.request.GET.get('sort', '-date')
if sort_by in ['date', '-date', 'title', '-title', 'location', '-location']:
    queryset = queryset.order_by(sort_by)
```

Знак минус перед полем означает обратную сортировку.

## Регистрация на гонки

### Процесс регистрации

1. Пользователь открывает страницу гонки
2. Проверяется, заполнен ли профиль
3. Проверяется, не зарегистрирован ли уже
4. Если все ок, пользователь может зарегистрироваться

**Код проверки:**

```python
# Проверка профиля
if not driver_profile.full_name or driver_profile.full_name.strip() == '':
    messages.warning(request, 'Для регистрации на гонку сначала заполните профиль')
    return redirect('driverprofile_update')

# Проверка существующей регистрации
existing_registration = Registration.objects.filter(
    driver=driver_profile,
    race=race,
    active=True
).first()

if existing_registration:
    messages.warning(request, 'Вы уже зарегистрированы на эту гонку')
    return redirect('race_detail', pk=pk)
```

### Уникальность регистрации

В базе данных есть ограничение, которое не позволяет одному водителю зарегистрироваться на одну гонку дважды:

```python
constraints = [
    UniqueConstraint(
        fields=['driver', 'race'],
        name='unique_driver_race_registration'
    )
]
```

Если кто-то попытается обойти проверку в коде, база данных выдаст ошибку.

### Отмена регистрации

Водитель может отменить свою регистрацию. При этом регистрация не удаляется, а помечается как неактивная:

```python
registration.active = False
registration.save()
```

Это сохраняет историю регистраций.

## Заезды и результаты

### Создание заездов

Заезды создаются администратором через админ-панель. Один заезд относится к одной гонке.

Типичная структура:

- Квалификация (5 кругов)
- Полуфинал (8 кругов)
- Финал (12 кругов)

### Добавление результатов

При добавлении результата водителя в заезде происходит важная проверка:

**Водитель должен быть зарегистрирован на эту гонку!**

```python
def clean(self):
    if self.heat and self.driver:
        is_registered = Registration.objects.filter(
            driver=self.driver,
            race=self.heat.race,
            active=True
        ).exists()
        
        if not is_registered:
            raise ValidationError(
                f'Водитель {self.driver.full_name} не зарегистрирован на гонку'
            )
```

Этот метод вызывается автоматически перед сохранением в базу:

```python
def save(self, *args, **kwargs):
    self.clean()  # Вызываем валидацию
    super().save(*args, **kwargs)
```

### Уникальность результатов

Один водитель может иметь только один результат в одном заезде:

```python
constraints = [
    UniqueConstraint(
        fields=['heat', 'driver'],
        name='unique_heat_driver_result'
    )
]
```

### Отображение результатов

На странице гонки результаты отображаются отсортированными по позиции:

```python
results = heat.results.select_related('driver', 'driver__team').order_by('position', 'finish_time_seconds')
```

Первые три места получают медали в интерфейсе.

## Комментарии

### Добавление комментария

Только зарегистрированные пользователи с заполненным профилем могут добавлять комментарии.

**Валидация рейтинга:**

В форме проверяется, что рейтинг от 1 до 10:

```python
def clean_rating(self):
    rating = self.cleaned_data.get('rating')
    if rating is not None and (rating < 1 or rating > 10):
        raise ValidationError('Рейтинг должен быть от 1 до 10.')
    return rating
```

Также на уровне модели:

```python
rating = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(10)],
    verbose_name='Рейтинг (1-10)'
)
```

### Редактирование и удаление

Пользователь может редактировать и удалять только свои комментарии. Это проверяется через миксин `OwnerRequiredMixin`:

```python
class OwnerRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Админы могут редактировать что угодно
        if self.request.user.is_staff or self.request.user.is_superuser:
            return obj
        
        # Для комментариев проверяем автора
        if hasattr(obj, 'author'):
            if obj.author != self.request.user:
                raise PermissionDenied("Вы не можете редактировать чужой комментарий")
        
        # Для регистраций проверяем водителя
        elif hasattr(obj, 'driver'):
            if obj.driver.user != self.request.user:
                raise PermissionDenied("Вы не можете редактировать чужую регистрацию")
        
        return obj
```

## Права доступа

### LoginRequiredMixin

Многие страницы доступны только авторизованным пользователям. Для этого используется миксин:

```python
class RegistrationListView(LoginRequiredMixin, ListView):
    # Если пользователь не авторизован, его перенаправит на страницу входа
    ...
```

### Разделение прав админов и пользователей

В представлениях проверяется статус пользователя:

```python
is_admin = self.request.user.is_authenticated and (
    self.request.user.is_staff or self.request.user.is_superuser
)
```

Админы видят:

- Все регистрации (не только свои)
- Больше информации в списках
- Кнопки для редактирования чужих объектов
- Ссылку на админ-панель в меню

## Пагинация

Для длинных списков используется пагинация:

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

paginator = Paginator(registrations, 6)  # 6 объектов на страницу
page = self.request.GET.get('page_participants')

try:
    registrations_page = paginator.page(page)
except PageNotAnInteger:
    registrations_page = paginator.page(1)
except EmptyPage:
    registrations_page = paginator.page(paginator.num_pages)
```

Параметры поиска и сортировки сохраняются при переходе между страницами:

```python
query_params = self.request.GET.copy()
if 'page' in query_params:
    query_params.pop('page')
context['query_string'] = query_params.urlencode()
```

## Оптимизация запросов

Для уменьшения количества запросов к базе данных используются:

### select_related

Для связей ForeignKey и OneToOneField:

```python
registrations = Registration.objects.select_related('driver', 'driver__team', 'race')
```

Это загружает связанные объекты за один SQL запрос вместо множества.

### prefetch_related

Для обратных связей:

```python
heats = race.heats.all().prefetch_related('results__driver__team')
```

### annotate

Для подсчета связанных объектов:

```python
qs = super().get_queryset(request)
return qs.annotate(
    _registrations_count=Count('registrations', distinct=True),
    _heats_count=Count('heats', distinct=True)
)
```

Это позволяет получить количество без дополнительных запросов.

## Сообщения пользователю

Для информирования пользователя о результатах действий используется `messages`:

```python
from django.contrib import messages

# Успех
messages.success(request, 'Профиль успешно обновлен')

# Предупреждение
messages.warning(request, 'Заполните профиль перед регистрацией')

# Информация
messages.info(request, 'Ваша регистрация отменена')

# Ошибка
messages.error(request, 'Произошла ошибка')
```

Сообщения отображаются в шаблоне `base.html` с помощью Bootstrap alerts.

## Итоги

Основные бизнес-правила проекта:

1. Профиль должен быть заполнен для участия
2. Один водитель - одна регистрация на гонку
3. Результаты только для зарегистрированных водителей
4. Один результат на водителя в заезде
5. Пользователи редактируют только свои объекты
6. Админы управляют всем
7. Рейтинг от 1 до 10
8. Видны только опубликованные гонки

Все эти правила реализованы через проверки в представлениях, валидацию в моделях и формах, и ограничения в базе данных.



