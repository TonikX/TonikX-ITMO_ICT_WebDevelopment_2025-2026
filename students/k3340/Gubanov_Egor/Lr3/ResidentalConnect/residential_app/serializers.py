from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Building, Apartment, ServiceCategory, ServiceRequest, MeterReading

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone_number', 'address',
            'birth_date', 'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'phone_number', 'address', 'birth_date'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class BuildingListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для Building (для вложенных объектов)"""
    
    class Meta:
        model = Building
        fields = ['id', 'address', 'total_floors', 'year_built']


class BuildingSerializer(serializers.ModelSerializer):
    """Полный сериализатор для Building"""
    
    class Meta:
        model = Building
        fields = [
            'id', 'address', 'total_floors', 'year_built',
            'total_apartments', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApartmentSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры"""
    building = BuildingListSerializer(read_only=True)
    building_id = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(),
        source='building',
        write_only=True
    )
    owner = CustomUserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owner',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Apartment
        fields = [
            'id', 'building', 'building_id', 'number', 'floor', 'area',
            'rooms', 'balance', 'owner', 'owner_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории услуг"""
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class ServiceRequestSerializer(serializers.ModelSerializer):
    """Сериализатор заявки"""
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    apartment = ApartmentSerializer(read_only=True)
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.all(),
        source='apartment',
        write_only=True
    )
    requester = CustomUserSerializer(read_only=True)
    requester_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='requester',
        write_only=True
    )
    worker = CustomUserSerializer(read_only=True)
    worker_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='worker',
        write_only=True,
        required=False,
        allow_null=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'title', 'description', 'status', 'status_display',
            'priority', 'priority_display', 'created_at', 'updated_at',
            'assigned_at', 'started_at', 'resolved_at', 'worker_comment',
            'category', 'category_id', 'apartment', 'apartment_id',
            'requester', 'requester_id', 'worker', 'worker_id'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'requester', 'worker',
            'assigned_at', 'started_at'
        ]


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки (без worker)"""
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        required=False,
        allow_null=True
    )
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.all(),
        source='apartment'
    )
    
    class Meta:
        model = ServiceRequest
        fields = [
            'title', 'description', 'priority', 'category_id', 'apartment_id'
        ]


# ========== СЕРИАЛИЗАТОРЫ СОГЛАСНО ТЗ ==========

class ServiceRequestBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор заявки (плоская структура для создания/обновления)"""
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.all(),
        source='apartment',
        write_only=True
    )
    requester_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='requester',
        write_only=True,
        required=False
    )
    worker_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='worker',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'category_id', 'apartment_id', 'requester_id', 'worker_id',
            'worker_comment', 'created_at', 'updated_at',
            'assigned_at', 'started_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RequestApartmentSerializer(serializers.ModelSerializer):
    """Сериализатор заявки с вложенным объектом квартиры"""
    apartment = ApartmentSerializer(read_only=True)
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.all(),
        source='apartment',
        write_only=True
    )
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'apartment', 'apartment_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RequestCategorySerializer(serializers.ModelSerializer):
    """Сериализатор заявки с вложенным объектом категории"""
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'category', 'category_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RequestDetailSerializer(serializers.ModelSerializer):
    """Полный сериализатор для детального просмотра заявки"""
    apartment = ApartmentSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    requester = CustomUserSerializer(read_only=True)
    worker = CustomUserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'title', 'description', 'status', 'status_display',
            'priority', 'priority_display', 'created_at', 'updated_at',
            'assigned_at', 'started_at', 'resolved_at', 'worker_comment',
            'apartment', 'category', 'requester', 'worker'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'assigned_at',
            'started_at', 'resolved_at', 'apartment', 'category',
            'requester', 'worker'
        ]


class MeterReadingSerializer(serializers.ModelSerializer):
    """Сериализатор показаний счетчика"""
    apartment = ApartmentSerializer(read_only=True)
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.all(),
        source='apartment',
        write_only=True
    )
    meter_type_display = serializers.CharField(source='get_meter_type_display', read_only=True)
    
    class Meta:
        model = MeterReading
        fields = [
            'id', 'apartment', 'apartment_id', 'meter_type',
            'meter_type_display', 'value', 'previous_value', 'consumption',
            'date_recorded', 'created_at'
        ]
        read_only_fields = ['id', 'date_recorded', 'created_at', 'consumption']
    
    def validate_value(self, value):
        """Валидация значения показаний"""
        if value < 0:
            raise serializers.ValidationError("Показания не могут быть отрицательными")
        return value
    
    def validate(self, data):
        """Валидация и расчет расхода"""
        value = data.get('value')
        previous_value = data.get('previous_value')
        
        if previous_value is not None and value is not None:
            if value < previous_value:
                raise serializers.ValidationError({
                    'value': 'Текущие показания не могут быть меньше предыдущих'
                })
            data['consumption'] = value - previous_value
        
        return data

