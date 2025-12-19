from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    SecurityCompany, Category, Service, ServiceCategory,
    ServiceDiscount, ServiceRequest, Review, UserFavorite
)
from .mixins import CurrentDiscountMixin

User = get_user_model()


# =============== SIMPLE SERIALIZERS ===============
class SimpleReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    company_name = serializers.CharField(source='security_company.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'user_name', 'company_name', 'created_at']

    def get_user_name(self, obj):
        return f"{obj.user.name} {obj.user.surname}"


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'patronymic']


class SimpleSecurityCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityCompany
        fields = ['id', 'name', 'logo', 'website']


class SimpleUserFavoriteSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_company = serializers.CharField(source='service.security_company.name', read_only=True)
    service_price = serializers.DecimalField(
        source='service.price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = UserFavorite
        fields = ['id', 'service_name', 'service_company', 'service_price', 'created_at']


class SimpleServiceRequestSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    service_info = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'user_info', 'service_info',
            'description', 'status', 'admin_comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'name': f"{obj.user.name} {obj.user.surname}",
            'phone': getattr(obj.user, 'phone', None)
        }

    def get_service_info(self, obj):
        return {
            'id': obj.service.id,
            'name': obj.service.name,
            'price': str(obj.service.price),
            'current_price': str(obj.service.current_price)
            if hasattr(obj.service, 'current_price')
            else str(obj.service.price)
        }

class SimpleServiceSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    current_discount = serializers.SerializerMethodField()
    security_company = SimpleSecurityCompanySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'price', 'current_price',
            'description', 'security_company', 'current_discount'
        ]

    def get_current_discount(self, obj):
        return CurrentDiscountMixin().get_current_discount(obj)


class SimpleServiceDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDiscount
        fields = ['id', 'discount_percent', 'start_date', 'end_date']


# =============== USER SERIALIZERS ===============

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'surname', 'patronymic',
            'is_staff', 'is_superuser', 'is_active'
        ]
        read_only_fields = [
            'is_staff', 'is_superuser', 'is_active'
        ]


class CustomUserCreateSerializer(UserCreateSerializer):
    name = serializers.CharField(required=True, max_length=100)
    surname = serializers.CharField(required=True, max_length=100)
    patronymic = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + (
            'name', 'surname', 'patronymic', 're_password'
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise serializers.ValidationError({
                "password": "Пароли не совпадают"
            })
        attrs.pop('re_password', None)
        return super().validate(attrs)

    def create(self, validated_data):
        name = validated_data.pop('name', '')
        surname = validated_data.pop('surname', '')
        patronymic = validated_data.pop('patronymic', '')
        user = super().create(validated_data)

        user.name = name
        user.surname = surname
        user.patronymic = patronymic
        user.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    security_companies = SimpleSecurityCompanySerializer(read_only=True)
    favorites = SimpleUserFavoriteSerializer(many=True, read_only=True)
    service_requests = SimpleServiceRequestSerializer(many=True, read_only=True)
    reviews = SimpleReviewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'surname', 'patronymic',
            'is_staff', 'is_superuser', 'is_active',
            'security_companies', 'favorites', 'service_requests', 'reviews'
        ]
        read_only_fields = [
            'is_staff', 'is_superuser', 'is_active'
        ]


# =============== SECURITY COMPANY SERIALIZERS ===============

class SecurityCompanyListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    services_count = serializers.IntegerField(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = SecurityCompany
        fields = [
            'id', 'user', 'name', 'description', 'logo', 'website',
            'average_rating', 'services_count'
        ]
        read_only_fields = ['average_rating', 'services_count']


class SecurityCompanyDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    services = serializers.SerializerMethodField()
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = SecurityCompany
        fields = [
            'id', 'user', 'name', 'description', 'logo', 'website',
            'average_rating', 'services', 'reviews'
        ]
        read_only_fields = ['average_rating']

    def get_services(self, obj):
        services = obj.services.all()
        return ServiceWithDiscountSerializer(services, many=True, context=self.context).data


class SecurityCompanyMySerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    services = serializers.SerializerMethodField()
    reviews = SimpleReviewSerializer(many=True, read_only=True)
    service_requests = serializers.SerializerMethodField()

    class Meta:
        model = SecurityCompany
        fields = [
            'id', 'name', 'description', 'logo', 'website',
            'average_rating', 'services', 'reviews', 'service_requests'
        ]
        read_only_fields = ['average_rating']

    def get_services(self, obj):
        services = obj.services.all()
        return ServiceWithDiscountSerializer(services, many=True, context=self.context).data

    def get_service_requests(self, obj):
        requests = ServiceRequest.objects.filter(
            service__security_company=obj
        ).select_related('service', 'user')
        return SimpleServiceRequestSerializer(requests, many=True).data


class SecurityCompanyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityCompany
        fields = ['id', 'name', 'description', 'logo', 'website']
        read_only_fields = ['id']


# =============== SERVICE SERIALIZERS ===============

class ServiceWithDiscountSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    current_discount = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'price', 'current_price',
            'current_discount', 'description'
        ]

    def get_current_discount(self, obj):
        return CurrentDiscountMixin().get_current_discount(obj)


