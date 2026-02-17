# Представления и URL Lab2

## Описание

В проекте используются функции-представления (function-based views) Django. Все представления находятся в файле `tours/views.py`.

## URL маршруты

Все маршруты определены в `tours/urls.py`:

```python
urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('tour/<int:tour_id>/review/', views.create_review, name='create_review'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/delete/', views.delete_reservation, name='delete_reservation'),
    path('sold-tours/', views.sold_tours_by_country, name='sold_tours_by_country'),
    path('register/', views.register, name='register'),
]
```

## Представления

### tour_list - Список туров

**URL:** `/`  
**Метод:** GET  
**Требования:** Нет

Отображает список всех туров с поиском и пагинацией.

**Особенности:**
- Поиск по названию, описанию, турагенству и стране
- Пагинация (6 туров на страницу)
- Использование Q объектов для сложных запросов

**Пример запроса:**
```
GET /?search=Турция&page=2
```

**Код:**
```python
def tour_list(request):
    tours = Tour.objects.all()
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        tours = tours.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(travel_agency__icontains=search_query) |
            Q(country__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(tours, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tours/tour_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })
```

### tour_detail - Детали тура

**URL:** `/tour/<id>/`  
**Метод:** GET  
**Требования:** Нет

Отображает детальную информацию о туре, последние отзывы и информацию о резервировании пользователя.

**Особенности:**
- Показывает последние 5 отзывов
- Проверяет наличие резервирования у текущего пользователя
- Использует `get_object_or_404` для обработки несуществующих туров

**Код:**
```python
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = tour.reviews.all()[:5]
    
    user_reservation = None
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(
            tour=tour, 
            user=request.user
        ).first()
    
    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'reviews': reviews,
        'user_reservation': user_reservation,
    })
```

### create_reservation - Создание резервирования

**URL:** `/tour/<tour_id>/reserve/`  
**Метод:** GET, POST  
**Требования:** `@login_required`

Создает новое резервирование тура для текущего пользователя.

**Особенности:**
- Проверяет, нет ли уже резервирования у пользователя
- Использует форму Django для валидации данных
- Сообщения об успехе/ошибке через Django messages

**Код:**
```python
@login_required
def create_reservation(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    
    # Проверка существующего резервирования
    existing_reservation = Reservation.objects.filter(
        tour=tour, 
        user=request.user
    ).first()
    if existing_reservation:
        messages.warning(request, 'У вас уже есть резервирование этого тура.')
        return redirect('tour_detail', pk=tour_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.tour = tour
            reservation.user = request.user
            reservation.save()
            messages.success(request, 'Резервирование успешно создано!')
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    
    return render(request, 'tours/create_reservation.html', {
        'form': form,
        'tour': tour,
    })
```

### my_reservations - Мои резервирования

**URL:** `/my-reservations/`  
**Метод:** GET  
**Требования:** `@login_required`

Отображает список всех резервирований текущего пользователя.

**Код:**
```python
@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(
        user=request.user
    ).order_by('-reservation_date')
    
    return render(request, 'tours/my_reservations.html', {
        'reservations': reservations,
    })
```

### edit_reservation - Редактирование резервирования

**URL:** `/reservation/<id>/edit/`  
**Метод:** GET, POST  
**Требования:** `@login_required`

Редактирует существующее резервирование пользователя.

**Особенности:**
- Проверяет, что резервирование принадлежит пользователю
- Не позволяет редактировать подтвержденные резервирования

**Код:**
```python
@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if reservation.status == 'confirmed':
        messages.error(request, 'Нельзя редактировать подтвержденное резервирование.')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование успешно обновлено!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'tours/edit_reservation.html', {
        'form': form,
        'reservation': reservation,
    })
```

### delete_reservation - Удаление резервирования

**URL:** `/reservation/<id>/delete/`  
**Метод:** GET, POST  
**Требования:** `@login_required`

Удаляет резервирование пользователя.

**Особенности:**
- Подтверждение удаления через форму
- Не позволяет удалять подтвержденные резервирования

**Код:**
```python
@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if reservation.status == 'confirmed':
        messages.error(request, 'Нельзя удалить подтвержденное резервирование.')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование успешно удалено!')
        return redirect('my_reservations')
    
    return render(request, 'tours/delete_reservation.html', {
        'reservation': reservation,
    })
```

### create_review - Создание отзыва

**URL:** `/tour/<tour_id>/review/`  
**Метод:** GET, POST  
**Требования:** `@login_required`

Создает отзыв о туре.

**Особенности:**
- Проверяет, нет ли уже отзыва от пользователя
- Валидация рейтинга (1-10)

**Код:**
```python
@login_required
def create_review(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    
    existing_review = Review.objects.filter(
        tour=tour, 
        user=request.user
    ).first()
    if existing_review:
        messages.warning(request, 'Вы уже оставили отзыв на этот тур.')
        return redirect('tour_detail', pk=tour_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('tour_detail', pk=tour_id)
    else:
        form = ReviewForm()
    
    return render(request, 'tours/create_review.html', {
        'form': form,
        'tour': tour,
    })
```

### sold_tours_by_country - Проданные туры по странам

**URL:** `/sold-tours/`  
**Метод:** GET  
**Требования:** Нет

Отображает таблицу проданных туров, сгруппированных по странам.

**Особенности:**
- Использует агрегацию Django (Count)
- Группировка по странам
- Сортировка по количеству резервирований

**Код:**
```python
def sold_tours_by_country(request):
    confirmed_reservations = Reservation.objects.filter(status='confirmed')
    
    tours_by_country = (
        confirmed_reservations
        .values('tour__country')
        .annotate(
            total_reservations=Count('id'),
            total_tours=Count('tour', distinct=True)
        )
        .order_by('-total_reservations')
    )
    
    return render(request, 'tours/sold_tours_by_country.html', {
        'tours_by_country': tours_by_country,
    })
```

### register - Регистрация пользователя

**URL:** `/register/`  
**Метод:** GET, POST  
**Требования:** Нет

Регистрирует нового пользователя и автоматически входит в систему.

**Код:**
```python
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('tour_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'tours/register.html', {
        'form': form,
    })
```

## Декораторы

### @login_required

Используется для защиты представлений, требующих аутентификации:

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_reservations(request):
    # Код представления
```

Если пользователь не аутентифицирован, Django перенаправит его на страницу входа.

## Сообщения (Messages)

Django messages framework используется для отображения уведомлений:

```python
from django.contrib import messages

messages.success(request, 'Операция успешна!')
messages.error(request, 'Произошла ошибка!')
messages.warning(request, 'Предупреждение!')
messages.info(request, 'Информация')
```

В шаблонах сообщения отображаются через:

```django
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

## Обработка ошибок

### get_object_or_404

Используется для получения объекта или возврата 404:

```python
tour = get_object_or_404(Tour, pk=pk)
```

### Перенаправления

```python
from django.shortcuts import redirect

return redirect('tour_list')
return redirect('tour_detail', pk=tour_id)
```
