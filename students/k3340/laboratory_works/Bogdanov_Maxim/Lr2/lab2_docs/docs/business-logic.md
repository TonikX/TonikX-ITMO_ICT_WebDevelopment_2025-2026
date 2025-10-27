# Бизнес-логика

## Проверка доступности номеров

### Алгоритм

Номер считается **недоступным**, если существует бронирование со статусом `confirmed`, `checked_in` или `checked_out`, интервалы которого пересекаются с запрашиваемым периодом.

**Условие пересечения интервалов:**
```python
NOT (booking.check_out <= new_check_in OR booking.check_in >= new_check_out)
```

Эквивалентно:
```python
booking.check_out > new_check_in AND booking.check_in < new_check_out
```

### Реализация
```python
def check_room_availability(room, check_in, check_out, exclude_booking_id=None):
    """
    Проверяет доступность номера на указанные даты.
    
    Args:
        room: Объект Room
        check_in: Дата заезда
        check_out: Дата выезда
        exclude_booking_id: ID бронирования для исключения (при редактировании)
    
    Returns:
        bool: True если номер доступен, False если занят
    """
    blocking_statuses = ['confirmed', 'checked_in', 'checked_out']
    
    overlapping_bookings = Booking.objects.filter(
        room=room,
        status__in=blocking_statuses
    ).filter(
        ~Q(check_out__lte=check_in) & ~Q(check_in__gte=check_out)
    )
    
    if exclude_booking_id:
        overlapping_bookings = overlapping_bookings.exclude(id=exclude_booking_id)
    
    return not overlapping_bookings.exists()
```

### Блок-схема
```
Начало
  ↓
Получить бронирования номера
со статусами: confirmed, checked_in, checked_out
  ↓
Отфильтровать по пересечению дат:
NOT (check_out <= new_check_in OR check_in >= new_check_out)
  ↓
Исключить текущее бронирование (если редактирование)
  ↓
Есть пересечения? ─ Да → Номер ЗАНЯТ
  ↓ Нет
Номер ДОСТУПЕН
```

---

## Валидация бронирований

### Правила

1. **Даты:**
   - `check_in < check_out`
   - `check_in >= today` (только при создании)

2. **Доступность:**
   - Номер должен быть свободен на выбранные даты
   - Проверка через `check_room_availability()`

3. **Статус:**
   - При создании автоматически `pending`
   - Пользователь может редактировать только со статусами `pending` или `confirmed`

4. **Права:**
   - Редактировать можно только до даты заезда
   - Отменить можно до даты заезда

### Реализация в форме
```python
class BookingForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError('Дата выезда должна быть позже даты заезда')

            if room:
                exclude_id = self.instance.pk if self.instance.pk else None
                if not check_room_availability(room, check_in, check_out, exclude_id):
                    raise ValidationError('Номер недоступен на выбранные даты')

        return cleaned_data
```

---

## Валидация отзывов

### Правила

1. **Право на отзыв:**
   - Должна существовать бронь пользователя на этот номер
   - Статус брони: `checked_in` или `checked_out`
   - Период отзыва должен пересекаться с периодом брони
   - Текущая дата >= дата заезда

2. **Рейтинг:**
   - От 1 до 10 (валидаторы Django)

3. **Уникальность:**
   - Один отзыв на одно бронирование

### Реализация в форме
```python
class ReviewForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        
        if self.booking:
            # Проверка даты
            if self.booking.check_in > date.today():
                raise ValidationError('Отзыв можно оставить только после заезда')
            
            # Проверка статуса
            if self.booking.status not in ['checked_in', 'checked_out']:
                raise ValidationError('Отзыв можно оставить только для подтверждённых бронирований')
            
            # Проверка уникальности
            if not self.instance.pk:
                existing_review = Review.objects.filter(
                    booking=self.booking,
                    user=self.user
                ).exists()
                
                if existing_review:
                    raise ValidationError('Вы уже оставили отзыв на это бронирование')
        
        return cleaned_data
```

---

## Расчёт стоимости
```python
def calculate_booking_price(room, check_in, check_out):
    """
    Рассчитывает стоимость бронирования.
    
    Args:
        room: Объект Room
        check_in: Дата заезда
        check_out: Дата выезда
    
    Returns:
        Decimal: Общая стоимость (количество ночей × цена за ночь)
    """
    nights = (check_out - check_in).days
    return room.room_type.price_per_night * nights
```

---

