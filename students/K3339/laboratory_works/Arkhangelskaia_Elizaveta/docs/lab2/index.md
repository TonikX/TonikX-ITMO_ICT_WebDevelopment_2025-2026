# Лабораторная работа 2

--- 


## РЕАЛИЗАЦИЯ ПРОСТОГО САЙТА СРЕДСТВАМИ DJANGO

**Цель:** овладеть практическими навыками и умениями реализации web-сервисов средствами Django 2.2.

**Практическое задание:** реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL, в соответствии с вариантом задания лабораторной работы.

Мой вариант задания 1. 

**Тема:** Список отелей.
**Требования:**
- Необходимо учитывать название отеля, владельца отеля, адрес, описание, типы номеров, стоимость, вместимость, удобства.
- Регистрация новых пользователей. 
- Просмотр и резервирование номеров. Пользователь должен иметь возможность редактирования и удаления своих резервирований. 
- Написание отзывов к номерам. При добавлении комментариев, должны сохраняться период проживания, текст комментария, рейтинг (1-10),  информация о комментаторе.
- Администратор должен иметь возможность заселить пользователя в отель и выселить из отеля средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая постояльцев отеля за последний месяц.

Марашруты: 

```python
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'),
    path('hotels/', hotels, name='hotels'),
    path('all_rooms/', all_rooms, name='all_rooms'),
    path('book_room/<int:pk>', book_room, name='book_room'),
    path('', home, name='home'),
    path('reservations/', reservations, name='reservations'),
    path('reservation/<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='edit_reservation'),
    path('reservation/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='delete_reservation'),
    path('guests/', views.last_month_guests, name='last_month_guests'),
    path('review/<int:pk>/', views.get_review, name='get_review'),
]

```

Модели: 

```python
class Hotel(models.Model):
    name = models.CharField(max_length=100, null=False)
    owner = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=False)


class HotelUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class RoomType(models.Model):
    id_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=30, null=False)
    price = models.IntegerField(null=False)
    capacity = models.IntegerField(null=False)
    count = models.IntegerField(null=True)


class Facility(models.Model):
    id_room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    facility = models.CharField(max_length=30, null=False)


class Reservation(models.Model):
    id_user = models.ForeignKey(HotelUser, on_delete=models.CASCADE)
    id_rooms = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    reservation_date = models.DateField(null=False)
    num_of_people = models.IntegerField(default=1)

class Review(models.Model):
    id_reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)
    review_text = models.CharField(max_length=500, null=False)
```

