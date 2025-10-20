from rest_framework import serializers
from .models import Room, Client, Stay, Employee, EmployeeSchedule


# Сериализатор для номеров гостиницы
# Преобразует модель Room в JSON для API
# Добавляет читаемое отображение типа номера (одноместный/двухместный/трехместный)
class RoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'room_type', 'room_type_display', 'daily_rate', 'phone']


# Сериализатор для клиентов гостиницы
# Преобразует модель Client в JSON для API
# Содержит паспортные данные и контактную информацию
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'passport_number', 'last_name', 'first_name', 'patronymic', 'city']


# Сериализатор для проживаний клиентов
# Преобразует модель Stay в JSON для API
# Добавляет читаемые имена клиентов и номера комнат для удобства
class StaySerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.__str__', read_only=True)
    room_number = serializers.IntegerField(source='room.number', read_only=True)
    
    class Meta:
        model = Stay
        fields = ['id', 'client', 'client_name', 'room', 'room_number', 'check_in', 'check_out']


# Сериализатор для сотрудников гостиницы
# Преобразует модель Employee в JSON для API
# Включает статус активности сотрудника
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'last_name', 'first_name', 'patronymic', 'is_active']


# Сериализатор для расписания работы сотрудников
# Преобразует модель EmployeeSchedule в JSON для API
# Добавляет читаемые имена сотрудников и дни недели
class EmployeeScheduleSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.__str__', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = EmployeeSchedule
        fields = ['id', 'employee', 'employee_name', 'weekday', 'weekday_display', 'floor']


# ===== ВСПОМОГАТЕЛЬНЫЕ СЕРИАЛИЗАТОРЫ ДЛЯ СПЕЦИАЛЬНЫХ ОТВЕТОВ =====

# Упрощенный сериализатор клиентов для списков
# Используется когда нужны только основные данные клиента без дополнительной информации
class ClientListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "passport_number",
            "last_name",
            "first_name",
            "patronymic",
            "city",
        ]


# Сериализатор для подсчета количества клиентов в номере
# Используется в аналитических запросах для статистики по номерам
class RoomClientsCountSerializer(serializers.Serializer):
    room = serializers.IntegerField()
    clients = serializers.IntegerField()


# Сериализатор для дохода по номеру
# Используется в отчетах для отображения прибыльности каждого номера
class RoomIncomeSerializer(serializers.Serializer):
    room = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)


# Сериализатор для общих показателей гостиницы
# Используется в дашборде для отображения общей статистики доходов
class HotelTotalsSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=14, decimal_places=2)

