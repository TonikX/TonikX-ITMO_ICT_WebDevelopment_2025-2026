# Запуск и окружение

## Бэкенд (ЛР3)
```bash
cd students/k3340/Ivanov_Viktor/lr_3
source .venv/bin/activate
python manage.py runserver 8002
```
- CORS включён (`django-cors-headers`), разрешены `http://127.0.0.1:5173` и `http://localhost:5173`.
- Тестовые данные уже загружены (классы, ученики, расписание, оценки).

## Фронтенд (ЛР4)
```bash
cd students/k3340/Ivanov_Viktor/lr_4/frontend
npm install          # первый раз
npm run dev -- --host --port 5173
```
Открыть в браузере: `http://127.0.0.1:5173/`

## Авторизация
- Djoser token auth: `POST /api/auth/token/login/`
- Готовый суперпользователь: `donperenon` / `Admin123!` (при необходимости сменить).
- Профиль: `GET /api/auth/users/me/`

## Сборка
```bash
npm run build
```
Сборка появится в `frontend/dist/` (можно раздавать статикой или через любой хостинг).*** End Patch

