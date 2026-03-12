# Лабораторная работа №3: Реализация серверной части на Django REST Framework

## Название работы

Реализация серверной части на django rest. Документирование API.

## Цель работы

Реализация серверной части приложения средствами Django и Django REST Framework для системы управления библиотекой.

## Задание

1. Реализовать модель базы данных средствами Django ORM
2. Реализовать логику работы API средствами Django REST Framework (используя методы сериализации)
3. Подключить регистрацию / авторизацию по токенам / вывод информации о текущем пользователе средствами Djoser

## Предметная область

Создание программной системы для работников библиотеки, обеспечивающей хранение сведений о:

- Книгах в библиотеке
- Читателях библиотеки
- Читальных залах

## Выполнение работы

### 1. Настройка проекта

Был создан Django проект в папке `lab3/lr3/config/` со следующей структурой:

```
config/
├── config/           # Основные настройки проекта
├── library/          # Приложение библиотеки
├── manage.py         # Управляющий скрипт Django
└── db.sqlite3        # База данных SQLite
```

### 2. Настройка зависимостей и INSTALLED_APPS

В файле `settings.py` были добавлены необходимые приложения:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'library',
    'drf_yasg',
    'djoser',
    'corsheaders',
]
```

### 3. Реализация моделей базы данных

В файле `library/models.py` были созданы следующие модели:

#### Модель читального зала (Hall)

```python
class Hall(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
```

#### Модель книги (Book)

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    year = models.IntegerField()
    section = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
```

#### Модель книги в зале (BookInHall)

```python
class BookInHall(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    copies = models.IntegerField()

    class Meta:
        unique_together = ('book', 'hall')
```

#### Модель читателя (Reader)

```python
class Reader(models.Model):
    ticket_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    passport_number = models.CharField(max_length=50)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=50)
    academic_degree = models.BooleanField(default=False)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

#### Модель выдачи книги (BookIssue)

```python
class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book_in_hall = models.ForeignKey(
        BookInHall, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Из какого зала выдана книга (для учета копий)"
    )
    issue_date = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)
```

### 4. Реализация сериализаторов

В файле `library/serializers.py` были созданы сериализаторы для всех моделей:

#### Базовые сериализаторы

```python
class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'
```

#### Расширенный сериализатор для BookInHall

```python
class BookInHallSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    authors = serializers.CharField(source='book.authors', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)

    class Meta:
        model = BookInHall
        fields = '__all__'
        extra_kwargs = {
            'book': {'required': False},
        }

    def validate(self, attrs):
        instance = self.instance
        hall = attrs.get('hall') or (instance.hall if instance else None)
        book = attrs.get('book') or (instance.book if instance else None)

        if not hall or not book:
            return attrs

        qs = BookInHall.objects.filter(hall=hall)
        if instance:
            qs = qs.exclude(pk=instance.pk)

        current_count = qs.count()

        if hall.capacity is not None and current_count >= hall.capacity and not instance:
            raise serializers.ValidationError({
                'hall': 'В этом зале достигнута максимальная вместимость по разным книгам.'
            })

        return attrs
```

### 5. Реализация ViewSets

В файле `library/views.py` были созданы ViewSets с использованием Django REST Framework:

#### HallViewSet

```python
@method_decorator(swagger_auto_schema(tags=['Halls']), name='list')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='create')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='retrieve')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='update')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='partial_update')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='destroy')
class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
```

#### BookViewSet с дополнительными действиями

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @swagger_auto_schema(tags=['Books'])
    @action(detail=False, methods=['get'])
    def rare(self, request):
        books = Book.objects.filter(bookinhall__copies__lte=2).distinct()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
```

#### ReaderViewSet с бизнес-логикой