class ServiceSerializer(serializers.ModelSerializer):
    security_company = SimpleSecurityCompanySerializer(read_only=True)
    security_company_id = serializers.PrimaryKeyRelatedField(
        queryset=SecurityCompany.objects.all(),
        source='security_company',
        write_only=True
    )
    categories = serializers.SerializerMethodField()
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='categories',
        many=True,
        write_only=True,
        required=False
    )
    discounts = serializers.SerializerMethodField()
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    current_discount = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'security_company', 'security_company_id',
            'name', 'description', 'price', 'current_price',
            'categories', 'category_ids', 'discounts', 'current_discount'
        ]
        read_only_fields = ['current_price']

    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data

    def get_discounts(self, obj):
        discounts = obj.discounts.all()
        return ServiceDiscountSerializer(discounts, many=True).data

    def get_current_discount(self, obj):
        return CurrentDiscountMixin().get_current_discount(obj)


class ServiceListSerializer(serializers.ModelSerializer):
    security_company = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    current_discount = serializers.SerializerMethodField()
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price', 'current_price',
            'security_company', 'categories', 'current_discount'
        ]
        read_only_fields = ['current_price']

    def get_security_company(self, obj):
        return {
            'id': obj.security_company.id,
            'name': obj.security_company.name
        }

    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data

    def get_current_discount(self, obj):
        return CurrentDiscountMixin().get_current_discount(obj)


class ServiceDetailSerializer(serializers.ModelSerializer):
    security_company = SimpleSecurityCompanySerializer(read_only=True)
    categories = serializers.SerializerMethodField()
    current_discount = serializers.SerializerMethodField()
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price', 'current_price',
            'security_company', 'categories', 'current_discount'
        ]
        read_only_fields = ['current_price']

    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data

    def get_current_discount(self, obj):
        return CurrentDiscountMixin().get_current_discount(obj)


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='categories',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'category_ids']
        read_only_fields = ['id']


# =============== OTHER SERIALIZERS ===============

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ServiceDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDiscount
        fields = [
            'id', 'service', 'discount_percent',
            'start_date', 'end_date'
        ]


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(required=True)

    class Meta:
        model = ServiceRequest
        fields = ['service_id', 'description']

    def validate_service_id(self, value):
        """Проверка существования услуги"""
        if not Service.objects.filter(id=value).exists():
            raise serializers.ValidationError("Услуга не найдена")
        return value

    def create(self, validated_data):
        """Создание заявки с автоматическим назначением пользователя"""
        service_id = validated_data.pop('service_id')
        service = Service.objects.get(id=service_id)
        user = self.context['request'].user

        request_obj = ServiceRequest.objects.create(
            user=user,
            service=service,
            description=validated_data.get('description', ''),
            status='pending'
        )

        return request_obj


class ServiceRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceRequest
        fields = ['description', 'status', 'admin_comment']
        read_only_fields = []  # Все поля доступны для отправки

    def validate(self, data):
        """Валидация прав на изменение полей"""
        request = self.context['request']
        instance = self.instance
        user = request.user

        is_author = instance.user == user
        is_company_owner = (
                hasattr(instance.service, 'security_company') and
                instance.service.security_company.user == user
        )
        is_admin = user.is_staff

        updating_description = 'description' in data
        updating_status = 'status' in data
        updating_comment = 'admin_comment' in data

        if is_author:
            if updating_status:
                raise serializers.ValidationError({
                    'status': 'Вы не можете изменять статус своей заявки'
                })
            if updating_comment:
                raise serializers.ValidationError({
                    'admin_comment': 'Вы не можете добавлять комментарии к своей заявке'
                })
        elif is_company_owner:
            if updating_description:
                raise serializers.ValidationError({
                    'description': 'Вы можете изменять только статус и комментарий к заявкам на ваши услуги'
                })
            if updating_status:
                new_status = data['status']
                current_status = instance.status

                # Список допустимых переходов статусов
                allowed_transitions = {
                    'pending': ['confirmed', 'cancelled'],
                    'confirmed': ['in_progress', 'cancelled'],
                    'in_progress': ['completed', 'cancelled'],
                    'completed': [],
                    'cancelled': []
                }

                if new_status not in allowed_transitions.get(current_status, []):
                    raise serializers.ValidationError({
                        'status': f"Невозможно изменить статус с '{current_status}' на '{new_status}'"
                    })
        elif is_admin:
            if updating_status:
                new_status = data['status']
                current_status = instance.status
                allowed_transitions = {
                    'pending': ['confirmed', 'cancelled'],
                    'confirmed': ['in_progress', 'cancelled', 'pending'],
                    'in_progress': ['completed', 'cancelled', 'confirmed'],
                    'completed': ['in_progress'],  # можно вернуть в работу
                    'cancelled': ['pending']  # можно восстановить
                }

                if new_status not in allowed_transitions.get(current_status, []):
                    raise serializers.ValidationError({
                        'status': f"Невозможно изменить статус с '{current_status}' на '{new_status}'"
                    })

        else:
            errors = {}
            if updating_description:
                errors['description'] = 'Вы можете изменять только свои заявки'
            if updating_status:
                errors['status'] = 'Вы не можете изменять статус этой заявки'
            if updating_comment:
                errors['admin_comment'] = 'Вы не можете добавлять комментарии к этой заявке'

            if errors:
                raise serializers.ValidationError(errors)

        return data

    def update(self, instance, validated_data):
        # Обновляем только те поля, которые есть в validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ServiceRequestSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    service_info = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'user_info', 'service_info',
            'description', 'status', 'admin_comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'name': f"{obj.user.name} {obj.user.surname}"
        }

    def get_service_info(self, obj):
        return {
            'id': obj.service.id,
            'name': obj.service.name,
            'price': str(obj.service.price),
            'company': {
                'id': obj.service.security_company.id,
                'name': obj.service.security_company.name
            }
        }


