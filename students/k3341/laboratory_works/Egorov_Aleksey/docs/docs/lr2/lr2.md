# РЕАЛИЗАЦИЯ ПРОСТОГО САЙТА СРЕДСТВАМИ DJANGO

## Цель
Овладеть практическими навыками и умениями реализации web-сервисов средствами Django 2.2.

## Практическое задание
Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL\*, в соответствии с вариантом задания лабораторной работы.

**Вариант:** 1 (по списку 7)  

**Список отелей**  
Необходимо учитывать название отеля, владельца отеля, адрес, описание, типы
номеров, стоимость, вместимость, удобства.
Необходимо реализовать следующий функционал:  
 - Регистрация новых пользователей.  
 - Просмотр и резервирование номеров. Пользователь должен иметь возможность редактирования и удаления своих резервирований.  
 - Написание отзывов к номерам. При добавлении комментариев, должны сохраняться период проживания, текст комментария, рейтинг (1-10), информация о комментаторе.  
 - Администратор должен иметь возможность заселить пользователя в отель и
выселить из отеля средствами Django-admin.  
 - В клиентской части должна формироваться таблица, отображающая постояльцев отеля за последний месяц.

## Решение

### Структура проекта

```
H:.
│   db.sqlite3
│   manage.py
│   
├───.idea
│   │   .gitignore
│   │   lr_2.iml
│   │   misc.xml
│   │   modules.xml
│   │   vcs.xml
│   │   
│   └───inspectionProfiles
│           profiles_settings.xml
│           
├───config
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           settings.cpython-310.pyc
│           urls.cpython-310.pyc
│           wsgi.cpython-310.pyc
│           __init__.cpython-310.pyc
│           
├───hotels
│   │   360_F_592014361_dTHLlO1ReaWatAh9ms37icmwaazXWswG.jpg
│   │   AAACQC4BkqJqzJIjL2reKqO2ViSBzcN2oG7AHi30riU8Mr5ycVNYgIZuV-riw2XuSyRkoXAFCpm5Einwb7ZaUFI9Pa8.jpg
│   │   
│   └───hotels
│           360_F_592014361_dTHLlO1ReaWatAh9ms37icmwaazXWswG.jpg
│           AAACQC4BkqJqzJIjL2reKqO2ViSBzcN2oG7AHi30riU8Mr5ycVNYgIZuV-riw2XuSyRkoXAFCpm5Einwb_JlMLb2F.jpg
│           
└───hotelsales
    │   admin.py
    │   apps.py
    │   forms.py
    │   models.py
    │   tests.py
    │   urls.py
    │   views.py
    │   __init__.py
    │   
    ├───migrations
    │   │   0001_initial.py
    │   │   0002_booking_adults_booking_children.py
    │   │   0003_alter_booking_check_in_alter_booking_check_out_and_more.py
    │   │   0004_hotel_photo_alter_booking_total_price_and_more.py
    │   │   0005_alter_booking_id_alter_hotel_id_alter_review_id_and_more.py
    │   │   __init__.py
    │   │   
    │   └───__pycache__
    │           0001_initial.cpython-310.pyc
    │           0002_booking_adults_booking_children.cpython-310.pyc
    │           0003_alter_booking_check_in_alter_booking_check_out_and_more.cpython-310.pyc
    │           0004_hotel_photo_alter_booking_total_price_and_more.cpython-310.pyc
    │           0005_alter_booking_id_alter_hotel_id_alter_review_id_and_more.cpython-310.pyc
    │           __init__.cpython-310.pyc
    │           
    ├───templates
    │   └───hotelsales
    │           add_review.html
    │           booking_form.html
    │           edit_booking.html
    │           home.html
    │           hotel_detail.html
    │           my_bookings.html
    │           recent_guests.html
    │           register.html
    │           
    └───__pycache__
            admin.cpython-310.pyc
            apps.cpython-310.pyc
            forms.cpython-310.pyc
            models.cpython-310.pyc
            urls.cpython-310.pyc
            views.cpython-310.pyc
            __init__.cpython-310.pyc
```

### Модели:
**Hotel** — отели (название, владелец, адрес, описание, фото)

**RoomType** — типы номеров (название, описание, отель, стоимость за ночь, вместимость, удобства)

**Booking** — бронирования (пользователь, тип номера, даты заезда/выезда, количество взрослых/детей, общая стоимость, статус)

**Review** — отзывы (бронирование, рейтинг 1–10, комментарий, дата создания)

### Возможности системы

**Для всех пользователей (без авторизации):**
- Просмотр списка отелей
- Поиск по названию отеля
- Просмотр информации об отелях и номерах
- Просмотр отзывов о номерах
- Регистрация и вход в систему

**Для авторизованных пользователей:**
- Бронирование номеров с проверкой доступности
- Редактирование и отмена своих бронирований
- Написание отзывов после выселения
- Личный кабинет с историей бронирований

**Для персонала (администраторов):**
- Доступ к админ-панели Django
- Редактирование любых бронирований
- Просмотр всех гостей за выбранный период
- Управление статусами заселения и выселения

### Технические особенности
- В проекте используется Bootstrap для адаптивного интерфейса
- Настроена пагинация для списка отелей
- Реализован поиск по названию отеля

### Скриншоты работы сайта


**Стартовая страница**
![Список отелей или стартовая страница](images/hotels_list.png)  
