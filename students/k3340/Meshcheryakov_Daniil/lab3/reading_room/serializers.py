from rest_framework import serializers
from .models import ReadingRoom, Reader, Reservation, Librarian, Schedule


# Сериализатор для читальных залов
# Преобразует модель ReadingRoom в JSON для API
# Добавляет читаемое отображение типа зала (малый/средний/большой)
class ReadingRoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    
    class Meta:
        model = ReadingRoom
        fields = ['id', 'number', 'floor', 'room_type', 'room_type_display', 'capacity', 'hourly_rate', 'description']


# Сериализатор для читателей
# Преобразует модель Reader в JSON для API
# Содержит данные читательского билета и контактную информацию
class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ['id', 'library_card', 'last_name', 'first_name', 'patronymic', 'phone', 'email']


# Сериализатор для бронирований
# Преобразует модель Reservation в JSON для API
# Добавляет читаемые имена читателей и номера залов для удобства
class ReservationSerializer(serializers.ModelSerializer):
    reader_name = serializers.CharField(source='reader.__str__', read_only=True)
    reading_room_number = serializers.IntegerField(source='reading_room.number', read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'reader', 'reader_name', 'reading_room', 'reading_room_number', 'reserved_from', 'reserved_to', 'is_active']


# Сериализатор для библиотекарей
# Преобразует модель Librarian в JSON для API
# Включает статус активности библиотекаря
class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ['id', 'last_name', 'first_name', 'patronymic', 'is_active']


# Сериализатор для расписания работы библиотекарей
# Преобразует модель Schedule в JSON для API
# Добавляет читаемые имена библиотекарей и дни недели
class ScheduleSerializer(serializers.ModelSerializer):
    librarian_name = serializers.CharField(source='librarian.__str__', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'librarian', 'librarian_name', 'weekday', 'weekday_display', 'floor']


# ===== ВСПОМОГАТЕЛЬНЫЕ СЕРИАЛИЗАТОРЫ ДЛЯ СПЕЦИАЛЬНЫХ ОТВЕТОВ =====

# Упрощенный сериализатор читателей для списков
# Используется когда нужны только основные данные читателя без дополнительной информации
class ReaderListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = [
            "id",
            "library_card",
            "last_name",
            "first_name",
            "patronymic",
            "phone",
            "email",
        ]


# Сериализатор для подсчета количества читателей в зале
# Используется в аналитических запросах для статистики по залам
class ReadingRoomReadersCountSerializer(serializers.Serializer):
    reading_room = serializers.IntegerField()
    readers = serializers.IntegerField()


# Сериализатор для дохода по залу
# Используется в отчетах для отображения прибыльности каждого зала
class ReadingRoomIncomeSerializer(serializers.Serializer):
    reading_room = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)


# Сериализатор для общих показателей читального зала
# Используется в дашборде для отображения общей статистики доходов
class ReadingRoomTotalsSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=14, decimal_places=2)

