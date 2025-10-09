# Лабораторная работа 2: Django проекты

Добро пожаловать в документацию по лабораторной работе 2! Здесь представлены два Django проекта, созданных в рамках курса веб-разработки.

## 📚 Проекты

### 🎓 Доска домашних заданий (homework_board)
Современная веб-система для управления домашними заданиями в учебных заведениях.

**Основные возможности:**
- Управление заданиями для студентов и преподавателей
- Система оценок и комментариев
- Статистика и аналитика
- Адаптивный дизайн с Bootstrap 5

[Подробнее о проекте →](homework_board/index.md)

### 🚗 Система управления автовладельцами (tutorial)
Веб-приложение для управления информацией об автовладельцах, их автомобилях и водительских удостоверениях.

**Основные возможности:**
- Управление владельцами автомобилей
- Регистрация автомобилей
- Отслеживание истории владения
- Управление водительскими удостоверениями

[Подробнее о проекте →](tutorial/index.md)

## 🛠 Технологии

- **Backend**: Django 5.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **База данных**: SQLite
- **Язык**: Python 3.12+

## 🚀 Быстрый старт

### Установка зависимостей
```bash
# Для homework_board
cd homework_board
python -m venv homework-env
source homework-env/bin/activate  # Linux/Mac
pip install django

# Для tutorial
cd tutorial
python -m venv tutorial-env
source tutorial-env/bin/activate  # Linux/Mac
pip install django
```

### Запуск проектов
```bash
# homework_board
cd homework_board
python manage.py migrate
python manage.py runserver

# tutorial
cd tutorial
python manage.py migrate
python manage.py runserver
```

## 📖 Структура репозитория

```
├── homework_board/          # Проект доски домашних заданий
│   ├── assignments/         # Основное приложение
│   ├── templates/           # HTML шаблоны
│   ├── static/             # Статические файлы
│   └── manage.py           # Управление Django
├── tutorial/               # Проект управления автовладельцами
│   ├── project_first_app/  # Основное приложение
│   ├── templates/          # HTML шаблоны
│   └── manage.py           # Управление Django
├── docs/                   # Документация MkDocs
└── mkdocs.yml             # Конфигурация MkDocs
```

## 👨‍💻 Автор

**Арсений Филатов** - студент курса веб-разработки

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](../LICENSE) для подробностей.

---

*Документация создана с помощью [MkDocs](https://www.mkdocs.org/) и [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)*
