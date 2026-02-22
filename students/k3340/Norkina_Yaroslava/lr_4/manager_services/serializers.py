from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'phone', 'password')

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'phone', 'role', 'date_joined')


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Service, File, Order, OrderStatusHistory, Comment, Review
from django.utils import timezone

User = get_user_model()


class ServiceListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка услуг (публичный)"""
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration',
                  'category', 'primary_image', 'created_at']
        read_only_fields = ['created_at']

    def get_primary_image(self, obj):
        """Получить главное изображение услуги"""
        primary_file = obj.files.filter(is_primary=True).first()
        if primary_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_file.file_path)
            return primary_file.file_path
        return None


class ServiceDetailSerializer(ServiceListSerializer):
    """Сериализатор для деталей услуги (публичный)"""
    images = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta(ServiceListSerializer.Meta):
        fields = ServiceListSerializer.Meta.fields + [
            'images', 'review_count', 'average_rating'
        ]

    def get_images(self, obj):
        """Получить все изображения услуги"""
        files = obj.files.all().order_by('display_order')
        request = self.context.get('request')
        return [
            {
                'id': file.id,
                'url': request.build_absolute_uri(file.file_path) if request else file.file_path,
                'alt_text': file.alt_text,
                'is_primary': file.is_primary
            }
            for file in files
        ]

    def get_review_count(self, obj):
        """Количество опубликованных отзывов"""
        return obj.reviews.filter(is_published=True).count()

    def get_average_rating(self, obj):
        """Средний рейтинг опубликованных отзывов"""
        published_reviews = obj.reviews.filter(is_published=True)
        if published_reviews.exists():
            return round(
                sum(review.rating for review in published_reviews) / published_reviews.count(),
                1
            )
        return None


class ServiceAdminSerializer(ServiceListSerializer):  # Изменено: наследуемся от ServiceListSerializer
    """Сериализатор для админской работы с услугами"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta(ServiceListSerializer.Meta):
        fields = ServiceListSerializer.Meta.fields + ['is_active', 'created_by', 'created_by_email',
                  'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        """При создании услуги автоматически устанавливаем создателя"""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class FileSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов (админ)"""
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'service', 'service_name', 'file_name', 'file_url',
                  'file_path', 'file_size', 'mime_type', 'is_primary',
                  'display_order', 'uploaded_by', 'uploaded_by_email',
                  'uploaded_at', 'alt_text']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'file_path',
                            'file_size', 'mime_type']

    def get_file_url(self, obj):
        """Полный URL к файлу"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file_path)
        return obj.file_path

    def validate(self, data):
        """Проверка, что только один файл может быть главным"""
        if data.get('is_primary', False):
            service = data.get('service') or self.instance.service
            # Если это обновление, исключаем текущий файл из проверки
            if self.instance:
                other_primary = File.objects.filter(
                    service=service,
                    is_primary=True
                ).exclude(id=self.instance.id).exists()
            else:
                other_primary = File.objects.filter(
                    service=service,
                    is_primary=True
                ).exists()

            if other_primary:
                raise serializers.ValidationError({
                    'is_primary': 'У услуги уже есть главное изображение'
                })
        return data

    def create(self, validated_data):
        """При создании файла автоматически устанавливаем загрузившего"""
        user = self.context['request'].user
        validated_data['uploaded_by'] = user
        return super().create(validated_data)


class FileUploadSerializer(serializers.Serializer):
    """Сериализатор для загрузки файлов"""
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    file = serializers.FileField()
    alt_text = serializers.CharField(max_length=255, required=False, allow_blank=True)
    is_primary = serializers.BooleanField(default=False)
    display_order = serializers.IntegerField(default=0, min_value=0)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    admin_email = serializers.EmailField(source='admin.email', read_only=True)
    admin_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'order', 'admin', 'admin_email', 'admin_full_name',
                  'content', 'created_at', 'is_visible_to_user']
        read_only_fields = ['admin', 'created_at']

    def get_admin_full_name(self, obj):
        return obj.admin.get_full_name()

    def create(self, validated_data):
        """При создании комментария автоматически устанавливаем администратора"""
        user = self.context['request'].user
        validated_data['admin'] = user
        return super().create(validated_data)


class CommentVisibilitySerializer(serializers.ModelSerializer):
    """Сериализатор для изменения видимости комментария"""

    class Meta:
        model = Comment
        fields = ['is_visible_to_user']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""

    class Meta:
        model = Review
        fields = ['order', 'service', 'rating', 'title', 'content']
        read_only_fields = ['user', 'is_verified', 'is_published']

    def validate(self, data):
        """Проверка возможности оставить отзыв"""
        user = self.context['request'].user
        order = data['order']
        service = data['service']

        # Проверка, что заявка принадлежит пользователю
        if order.user != user:
            raise serializers.ValidationError({
                'order': 'Эта заявка не принадлежит вам'
            })

        # Проверка, что заявка завершена
        if order.status != Order.Status.COMPLETED:
            raise serializers.ValidationError({
                'order': 'Отзыв можно оставить только к завершенной заявке'
            })

        # Проверка, что услуга в заявке соответствует выбранной услуге
        if order.service != service:
            raise serializers.ValidationError({
                'service': 'Услуга в заявке не соответствует выбранной услуге'
            })

        # Проверка, что отзыв еще не оставляли
        if Review.objects.filter(order=order).exists():
            raise serializers.ValidationError({
                'order': 'Вы уже оставляли отзыв к этой заявке'
            })

        return data

    def create(self, validated_data):
        """При создании отзыва автоматически устанавливаем пользователя"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка отзывов (публичный)"""
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_full_name', 'rating', 'title', 'content',
                  'created_at', 'is_verified']
        read_only_fields = ['created_at']

    def get_user_full_name(self, obj):
        # Показываем только инициалы для приватности
        full_name = obj.user.get_full_name()
        if full_name:
            parts = full_name.split()
            if len(parts) >= 2:
                return f"{parts[0]} {parts[1][0]}."
        return full_name


