# Практическая часть (ORM)

В каталоге `laboratory_work_3/practical` собраны небольшие скрипты для отработки Django ORM без запуска основного API.

## Состав
- `models.py` — настройка Django, описание моделей и создание таблиц при необходимости (`ensure_tables()`).
- `seed_data.py` — очищает таблицы, заполняет тестовыми владельцами, машинами, удостоверениями и связями, выводит результат.
- `query_data.py` — выполняет выборки и фильтры по уже созданным данным, печатает вывод.
- `create_data.py` — объединяет наполнение и выполнение запросов подряд.

## Запуск
В примерах ниже предполагается активированное виртуальное окружение `.venv` в корне репозитория.

```bash
# Только наполнение
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/practical/seed_data.py

# Только запросы (данные должны уже быть загружены)
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/practical/query_data.py

# Наполнение + запросы одним запуском
.venv/bin/python lab1/students/K3341/laboratory_works/Владзиевский_Евгений/laboratory_work_3/practical/create_data.py
```
