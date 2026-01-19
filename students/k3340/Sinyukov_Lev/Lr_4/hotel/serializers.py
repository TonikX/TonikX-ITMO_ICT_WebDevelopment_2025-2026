from rest_framework import serializers  # DRF сериализаторы
from .models import Room, Client, Stay, Employee, CleaningSchedule  # модели приложения


# CRUD сериализаторы: отдать/принять все поля модели

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"  # включаем все поля модели (id, number, floor)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = "__all__"


# Вспомогательные/детальные сериализаторы

class StayShortSerializer(serializers.ModelSerializer):
    # Доп. поле: номер комнаты (берётся из связанного объекта room.number)
    # read_only=True - поле только для вывода, не принимаем его во входных данных
    room_number = serializers.IntegerField(source="room.number", read_only=True)

    class Meta:
        model = Stay
        # Укороченный набор полей, полезен для списка проживаний у клиента
        fields = ["id", "check_in", "check_out", "room_number"]


class ClientDetailSerializer(serializers.ModelSerializer):
    # Поле stays берется из related_name="stays" у Stay.client
    # many=True - список проживаний
    # read_only=True - нельзя создавать stays через Client serializer
    stays = StayShortSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        # Все поля клиента + поле stays (потому что оно явно объявлено выше)
        fields = "__all__"


class ClientShortSerializer(serializers.ModelSerializer):
    # Минимальный сериализатор клиента (удобно вкладывать в другие ответы)
    class Meta:
        model = Client
        fields = ["id", "passport_number", "last_name", "first_name"]


class RoomDetailSerializer(serializers.ModelSerializer):
    # stays не является полем модели Room напрямую - вычисляем вручную через метод
    stays = serializers.SerializerMethodField()

    def get_stays(self, obj):
        """
        obj - экземпляр Room
        Возвращаем список проживаний в этом номере с вложенными данными клиента
        """
        # obj.stays - related_name="stays" у Stay.room
        # select_related("client") оптимизирует запросы (JOIN вместо N+1)
        stays = obj.stays.select_related("client")

        # Формируем список словарей вручную
        return [
            {
                "id": s.id,
                "check_in": s.check_in,
                "check_out": s.check_out,
                # Короткая информация о клиенте
                "client": ClientShortSerializer(s.client).data,
            }
            for s in stays
        ]

    class Meta:
        model = Room
        fields = "__all__"
