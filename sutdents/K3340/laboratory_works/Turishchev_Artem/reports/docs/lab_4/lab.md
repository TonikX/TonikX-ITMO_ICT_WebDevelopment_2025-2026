# Задание
1. Настроить для серверной части, реализованной в лабораторной работе №3 CORS (Cross-origin resource sharing)
2. Реализовать интерфейсы авторизации, регистрации и изменения учётных данных и настроить взаимодействие с серверной частью.
3. Реализовать клиентские интерфейсы и настроить взаимодействие с серверной частью
4. Подключить vuetify или аналогичную библиотеку.
# Выполнение
# 1
Подключение cors делается при помощи библиотеки django-cors-headers
В settings.py нужно добавить приложение данной библиотеки и настроить доступ для приложения на vue при помощи CORS_ALLOWED_ORIGINS
# 2
![](photos/auth/1.png)
![](photos/auth/2.png)
# 3
Для отоброжения клиенстких интерфесов, была создана карточка под каждую сущность в компонентах и она использовалась для отображения как основных так и связанных сущностей везде, где нужно было. Для сущностей была сделана возможность, создать, изменить, удалить, а так же просмотреть список всех объектов данной сущности и 1 конкретный с более детальной информацией.
## Гости
![](photos/guest/1.png)
![](photos/guest/2.png)
![](photos/guest/3.png)
## Записи о проживании
![](photos/liv/1.png)
![](photos/liv/2.png)
![](photos/liv/3.png)
## Сотрудники
![](photos/staff/1.png)
![](photos/staff/2.png)
![](photos/staff/3.png)
## Комнаты
![](photos/rooms/1.png)
![](photos/rooms/2.png)
![](photos/rooms/3.png)
# Расписание уборкок
![](photos/cle/1.png)
![](photos/cle/2.png)
![](photos/cle/3.png)
## Записи об уборках 
![](photos/cle_rec/1.png)
![](photos/cle_rec/2.png)
![](photos/cle_rec/3.png)
## Этажи
![](photos/floors/1.png)
![](photos/floors/2.png)
![](photos/floors/3.png)
## Доп запросы
![](photos/requests/1.png)
![](photos/requests/2.png)
![](photos/requests/3.png)
![](photos/requests/4.png)
![](photos/requests/5.png)
![](photos/requests/6.png)