# Лабораторная работа 4: Установка и запуск

## Системные требования

- Python 3.12+ (для backend `lab3`)
- Node.js 18+ и npm (для frontend `lab4`)
- Установленные зависимости из `lab3/requirements.txt` и `lab4/package.json`

## Структура для запуска

- `lab3/` — backend на Django REST Framework
- `lab4/` — frontend на Vue 3
- `lab3/docs/` — документация MkDocs

## Запуск backend (lab3)

```bash
cd lab3
USE_SQLITE=1 ./.venv/bin/python manage.py runserver 127.0.0.1:8003 --noreload
```

После запуска доступны:

- API root: `http://127.0.0.1:8003/`
- DRF router: `http://127.0.0.1:8003/api/`
- Django admin: `http://127.0.0.1:8003/admin/`

## Запуск frontend (lab4)

```bash
cd lab4
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

Frontend будет доступен по адресу:

- `http://127.0.0.1:5174/`

## Настройка переменных окружения

Файл `lab4/.env`:

```env
VITE_API_BASE=http://127.0.0.1:8003
```

## Проверка CORS

Для порта `5174` в backend добавлены разрешенные origin:

- `http://127.0.0.1:5174`
- `http://localhost:5174`

Настройка находится в `lab3/hackathon_project/settings.py`.

## Тестовые учетные записи

- `admin@example.com` / `ItmoWeb2026!` — администратор
- `cherepnyayar@gmail.com` / `ItmoWeb2026!` — капитан (`admin_josha`)
- `curator1@example.com` / `ItmoWeb2026!` — куратор
- `123124@mail.com` / `ItmoWeb2026!` — жюри

## Типовые проблемы

### Ошибка "Сервер API недоступен"

- Проверьте, что backend запущен на `127.0.0.1:8003`.
- Проверьте `VITE_API_BASE` в `lab4/.env`.
- Если backend и frontend на разных портах, проверьте CORS в `settings.py`.

### Порт уже занят

Проверьте процессы:

```bash
lsof -iTCP:8003 -sTCP:LISTEN -n -P
lsof -iTCP:5174 -sTCP:LISTEN -n -P
```

### Ошибка входа

В проекте `lab3` логин выполняется по `email`, а не по `username`.
