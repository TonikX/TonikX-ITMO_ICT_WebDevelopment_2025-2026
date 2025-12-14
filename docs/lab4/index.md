# Лабораторная работа №4: React Frontend для школьной системы

## Описание проекта

В рамках данной лабораторной работы был разработан frontend на React для REST API школьной системы управления, созданной в лабораторной работе №3 (lab3/teachers_system).

Приложение представляет собой административную панель для управления всеми сущностями школьной системы: предметами, кабинетами, учителями, классами, учениками, четвертями, назначениями преподавания, расписанием и оценками.

---

## Используемые технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| React | 18.x | Фреймворк для построения UI |
| React Router | 6.x | Маршрутизация в SPA |
| Axios | 1.x | HTTP-клиент для работы с API |
| Vite | 7.x | Сборщик и dev-сервер |

---

## Архитектура приложения

### Принципы проектирования

1. **Разделение ответственности** — логика работы с API вынесена в отдельный слой (`api/`), компоненты отвечают только за отображение.

2. **Переиспользуемость** — создан универсальный компонент `CrudPage`, который принимает конфигурацию (колонки таблицы, поля формы, сервис) и реализует полный CRUD-функционал. Это позволило избежать дублирования кода для 10 различных сущностей.

3. **Централизованное управление состоянием авторизации** — используется React Context (`AuthContext`) для хранения информации о текущем пользователе и токене авторизации.

4. **Защита маршрутов** — компонент `ProtectedRoute` проверяет авторизацию и перенаправляет неавторизованных пользователей на страницу входа.

---

## Реализованный функционал

### Авторизация

- Вход по логину и паролю
- Регистрация нового пользователя
- Автоматическое сохранение токена в localStorage
- Автоматический logout при истечении токена (401 ошибка)

### CRUD-операции

Для каждой сущности реализованы:

- Просмотр списка с таблицей
- Создание через модальное окно
- Редактирование через модальное окно
- Удаление с подтверждением

### Панель управления (Dashboard)

- Статистика: количество предметов, кабинетов, учителей, классов, учеников
- Статистика по полу в каждом классе (мальчики/девочки)
- Количество учителей по каждому предмету
- Количество кабинетов по типам
- Отображение текущей четверти

---

## Взаимодействие с Backend

### CORS

Для работы frontend на порту 5173 с backend на порту 8000 в Django было настроено:

- Установлен пакет `django-cors-headers`
- Добавлен middleware `CorsMiddleware`
- Разрешены запросы с `http://localhost:5173`

### Аутентификация

Используется Token-based аутентификация через Djoser:

- Получение токена: `POST /api/auth/token/login/`
- Токен передаётся в заголовке: `Authorization: Token <token>`

### Обработка ответов API

- Axios interceptor автоматически добавляет токен к запросам
- При 401 ошибке происходит автоматический logout
- Пагинация обрабатывается (поддержка `results` и прямого массива)

---

## Компоненты приложения

### AuthContext

Контекст авторизации для управления состоянием пользователя:

```jsx
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  
  const login = async (username, password) => {
    const response = await authAPI.login(username, password);
    setToken(response.auth_token);
    localStorage.setItem('token', response.auth_token);
  };
  
  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };
  
  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### CrudPage

Универсальный компонент для CRUD-операций:

```jsx
const CrudPage = ({ 
  title, 
  service, 
  columns, 
  formFields 
}) => {
  const [items, setItems] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  useEffect(() => {
    loadItems();
  }, []);
  
  const loadItems = async () => {
    const data = await service.getAll();
    setItems(data);
  };
  
  // ... CRUD методы
  
  return (
    <div className="crud-page">
      <h1>{title}</h1>
      <Table data={items} columns={columns} />
      <Modal isOpen={isModalOpen}>
        <Form fields={formFields} />
      </Modal>
    </div>
  );
};
```

### ProtectedRoute

Компонент для защиты маршрутов:

```jsx
const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  
  if (!token) {
    return <Navigate to="/login" />;
  }
  
  return children;
};
```

---

## API-сервисы

### Сервисы для сущностей

```javascript
// api/services.js
import api from './axios';

export const subjectsService = {
  getAll: () => api.get('/subjects/').then(r => r.data),
  getById: (id) => api.get(`/subjects/${id}/`).then(r => r.data),
  create: (data) => api.post('/subjects/', data).then(r => r.data),
  update: (id, data) => api.put(`/subjects/${id}/`, data).then(r => r.data),
  delete: (id) => api.delete(`/subjects/${id}/`),
};

// Аналогично для остальных сущностей...
```

---

## Маршрутизация

```jsx
// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<Dashboard />} />
            <Route path="subjects" element={<Subjects />} />
            <Route path="classrooms" element={<Classrooms />} />
            <Route path="teachers" element={<Teachers />} />
            <Route path="classes" element={<SchoolClasses />} />
            <Route path="students" element={<Students />} />
            <Route path="quarters" element={<Quarters />} />
            <Route path="assignments" element={<TeachingAssignments />} />
            <Route path="schedule" element={<Schedule />} />
            <Route path="grades" element={<Grades />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
```

---

## Запуск проекта

### 1. Запуск Backend (Django)

```bash
cd students/k3339/Zoteev_Maksim/lab3/teachers_system
source project-env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Backend будет доступен на http://localhost:8000

### 2. Запуск Frontend (React)

```bash
cd students/k3339/Zoteev_Maksim/lab4/teachers_system_react
npm install
npm run dev
```

Frontend будет доступен на http://localhost:5173

---

## Выводы

В ходе выполнения лабораторной работы были получены практические навыки:

- Разработки SPA на React
- Работы с REST API через Axios
- Реализации аутентификации на стороне клиента
- Использования React Router для навигации
- Применения React Context для глобального состояния
- Настройки CORS для взаимодействия frontend и backend

