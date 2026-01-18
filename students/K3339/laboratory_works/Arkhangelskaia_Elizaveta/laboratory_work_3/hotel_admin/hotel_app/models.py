from django.db import models


class RoomType(models.Model):
    """
    Тип номера
    """
    room_types = (
       ('1', '1-местный'),
       ('2', '2-местный'),
       ('3', '3-местный'),
    )
    room_type = models.CharField(max_length=1, choices=room_types, verbose_name='Тип номера')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
       return f'мест: {self.room_type}, цена {self.price}'


class Rooms(models.Model):
    """
    Номера в отеле
    """
    id_room_type = models.ForeignKey('RoomType',  verbose_name='Номер отеля', on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField(verbose_name='Номер комнаты')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', unique=True)
    floor = models.IntegerField(verbose_name='Этаж')

    def __str__(self):
        return f'комната: {self.room_number}, телефон: {self.phone_number}, этаж: {self.floor}'


class Residents(models.Model):
    """
    Проживающие гостиницы
    """

    passport_number = models.CharField(max_length=30, verbose_name='Номер паспорта')
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество')
    city = models.CharField(max_length=40, verbose_name='Город')

    def __str__(self):
       return f'Проживающий: {self.name} {self.surname} {self.patronymic}'


class Reservation(models.Model):
    """
    Бронирование номера
    """

    residents = models.ManyToManyField('Residents', related_name='reservations')
    rooms = models.ManyToManyField('Rooms', related_name='reservations')
    start_date = models.DateField(verbose_name='Дата заезда', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата выезда', null=True, blank=True)

    def __str__(self):
        return f"Бронирование {self.id} c {self.start_date} по {self.end_date}"


class Workers(models.Model):
    """
    Работники гостиницы
    """

    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество')
    is_employed = models.BooleanField(verbose_name="Трудоустроен", null=True, blank=True)

    def __str__(self):
       return f'Работник: {self.name} {self.surname} {self.patronymic}'


class CleaningInformation(models.Model):
    """
    Информация об уборке номеров
    """

    week_days = (('mon', 'monday'),
                 ('tue', 'tuesday'),
                 ('wed', 'wednesday'),
                 ('thu', 'thursday'),
                 ('fri', 'friday'),
                 ('sat', 'saturday'),
                 ('sun', 'sunday'))
    id_worker = models.ForeignKey('Workers', related_name='cleaning_information', on_delete=models.CASCADE)
    week_day = models.CharField(max_length=3, choices=week_days, verbose_name='День недели')
    floor = models.IntegerField(verbose_name='Этаж')

    def __str__(self):
        return f'{self.id_worker} {self.week_day} {self.floor}'


class Cleaning(models.Model):
    """
    Фактическая уборка номера
    """

    worker = models.ForeignKey('Workers', on_delete=models.CASCADE, related_name='cleanings')
    room = models.ForeignKey('Rooms', on_delete=models.CASCADE, related_name='cleanings')
    cleaning_date = models.DateTimeField(verbose_name='Дата уборки')


    def __str__(self):
        return f"Уборка комнаты {self.room.room_number} работником {self.worker} в {self.cleaning_date}"
