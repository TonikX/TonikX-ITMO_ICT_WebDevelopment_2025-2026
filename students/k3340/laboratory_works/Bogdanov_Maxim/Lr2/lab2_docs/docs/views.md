# Представления и шаблоны

## Архитектура представлений

Проект использует **Class-Based Views (CBV)** Django для обеспечения повторного использования кода и следования принципу DRY.

## Основные представления

### Регистрация и аутентификация

#### RegisterView
```python
class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
```

**Назначение:** Регистрация новых пользователей.

**Особенности:**
- Использует встроенную форму Django `UserCreationForm`
- После успешной регистрации перенаправляет на страницу входа
- Отображает сообщение об успехе

---

### Отели

#### HotelListView
```python
class HotelListView(ListView):
    model = Hotel
    template_name = 'booking/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 10
```

**Назначение:** Список всех отелей с поиском и пагинацией.

**Особенности:**
- Поиск по названию и адресу
- 10 отелей на страницу
- Форма фильтрации `HotelFilterForm`

**Шаблон:** `hotel_list.html`
- Карточки отелей с описанием
- Форма поиска
- Пагинация с номерами страниц

#### HotelDetailView
```python
class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'booking/hotel_detail.html'
    context_object_name = 'hotel'
```

**Назначение:** Детальная информация об отеле.

**Дополнительный контекст:**
- `room_types` - типы номеров отеля
- `recent_guests` - постояльцы за последние 30 дней
- `reviews` - последние 10 отзывов
- `average_rating` - средний рейтинг отеля

**Шаблон:** `hotel_detail.html`
- Информация об отеле
- Список типов номеров
- Кнопка "Выбрать номер и забронировать"
- Таблица постояльцев
- Отзывы гостей

---

### Номера

#### RoomListView
```python
class RoomListView(ListView):
    model = Room
    template_name = 'booking/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 12
```

**Назначение:** Список номеров с фильтрацией.

**URL:** `/hotels/<hotel_id>/rooms/`

**Фильтры:**
- Тип номера
- Удобства (множественный выбор)
- Минимальная вместимость
- Максимальная цена
- Даты проживания (с проверкой доступности)

**Особенности:**
- Автоматическая фильтрация по отелю из URL
- Сохранение GET-параметров при пагинации
- 12 номеров на страницу

**Шаблон:** `room_list.html`
- Панель фильтров
- Карточки номеров с информацией
- Кнопки бронирования
- Умная пагинация

---

### Бронирования

#### BookingCreateView
```python
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('my_bookings')
```

**Назначение:** Создание нового бронирования.

**Защита:**
- `LoginRequiredMixin` - требуется авторизация

**Особенности:**
- Предзаполнение номера из GET-параметра `?room=<id>`
- Ограничение выбора номеров по отелю
- Автоматический расчёт стоимости
- Валидация доступности

#### MyBookingsView
```python
class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
```

**Назначение:** Список бронирований текущего пользователя.

**Особенности:**
- Фильтрация `user=request.user`
- Сортировка по дате создания (новые первыми)
- Отображение статусов
- Кнопки действий (редактировать/отменить)

#### BookingDetailView
```python
class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    context_object_name = 'booking'
```

**Назначение:** Детальная информация о бронировании.

**Дополнительный контекст:**
- `has_review` - есть ли отзыв на это бронирование
- `can_review` - можно ли оставить отзыв

**Особенности:**
- Кнопка "Оставить отзыв" (если возможно)
- Отображение существующего отзыва
- Информация об отеле и номере

#### BookingUpdateView
```python
class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('my_bookings')
```

**Назначение:** Редактирование бронирования.

**Защита:**
- Проверка владельца через `get_queryset()`
- Проверка возможности редактирования через `can_edit`

#### BookingDeleteView
```python
class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_confirm_delete.html'
    success_url = reverse_lazy('my_bookings')
```

**Назначение:** Отмена бронирования.

**Особенности:**
- Не удаляет, а меняет статус на `cancelled`
- Проверка возможности отмены через `can_cancel`

---

### Отзывы

#### ReviewCreateView
```python
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'booking/review_form.html'
    success_url = reverse_lazy('my_bookings')
```

**Назначение:** Создание отзыва на бронирование.

**URL:** `/reviews/new/<booking_id>/`

**Особенности:**
- Получение бронирования из URL
- Автоматическое заполнение дат из бронирования
- Валидация права на отзыв
- Простая форма (только рейтинг и комментарий)

#### MyReviewsView
```python
class MyReviewsView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'booking/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
```

**Назначение:** Список отзывов текущего пользователя.

**Особенности:**
- Фильтрация по пользователю
- Отображение рейтинга с цветовой индикацией
- Ссылки на бронирования

---

## Шаблоны

### Базовый шаблон

**Файл:** `templates/base.html`

**Структура:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link href="Bootstrap 5 CDN" />
</head>
<body>
    <nav class="navbar">
        <!-- Навигация -->
    </nav>
    
    <main class="container">
        <!-- Сообщения -->
        {% if messages %}
            <!-- Django messages -->
        {% endif %}
        
        <!-- Контент страницы -->
        {% block content %}
        {% endblock %}
    </main>
    
    <footer>
        <!-- Подвал -->
    </footer>
</body>
</html>
```

**Особенности:**
- Bootstrap 5 из CDN
- Navbar с адаптивным меню
- Отображение Django messages
- Блок для кастомного контента

### Ключевые шаблоны

#### hotel_list.html
- Форма поиска
- Карточки отелей (Grid Layout)
- Пагинация

#### hotel_detail.html
- Информация об отеле
- Типы номеров (карточки)
- Кнопка перехода к выбору номеров
- Отзывы гостей
- Таблица постояльцев

#### room_list.html
- Панель фильтров (collapse)
- Карточки номеров (Grid 3 колонки)
- Пагинация с сохранением фильтров
- Счётчик результатов

#### booking_form.html
- Форма с полями: номер, даты
- Отображение информации о номере
- Валидационные ошибки
- Кнопки сохранения/отмены

#### booking_list.html
- Таблица бронирований
- Цветовая индикация статусов
- Кнопки действий (условные)
- Пагинация

#### review_form.html
- Информация о бронировании
- Поля: рейтинг (1-10), комментарий
- Валидация
- Подсказки

---

## URL-маршруты
```python
urlpatterns = [
    # Главная и отели
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('hotels/<int:hotel_id>/rooms/', views.RoomListView.as_view(), name='hotel_rooms'),
    
    # Бронирования
    path('bookings/new/', views.BookingCreateView.as_view(), name='booking_create'),
    path('bookings/my/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    
    # Отзывы
    path('reviews/new/<int:booking_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/my/', views.MyReviewsView.as_view(), name='my_reviews'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]
```

---

## Безопасность в представлениях

### Аутентификация
```python
class MyBookingsView(LoginRequiredMixin, ListView):
    # Требует входа в систему
    pass
```

### Авторизация
```python
def get_queryset(self):
    # Только свои бронирования
    return Booking.objects.filter(user=self.request.user)
```

### CSRF Protection
```html
<form method="post">
    {% csrf_token %}
    <!-- Поля формы -->
</form>
```

### Валидация прав
```python
def get_object(self, queryset=None):
    obj = super().get_object(queryset)
    if not obj.can_edit:
        messages.error(self.request, 'Это бронирование нельзя редактировать')
        return redirect('my_bookings')
    return obj
```