```python
class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=False, methods=['get'])
    def rare_books(self, request):
        issues = BookIssue.objects.filter(book__bookinhall__copies__lte=2)
        result = []
        for issue in issues:
            result.append({
                "reader": issue.reader.full_name,
                "book": issue.book.title,
            })
        unique = {
            (item["reader"], item["book"]): item
            for item in result
        }.values()
        return Response(list(unique))

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        reader = self.get_object()
        issues = BookIssue.objects.filter(reader=reader)
        books = [issue.book.title for issue in issues]
        return Response(books)

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=False, methods=['get'])
    def under_20(self, request):
        today = date.today()
        readers = Reader.objects.all()
        count = 0
        for r in readers:
            age = today.year - r.birth_date.year
            if age < 20:
                count += 1
        return Response({"readers_under_20": count})

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=False, methods=['get'])
    def education_stats(self, request):
        total = Reader.objects.count()
        if total == 0:
            return Response({})

        primary = Reader.objects.filter(education="primary").count()
        secondary = Reader.objects.filter(education="secondary").count()
        higher = Reader.objects.filter(education="higher").count()
        degree = Reader.objects.filter(academic_degree=True).count()

        data = {
            "primary_%": round(primary / total * 100, 2),
            "secondary_%": round(secondary / total * 100, 2),
            "higher_%": round(higher / total * 100, 2),
            "degree_%": round(degree / total * 100, 2),
        }
        return Response(data)
```

#### BookIssueViewSet с автоматическим учетом копий

```python
class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.book_in_hall and instance.book_in_hall.copies > 0:
            instance.book_in_hall.copies -= 1
            instance.book_in_hall.save(update_fields=['copies'])

    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_return = old_instance.return_date
        instance = serializer.save()
        if instance.book_in_hall and instance.return_date and not old_return:
            instance.book_in_hall.copies += 1
            instance.book_in_hall.save(update_fields=['copies'])

    @swagger_auto_schema(tags=['Issues'])
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        month_ago = timezone.now() - timedelta(days=30)
        issues = BookIssue.objects.filter(issue_date__lt=month_ago)
        readers = [issue.reader.full_name for issue in issues]
        return Response(list(set(readers)))
```

### 6. Настройка URL маршрутизации

В файле `library/urls.py` была настроена маршрутизация API:

```python
from rest_framework.routers import DefaultRouter
from .views import HallViewSet, BookViewSet, ReaderViewSet, BookIssueViewSet, BookInHallViewSet

router = DefaultRouter()

router.register('halls', HallViewSet)
router.register('books', BookViewSet)
router.register('books-in-halls', BookInHallViewSet)
router.register('readers', ReaderViewSet)
router.register('issues', BookIssueViewSet)

urlpatterns = router.urls
```

### 7. Настройка основной маршрутизации и Swagger

В файле `config/urls.py` была настроена основная маршрутизация:

```python
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="API для системы библиотеки",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
```

### 8. Настройка аутентификации и авторизации

В файле `settings.py` была настроена аутентификация по токенам:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

INSTALLED_APPS += [
    'rest_framework.authtoken'
]

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
```

### 9. Создание Swagger документации

Для создания документации API был использован `drf-yasg`:

1. **Установка пакета**: `drf-yasg` добавлен в `INSTALLED_APPS`
2. **Настройка схемы**: Создан `schema_view` с информацией об API
3. **URL для Swagger**: Добавлен путь `/swagger/` для доступа к документации
4. **Настройка безопасности**: Добавлена аутентификация по токенам в Swagger

Доступ к документации осуществляется по URL: `http://localhost:8000/swagger/`

### 10. Реализация дополнительных запросов

В файле `library/queries.py` были реализованы дополнительные функции для бизнес-логики:

