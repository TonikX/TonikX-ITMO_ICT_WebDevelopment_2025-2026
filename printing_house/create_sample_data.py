#!/usr/bin/env python
"""
Скрипт для создания тестовых данных для системы типографии
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printing_house.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    Employee, Manager, Editor, Author, Book, Contract, ContractAuthor,
    BookEditor, Customer, Order, OrderItem, FinancialRecord
)


def create_sample_data():
    """Создание тестовых данных"""
    
    # Создание пользователей и сотрудников
    manager_user = User.objects.create_user(
        username='manager1',
        email='manager1@printing.com',
        password='password123',
        first_name='Иван',
        last_name='Петров'
    )
    manager = Manager.objects.create(
        user=manager_user,
        position='Менеджер по издательству',
        hire_date=date(2020, 1, 15),
        salary=Decimal('80000.00'),
        phone='+7-999-123-4567',
        address='г. Москва, ул. Тверская, д. 1',
        department='Издательский отдел'
    )
    
    # Редакторы
    editor1_user = User.objects.create_user(
        username='editor1',
        email='editor1@printing.com',
        password='password123',
        first_name='Анна',
        last_name='Смирнова'
    )
    editor1 = Editor.objects.create(
        user=editor1_user,
        position='Редактор',
        hire_date=date(2019, 3, 10),
        salary=Decimal('60000.00'),
        phone='+7-999-234-5678',
        address='г. Москва, ул. Арбат, д. 10',
        specialization='Художественная литература',
        experience_years=5
    )
    
    editor2_user = User.objects.create_user(
        username='editor2',
        email='editor2@printing.com',
        password='password123',
        first_name='Михаил',
        last_name='Козлов'
    )
    editor2 = Editor.objects.create(
        user=editor2_user,
        position='Редактор',
        hire_date=date(2021, 6, 1),
        salary=Decimal('55000.00'),
        phone='+7-999-345-6789',
        address='г. Москва, ул. Ленина, д. 5',
        specialization='Научная литература',
        experience_years=3
    )
    
    # Создание авторов
    author1 = Author.objects.create(
        first_name='Александр',
        last_name='Пушкин',
        birth_date=date(1799, 6, 6),
        biography='Великий русский поэт и писатель',
        contact_email='pushkin@example.com',
        contact_phone='+7-999-111-1111',
        address='г. Санкт-Петербург, наб. Мойки, д. 12'
    )
    
    author2 = Author.objects.create(
        first_name='Лев',
        last_name='Толстой',
        birth_date=date(1828, 9, 9),
        biography='Русский писатель и мыслитель',
        contact_email='tolstoy@example.com',
        contact_phone='+7-999-222-2222',
        address='г. Москва, ул. Льва Толстого, д. 21'
    )
    
    author3 = Author.objects.create(
        first_name='Фёдор',
        last_name='Достоевский',
        birth_date=date(1821, 11, 11),
        biography='Русский писатель, философ',
        contact_email='dostoevsky@example.com',
        contact_phone='+7-999-333-3333',
        address='г. Санкт-Петербург, ул. Достоевского, д. 2'
    )
    
    # Создание книг
    book1 = Book.objects.create(
        title='Евгений Онегин',
        isbn='9781234567890',
        publication_date=date(2023, 1, 15),
        pages=320,
        price=Decimal('450.00'),
        genre='Художественная литература',
        description='Роман в стихах Александра Пушкина'
    )
    
    book2 = Book.objects.create(
        title='Война и мир',
        isbn='9781234567891',
        publication_date=date(2023, 3, 20),
        pages=1274,
        price=Decimal('1200.00'),
        genre='Художественная литература',
        description='Роман-эпопея Льва Толстого'
    )
    
    book3 = Book.objects.create(
        title='Преступление и наказание',
        isbn='9781234567892',
        publication_date=date(2023, 5, 10),
        pages=671,
        price=Decimal('650.00'),
        genre='Художественная литература',
        description='Роман Фёдора Достоевского'
    )
    
    # Создание контрактов
    contract1 = Contract.objects.create(
        contract_number='CTR-2023-001',
        signing_date=date(2022, 12, 1),
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
        total_amount=Decimal('500000.00'),
        status='active',
        manager=manager,
        book=book1
    )
    
    contract2 = Contract.objects.create(
        contract_number='CTR-2023-002',
        signing_date=date(2022, 11, 15),
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
        total_amount=Decimal('800000.00'),
        status='active',
        manager=manager,
        book=book2
    )
    
    contract3 = Contract.objects.create(
        contract_number='CTR-2023-003',
        signing_date=date(2023, 2, 1),
        start_date=date(2023, 3, 1),
        end_date=date(2023, 12, 31),
        total_amount=Decimal('600000.00'),
        status='active',
        manager=manager,
        book=book3
    )
    
    # Связывание авторов с контрактами
    ContractAuthor.objects.create(
        contract=contract1,
        author=author1,
        order_on_cover=1,
        royalty_percentage=Decimal('15.00'),
        royalty_amount=Decimal('75000.00')
    )
    
    ContractAuthor.objects.create(
        contract=contract2,
        author=author2,
        order_on_cover=1,
        royalty_percentage=Decimal('12.00'),
        royalty_amount=Decimal('96000.00')
    )
    
    ContractAuthor.objects.create(
        contract=contract3,
        author=author3,
        order_on_cover=1,
        royalty_percentage=Decimal('10.00'),
        royalty_amount=Decimal('60000.00')
    )
    
    # Связывание редакторов с книгами
    BookEditor.objects.create(
        book=book1,
        editor=editor1,
        is_lead_editor=True,
        start_date=date(2022, 12, 1),
        end_date=date(2023, 1, 15)
    )
    
    BookEditor.objects.create(
        book=book2,
        editor=editor1,
        is_lead_editor=True,
        start_date=date(2022, 11, 15),
        end_date=date(2023, 3, 20)
    )
    
    BookEditor.objects.create(
        book=book3,
        editor=editor2,
        is_lead_editor=True,
        start_date=date(2023, 2, 1),
        end_date=date(2023, 5, 10)
    )
    
    # Создание заказчиков
    print("Создание заказчиков...")
    customer1 = Customer.objects.create(
        name='ООО "Книжный мир"',
        contact_person='Иванов Иван Иванович',
        email='info@bookworld.ru',
        phone='+7-495-123-4567',
        address='г. Москва, ул. Тверская, д. 15',
        customer_type='organization'
    )
    
    customer2 = Customer.objects.create(
        name='Петров Петр Петрович',
        contact_person='Петров Петр Петрович',
        email='petrov@example.com',
        phone='+7-999-555-5555',
        address='г. Москва, ул. Ленина, д. 10',
        customer_type='individual'
    )
    
    # Создание заказов
    order1 = Order.objects.create(
        order_number='ORD-2023-001',
        order_date=date(2023, 2, 1),
        delivery_date=date(2023, 2, 15),
        total_amount=Decimal('4500.00'),
        status='delivered',
        customer=customer1
    )
    
    order2 = Order.objects.create(
        order_number='ORD-2023-002',
        order_date=date(2023, 3, 1),
        delivery_date=date(2023, 3, 15),
        total_amount=Decimal('1200.00'),
        status='delivered',
        customer=customer2
    )
    
    # Создание позиций заказов
    OrderItem.objects.create(
        order=order1,
        book=book1,
        quantity=10,
        unit_price=book1.price,
        total_price=book1.price * 10
    )
    
    OrderItem.objects.create(
        order=order2,
        book=book2,
        quantity=1,
        unit_price=book2.price,
        total_price=book2.price
    )
    
    # Создание финансовых записей
    FinancialRecord.objects.create(
        date=date(2023, 1, 15),
        record_type='income',
        amount=Decimal('4500.00'),
        description='Продажа книг по заказу ORD-2023-001',
        related_order=order1
    )
    
    FinancialRecord.objects.create(
        date=date(2023, 2, 1),
        record_type='royalty',
        amount=Decimal('75000.00'),
        description='Гонорар автору Пушкину за книгу "Евгений Онегин"',
        related_contract=contract1
    )
    
    FinancialRecord.objects.create(
        date=date(2023, 1, 31),
        record_type='salary',
        amount=Decimal('80000.00'),
        description='Зарплата менеджеру Петрову И.И.',
        related_contract=None
    )
    print("Тестовые данные успешно созданы!")
    print(f"Создано:")
    print(f"- Сотрудников: {Employee.objects.count()}")
    print(f"- Авторов: {Author.objects.count()}")
    print(f"- Книг: {Book.objects.count()}")
    print(f"- Контрактов: {Contract.objects.count()}")
    print(f"- Заказчиков: {Customer.objects.count()}")
    print(f"- Заказов: {Order.objects.count()}")
    print(f"- Финансовых записей: {FinancialRecord.objects.count()}")


if __name__ == '__main__':
    create_sample_data()
