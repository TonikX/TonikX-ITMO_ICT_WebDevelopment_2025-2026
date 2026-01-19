# Интерфейс авторизации

## Страница входа (LoginPage)

![Login Page](../images/login.png)

### Описание

Страница входа позволяет пользователю авторизоваться в системе с использованием имени пользователя и пароля.

### Функциональность

- Ввод имени пользователя
- Ввод пароля (с возможностью показать/скрыть)
- Валидация формы
- Отображение ошибок
- Перенаправление после успешного входа

### Валидация

| Поле | Правило |
|------|---------|
| Имя пользователя | Минимум 3 символа |
| Пароль | Минимум 6 символов |

### Пример использования

```tsx
// Логика отправки формы
const onSubmit = async (data: LoginFormData) => {
  try {
    await login(data.username, data.password);
    navigate('/tours');
  } catch (error) {
    // Показать ошибку
  }
};
```

### API-запрос

```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secret123
```

### Ответ

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Страница регистрации (RegisterPage)

![Register Page](../images/register.png)

### Описание

Страница регистрации позволяет создать новую учётную запись.

### Поля формы

| Поле | Тип | Обязательное |
|------|-----|--------------|
| Имя пользователя | text | Да |
| Email | email | Да |
| Пароль | password | Да |
| Подтверждение пароля | password | Да |

### Валидация

| Поле | Правило |
|------|---------|
| Имя пользователя | 3-150 символов |
| Email | Корректный email |
| Пароль | Минимум 6 символов |
| Подтверждение | Совпадает с паролем |

### API-запрос

```
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "secret123"
}
```

### После регистрации

После успешной регистрации пользователь автоматически авторизуется и перенаправляется на страницу туров.

---

## Хранение токена

JWT-токен сохраняется в `localStorage`:

```typescript
// Сохранение
localStorage.setItem('token', tokenData.access_token);

// Использование в запросах
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

---

## Выход из системы

При выходе:
1. Удаляется токен из `localStorage`
2. Очищается состояние пользователя в store
3. Пользователь перенаправляется на главную страницу

```typescript
const logout = () => {
  localStorage.removeItem('token');
  set({ user: null, token: null, isAuthenticated: false });
};
```
