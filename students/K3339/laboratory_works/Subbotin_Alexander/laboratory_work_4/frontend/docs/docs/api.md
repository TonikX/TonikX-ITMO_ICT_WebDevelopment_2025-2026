# API-клиент

## Конфигурация

### Базовая настройка Axios

```typescript
// src/api/client.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Interceptors

#### Request Interceptor

Добавляет JWT-токен к запросам:

```typescript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

#### Response Interceptor

Обрабатывает ошибки авторизации:

```typescript
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

---

## API-модули

### authApi

```typescript
// src/api/auth.ts

export const authApi = {
  register: (data: UserCreate) => 
    api.post<User>('/auth/register', data),

  login: (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    return api.post<Token>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },

  getCurrentUser: () => 
    api.get<User>('/auth/me'),

  getProfile: () => 
    api.get<UserProfile>('/auth/me/profile'),

  updateProfile: (data: { date_of_birth?: string }) => 
    api.put<UserProfile>('/auth/me/profile', data),
};
```

### toursApi

```typescript
// src/api/tours.ts

export const toursApi = {
  getAll: (params?: { limit?: number; offset?: number; city?: string }) =>
    api.get<Tour[]>('/tours/', { params }),

  getById: (id: number) =>
    api.get<Tour>(`/tours/${id}`),

  create: (data: TourCreate) =>
    api.post<Tour>('/tours/', data),

  update: (id: number, data: TourUpdate) =>
    api.put<Tour>(`/tours/${id}`, data),

  delete: (id: number) =>
    api.delete(`/tours/${id}`),
};
```

### reservationsApi

```typescript
// src/api/reservations.ts

export const reservationsApi = {
  getMy: (params?: { limit?: number; offset?: number }) =>
    api.get<Reservation[]>('/reservations/my', { params }),

  getById: (id: number) =>
    api.get<Reservation>(`/reservations/${id}`),

  create: (data: ReservationCreate) =>
    api.post<Reservation>('/reservations/', data),

  update: (id: number, data: ReservationUpdate) =>
    api.put<Reservation>(`/reservations/${id}`, data),

  delete: (id: number) =>
    api.delete(`/reservations/${id}`),
};
```

### reviewsApi

```typescript
// src/api/reviews.ts

export const reviewsApi = {
  getByTour: (tourId: number, params?: { limit?: number; offset?: number }) =>
    api.get<Review[]>(`/reviews/tour/${tourId}`, { params }),

  getById: (id: number) =>
    api.get<Review>(`/reviews/${id}`),

  create: (data: ReviewCreate) =>
    api.post<Review>('/reviews/', data),

  update: (id: number, data: ReviewUpdate) =>
    api.put<Review>(`/reviews/${id}`, data),

  delete: (id: number) =>
    api.delete(`/reviews/${id}`),
};
```

---

## Типы данных

### User

```typescript
interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}
```

### Tour

```typescript
interface Tour {
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
```

### Reservation

```typescript
interface Reservation {
  id: number;
  tour_id: number;
  user_id: number;
  guests: number;
  notes: string | null;
  confirmed: boolean;
  created_at: string;
  tour: Tour;
}
```

### Review

```typescript
interface Review {
  id: number;
  tour_id: number;
  user_id: number | null;
  text: string;
  rating: number;
  created_at: string;
  username?: string;
}
```

---

## Обработка ошибок

### API Error

```typescript
interface ApiError {
  detail: string;
}
```

### Пример обработки

```typescript
try {
  await toursApi.create(tourData);
} catch (error) {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.detail || 'Произошла ошибка';
    toast({ variant: 'destructive', title: 'Ошибка', description: message });
  }
}
```
