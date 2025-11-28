from rest_framework import viewsets, permissions

from .models import Author, Book, Contract, Customer, Order, BookAuthor, BookEditor, OrderItem
from .serializers import (
    AuthorSerializer, BookSerializer, ContractSerializer,
    CustomerSerializer, OrderSerializer, BookAuthorSerializer,
    BookEditorSerializer, OrderItemSerializer
)

DEFAULT_PERMISSION = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = DEFAULT_PERMISSION


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = DEFAULT_PERMISSION


class BookAuthorViewSet(viewsets.ModelViewSet):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer
    permission_classes = DEFAULT_PERMISSION


class BookEditorViewSet(viewsets.ModelViewSet):
    queryset = BookEditor.objects.all()
    serializer_class = BookEditorSerializer
    permission_classes = DEFAULT_PERMISSION


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = DEFAULT_PERMISSION


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = DEFAULT_PERMISSION


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = DEFAULT_PERMISSION


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = DEFAULT_PERMISSION
