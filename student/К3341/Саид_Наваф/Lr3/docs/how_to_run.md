# Как запустить проект локально (инструкция)

1) Клонирование / местоположение
- Рабочая папка репозитория: `students/К3341/Саид_Наваф/laboratory_work_3/`
- Внутри должна быть корневая папка проекта Django (manage.py), приложение `carApp` и файлы документации.

2) Создание и активация виртуального окружения (Windows PowerShell пример):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

3) Установка зависимостей:
```bash
pip install -r requirements.txt
```
Пример requirements.txt (см. файл в репозитории).

4) Настройка settings.py:
- В `INSTALLED_APPS` добавить:
  - 'rest_framework'
  - 'djoser'
  - 'drf_spectacular'
  - 'carApp'
- Убедиться, что REST_FRAMEWORK настроен для JWT:
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```
- Добавить `SIMPLE_JWT` настройки, если требуется.

5) Миграции и наполнение (выполните в папке с manage.py):
```bash
python manage.py makemigrations
python manage.py migrate
# Заполнить тестовыми данными
python populate_lab3_practice3_1.py
```
(Или выполните содержимое populate в manage.py shell)

6) Запуск сервера:
```bash
python manage.py runserver
```
- Swagger UI: http://127.0.0.1:8000/api/docs/swagger/
- ReDoc: http://127.0.0.1:8000/api/docs/redoc/
- Admin: http://127.0.0.1:8000/admin/

7) Тестирование API:
- Зарегистрируйте пользователя через `POST /auth/users/` или создайте суперадмина `python manage.py createsuperuser`.
- Запросите токен `POST /api/token/` и используйте `Authorization: Bearer <token>`.