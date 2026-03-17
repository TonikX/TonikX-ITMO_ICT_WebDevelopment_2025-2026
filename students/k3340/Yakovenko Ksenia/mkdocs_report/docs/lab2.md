# Лабораторная работа №2

## Тема
Разработка веб-приложения системы бронирования туров с использованием Django.

## Цель работы

Изучить основы разработки веб-приложений с использованием Django, реализовать систему просмотра туров, бронирования туров, добавления отзывов и администрирования данных.

## Задачи

В рамках работы необходимо реализовать:

- регистрацию пользователей
- просмотр туров
- бронирование туров
- удаление бронирований
- систему отзывов
- подтверждение бронирований администратором
- таблицу проданных туров по странам
- поиск
- пагинацию
- 
## Модели базы данных

Модель в Django представляет таблицу базы данных.

## Модель Tour

```python
    class Tour(models.Model):
        title = models.CharField(max_length=200)
        agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
        country = models.ForeignKey(Country, on_delete=models.PROTECT)
        description = models.TextField()
        start_date = models.DateField()
        end_date = models.DateField()
        payment_terms = models.TextField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
```

### Объяснение

`CharField` используется для хранения строк

`TextField` хранит длинный текст

`DateField` хранит дату

`DecimalField` хранит денежные значения

`ForeignKey` создаёт связь между таблицами

## Модель Booking
```python
class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
```
Модель хранит информацию о бронировании тура пользователем.

## Представления

Представления (views) обрабатывают HTTP-запросы.

### Отображение списка туров

```python
class TourListView(ListView):
    model = Tour
    template_name = "tours/tour_list.html"
    paginate_by = 6
```

### Объяснение

`ListView` отображает список объектов

`model = Tour` указывает используемую модель

`paginate_by` включает пагинацию

## Реализация поиска

```python
def get_queryset(self):
    qs = Tour.objects.select_related("agency", "country")
    q = self.request.GET.get("q", "").strip()

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(country__name__icontains=q)
        )

    return qs
```

Поиск выполняется по названию тура и стране.

## Шаблоны

Шаблоны используются для генерации HTML-страниц.

### Пример шаблона:
```html
{% for tour in tours %}
    <h3>{{ tour.title }}</h3>
{% endfor %}
What is this?
```
### Объяснение

`{% for %}` используется для циклов

`{{ }}` выводит значение переменной

# Административная панель

Django имеет встроенную административную панель.

Администратор может:

- управлять турами

- подтверждать бронирования

- просматривать отзывы

### Подтверждение бронирования

```python
@admin.action(description="Confirm bookings")
def confirm_bookings(self, request, queryset):
    queryset.update(is_confirmed=True)
```
Эта функция позволяет администратору подтверждать выбранные бронирования.