class ReviewDetailSerializer(ReviewListSerializer):
    """Сериализатор для деталей отзыва"""
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta(ReviewListSerializer.Meta):
        fields = ReviewListSerializer.Meta.fields + ['service_name', 'updated_at']


class ReviewAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админской работы с отзывами"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_email',
                  'service', 'service_name', 'order_id', 'rating',
                  'title', 'content', 'is_verified', 'is_published',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'service', 'order', 'created_at', 'updated_at']


class UserAdminListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей (админ)"""
    order_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone',
                  'role', 'date_joined', 'order_count', 'review_count']

    def get_order_count(self, obj):
        return obj.orders.count()

    def get_review_count(self, obj):
        return obj.reviews.count()


class UserAdminDetailSerializer(UserAdminListSerializer):
    """Сериализатор для деталей пользователя (админ)"""

    class Meta(UserAdminListSerializer.Meta):
        fields = UserAdminListSerializer.Meta.fields + ['last_login']


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения роли пользователя"""

    class Meta:
        model = User
        fields = ['role']


class CategorySerializer(serializers.Serializer):
    """Сериализатор для категорий услуг"""
    name = serializers.CharField()
    service_count = serializers.IntegerField()


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки"""

    class Meta:
        model = Order
        fields = ['service', 'notes']

    def validate_service(self, value):
        """Проверка, что услуга активна"""
        if not value.is_active:
            raise serializers.ValidationError("Эта услуга временно недоступна")
        return value

    def create(self, validated_data):
        """При создании заявки автоматически устанавливаем пользователя"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заявок пользователя"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(
        source='service.price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'service', 'service_name', 'service_price',
                  'status', 'created_at', 'completed_at', 'comment_count']
        read_only_fields = ['status', 'created_at', 'completed_at']

    def get_comment_count(self, obj):
        """Количество видимых комментариев"""
        return obj.comments.filter(is_visible_to_user=True).count()


class OrderDetailSerializer(OrderListSerializer):
    """Сериализатор для деталей заявки"""
    service_details = ServiceListSerializer(source='service', read_only=True)
    visible_comments = serializers.SerializerMethodField()

    class Meta(OrderListSerializer.Meta):
        fields = OrderListSerializer.Meta.fields + [
            'notes', 'service_details', 'visible_comments'
        ]

    def get_visible_comments(self, obj):
        """Только видимые пользователю комментарии"""
        comments = obj.comments.filter(is_visible_to_user=True)
        return CommentSerializer(comments, many=True, context=self.context).data


class OrderAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админской работы с заявками"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name', read_only=True)
    all_comments = CommentSerializer(source='comments', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'user_full_name',
                  'service', 'service_name', 'status', 'notes',
                  'created_at', 'completed_at', 'all_comments']
        read_only_fields = ['user', 'service', 'created_at']

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Сериализатор для изменения статуса заявки"""
    status = serializers.ChoiceField(choices=Order.Status.choices)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_status(self, value):
        """Проверка валидности статуса"""
        order = self.context.get('order')
        if order and order.status == Order.Status.COMPLETED and value != Order.Status.COMPLETED:
            raise serializers.ValidationError(
                "Нельзя изменить статус завершенной заявки"
            )
        return value


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории статусов"""
    changed_by_email = serializers.EmailField(source='changed_by.email', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'old_status', 'new_status', 'changed_by',
                  'changed_by_email', 'changed_at', 'comment']
        read_only_fields = ['changed_by', 'changed_at']

class ReviewPublishSerializer(serializers.Serializer):
    """Сериализатор для публикации отзыва"""
    is_published = serializers.BooleanField(required=True)

class ReviewVerifySerializer(serializers.Serializer):
    """Сериализатор для подтверждения отзыва"""
    is_verified = serializers.BooleanField(required=True)