# Как запустить (обновлено для ЛР4)

Требования:
- Python 3.10+ (или версия проекта)
- node/npm или yarn для фронтенда
- виртуальное окружение (venv)

1) Настройка окружения (backend)
- Скопируйте `.env`/настройки или используйте `settings.py` как в проекте.
- Для разделения БД ЛР3/ЛР4 (рекомендация) можно использовать переменную окружения `DJANGO_DB_NAME` в `settings.py`:
  DATABASES['default']['NAME'] = BASE_DIR / os.environ.get('DJANGO_DB_NAME', 'db.sqlite3')

Примеры:
- Для работы с Lab3: `set DJANGO_DB_NAME=db_lab3.sqlite3` (Windows PowerShell: `$env:DJANGO_DB_NAME="db_lab3.sqlite3"`)
- Для работы с Lab4: `set DJANGO_DB_NAME=db_lab4.sqlite3`

2) Миграции
```bash
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

3) Создать суперпользователя для тестирования JWT:
```bash
python manage.py createsuperuser
```

4) Запустить сервер:
```bash
python manage.py runserver 8000
```

5) Запуск фронтенда (Vue)
- Установите зависимости и запустите dev сервер:
```bash
cd frontend
npm install
# или yarn
npm run dev
```
- Фронтенд использует переменную `VITE_API_URL` (в файле `.env.local`), например:
```
VITE_API_URL=http://localhost:8000
```

6) Тестирование аутентификации
- Получить токен: POST /api/token/ с username/password
- В фронтенде: перейти на /login и ввести учётные данные, токены сохранятся в localStorage

7) Загрузка тестовых данных
- Скрипт `populate_lab3_practice3_1.py` обновлён и idempotent — можно запускать несколько раз:
```bash
python populate_lab3_practice3_1.py
```
