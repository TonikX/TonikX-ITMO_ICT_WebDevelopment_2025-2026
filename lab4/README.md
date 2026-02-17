# Лабораторная работа 4 (Vue.js)

Клиентская часть для `lab3` (Hackathon API на Django REST).

## Что реализовано

- Авторизация и регистрация через Djoser
- Просмотр и создание задач, команд, решений, оценок (в соответствии с ролями)
- Детальные страницы задач, команд и решений
- Интерфейс изменения учетных данных (`/profile`)
- Подключена UI-библиотека `bootstrap` (как аналог Vuetify)

## Быстрый запуск

1. Запустить backend (`lab3`):

```bash
cd ../lab3
USE_SQLITE=1 ./.venv/bin/python manage.py runserver 127.0.0.1:8003 --noreload
```

2. Запустить frontend (`lab4`):

```bash
cd ../lab4
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

3. Открыть:

`http://127.0.0.1:5174`

## Настройка API

В `lab4/.env`:

```env
VITE_API_BASE=http://127.0.0.1:8003
```