```python
def get_books_by_reader(reader_id):
    issues = BookIssue.objects.filter(reader_id=reader_id)
    books = []
    for issue in issues:
        books.append(issue.book.title)
    return books

def readers_with_old_books():
    month_ago = timezone.now() - timedelta(days=30)
    issues = BookIssue.objects.filter(issue_date__lt=month_ago)
    readers = []
    for issue in issues:
        readers.append(issue.reader.full_name)
    return list(set(readers))

def readers_with_rare_books():
    issues = BookIssue.objects.filter(book__copies__lte=2)
    result = []
    for issue in issues:
        result.append({
            "reader": issue.reader.full_name,
            "book": issue.book.title
        })
    return result

def count_readers_under_20():
    today = date.today()
    readers = Reader.objects.all()
    count = 0
    for reader in readers:
        age = today.year - reader.birth_date.year
        if age < 20:
            count += 1
    return count

def education_statistics():
    readers = Reader.objects.all()
    total = readers.count()

    if total == 0:
        return {}

    primary = readers.filter(education="primary").count()
    secondary = readers.filter(education="secondary").count()
    higher = readers.filter(education="higher").count()
    degree = readers.filter(academic_degree=True).count()

    return {
        "primary_%": round(primary / total * 100, 2),
        "secondary_%": round(secondary / total * 100, 2),
        "higher_%": round(higher / total * 100, 2),
        "degree_%": round(degree / total * 100, 2),
    }
```

### 11. Настройка админ панели

В файле `library/admin.py` была настроена админ панель для управления данными:

```python
from django.contrib import admin
from .models import Hall, Book, Reader, BookIssue

admin.site.register(Hall)
admin.site.register(Book)
admin.site.register(Reader)
admin.site.register(BookIssue)
```

Админ панель доступна по URL: `http://localhost:8000/admin/` и предоставляет удобный интерфейс для управления всеми моделями системы.

## Реализованные эндпоинты API

### Основные CRUD операции:

- `GET/POST /api/halls/` - Получение/создание читальных залов
- `GET/PUT/DELETE /api/halls/{id}/` - Управление конкретным залом
- `GET/POST /api/books/` - Получение/создание книг
- `GET/PUT/DELETE /api/books/{id}/` - Управление конкретной книгой
- `GET/POST /api/books-in-halls/` - Получение/создание книг в залах
- `GET/PUT/DELETE /api/books-in-halls/{id}/` - Управление книгами в залах
- `GET/POST /api/readers/` - Получение/создание читателей
- `GET/PUT/DELETE /api/readers/{id}/` - Управление конкретным читателем
- `GET/POST /api/issues/` - Получение/создание выдач книг
- `GET/PUT/DELETE /api/issues/{id}/` - Управление конкретной выдачей

### Дополнительные эндпоинты:

- `GET /api/books/rare/` - Получение редких книг (≤ 2 экземпляра)
- `GET /api/readers/rare_books/` - Читатели с редкими книгами
- `GET /api/readers/{id}/books/` - Книги закрепленные за читателем
- `GET /api/readers/under_20/` - Количество читателей младше 20 лет
- `GET /api/readers/education_stats/` - Статистика образования читателей
- `GET /api/issues/overdue/` - Читатели с просроченными книгами

### Эндпоинты аутентификации (через Djoser):

- `POST /auth/users/` - Регистрация пользователя
- `POST /auth/token/login/` - Получение токена
- `POST /auth/token/logout/` - Выход из системы
- `GET /auth/users/me/` - Информация о текущем пользователе

## Валидация и бизнес-логика

### Реализованные правила валидации:

1. **Проверка вместимости зала**: Нельзя добавить больше книг в зал, чем его вместимость
2. **Учет копий книг**: Автоматическое уменьшение/увеличение количества копий при выдаче/возврате
3. **Уникальность книг в зале**: Каждая книга может быть только один раз в каждом зале

### Бизнес-логика:

1. **Автоматический учет копий**: При выдаче книги количество копий уменьшается, при возврате - увеличивается
2. **Статистические запросы**: Реализованы все требуемые статистические запросы
3. **Фильтрация данных**: Эффективная фильтрация по различным параметрам

## Запуск проекта

1. Активация виртуального окружения:

```bash
source venv/bin/activate
```

