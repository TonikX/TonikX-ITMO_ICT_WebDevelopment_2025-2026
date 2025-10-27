# Настройка PostgreSQL для проекта "Читальный зал"

## Шаг 1: Установка PostgreSQL

### Windows:
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Запустите установщик
3. Запомните пароль, который вы установите для пользователя `postgres`
4. Убедитесь, что порт 5432 не занят

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS:
```bash
brew install postgresql
brew services start postgresql
```

## Шаг 2: Создание базы данных

### Вариант 1: Через psql (командная строка)

1. Войдите в PostgreSQL:
```bash
psql -U postgres
```

2. Создайте базу данных:
```sql
CREATE DATABASE reading_room_db;
```

3. Создайте пользователя (опционально):
```sql
CREATE USER reading_room_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE reading_room_db TO reading_room_user;
```

4. Выйдите из psql:
```sql
\q
```

### Вариант 2: Через pgAdmin (GUI)

1. Откройте pgAdmin
2. Подключитесь к серверу PostgreSQL
3. Правый клик на "Databases" → "Create" → "Database"
4. Введите имя: `reading_room_db`
5. Нажмите "Save"

## Шаг 3: Настройка Django

1. Откройте файл `django_project_meshcheryakov/settings.py`

2. Найдите секцию `DATABASES` и раскомментируйте PostgreSQL конфигурацию:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'reading_room_db',
        'USER': 'postgres',  # или ваш пользователь
        'PASSWORD': 'your_password',  # ваш пароль
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Закомментируйте SQLite конфигурацию:

```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

## Шаг 4: Миграция на PostgreSQL

1. Убедитесь, что `psycopg2-binary` установлен:
```bash
pip install psycopg2-binary
```

2. Примените миграции:
```bash
python manage.py migrate
```

3. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

## Шаг 5: Проверка подключения

Запустите сервер разработки:
```bash
python manage.py runserver
```

Если всё настроено правильно, вы увидите сообщение:
```
Django version 5.x.x, using settings 'django_project_meshcheryakov.settings'
Starting development server at http://127.0.0.1:8000/
```

## Возможные ошибки

### Ошибка: "FATAL: password authentication failed"
- Проверьте пароль в settings.py
- Убедитесь, что пользователь существует в PostgreSQL

### Ошибка: "could not connect to server"
- Убедитесь, что PostgreSQL запущен
- Проверьте, что порт 5432 не занят другим процессом

### Ошибка: "database does not exist"
- Создайте базу данных через psql или pgAdmin (см. Шаг 2)

## Резервное копирование и восстановление

### Создание резервной копии:
```bash
pg_dump -U postgres reading_room_db > backup.sql
```

### Восстановление из резервной копии:
```bash
psql -U postgres reading_room_db < backup.sql
```

## Примечания

- Для production рекомендуется использовать переменные окружения для хранения паролей
- Не коммитьте пароли в систему контроля версий
- Регулярно делайте резервные копии базы данных


