# Авторизация и регистрация

## Описание

Модуль авторизации обеспечивает аутентификацию пользователей с использованием токенов Django REST Framework.

## Страница входа

**Путь:** `/login`

**Компонент:** `LoginView.vue`

### Функционал

- Вход в систему по логину и паролю
- Валидация формы на клиенте
- Отображение ошибок сервера
- Редирект на запрошенную страницу после входа

### Скриншот интерфейса

Форма входа содержит:

- Поле "Имя пользователя"
- Поле "Пароль" с возможностью показать/скрыть
- Кнопка "Войти"
- Ссылка на регистрацию

### API endpoints

```
POST /api/auth/token/login/
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}

Response:
{
  "auth_token": "abc123..."
}
```

## Страница регистрации

**Путь:** `/register`

**Компонент:** `RegisterView.vue`

### Функционал

- Регистрация нового пользователя
- Валидация:
  - Обязательные поля
  - Минимальная длина имени (3 символа)
  - Минимальная длина пароля (8 символов)
  - Валидация email
  - Совпадение паролей
- Автоматический вход после регистрации

### Поля формы

| Поле | Тип | Валидация |
|------|-----|-----------|
| Имя пользователя | text | Обязательное, мин. 3 символа |
| Email | email | Обязательное, формат email |
| Пароль | password | Обязательное, мин. 8 символов |
| Подтверждение пароля | password | Должен совпадать с паролем |

### API endpoints

```
POST /api/auth/users/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "re_password": "password123"
}
```

## Страница профиля

**Путь:** `/profile`

**Компонент:** `ProfileView.vue`

**Требует авторизации:** Да

### Функционал

Две вкладки:

1. **Информация** — редактирование данных пользователя
2. **Смена пароля** — изменение пароля

### Редактирование профиля

| Поле | Тип |
|------|-----|
| Имя пользователя | text |
| Email | email |
| Имя | text |
| Фамилия | text |

### API endpoints

```
GET /api/auth/users/me/

PATCH /api/auth/users/me/
{
  "first_name": "Иван",
  "last_name": "Иванов"
}
```

### Смена пароля

```
POST /api/auth/users/set_password/
{
  "current_password": "oldpass",
  "new_password": "newpass",
  "re_new_password": "newpass"
}
```

## Store авторизации

### Состояние

```javascript
const user = ref(null)        // Данные пользователя
const token = ref(null)       // Токен авторизации
const loading = ref(false)    // Индикатор загрузки
const error = ref(null)       // Ошибки
```

### Методы

```javascript
// Вход в систему
await authStore.login({ username, password })

// Регистрация
await authStore.register({ username, email, password, re_password })

// Выход
await authStore.logout()

// Обновление профиля
await authStore.updateUser({ first_name, last_name })

// Смена пароля
await authStore.changePassword({ 
  current_password, 
  new_password, 
  re_new_password 
})
```

## Хранение токена

Токен сохраняется в `localStorage`:

```javascript
// При входе
localStorage.setItem('token', token)
localStorage.setItem('user', JSON.stringify(user))

// При выходе
localStorage.removeItem('token')
localStorage.removeItem('user')
```

## Interceptor авторизации

Все запросы автоматически включают токен:

```javascript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})
```
