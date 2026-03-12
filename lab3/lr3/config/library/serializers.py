from rest_framework import serializers
from .models import Hall, Book, Reader, BookIssue, BookInHall


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookInHallSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    authors = serializers.CharField(source='book.authors', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)

    class Meta:
        model = BookInHall
        fields = '__all__'
        extra_kwargs = {
            'book': {'required': False},
        }

    def validate(self, attrs):
        instance = self.instance
        hall = attrs.get('hall') or (instance.hall if instance else None)
        book = attrs.get('book') or (instance.book if instance else None)

        if not hall or not book:
            return attrs

        qs = BookInHall.objects.filter(hall=hall)
        if instance:
            qs = qs.exclude(pk=instance.pk)

        current_count = qs.count()

        if hall.capacity is not None and current_count >= hall.capacity and not instance:
            raise serializers.ValidationError({
                'hall': 'В этом зале достигнута максимальная вместимость по разным книгам.'
            })

        if hall.capacity is not None and current_count >= hall.capacity and instance and hall != instance.hall:
            raise serializers.ValidationError({
                'hall': 'В выбранном зале уже достигнута максимальная вместимость по разным книгам.'
            })

        return attrs


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'


class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    reader_name = serializers.CharField(source='reader.full_name', read_only=True)

    class Meta:
        model = BookIssue
        fields = '__all__'
        extra_kwargs = {'book': {'required': False}}

    def validate(self, attrs):
        if not attrs.get('book') and not attrs.get('book_in_hall'):
            raise serializers.ValidationError({'book_in_hall': 'Укажите книгу в зале или книгу.'})
        if attrs.get('book_in_hall') and 'book' not in attrs:
            attrs['book'] = attrs['book_in_hall'].book
        return attrs

    def create(self, validated_data):
        book_in_hall = validated_data.get('book_in_hall')
        if book_in_hall and not validated_data.get('book'):
            validated_data['book'] = book_in_hall.book
        return super().create(validated_data)