2. Применение миграций:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Создание суперпользователя:

```bash
python manage.py createsuperuser
```

4. Запуск сервера:

```bash
python manage.py runserver
```

5. Доступ к API:

- API: `http://localhost:8000/api/`
- Swagger документация: `http://localhost:8000/swagger/`
- Админ панель: `http://localhost:8000/admin/`

## Примеры использования API

### 1. Регистрация пользователя и получение токена

```bash
# Регистрация
curl -X POST http://localhost:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "librarian",
    "password": "securepassword123",
    "email": "librarian@library.com"
  }'

# Получение токена
curl -X POST http://localhost:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "librarian",
    "password": "securepassword123"
  }'
```

### 2. Создание читального зала

```bash
curl -X POST http://localhost:8000/api/halls/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{
    "number": 1,
    "name": "Главный читальный зал",
    "capacity": 100
  }'
```

### 3. Добавление книги и размещение в зале

```bash
# Создание книги
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Война и мир",
    "authors": "Лев Толстой",
    "publisher": "Эксмо",
    "year": 2020,
    "section": "Художественная литература",
    "code": "Т-123"
  }'

# Размещение книги в зале
curl -X POST http://localhost:8000/api/books-in-halls/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "hall": 1,
    "copies": 5
  }'
```

### 4. Регистрация читателя

```bash
curl -X POST http://localhost:8000/api/readers/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_number": "ЧБ-001",
    "full_name": "Иванов Иван Иванович",
    "passport_number": "1234 567890",
    "birth_date": "1990-05-15",
    "address": "г. Москва, ул. Ленина, д. 1",
    "phone": "+7(999)123-45-67",
    "education": "higher",
    "academic_degree": false,
    "hall": 1
  }'
```

### 5. Выдача книги читателю

```bash
curl -X POST http://localhost:8000/api/issues/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "reader": 1,
    "book_in_hall": 1
  }'
```

### 6. Получение статистической информации

```bash
# Читатели младше 20 лет
curl -X GET http://localhost:8000/api/readers/under_20/ \
  -H "Authorization: Token ваш_токен"

# Статистика образования
curl -X GET http://localhost:8000/api/readers/education_stats/ \
  -H "Authorization: Token ваш_токен"

# Редкие книги
curl -X GET http://localhost:8000/api/books/rare/ \
  -H "Authorization: Token ваш_токен"

# Просроченные выдачи
curl -X GET http://localhost:8000/api/issues/overdue/ \
  -H "Authorization: Token ваш_токен"
```

## Архитектурные решения и лучшие практики

### 1. Разделение ответственности

- **Models**: Описание структуры данных и бизнес-правил
- **Serializers**: Преобразование данных и валидация
- **Views**: Бизнес-логика и обработка HTTP запросов
- **URLs**: Маршрутизация запросов

### 2. Безопасность

- Токенная аутентификация для защиты API
- Валидация данных на уровне сериализаторов
- Проверка прав доступа при операциях с данными

### 3. Масштабируемость

- Использование ViewSets для стандартных CRUD операций
- Кастомные действия для специфической бизнес-логики
- Оптимизированные запросы к базе данных

### 4. Документирование

- Автоматическая генерация Swagger документации
- Описание всех эндпоинтов и параметров
- Примеры запросов и ответов

## Выводы

В ходе выполнения лабораторной работы были успешно решены все поставленные задачи:

1. **Реализована модель базы данных** средствами Django ORM с учетом всех требований предметной области
2. **Реализована логика работы API** средствами Django REST Framework с использованием сериализаторов
3. **Подключена регистрация/авторизация** по токенам средствами Djoser
4. **Создана Swagger документация** для всех эндпоинтов API
5. **Реализована бизнес-логика** для всех требуемых запросов
6. **Настроена валидация данных** и автоматический учет ресурсов

Система готова к использованию и предоставляет полный функционал для управления библиотекой через REST API с современной документацией и безопасной аутентификацией.
