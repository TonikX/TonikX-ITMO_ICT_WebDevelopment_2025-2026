from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Author, Book, Contract, Customer, Order, BookAuthor, BookEditor, OrderItem

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors_details = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'pages_count', 'has_illustrations', 'authors_details']

    def get_authors_details(self, obj):
        authors_links = BookAuthor.objects.filter(book=obj).order_by('order_position')
        return [
            {
                "author_name": link.author.full_name,
                "order": link.order_position
            }
            for link in authors_links
        ]


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ['id', 'book', 'author', 'order_position']


class BookEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEditor
        fields = ['id', 'book', 'editor', 'is_responsible']


class ContractSerializer(serializers.ModelSerializer):
    manager_details = UserSerializer(source='manager', read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