## Постояльцы за период
```python
def get_recent_guests(hotel, days=30):
    """
    Возвращает постояльцев отеля за последние N дней.
    
    Args:
        hotel: Объект Hotel
        days: Количество дней (по умолчанию 30)
    
    Returns:
        QuerySet: Бронирования со статусами checked_in/checked_out
    """
    cutoff_date = date.today() - timedelta(days=days)
    
    bookings = Booking.objects.filter(
        room__room_type__hotel=hotel,
        check_in__lte=date.today(),
        check_out__gte=cutoff_date,
        status__in=['checked_in', 'checked_out']
    ).select_related('user', 'room__room_type').order_by('-check_in')
    
    return bookings
```

### Логика фильтрации

Бронирование попадает в список, если:
`check_in <= today AND check_out = (today - 30 days) AND status IN ('checked_in', 'checked_out')`

## Управление статусами в админке

### Заселение (Check-in)
```python
def can_check_in(booking):
    """
    Проверяет возможность заселения.
    
    Условия:
    - Статус: confirmed
    - Дата заезда <= сегодня
    """
    return (
        booking.status == 'confirmed' and
        booking.check_in <= date.today()
    )
```

**Admin action:**
```python
def check_in_booking(self, request, queryset):
    success_count = 0
    for booking in queryset:
        if can_check_in(booking):
            booking.status = 'checked_in'
            booking.save()
            success_count += 1
        else:
            self.message_user(
                request,
                f'Бронирование {booking.id} нельзя перевести в статус "Заселён"',
                level=messages.WARNING
            )
    
    if success_count:
        self.message_user(
            request,
            f'Успешно заселено гостей: {success_count}',
            level=messages.SUCCESS
        )
```

### Выселение (Check-out)
```python
def can_check_out(booking):
    """
    Проверяет возможность выселения.
    
    Условия:
    - Статус: checked_in
    """
    return booking.status == 'checked_in'
```

**Admin action:**
```python
def check_out_booking(self, request, queryset):
    success_count = 0
    for booking in queryset:
        if can_check_out(booking):
            booking.status = 'checked_out'
            booking.save()
            success_count += 1
        else:
            self.message_user(
                request,
                f'Бронирование {booking.id} нельзя перевести в статус "Выселен"',
                level=messages.WARNING
            )
    
    if success_count:
        self.message_user(
            request,
            f'Успешно выселено гостей: {success_count}',
            level=messages.SUCCESS
        )
```

---

## Фильтрация номеров

### Параметры фильтрации
```python
class RoomFilterForm(forms.Form):
    room_type = forms.ModelChoiceField(...)        # Тип номера
    amenities = forms.ModelMultipleChoiceField(...) # Удобства (множественный выбор)
    min_capacity = forms.IntegerField(...)         # Минимальная вместимость
    max_price = forms.DecimalField(...)            # Максимальная цена
    check_in = forms.DateField(...)                # Дата заезда
    check_out = forms.DateField(...)               # Дата выезда
```

### Алгоритм фильтрации
```python
def get_queryset(self):
    queryset = Room.objects.filter(is_active=True)
    
    # Фильтр по отелю
    if hotel_id:
        queryset = queryset.filter(room_type__hotel_id=hotel_id)
    
    # Фильтр по типу
    if room_type:
        queryset = queryset.filter(room_type=room_type)
    
    # Фильтр по удобствам (AND-логика)
    if amenities:
        for amenity in amenities:
            queryset = queryset.filter(room_type__amenities=amenity)
    
    # Фильтр по вместимости
    if min_capacity:
        queryset = queryset.filter(room_type__capacity__gte=min_capacity)
    
    # Фильтр по цене
    if max_price:
        queryset = queryset.filter(room_type__price_per_night__lte=max_price)
    
    # Фильтр по доступности на даты
    if check_in and check_out:
        available_rooms = get_available_rooms(check_in, check_out)
        queryset = queryset.filter(id__in=available_rooms)
    
    return queryset.distinct()
```

### Получение доступных номеров
```python
def get_available_rooms(check_in, check_out, hotel=None, room_type=None):
    """
    Возвращает QuerySet доступных номеров.
    """
    rooms = Room.objects.filter(is_active=True)
    
    if hotel:
        rooms = rooms.filter(room_type__hotel=hotel)
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    # Получаем ID занятых номеров
    blocking_statuses = ['confirmed', 'checked_in', 'checked_out']
    unavailable_room_ids = Booking.objects.filter(
        status__in=blocking_statuses
    ).filter(
        ~Q(check_out__lte=check_in) & ~Q(check_in__gte=check_out)
    ).values_list('room_id', flat=True)
    
    # Исключаем недоступные
    return rooms.exclude(id__in=unavailable_room_ids)
```