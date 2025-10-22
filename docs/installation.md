# Установка и запуск

## Требования

- Python 3.8+
- Django 4.2.7
- Django REST Framework
- SQLite (входит в Python)

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/TonikX-ITMO_ICT_WebDevelopment_2025-2026.git
cd TonikX-ITMO_ICT_WebDevelopment_2025-2026/car_owners_project
```

### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install django
pip install djangorestframework
pip install mkdocs
pip install mkdocs-material
```

### 4. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание тестовых данных

```bash
python create_test_data.py
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

### 7. Запуск документации

```bash
mkdocs serve
```

## Доступ к приложению

После запуска сервера приложение будет доступно по адресам:

- **API**: http://localhost:8000/warriors/
- **Админка**: http://localhost:8000/admin/
- **Документация**: http://localhost:127.0.0.1:8000

## Тестирование

### Автоматическое тестирование

```bash
python test_api_examples.py
```

### Ручное тестирование

1. Откройте браузер и перейдите на http://localhost:8000/warriors/
2. Используйте инструменты типа Postman для тестирования API
3. Проверьте все endpoints согласно документации

## Создание суперпользователя

Для доступа к админке Django:

```bash
python manage.py createsuperuser
```

## 🔧 Настройка разработки

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Настройка IDE

Рекомендуемые расширения для VS Code:
- Python
- Django
- REST Client
- Thunder Client

## Решение проблем

### Ошибка "ModuleNotFoundError: No module named 'django'"

```bash
# Убедитесь, что виртуальное окружение активировано
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Переустановите зависимости
pip install -r requirements.txt
```

### Ошибка "django.core.exceptions.ImproperlyConfigured"

```bash
# Проверьте настройки в settings.py
# Убедитесь, что все приложения добавлены в INSTALLED_APPS
```

### Ошибка подключения к базе данных

```bash
# Удалите файл базы данных и создайте заново
rm db.sqlite3
python manage.py migrate
python create_test_data.py
```

## Структура проекта

```
car_owners_project/
├── car_owners_project/     # Настройки Django
├── car_owners/             # Приложение автомобилей
├── warriors_app/           # Приложение воинов
├── docs/                   # Документация MkDocs
├── mkdocs.yml             # Конфигурация MkDocs
├── create_test_data.py    # Скрипт тестовых данных
├── test_api_examples.py   # Примеры тестирования
└── manage.py              # Управление Django
```

## Следующие шаги

После успешной установки:

1. Изучите [API Документацию](api/overview.md)
2. Попробуйте [Примеры использования](api/examples.md)
3. Запустите [Тестирование](testing.md)
4. Изучите [Заключение](conclusion.md)

---

**Готово!**  Проект успешно установлен и готов к использованию.
