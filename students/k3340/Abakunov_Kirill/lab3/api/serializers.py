"""
Сериализаторы для REST API
"""
from rest_framework import serializers
from django.db import models
from django.utils import timezone
from .models import Room, Guest, Staff, CleaningSchedule


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для номеров"""
    
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    is_available = serializers.SerializerMethodField()
    current_guests_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'number', 'room_type', 'room_type_display', 
            'floor', 'phone', 'price_per_day', 'is_available',
            'current_guests_count'
        ]
    
    def get_is_available(self, obj):
        """Проверка доступности номера"""
        return obj.is_available()
    
    def get_current_guests_count(self, obj):
        """Количество текущих гостей"""
        today = timezone.now().date()
        return obj.guests.filter(
            check_in_date__lte=today
        ).filter(
            models.Q(check_out_date__isnull=True) | 
            models.Q(check_out_date__gte=today)
        ).count()


class GuestSerializer(serializers.ModelSerializer):
    """Сериализатор для клиентов"""
    
    full_name = serializers.CharField(read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    room_number = serializers.CharField(source='room.number', read_only=True)
    
    class Meta:
        model = Guest
        fields = [
            'id', 'passport_number', 'last_name', 'first_name', 
            'middle_name', 'full_name', 'city', 'room', 'room_number',
            'check_in_date', 'check_out_date', 'is_current'
        ]
    
    def validate(self, data):
        """Валидация данных гостя"""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_out and check_in and check_in > check_out:
            raise serializers.ValidationError(
                "Дата выселения не может быть раньше даты заселения"
            )
        
        # Проверка доступности номера
        room = data.get('room')
        if room and check_in:
            # При обновлении исключаем текущего гостя
            instance_id = self.instance.id if self.instance else None
            
            overlapping_guests = Guest.objects.filter(
                room=room,
                check_in_date__lte=check_out if check_out else check_in,
            ).filter(
                models.Q(check_out_date__isnull=True) | 
                models.Q(check_out_date__gte=check_in)
            )
            
            if instance_id:
                overlapping_guests = overlapping_guests.exclude(id=instance_id)
            
            if overlapping_guests.exists():
                raise serializers.ValidationError(
                    f"Номер {room.number} занят в указанный период"
                )
        
        return data


class GuestCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания клиента (поселение)"""
    
    class Meta:
        model = Guest
        fields = [
            'passport_number', 'last_name', 'first_name', 
            'middle_name', 'city', 'room', 'check_in_date'
        ]


class GuestCheckOutSerializer(serializers.ModelSerializer):
    """Сериализатор для выселения клиента"""
    
    class Meta:
        model = Guest
        fields = ['check_out_date']
    
    def validate_check_out_date(self, value):
        """Валидация даты выселения"""
        if self.instance and value < self.instance.check_in_date:
            raise serializers.ValidationError(
                "Дата выселения не может быть раньше даты заселения"
            )
        return value


class CleaningScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для расписания уборки"""
    
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    
    class Meta:
        model = CleaningSchedule
        fields = [
            'id', 'staff', 'staff_name', 'floor', 
            'weekday', 'weekday_display'
        ]


class StaffSerializer(serializers.ModelSerializer):
    """Сериализатор для служащих"""
    
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'last_name', 'first_name', 'middle_name', 
            'full_name', 'is_active', 'hire_date', 'fire_date'
        ]
    
    def validate(self, data):
        """Валидация данных служащего"""
        hire_date = data.get('hire_date')
        fire_date = data.get('fire_date')
        
        if fire_date and hire_date and hire_date > fire_date:
            raise serializers.ValidationError(
                "Дата увольнения не может быть раньше даты приема на работу"
            )
        
        return data


class StaffCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для приема служащего на работу"""
    
    class Meta:
        model = Staff
        fields = [
            'last_name', 'first_name', 'middle_name', 'hire_date'
        ]


class StaffFireSerializer(serializers.ModelSerializer):
    """Сериализатор для увольнения служащего"""
    
    class Meta:
        model = Staff
        fields = ['fire_date']
    
    def validate_fire_date(self, value):
        """Валидация даты увольнения"""
        if self.instance and value < self.instance.hire_date:
            raise serializers.ValidationError(
                "Дата увольнения не может быть раньше даты приема на работу"
            )
        return value
