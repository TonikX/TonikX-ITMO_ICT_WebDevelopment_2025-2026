# Лабораторная работа 4. Реализация клиентской части средствами React.js

## Цель работы
Овладеть практическими навыками реализации клиентской части (frontend) SPA-приложения с использованием React, TypeScript и современных библиотек экосистемы.

---

## Архитектура приложения

### Общая структура

Приложение построено по принципу **компонентной архитектуры** с централизованным управлением состоянием:

```
frontend/src/
├── main.tsx                # Точка входа, провайдеры
├── App.tsx                 # Корневой компонент, роутинг
├── api/                    # HTTP-клиент и API-функции
│   ├── client.ts           # Axios instance с interceptors
│   ├── auth.ts             # API аутентификации
│   ├── tours.ts            # API туров
│   ├── reservations.ts     # API бронирований
│   └── reviews.ts          # API отзывов
├── components/
│   ├── layout/             # Header, Footer, Layout
│   ├── ui/                 # UI-компоненты (shadcn/ui)
│   └── PrivateRoute.tsx    # Защищённый маршрут
├── pages/                  # Страницы приложения
├── store/                  # Zustand store
└── types/                  # TypeScript типы
```

### Принципы организации кода

1. **Страницы (Pages)** — контейнерные компоненты, отвечающие за бизнес-логику
2. **Компоненты (Components)** — переиспользуемые UI-элементы
3. **API Layer** — изолированный слой для HTTP-запросов
4. **Store** — глобальное состояние (аутентификация)
5. **Types** — централизованные TypeScript-интерфейсы

---

## Технологический стек

### Основные технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| **React** | 18.2 | UI-библиотека |
| **TypeScript** | 5.x | Типизация |
| **Vite** | 5.x | Сборщик и dev-сервер |
| **React Router** | 6.21 | Клиентский роутинг |
| **TanStack Query** | 5.17 | Кэширование и синхронизация данных |
| **Zustand** | 4.5 | Управление состоянием |
| **Axios** | 1.6 | HTTP-клиент |
| **Tailwind CSS** | 3.4 | Утилитарные стили |
| **shadcn/ui** | — | Библиотека UI-компонентов |

### Дополнительные библиотеки

- **react-hook-form** + **zod** — валидация форм
- **date-fns** — форматирование дат
- **lucide-react** — иконки
- **Radix UI** — примитивы для компонентов

---

## Управление состоянием

### Zustand Store (authStore.ts)

Глобальное состояние аутентификации реализовано через Zustand с middleware `persist`:

```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}
```

**Особенности реализации:**

- Токен сохраняется в `localStorage` через `persist` middleware
- При инициализации приложения автоматически восстанавливается сессия
- После успешного логина загружаются данные пользователя
- При ошибке 401 выполняется автоматический logout

### TanStack Query (React Query)

Серверное состояние управляется через React Query:

```typescript
// Кэширование списка туров
const { data: tours, isLoading } = useQuery({
  queryKey: ['tours'],
  queryFn: () => toursApi.getAll(),
});

// Мутация с инвалидацией кэша
const mutation = useMutation({
  mutationFn: (data) => toursApi.create(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tours'] });
  },
});
```

---

## HTTP-клиент

### Axios Configuration (client.ts)

