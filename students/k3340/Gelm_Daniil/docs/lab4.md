# Лабораторная работа 4. Реализация клиентской части приложения средствами Vue.js

## Вариант 1: Система управления гостиницей

Клиентская часть для системы управления гостиницей на Vue.js 3, Vue Router и Vuetify.

## Технологии

- Vue.js 3
- Vue Router
- Vuetify 3
- Axios
- Vite

## Структура проекта

```
lab4/
├── src/
│   ├── api/           # API клиенты
│   │   ├── axios.js   # Настройка axios
│   │   ├── auth.js    # API авторизации
│   │   └── hotel.js   # API гостиницы
│   ├── composables/   # Композаблы
│   │   └── useAuth.js # Логика авторизации
│   ├── router/        # Роутинг
│   │   └── index.js
│   ├── views/         # Страницы
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Rooms.vue
│   │   ├── Guests.vue
│   │   └── Stays.vue
│   ├── App.vue        # Главный компонент
│   └── main.js        # Точка входа
├── index.html
├── package.json
└── vite.config.js
```

## Настройка CORS

В lab3 настроен CORS для работы с фронтендом:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
```

## API клиент

### Настройка axios

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})
```

### API методы

**Авторизация:**
- `authAPI.register(data)` - регистрация
- `authAPI.login(data)` - вход
- `authAPI.logout()` - выход
- `authAPI.getCurrentUser()` - текущий пользователь

**Гостиница:**
- `hotelAPI.rooms.list()` - список номеров
- `hotelAPI.rooms.create(data)` - создать номер
- `hotelAPI.rooms.update(id, data)` - обновить номер
- `hotelAPI.rooms.delete(id)` - удалить номер
- `hotelAPI.guests.*` - аналогично для клиентов
- `hotelAPI.stays.*` - аналогично для проживаний

## Авторизация

### Композабл useAuth

```javascript
const { isAuthenticated, login, register, logout } = useAuth()
```

- `isAuthenticated` - реактивная переменная, показывает авторизован ли пользователь
- `login(username, password)` - вход
- `register(data)` - регистрация
- `logout()` - выход

Токен хранится в `localStorage` и автоматически добавляется в заголовки запросов.

## Роутинг

### Защищенные маршруты

```javascript
{
  path: '/rooms',
  name: 'Rooms',
  component: () => import('../views/Rooms.vue'),
  meta: { requiresAuth: true }
}
```

Роутер проверяет авторизацию перед переходом на защищенные страницы.

### Маршруты

- `/` - главная страница
- `/login` - вход
- `/register` - регистрация
- `/rooms` - управление номерами
- `/guests` - управление клиентами
- `/stays` - управление проживаниями

## Компоненты

### Home.vue

Главная страница с карточками для навигации по разделам.

### Login.vue

Форма входа с валидацией.

### Register.vue

Форма регистрации с проверкой совпадения паролей.

### Rooms.vue

- Таблица с номерами
- Диалог для добавления/редактирования
- Удаление номеров
- Фильтрация по типу и статусу

### Guests.vue

- Таблица с клиентами
- Диалог для добавления/редактирования
- Удаление клиентов

### Stays.vue

- Таблица с проживаниями
- Диалог для добавления/редактирования
- Выбор клиента и номера из списков
- Удаление проживаний

## Vuetify

Используется Vuetify 3 для UI компонентов:

- `v-app` - главный контейнер
- `v-app-bar` - шапка
- `v-data-table` - таблицы
- `v-dialog` - модальные окна
- `v-form` - формы
- `v-btn`, `v-text-field`, `v-select` - элементы форм

## Установка и запуск

1. Установить зависимости:
```bash
cd lab4
npm install
```

2. Запустить фронтенд:
```bash
npm run dev
```

3. Запустить бэкенд (в другом терминале):
```bash
cd lab3
python manage.py runserver
```

4. Открыть http://localhost:5173

## Использование

1. Зарегистрироваться или войти
2. После входа доступны страницы управления
3. Можно добавлять, редактировать и удалять номера, клиентов и проживания

## Важные блоки кода

### Защита маршрутов

```javascript
router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuth()
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login')
  } else {
    next()
  }
})
```

### Работа с API

```javascript
const loadRooms = async () => {
  loading.value = true
  try {
    const response = await hotelAPI.rooms.list()
    rooms.value = response.data.results || response.data
  } catch (error) {
    console.error('Error loading rooms:', error)
  } finally {
    loading.value = false
  }
}
```

### Сохранение данных

```javascript
const saveRoom = async () => {
  try {
    if (editingRoom.value) {
      await hotelAPI.rooms.update(editingRoom.value.id, form.value)
    } else {
      await hotelAPI.rooms.create(form.value)
    }
    showDialog.value = false
    loadRooms()
  } catch (error) {
    console.error('Error saving room:', error)
  }
}
```

