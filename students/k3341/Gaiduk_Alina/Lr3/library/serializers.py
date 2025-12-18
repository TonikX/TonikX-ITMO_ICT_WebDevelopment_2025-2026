"""
Serializers for library API.
"""
from rest_framework import serializers
from django.utils import timezone
from django.conf import settings
from .models import (
    Author, Publisher, BookSection, Book,
    Hall, Reader, BookCopy, BookIssue, HallBookStock, Staff
)

class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора."""
    class Meta:
        model = Author
        fields = ['author_id', 'full_name', 'created_at', 'updated_at']
        read_only_fields = ['author_id', 'created_at', 'updated_at']


class PublisherSerializer(serializers.ModelSerializer):
    """Сериализатор для издательства."""
    
    class Meta:
        model = Publisher
        fields = ['publisher_id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['publisher_id', 'created_at', 'updated_at']


class BookSectionSerializer(serializers.ModelSerializer):
    """Сериализатор для раздела книги."""
    
    class Meta:
        model = BookSection
        fields = ['section_id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['section_id', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги."""
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'book_id', 'title', 'publisher', 'publisher_name',
            'publish_year', 'section', 'section_name',
            'cipher', 'authors', 'created_at', 'updated_at'
        ]
        read_only_fields = ['book_id', 'created_at', 'updated_at']


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления книги с авторами."""
    author_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text='Список ID авторов'
    )
    
    class Meta:
        model = Book
        fields = [
            'book_id', 'title', 'publisher', 'publish_year',
            'section', 'cipher', 'author_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['book_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Создание книги с авторами."""
        # Извлекаем id авторов и удаляем это поле
        author_ids = validated_data.pop('author_ids', [])
        book = Book.objects.create(**validated_data)
        
        if author_ids:
            authors = Author.objects.filter(author_id__in=author_ids)
            if authors.count() != len(author_ids):
                raise serializers.ValidationError('Некоторые авторы не найдены.')
            
            # Используем SQL для создания связей, так как в таблице нет поля id
            from django.db import connection
            for author in authors:
                try:
                    with connection.cursor() as cursor:
                        # Проверяем существование связи
                        cursor.execute(
                            "SELECT COUNT(*) FROM book_author WHERE book_id = %s AND author_id = %s",
                            [book.book_id, author.author_id]
                        )
                        exists = cursor.fetchone()[0] > 0
                        
                        if not exists:
                            # Создаём связь через raw SQL
                            cursor.execute(
                                "INSERT INTO book_author (book_id, author_id, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())",
                                [book.book_id, author.author_id]
                            )
                except Exception:
                    # Связь уже существует или другая ошибка - пропускаем
                    pass
        
        return book
    
    def update(self, instance, validated_data):
        """Обновление книги с авторами."""
        author_ids = validated_data.pop('author_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if author_ids is not None:
            # Удаляем старые связи через raw SQL
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM book_author WHERE book_id = %s",
                    [instance.book_id]
                )
            
            # Создаём новые связи
            if author_ids:
                authors = Author.objects.filter(author_id__in=author_ids)
                if authors.count() != len(author_ids):
                    raise serializers.ValidationError('Некоторые авторы не найдены.')
                
                # Используем raw SQL для создания связей
                for author in authors:
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO book_author (book_id, author_id, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())",
                                [instance.book_id, author.author_id]
                            )
                    except Exception:
                        # Игнорируем ошибки
                        pass
        
        return instance


class HallSerializer(serializers.ModelSerializer):
    """Сериализатор для читального зала."""
    
    class Meta:
        model = Hall
        fields = ['hall_id', 'hall_number', 'name', 'capacity', 'created_at', 'updated_at']
        read_only_fields = ['hall_id', 'created_at', 'updated_at']


class ReaderSerializer(serializers.ModelSerializer):
    """Сериализатор для читателя."""
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    age = serializers.SerializerMethodField()
    registration_date = serializers.DateField(read_only=True)
    
    class Meta:
        model = Reader
        fields = [
            'reader_id', 'card_number', 'full_name', 'passport_number',
            'birth_date', 'age', 'address', 'phone', 'education_level',
            'has_academic_degree', 'hall', 'hall_name', 'registration_date',
            'last_reregistration_date', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'reader_id', 'registration_date',
            'created_at', 'updated_at'
        ]
    
    def get_age(self, obj) -> int:
        """Вычисление возраста читателя."""
        today = timezone.now().date()
        return today.year - obj.birth_date.year - (
            (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day)
        )