```typescript
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor для JWT-токена
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor для обработки 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### API-модули

Каждая сущность имеет свой API-модуль:

```typescript
// tours.ts
export const toursApi = {
  getAll: async (params?) => api.get('/tours/', { params }),
  getById: async (id) => api.get(`/tours/${id}`),
  create: async (data) => api.post('/tours/', data),
  update: async (id, data) => api.put(`/tours/${id}`, data),
  delete: async (id) => api.delete(`/tours/${id}`),
};
```

---

## Маршрутизация

### React Router Configuration (App.tsx)

```typescript
<Routes>
  {/* Public routes */}
  <Route path="/" element={<HomePage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />
  <Route path="/tours" element={<ToursPage />} />
  <Route path="/tours/:id" element={<TourDetailPage />} />
  <Route path="/terms" element={<TermsPage />} />

  {/* Protected routes */}
  <Route path="/profile" element={
    <PrivateRoute><ProfilePage /></PrivateRoute>
  } />
  <Route path="/tours/new" element={
    <PrivateRoute><TourFormPage /></PrivateRoute>
  } />
  <Route path="/reservations" element={
    <PrivateRoute><ReservationsPage /></PrivateRoute>
  } />
  <Route path="/admin/reservations" element={
    <PrivateRoute><AdminReservationsPage /></PrivateRoute>
  } />
</Routes>
```

### PrivateRoute Component

Компонент-обёртка для защищённых маршрутов:

```typescript
export function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthStore();
  
  if (isLoading) return <Loader />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  
  return <>{children}</>;
}
```

---

## Страницы приложения

### HomePage
- Главная страница с hero-секцией
- **Карусель изображений** с автопрокруткой (6 слайдов)
- Навигационные кнопки и индикаторы
- Секции преимуществ с иконками

### ToursPage
- Список доступных туров с пагинацией
- Фильтрация по городу
- Карточки туров с основной информацией

### TourDetailPage
- Детальная информация о туре
- **Бронирование** (для авторизованных)
- **Отзывы** с возможностью добавления/редактирования
- Управление туром (только для админов)

### ProfilePage
- Редактирование username и email
- Редактирование даты рождения
- Смена пароля через диалоговое окно

### ReservationsPage
- Список бронирований пользователя
- Статусы: pending, confirmed, rejected

### AdminReservationsPage
- Управление всеми бронированиями
- Подтверждение/отклонение бронирований

---

## UI-компоненты (shadcn/ui)

Используются компоненты на базе Radix UI:

| Компонент | Назначение |
|-----------|------------|
| `Button` | Кнопки с вариантами |
| `Card` | Карточки контента |
| `Dialog` | Модальные окна |
| `Select` | Выпадающие списки |
| `Input`, `Textarea`, `Label` | Элементы форм |
| `Badge` | Статусные метки |
| `Toast` | Уведомления |
| `DropdownMenu` | Контекстные меню |
| `Avatar` | Аватар пользователя |

---

## Валидация форм

### React Hook Form + Zod

```typescript
const reservationSchema = z.object({
  notes: z.string().optional(),
});

const reviewSchema = z.object({
  text: z.string().min(1, 'Введите текст отзыва'),
  rating: z.coerce.number().min(1).max(10),
});

// Использование в компоненте
const form = useForm<ReviewFormData>({
  resolver: zodResolver(reviewSchema),
  defaultValues: { text: '', rating: 5 },
});
```

---

## CORS и Proxy

### Vite Dev Server Proxy (vite.config.ts)

```typescript
export default defineConfig({
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: true,
    proxy: {
      '/api': {
        target: 'http://app:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
```

**Принцип работы:**

1. Frontend работает на порту 3000
2. Запросы `/api/*` проксируются на FastAPI (порт 8000)
3. Vite dev server выступает прокси-сервером
4. CORS-заголовки не требуются при таком подходе

---

## TypeScript типизация

### Централизованные типы (types/index.ts)

```typescript
// User types
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

// Tour types
export interface Tour {
  id: number;
  title: string;
  agency: string;
  description: string | null;
  start_date: string;
  end_date: string;
  price: number;
  city: string;
  payment_terms: string | null;
}

// Reservation types
export interface Reservation {
  id: number;
  tour_id: number;
  user_id: number;
  notes: string | null;
  status: 'pending' | 'confirmed' | 'rejected';
  created_at: string;
}
```

---

## Контейнеризация Frontend

### Dockerfile (Dev Mode)

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

### Docker Compose Integration

```yaml
frontend:
  build: ./frontend
  ports:
    - "3000:3000"
  depends_on:
    - app
  volumes:
    - ./frontend:/app
    - /app/node_modules
```

---

## Выводы

В ходе выполнения лабораторной работы были изучены:

1. **React 18** — функциональные компоненты, хуки, контекст
2. **TypeScript** — строгая типизация props, состояния и API-ответов
3. **Vite** — быстрая сборка и HMR для разработки
4. **React Router 6** — декларативный роутинг с защищёнными маршрутами
5. **TanStack Query** — кэширование, инвалидация, оптимистичные обновления
6. **Zustand** — минималистичное управление глобальным состоянием
7. **Axios Interceptors** — централизованная обработка JWT и ошибок
8. **shadcn/ui + Radix** — доступные и кастомизируемые компоненты
9. **react-hook-form + Zod** — декларативная валидация форм
10. **Tailwind CSS** — utility-first подход к стилизации
11. **Vite Proxy** — решение CORS для development окружения

---
