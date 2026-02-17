# Установка и запуск Lab2

## Требования

- Python 3.6+
- pip (менеджер пакетов Python)
- PostgreSQL (опционально, можно использовать SQLite)

## Установка

### 1. Переход в директорию проекта

```bash
cd lab2
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Зависимости из `requirements.txt`:
```
Django>=3.0
psycopg2-binary>=2.9.0
```

### 4. Настройка базы данных

#### Вариант 1: SQLite (для разработки)

SQLite используется по умолчанию в Django. Никаких дополнительных настроек не требуется.

#### Вариант 2: PostgreSQL (для продакшена)

1. Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE tours_db;
CREATE USER tours_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE tours_db TO tours_user;
```

2. Обновите настройки в `tours_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tours_db',
        'USER': 'tours_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Применение миграций

```bash
python manage.py migrate
```

Это создаст необходимые таблицы в базе данных.

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите имя пользователя, email и пароль для администратора.

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

## Первоначальная настройка

### Создание тестовых данных

Вы можете создать тестовые туры через административную панель Django:

1. Откройте `http://localhost:8000/admin/`
2. Войдите с учетными данными суперпользователя
3. Перейдите в раздел "Tours" → "Tours"
4. Нажмите "Add Tour" и заполните форму

### Или используйте Django shell:

```bash
python manage.py shell
```

```python
from tours.models import Tour
from datetime import date, timedelta

# Создание тура
tour = Tour.objects.create(
    title="Отдых в Турции",
    travel_agency="ТурАгентство",
    description="Прекрасный отдых на берегу моря",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=37),
    country="Турция",
    payment_conditions="Оплата в рассрочку"
)
```

## Структура команд Django

### Управление миграциями

```bash
# Создание миграций после изменения моделей
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Просмотр SQL миграций
python manage.py sqlmigrate tours 0001
```

### Работа с базой данных

```bash
# Открыть Django shell
python manage.py shell

# Создать суперпользователя
python manage.py createsuperuser

# Сбросить базу данных (удалить все данные)
python manage.py flush
```

### Запуск тестов

```bash
python manage.py test
```

### Сбор статических файлов (для продакшена)

```bash
python manage.py collectstatic
```

## Настройки проекта

Основные настройки находятся в `tours_project/settings.py`:

- **SECRET_KEY** - секретный ключ для криптографии
- **DEBUG** - режим отладки (True для разработки)
- **ALLOWED_HOSTS** - разрешенные хосты
- **DATABASES** - настройки базы данных
- **INSTALLED_APPS** - установленные приложения
- **MIDDLEWARE** - промежуточное ПО
- **TEMPLATES** - настройки шаблонов
- **STATIC_URL** - URL для статических файлов
- **MEDIA_URL** - URL для медиа файлов

## Решение проблем

### Проблема: "No module named 'psycopg2'"

**Решение:** Установите psycopg2-binary:
```bash
pip install psycopg2-binary
```

### Проблема: "django.db.utils.OperationalError: no such table"

**Решение:** Примените миграции:
```bash
python manage.py migrate
```

### Проблема: "TemplateDoesNotExist"

**Решение:** Проверьте настройки TEMPLATES в settings.py и убедитесь, что шаблоны находятся в правильной директории.

### Проблема: "CSRF verification failed"

**Решение:** Убедитесь, что в формах используется `{% csrf_token %}` и что CSRF middleware включен в settings.py.

## Полезные команды

```bash
# Показать все URL маршруты
python manage.py show_urls

# Проверить конфигурацию проекта
python manage.py check

# Создать новое приложение
python manage.py startapp app_name
```

## Следующие шаги

После установки и запуска:

1. Создайте суперпользователя
2. Добавьте несколько туров через админ-панель
3. Зарегистрируйте тестового пользователя
4. Создайте резервирование и отзыв
5. Изучите [модели данных](models.md) и [представления](views.md)
