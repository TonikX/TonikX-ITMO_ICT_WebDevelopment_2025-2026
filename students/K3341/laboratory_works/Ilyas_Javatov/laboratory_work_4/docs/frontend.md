## Клиентская часть (Vue.js)

Клиентское приложение предназначено для работы с API школьной системы.
Ниже приведены основные интерфейсы и правила взаимодействия с сервером.

### Запуск клиента

Команды (из папки `frontend/`):

```bash
npm install
npm run dev
```

По умолчанию клиент использует `http://localhost:8000/api`.
При необходимости можно задать переменную окружения:

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

### Настройка CORS на сервере

Для доступа из браузера используются параметры окружения:

```bash
CORS_ALLOW_ALL_ORIGINS=false
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8080
```

### Авторизация и пользователи

Основные экраны:
- регистрация пользователя;
- вход и получение токена;
- просмотр и изменение данных текущего пользователя.

Доступ к CRUD-интерфейсам и отчетам открыт только после успешного входа.

API:
- `POST /api/auth/users/` — регистрация;
- `POST /api/auth/token/login/` — получение токена;
- `POST /api/auth/token/logout/` — выход;
- `GET /api/auth/users/me/` — профиль.

Заголовок авторизации:

```
Authorization: Token <your_token>
```

### CRUD-интерфейсы

Администраторский блок для управления сущностями:
- учителя, ученики, классы;
- предметы, кабинеты;
- оценки, расписание;
- назначения учителей на предметы.

Для всех сущностей используются стандартные операции:
- `GET /api/<resource>/` — список;
- `POST /api/<resource>/` — создание;
- `GET /api/<resource>/{id}/` — детальная запись;
- `PUT/PATCH /api/<resource>/{id}/` — обновление;
- `DELETE /api/<resource>/{id}/` — удаление.

### Отчеты и аналитика

Интерфейсы отчетов:
- предмет в расписании;
- количество учителей по предметам;
- преподаватели с общими предметами;
- число мальчиков и девочек по классам;
- статистика кабинетов;
- успеваемость класса.

API:
- `GET /api/reports/subject_for_class/?class_id=1&day=1&lesson=2`
- `GET /api/reports/teachers_per_subject/`
- `GET /api/reports/same_subject_teachers/?class_id=1`
- `GET /api/reports/gender_count_per_class/`
- `GET /api/reports/classroom_stats/`
- `GET /api/reports/class_performance_report/?class_id=1&quarter=1&school_year=2025-2026`