class BookCopySerializer(serializers.ModelSerializer):
    """Сериализатор для экземпляра книги."""
    book_title = serializers.CharField(source='book.title', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    registration_date = serializers.DateField(read_only=True)
    
    class Meta:
        model = BookCopy
        fields = [
            'copy_id', 'book', 'book_title', 'hall', 'hall_name',
            'inventory_number', 'registration_date', 'writeoff_date',
            'is_written_off', 'created_at', 'updated_at'
        ]
        read_only_fields = ['copy_id', 'registration_date', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Валидация: если is_written_off=True, то writeoff_date обязателен."""
        is_written_off = data.get('is_written_off', self.instance.is_written_off if self.instance else False)
        writeoff_date = data.get('writeoff_date', self.instance.writeoff_date if self.instance else None)
        
        if is_written_off and not writeoff_date:
            raise serializers.ValidationError({
                'writeoff_date': 'Дата списания обязательна для списанных книг.'
            })
        if not is_written_off and writeoff_date:
            raise serializers.ValidationError({
                'is_written_off': 'Книга должна быть помечена как списанная, если указана дата списания.'
            })
        
        return data


class BookIssueSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи книги."""
    reader_name = serializers.CharField(source='reader.full_name', read_only=True)
    reader_card = serializers.CharField(source='reader.card_number', read_only=True)
    book_title = serializers.CharField(source='copy.book.title', read_only=True)
    copy_inventory = serializers.CharField(source='copy.inventory_number', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    is_returned = serializers.SerializerMethodField()
    issue_date = serializers.DateField(read_only=True)
    return_date = serializers.DateField(required=False, allow_null=True)
    
    class Meta:
        model = BookIssue
        fields = [
            'issue_id', 'reader', 'reader_name', 'reader_card',
            'copy', 'copy_inventory', 'book_title', 'hall', 'hall_name',
            'issue_date', 'return_date', 'is_returned', 'created_at', 'updated_at'
        ]
        read_only_fields = ['issue_id', 'issue_date', 'created_at', 'updated_at']
    
    def get_is_returned(self, obj) -> bool:
        """Проверка, возвращена ли книга."""
        return obj.return_date is not None
    
    def validate(self, data):
        """Валидация: return_date должен быть >= issue_date."""
        return_date = data.get('return_date')
        issue_date = data.get('issue_date', self.instance.issue_date if self.instance else timezone.now().date())
        
        if return_date and return_date < issue_date:
            raise serializers.ValidationError({
                'return_date': 'Дата возврата не может быть раньше даты выдачи.'
            })
        
        return data


class HallBookStockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада книг в зале."""
    book_title = serializers.CharField(source='book.title', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    
    class Meta:
        model = HallBookStock
        fields = [
            'id', 'hall', 'hall_name', 'book', 'book_title',
            'copies_total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудника (без пароля)."""
    
    class Meta:
        model = Staff
        fields = ['staff_id', 'login', 'email', 'created_at', 'updated_at']
        read_only_fields = ['staff_id', 'created_at', 'updated_at']


class StaffCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания сотрудника с паролем."""
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = Staff
        fields = ['staff_id', 'login', 'email', 'password', 'created_at', 'updated_at']
        read_only_fields = ['staff_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Создание сотрудника с хешированием пароля."""
        from django.contrib.auth.hashers import make_password
        password = validated_data.pop('password')
        validated_data['password_hash'] = make_password(password)
        return Staff.objects.create(**validated_data)


class StaffRegistrationSerializer(StaffCreateSerializer):
    """Сериализатор для регистрации сотрудника с секретным ключом."""
    registration_key = serializers.CharField(write_only=True, min_length=1)
    
    class Meta(StaffCreateSerializer.Meta):
        fields = StaffCreateSerializer.Meta.fields + ['registration_key']
        read_only_fields = StaffCreateSerializer.Meta.read_only_fields
    
    def validate_registration_key(self, value):
        expected = settings.STAFF_REGISTRATION_KEY or ''
        if not expected:
            raise serializers.ValidationError('Регистрация сотрудников временно отключена.')
        if value != expected:
            raise serializers.ValidationError('Неверный секретный ключ.')
        return value
    
    def create(self, validated_data):
        validated_data.pop('registration_key', None)
        return super().create(validated_data)


class StaffLoginSerializer(serializers.Serializer):
    """Сериализатор для входа сотрудника."""
    login = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class BookAcceptSerializer(serializers.Serializer):
    """Сериализатор для принятия книги в фонд библиотеки.
    Если книги нет, создаёт её. Затем создаёт экземпляр книги."""
    # Поля для книги (если нужно создать новую)
    book_id = serializers.IntegerField(required=False, allow_null=True, help_text='ID существующей книги. Если не указан, будет создана новая книга.')
    title = serializers.CharField(max_length=200, required=False, help_text='Название книги (обязательно, если book_id не указан)')
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), required=False, allow_null=True)
    publish_year = serializers.IntegerField(required=False, allow_null=True, min_value=1000)
    section = serializers.PrimaryKeyRelatedField(queryset=BookSection.objects.all(), required=False, allow_null=True)
    cipher = serializers.CharField(max_length=50, required=False, help_text='Шифр книги (обязательно, если book_id не указан)')
    author_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text='Список ID авторов (для новой книги)'
    )
    
    # Поля для экземпляра книги
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all(), required=True)
    inventory_number = serializers.CharField(max_length=50, required=True)
    
    def validate(self, attrs):
        """Валидация: либо book_id, либо данные для создания книги."""
        book_id = attrs.get('book_id')
        title = attrs.get('title')
        cipher = attrs.get('cipher')
        
        if book_id:
            # Проверяем, что книга существует
            try:
                Book.objects.get(book_id=book_id)
            except Book.DoesNotExist:
                raise serializers.ValidationError({
                    'book_id': 'Книга с указанным ID не найдена.'
                })
            # Если указан book_id, остальные поля книги игнорируются
        else:
            # Если book_id не указан, нужны title и cipher
            if not title:
                raise serializers.ValidationError({
                    'title': 'Поле title обязательно, если book_id не указан.'
                })
            if not cipher:
                raise serializers.ValidationError({
                    'cipher': 'Поле cipher обязательно, если book_id не указан.'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Создание или получение книги, затем создание экземпляра."""
        book_id = validated_data.get('book_id')
        hall = validated_data['hall']
        inventory_number = validated_data['inventory_number']
        
        # Проверяем уникальность инвентарного номера
        if BookCopy.objects.filter(inventory_number=inventory_number).exists():
            raise serializers.ValidationError({
                'inventory_number': 'Экземпляр с таким инвентарным номером уже существует.'
            })
        
        # Получаем или создаём книгу
        if book_id:
            book = Book.objects.get(book_id=book_id)
        else:
            # Создаём новую книгу
            book_data = {
                'title': validated_data['title'],
                'cipher': validated_data['cipher'],
                'publisher': validated_data.get('publisher'),
                'publish_year': validated_data.get('publish_year'),
                'section': validated_data.get('section'),
            }
            book = Book.objects.create(**book_data)
            
            # Добавляем авторов, если указаны
            author_ids = validated_data.get('author_ids', [])
            if author_ids:
                authors = Author.objects.filter(author_id__in=author_ids)
                if authors.count() != len(author_ids):
                    raise serializers.ValidationError('Некоторые авторы не найдены.')
                
                # Используем raw SQL для создания связей, так как в таблице нет поля id
                from django.db import connection
                for author in authors:
                    try:
                        with connection.cursor() as cursor:
                            # Проверяем существование связи
                            cursor.execute(
                                "SELECT COUNT(*) FROM book_author WHERE book_id = %s AND author_id = %s",
                                [book.book_id, author.author_id]
                            )
                            exists = cursor.fetchone()[0] > 0
                            
                            if not exists:
                                # Создаём связь через raw SQL
                                cursor.execute(
                                    "INSERT INTO book_author (book_id, author_id, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())",
                                    [book.book_id, author.author_id]
                                )
                    except Exception:
                        # Связь уже существует или другая ошибка - пропускаем
                        pass
        
        # Создаём экземпляр книги
        copy = BookCopy.objects.create(
            book=book,
            hall=hall,
            inventory_number=inventory_number
        )
        
        # Обновляем или создаём запись на складе через raw SQL
        from django.db import connection
        with connection.cursor() as cursor:
            # Проверяем существование записи
            cursor.execute(
                "SELECT COUNT(*) FROM hall_book_stock WHERE hall_id = %s AND book_id = %s",
                [hall.hall_id, book.book_id]
            )
            exists = cursor.fetchone()[0] > 0
            
            if exists:
                # Обновляем количество
                cursor.execute(
                    "UPDATE hall_book_stock SET copies_total = copies_total + 1, updated_at = NOW() WHERE hall_id = %s AND book_id = %s",
                    [hall.hall_id, book.book_id]
                )
            else:
                # Создаём новую запись
                cursor.execute(
                    "INSERT INTO hall_book_stock (hall_id, book_id, copies_total, created_at, updated_at) VALUES (%s, %s, 1, NOW(), NOW())",
                    [hall.hall_id, book.book_id]
                )
        
        return copy