class ReviewCreateSerializer(serializers.ModelSerializer):
    security_company_id = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ['security_company_id', 'rating', 'comment']

    def validate_security_company_id(self, value):
        if not SecurityCompany.objects.filter(id=value).exists():
            raise serializers.ValidationError("Компания не найдена")

        # Проверка, что отзыв еще не оставлен
        user = self.context['request'].user
        if Review.objects.filter(user=user, security_company_id=value).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв для этой компании")

        return value

    def create(self, validated_data):
        security_company_id = validated_data.pop('security_company_id')
        security_company = SecurityCompany.objects.get(id=security_company_id)
        user = self.context['request'].user

        review = Review.objects.create(
            user=user,
            security_company=security_company,
            rating=validated_data.get('rating'),
            comment=validated_data.get('comment', '')
        )
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):
    security_company_id = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ['security_company_id', 'rating', 'comment']

    def validate_security_company_id(self, value):
        if not SecurityCompany.objects.filter(id=value).exists():
            raise serializers.ValidationError("Компания не найдена")

        # Проверка, что у пользователя нет другого отзыва на эту компанию
        user = self.context['request'].user
        if Review.objects.filter(user=user, security_company_id=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("У вас уже есть отзыв для этой компании")

        return value

    def update(self, instance, validated_data):
        security_company_id = validated_data.get('security_company_id')
        if security_company_id:
            security_company = SecurityCompany.objects.get(id=security_company_id)
            instance.security_company = security_company

        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()

        return instance


class ReviewSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    security_company_info = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user_info', 'security_company_info',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'name': f"{obj.user.name} {obj.user.surname}"
        }

    def get_security_company_info(self, obj):
        return {
            'id': obj.security_company.id,
            'name': obj.security_company.name,
            'logo': obj.security_company.logo,
            'website': obj.security_company.website
        }


class UserFavoriteCreateSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(required=True)

    class Meta:
        model = UserFavorite
        fields = ['service_id']

    def validate_service_id(self, value):
        if not Service.objects.filter(id=value).exists():
            raise serializers.ValidationError("Услуга не найдена")

        # Проверка, что услуга уже не в избранном
        user = self.context['request'].user
        if UserFavorite.objects.filter(user=user, service_id=value).exists():
            raise serializers.ValidationError("Услуга уже в избранном")

        return value

    def create(self, validated_data):
        service_id = validated_data.pop('service_id')
        service = Service.objects.get(id=service_id)
        user = self.context['request'].user

        favorite = UserFavorite.objects.create(
            user=user,
            service=service
        )
        return favorite


class UserFavoriteSerializer(serializers.ModelSerializer):
    service_info = serializers.SerializerMethodField()

    class Meta:
        model = UserFavorite
        fields = ['id', 'service_info', 'created_at']
        read_only_fields = ['created_at']

    def get_service_info(self, obj):
        service_serializer = SimpleServiceSerializer(obj.service, context=self.context)

        # Получаем текущую скидку через метод сериализатора
        current_discount = service_serializer.get_current_discount(obj.service)

        return {
            'id': obj.service.id,
            'name': obj.service.name,
            'description': obj.service.description,
            'price': str(obj.service.price),
            'current_price': str(obj.service.current_price),
            'company': {
                'id': obj.service.security_company.id,
                'name': obj.service.security_company.name,
                'logo': obj.service.security_company.logo,
                'website': obj.service.security_company.website
            },
            'current_discount': current_discount
        }


class AnalyticsSerializer(serializers.Serializer):
    pass