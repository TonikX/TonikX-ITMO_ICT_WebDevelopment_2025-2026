# Лабораторная работа 3: скрипты Django ORM

## Что где лежит
- `models.py` — настройка Django, описание моделей по схеме, создание таблиц при необходимости (`ensure_tables()`).
- `seed_data.py` — очищает таблицы, наполняет тестовыми владельцами/машинами/удостоверениями/владениями и печатает результат.
- `query_data.py` — выполняет запросы на фильтрацию по уже существующим данным и печатает вывод.
- `create_data.py` — запускает наполнение, затем сразу выполняет запросы.


## Как запускать


```bash
# Только наполнение
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/practical/seed_data.py

# Только запросы (ожидает, что данные уже есть)
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/practical/query_data.py

# Наполнение + запросы подряд
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/practical/create_data.py
```
