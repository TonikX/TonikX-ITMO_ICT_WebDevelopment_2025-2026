from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    SecurityCompany, Category, Service, ServiceCategory,
    ServiceDiscount, ServiceRequest, Review, UserFavorite
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'surname', 'patronymic',
            'is_staff', 'is_superuser', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_staff', 'is_superuser', 'is_active', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SecurityCompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = SecurityCompany
        fields = [
            'id', 'user', 'user_id', 'name', 'description',
            'logo', 'website', 'average_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'average_rating']


class ServiceDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDiscount
        fields = [
            'id', 'service', 'discount_percent',
            'start_date', 'end_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    security_company = SecurityCompanySerializer(read_only=True)
    security_company_id = serializers.PrimaryKeyRelatedField(
        queryset=SecurityCompany.objects.all(),
        source='security_company',
        write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='categories',
        many=True,
        write_only=True,
        required=False
    )
    discounts = ServiceDiscountSerializer(many=True, read_only=True)
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Service
        fields = [
            'id', 'security_company', 'security_company_id',
            'name', 'description', 'price', 'current_price',
            'categories', 'category_ids', 'discounts',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'current_price']


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(required=True)

    class Meta:
        model = ServiceRequest
        fields = ['service_id', 'description']

    def validate_service_id(self, value):
        if not Service.objects.filter(id=value).exists():
            raise serializers.ValidationError("Услуга не найдена")
        return value

    def create(self, validated_data):
        service_id = validated_data.pop('service_id')
        service = Service.objects.get(id=service_id)

        validated_data['service'] = service

        return super().create(validated_data)


class ServiceRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceRequest
        fields = ['description']


class ServiceRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'user', 'user_id', 'service', 'service_id',
            'description', 'status', 'admin_comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'admin_comment']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    security_company = SecurityCompanySerializer(read_only=True)
    security_company_id = serializers.PrimaryKeyRelatedField(
        queryset=SecurityCompany.objects.all(),
        source='security_company',
        write_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_id', 'security_company', 'security_company_id',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['created_at']


class UserFavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )

    class Meta:
        model = UserFavorite
        fields = ['id', 'user', 'user_id', 'service', 'service_id', 'created_at']
        read_only_fields = ['created_at']


# Упрощенные сериализаторы для вложенных представлений
class SimpleServiceSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'current_price', 'description']


# Специфичные сериализаторы
class ServiceWithCompanySerializer(ServiceSerializer):
    """Сериализатор услуги с полной информацией о компании"""
    security_company = SecurityCompanySerializer(read_only=True)


class CompanyWithServicesSerializer(SecurityCompanySerializer):
    """Сериализатор компании со списком услуг"""
    services = SimpleServiceSerializer(many=True, read_only=True)


    class Meta(SecurityCompanySerializer.Meta):
        fields = SecurityCompanySerializer.Meta.fields + ['services']

class AnalyticsSerializer(serializers.Serializer):
    pass
