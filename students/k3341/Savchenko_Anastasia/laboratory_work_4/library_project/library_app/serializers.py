from rest_framework import serializers
from .models import *

from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = tuple(UserSerializer.Meta.fields) + ('is_staff', 'is_superuser')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = '__all__'


class ReadingHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingHall
        fields = '__all__'


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'
        read_only_fields = [
            'library_card_id',
            'first_registered_at',
            'reader_id'
        ]
        # last_registration_at НЕ только для чтения - можно обновлять при перерегистрации
        extra_kwargs = {
            'is_active_member': {'default': True},
        }


class CopyOfBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopyOfBook
        fields = '__all__'


class LoanRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRecord
        fields = '__all__'


