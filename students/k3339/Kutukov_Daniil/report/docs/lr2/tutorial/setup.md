# Настройка Tutorial

## Установка

Аналогично Homework Board:

1. `pip install django`
2. Создать проект и приложение
3. Добавить в INSTALLED_APPS
4. `python manage.py makemigrations && python manage.py migrate`
5. `python manage.py createsuperuser`
6. `python manage.py runserver`

## Особенности

- Использует стандартную User модель Django
- Связи через ForeignKey для владения автомобилями