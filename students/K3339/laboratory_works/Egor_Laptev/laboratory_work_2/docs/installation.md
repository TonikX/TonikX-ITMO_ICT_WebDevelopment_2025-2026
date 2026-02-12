# Установка и запуск

## Требования

- Python 3.8 или выше
- Docker и Docker Compose
- pip (менеджер пакетов Python)

## Пошаговая инструкция

### 1. Клонирование проекта

Если проект находится в репозитории, выполните:

```bash
git clone <repository_url>
cd laboratory_work_2
```

### 2. Создание виртуального окружения

```bash
python -m venv lab-2-env
```

**Активация виртуального окружения:**

- Windows:
```bash
lab-2-env\Scripts\activate
```

- Linux/macOS:
```bash
source lab-2-env/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

**Зависимости проекта:**
- Django==5.2.8
- django-bootstrap3==25.3
- psycopg2-binary==2.9.9

### 4. Запуск PostgreSQL в Docker

```bash
docker-compose up -d
```

Эта команда:
- Скачает образ PostgreSQL 15
- Создаст контейнер `racing_postgres`
- Настроит базу данных `racing_db`
- Запустит PostgreSQL на порту 5432

**Проверка статуса:**
```bash
docker-compose ps
```

### 5. Настройка базы данных

#### Применение миграций

```bash
python manage.py migrate
```

Эта команда создаст все необходимые таблицы в базе данных.

#### Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

Введите:
- Username (имя пользователя)
- Email (опционально)
- Password (пароль)

### 6. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000/`

### 7. Доступ к приложению

- **Главная страница:** http://127.0.0.1:8000/
- **Админ-панель:** http://127.0.0.1:8000/admin/

---

## Настройка переменных окружения (опционально)

Создайте файл `.env` в корне проекта:

```env
# PostgreSQL Database Configuration
DB_NAME=racing_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Django Secret Key
SECRET_KEY=your-secret-key-here

# Django Settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Важно:** В production используйте более безопасный SECRET_KEY и установите DEBUG=False.

---

## Управление Docker контейнером

### Остановка контейнера

```bash
docker-compose down
```

### Остановка и удаление данных

```bash
docker-compose down -v
```

**Внимание:** Это удалит все данные в базе!

### Просмотр логов

```bash
docker-compose logs -f db
```

### Перезапуск контейнера

```bash
docker-compose restart db
```

---

## Создание тестовых данных

### Через админ-панель

1. Войдите в админ-панель: http://127.0.0.1:8000/admin/
2. Используйте созданного суперпользователя
3. Создайте тестовые данные:
   - Гонки (Race)
   - Профили участников (ParticipantProfile)
   - Автомобили (Car)
   - Регистрации (Registration)
   - Комментарии (Comment)

### Через Django shell

```bash
python manage.py shell
```

Пример создания тестовой гонки:

```python
from racing.models import Race
from django.utils import timezone
from datetime import timedelta

race = Race.objects.create(
    title="Гран-при Москвы",
    date=timezone.now() + timedelta(days=30),
    location="Москва, Автодром",
    description="Ежегодная гонка в столице России"
)
```

---

## Проверка работоспособности

После запуска проверьте:

1. Сервер запущен без ошибок
2. База данных подключена (нет ошибок в консоли)
3. Главная страница открывается
4. Админ-панель доступна
5. Можно зарегистрировать пользователя
6. Можно войти в систему

---

## Запуск документации MkDocs

Для просмотра документации:

```bash
# Установка MkDocs (если еще не установлен)
pip install mkdocs-material

# Запуск сервера документации
mkdocs serve
```

Документация будет доступна по адресу: http://127.0.0.1:8001/

Для сборки статической версии:

```bash
mkdocs build
```

Статические файлы будут в директории `site/`.

