# Лабораторная работа 3: скрипты Django ORM

## Что где лежит
- `models.py` — настройка Django, описание моделей по схеме, создание таблиц при необходимости (`ensure_tables()`).
- `seed_data.py` — очищает таблицы, наполняет тестовыми владельцами/машинами/удостоверениями/владениями и печатает результат.
- `query_data.py` — выполняет запросы на фильтрацию по уже существующим данным и печатает вывод.
- `create_data.py` — запускает наполнение, затем сразу выполняет запросы.

## Предварительно
- Используйте виртуальное окружение проекта `.venv` (Django уже установлен).
- Файл БД SQLite — `lab3.sqlite3` в той же директории; создаётся автоматически при отсутствии.

## Как запускать
Из корня репозитория (`/Users/lk2322/itmo/web_labs`):

```bash
# Только наполнение
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/seed_data.py

# Только запросы (ожидает, что данные уже есть)
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/query_data.py

# Наполнение + запросы подряд
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/create_data.py
```

Если пере создаёте виртуальное окружение, установите Django внутри `.venv`:
```bash
.venv/bin/python -m pip install django
```
