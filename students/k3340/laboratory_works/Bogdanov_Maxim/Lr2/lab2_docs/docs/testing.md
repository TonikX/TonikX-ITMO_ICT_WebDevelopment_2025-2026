# Тестирование

## Стратегия тестирования

Проект покрыт **модульными тестами** (unit tests) с использованием встроенного фреймворка Django Test.

### Покрытие

- Проверка доступности номеров
- Валидация бронирований
- Валидация отзывов
- Права доступа пользователей
- Фильтрация доступных номеров

Файл: `booking/tests.py`

## Запуск тестов

### Все тесты приложения
```bash
python manage.py test booking
```

### Конкретный класс тестов
```bash
python manage.py test booking.tests.BookingAvailabilityTestCase
```

### Конкретный тест
```bash
python manage.py test booking.tests.BookingAvailabilityTestCase.test_room_available_no_bookings
```

### С подробным выводом
```bash
python manage.py test booking --verbosity=2
```

---

## Результаты тестирования

При успешном прохождении всех тестов вывод должен быть примерно таким:
```
Found 13 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............
----------------------------------------------------------------------
Ran 13 tests in 5.123s

OK
Destroying test database for alias 'default'...
```

---

## Особенности тестирования

### Использование skip_validation

Для создания тестовых данных с датами в прошлом используется параметр `skip_validation`:
```python
booking = Booking(
    user=self.user,
    room=self.room,
    check_in=date.today() - timedelta(days=5),
    check_out=date.today() - timedelta(days=2),
    status='checked_out',
    total_price=300
)
booking.save(skip_validation=True)  # Пропускаем валидацию дат
```

### Тестовая БД

Django автоматически создаёт отдельную тестовую базу данных для каждого запуска тестов и удаляет её после завершения.

### Изоляция тестов

Каждый тест выполняется в отдельной транзакции, которая откатывается после завершения теста. Это гарантирует изоляцию тестов друг от друга.

---