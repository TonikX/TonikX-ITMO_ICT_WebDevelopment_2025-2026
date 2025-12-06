# API Модули

## Обзор

API модули находятся в папке `src/api/` и отвечают за взаимодействие с Django REST Framework бэкендом.

## Структура

### axios.js

Централизованная настройка Axios клиента с interceptors для автоматической работы с JWT токенами.

#### Request Interceptor

Автоматически добавляет JWT access токен к каждому запросу:

```javascript
config.headers.Authorization = `Bearer ${authStore.accessToken}`
```

#### Response Interceptor

Обрабатывает ошибки 401 (Unauthorized) и автоматически обновляет токен:

1. При получении 401 ошибки
2. Пытается обновить токен через refresh endpoint
3. Повторяет оригинальный запрос с новым токеном
4. Если обновление не удалось - выполняет logout

### auth.js

Методы для работы с аутентификацией через Djoser:

#### `login(usernameOrEmail, password)`

Вход пользователя в систему.

**Параметры:**
- `usernameOrEmail` (string) - Username или email пользователя
- `password` (string) - Пароль

**Возвращает:** Promise с JWT токенами (access и refresh)

**Примечание:** Djoser настроен на LOGIN_FIELD: "username", поэтому поле отправляется как "username", но можно передать email как username (если backend это поддерживает).

**Пример:**
```javascript
const tokens = await login('user@example.com', 'password123')
// или
const tokens = await login('username', 'password123')
// { access: '...', refresh: '...' }
```

#### `register(email, username, password, re_password)`

Регистрация нового пользователя.

**Параметры:**
- `email` (string) - Email пользователя
- `username` (string, optional) - Имя пользователя (генерируется из email если не указано)
- `password` (string) - Пароль
- `re_password` (string) - Подтверждение пароля

**Возвращает:** Promise с данными созданного пользователя

#### `refreshToken(refreshToken)`

Обновление JWT access токена.

**Параметры:**
- `refreshToken` (string) - Refresh токен

**Возвращает:** Promise с новым access токеном

#### `getCurrentUser()`

Получение информации о текущем авторизованном пользователе.

**Возвращает:** Promise с данными пользователя

#### `updateCurrentUser(userData)`

Обновление данных текущего пользователя.

**Параметры:**
- `userData` (object) - Объект с полями для обновления (email, username)

**Возвращает:** Promise с обновленными данными пользователя

#### `changePassword(currentPassword, newPassword, reNewPassword)`

Изменение пароля текущего пользователя.

**Параметры:**
- `currentPassword` (string) - Текущий пароль
- `newPassword` (string) - Новый пароль
- `reNewPassword` (string) - Подтверждение нового пароля

**Возвращает:** Promise

### profile.js

Методы для работы с профилем пользователя:

#### `getProfile()`

Получение профиля текущего пользователя.

**Возвращает:** Promise с данными профиля

**Структура ответа:**
```javascript
{
  user: {
    id: 1,
    username: 'user',
    email: 'user@example.com'
  },
  display_name: 'Имя пользователя',
  bio: 'О себе...',
  avatar: 'http://...',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z'
}
```

#### `updateProfile(profileData)`

Обновление профиля текущего пользователя.

**Параметры:**
- `profileData` (FormData|Object) - Данные профиля:
  - `display_name` (string, optional)
  - `bio` (string, optional)
  - `avatar` (File, optional)

**Возвращает:** Promise с обновленными данными профиля

**Пример с FormData (для загрузки аватара):**
```javascript
const formData = new FormData()
formData.append('display_name', 'Новое имя')
formData.append('bio', 'Новая биография')
formData.append('avatar', fileInput.files[0])

await updateProfile(formData)
```

#### `getUserProfile(userId)`

Получение профиля другого пользователя (только чтение).

**Параметры:**
- `userId` (number) - ID пользователя

**Возвращает:** Promise с данными профиля

## Обработка ошибок

Все API методы выбрасывают ошибки, которые можно обработать:

```javascript
try {
  await login(email, password)
} catch (error) {
  if (error.response) {
    // Ошибка от сервера
    console.error('Status:', error.response.status)
    console.error('Data:', error.response.data)
  } else {
    // Ошибка сети
    console.error('Network error:', error.message)
  }
}
```

## Базовая конфигурация

API клиент настроен на работу с бэкендом по адресу из переменной окружения `VITE_API_BASE_URL` (по умолчанию `http://localhost:8000`).

Все запросы автоматически включают:
- Заголовок `Content-Type: application/json`
- JWT токен в заголовке `Authorization` (для авторизованных запросов)
