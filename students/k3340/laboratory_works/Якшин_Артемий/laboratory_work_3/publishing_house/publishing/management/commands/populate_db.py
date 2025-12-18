from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random

from publishing.models import (
    Employee, Author, Book, Contract, BookAuthor, BookEditor,
    Customer, Order, OrderItem
)


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем заполнение базы данных...'))

        # Очищаем существующие данные
        self.stdout.write('Очистка существующих данных...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        BookEditor.objects.all().delete()
        BookAuthor.objects.all().delete()
        Contract.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Employee.objects.all().delete()

        # Создаем сотрудников
        self.stdout.write('Создание сотрудников...')
        employees = self.create_employees()
        self.stdout.write(self.style.SUCCESS(f'Создано {len(employees)} сотрудников'))

        # Создаем авторов
        self.stdout.write('Создание авторов...')
        authors = self.create_authors()
        self.stdout.write(self.style.SUCCESS(f'Создано {len(authors)} авторов'))

        # Создаем книги
        self.stdout.write('Создание книг...')
        books = self.create_books()
        self.stdout.write(self.style.SUCCESS(f'Создано {len(books)} книг'))

        # Создаем контракты
        self.stdout.write('Создание контрактов...')
        contracts = self.create_contracts(books, employees)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(contracts)} контрактов'))

        # Связываем книги с авторами
        self.stdout.write('Связывание книг с авторами...')
        book_authors = self.create_book_authors(books, authors)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(book_authors)} связей книга-автор'))

        # Связываем книги с редакторами
        self.stdout.write('Связывание книг с редакторами...')
        book_editors = self.create_book_editors(books, employees)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(book_editors)} связей книга-редактор'))

        # Создаем заказчиков
        self.stdout.write('Создание заказчиков...')
        customers = self.create_customers()
        self.stdout.write(self.style.SUCCESS(f'Создано {len(customers)} заказчиков'))

        # Создаем заказы
        self.stdout.write('Создание заказов...')
        orders = self.create_orders(customers, books)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(orders)} заказов'))

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))

    def create_employees(self):
        """Создает сотрудников (менеджеров и редакторов)"""
        employees = []

        # Менеджеры
        managers = [
            {'first_name': 'Иван', 'last_name': 'Петров', 'middle_name': 'Сергеевич', 'email': 'i.petrov@publishing.ru', 'position': 'Старший менеджер'},
            {'first_name': 'Мария', 'last_name': 'Иванова', 'middle_name': 'Дмитриевна', 'email': 'm.ivanova@publishing.ru', 'position': 'Менеджер по контрактам'},
            {'first_name': 'Алексей', 'last_name': 'Смирнов', 'middle_name': 'Николаевич', 'email': 'a.smirnov@publishing.ru', 'position': 'Менеджер проектов'},
        ]

        for data in managers:
            emp = Employee.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data['middle_name'],
                email=data['email'],
                role='MANAGER',
                position_title=data['position'],
                hire_date=datetime.now().date() - timedelta(days=random.randint(365, 1825)),
                phone=f'+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}'
            )
            employees.append(emp)

        # Редакторы
        editors = [
            {'first_name': 'Ольга', 'last_name': 'Васильева', 'middle_name': 'Петровна', 'email': 'o.vasilyeva@publishing.ru', 'position': 'Главный редактор'},
            {'first_name': 'Дмитрий', 'last_name': 'Козлов', 'middle_name': 'Александрович', 'email': 'd.kozlov@publishing.ru', 'position': 'Редактор художественной литературы'},
            {'first_name': 'Елена', 'last_name': 'Новикова', 'middle_name': 'Игоревна', 'email': 'e.novikova@publishing.ru', 'position': 'Редактор научной литературы'},
            {'first_name': 'Сергей', 'last_name': 'Морозов', 'middle_name': 'Владимирович', 'email': 's.morozov@publishing.ru', 'position': 'Технический редактор'},
        ]

        for data in editors:
            emp = Employee.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data['middle_name'],
                email=data['email'],
                role='EDITOR',
                position_title=data['position'],
                hire_date=datetime.now().date() - timedelta(days=random.randint(365, 1825)),
                phone=f'+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}'
            )
            employees.append(emp)

        return employees

    def create_authors(self):
        """Создает авторов книг"""
        authors_data = [
            {'first_name': 'Александр', 'last_name': 'Пушкин', 'middle_name': 'Сергеевич'},
            {'first_name': 'Лев', 'last_name': 'Толстой', 'middle_name': 'Николаевич'},
            {'first_name': 'Федор', 'last_name': 'Достоевский', 'middle_name': 'Михайлович'},
            {'first_name': 'Антон', 'last_name': 'Чехов', 'middle_name': 'Павлович'},
            {'first_name': 'Иван', 'last_name': 'Тургенев', 'middle_name': 'Сергеевич'},
            {'first_name': 'Николай', 'last_name': 'Гоголь', 'middle_name': 'Васильевич'},
            {'first_name': 'Михаил', 'last_name': 'Булгаков', 'middle_name': 'Афанасьевич'},
            {'first_name': 'Анна', 'last_name': 'Ахматова', 'middle_name': 'Андреевна'},
            {'first_name': 'Марина', 'last_name': 'Цветаева', 'middle_name': 'Ивановна'},
            {'first_name': 'Борис', 'last_name': 'Пастернак', 'middle_name': 'Леонидович'},
            {'first_name': 'Владимир', 'last_name': 'Набоков', 'middle_name': 'Владимирович'},
            {'first_name': 'Александр', 'last_name': 'Солженицын', 'middle_name': 'Исаевич'},
        ]

        authors = []
        for data in authors_data:
            author = Author.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data['middle_name'],
                email=f"{data['first_name'].lower()}.{data['last_name'].lower()}@authors.ru",
                bio=f"Выдающийся русский писатель {data['last_name']} {data['first_name']} {data['middle_name']}.",
                birth_date=datetime.now().date() - timedelta(days=random.randint(20000, 30000)),
                phone=f'+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}'
            )
            authors.append(author)

        return authors

    def create_books(self):
        """Создает книги"""
        books_data = [
            {'title': 'Евгений Онегин', 'genre': 'Поэзия', 'pages': 320, 'illustrations': True},
            {'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225, 'illustrations': False},
            {'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671, 'illustrations': False},
            {'title': 'Вишневый сад', 'genre': 'Пьеса', 'pages': 120, 'illustrations': True},
            {'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 384, 'illustrations': False},
            {'title': 'Мертвые души', 'genre': 'Поэма', 'pages': 352, 'illustrations': True},
            {'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480, 'illustrations': False},
            {'title': 'Анна Каренина', 'genre': 'Роман', 'pages': 864, 'illustrations': False},
            {'title': 'Идиот', 'genre': 'Роман', 'pages': 640, 'illustrations': False},
            {'title': 'Братья Карамазовы', 'genre': 'Роман', 'pages': 796, 'illustrations': False},
            {'title': 'Доктор Живаго', 'genre': 'Роман', 'pages': 592, 'illustrations': False},
            {'title': 'Лолита', 'genre': 'Роман', 'pages': 336, 'illustrations': False},
            {'title': 'Один день Ивана Денисовича', 'genre': 'Повесть', 'pages': 192, 'illustrations': False},
            {'title': 'Капитанская дочка', 'genre': 'Повесть', 'pages': 176, 'illustrations': True},
            {'title': 'Белая гвардия', 'genre': 'Роман', 'pages': 384, 'illustrations': False},
            {'title': 'Тихий Дон', 'genre': 'Роман', 'pages': 1400, 'illustrations': False},
        ]

        books = []
        for i, data in enumerate(books_data):
            # Генерируем ISBN-13 (ровно 13 цифр): 978 + 5 + 5 цифр + 3 цифры + 1 контрольная
            isbn = f'9785{random.randint(10000, 99999)}{random.randint(100, 999)}{random.randint(0, 9)}'

            book = Book.objects.create(
                title=data['title'],
                isbn=isbn,
                pages=data['pages'],
                has_illustrations=data['illustrations'],
                publication_date=datetime.now().date() - timedelta(days=random.randint(1, 730)),
                cover_price=Decimal(str(random.randint(300, 2000))),
                description=f"Описание книги '{data['title']}'. Жанр: {data['genre']}.",
                genre=data['genre'],
                language='RU'
            )
            books.append(book)

        return books

    def create_contracts(self, books, employees):
        """Создает контракты для книг"""
        contracts = []
        managers = [emp for emp in employees if emp.role == 'MANAGER']

        for i, book in enumerate(books):
            manager = random.choice(managers)
            contract = Contract.objects.create(
                contract_number=f'CONTRACT-2024-{str(i + 1).zfill(4)}',
                book=book,
                manager=manager,
                signed_date=datetime.now().date() - timedelta(days=random.randint(30, 365)),
                status=random.choice(['DRAFT', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'COMPLETED']),  # Больше активных
                advance_payment=Decimal(str(random.randint(50000, 200000))),
                total_budget=Decimal(str(random.randint(200000, 500000))),
                expiry_date=datetime.now().date() + timedelta(days=random.randint(180, 730)),
                notes=f'Контракт на издание книги "{book.title}"'
            )
            contracts.append(contract)

        return contracts

    def create_book_authors(self, books, authors):
        """Связывает книги с авторами"""
        book_authors = []

        for book in books:
            # Большинство книг с одним автором, некоторые с двумя
            num_authors = random.choice([1, 1, 1, 2])
            selected_authors = random.sample(authors, num_authors)

            for order, author in enumerate(selected_authors, 1):
                # Распределяем гонорар между авторами
                if num_authors == 1:
                    royalty = Decimal('100.00')
                else:
                    royalty = Decimal('50.00') if order == 1 else Decimal('50.00')

                ba = BookAuthor.objects.create(
                    book=book,
                    author=author,
                    author_order=order,
                    royalty_percentage=royalty
                )
                book_authors.append(ba)

        return book_authors

    def create_book_editors(self, books, employees):
        """Связывает книги с редакторами"""
        book_editors = []
        editors = [emp for emp in employees if emp.role == 'EDITOR']

        for book in books:
            # Каждая книга имеет 1-3 редактора
            num_editors = random.randint(1, min(3, len(editors)))
            selected_editors = random.sample(editors, num_editors)

            for i, editor in enumerate(selected_editors):
                # Первый редактор - ответственный
                is_chief = (i == 0)

                be = BookEditor.objects.create(
                    book=book,
                    editor=editor,
                    is_chief_editor=is_chief
                )
                book_editors.append(be)

        return book_editors

    def create_customers(self):
        """Создает заказчиков"""
        customers_data = [
            {'name': 'Василий Корнилов', 'company': 'Библиотека им. Ленина'},
            {'name': 'Татьяна Семенова', 'company': 'Книжный мир'},
            {'name': 'Игорь Волков', 'company': ''},
            {'name': 'Наталья Краснова', 'company': 'Читай-город'},
            {'name': 'Андрей Белов', 'company': 'Лабиринт'},
            {'name': 'Светлана Зайцева', 'company': ''},
            {'name': 'Павел Медведев', 'company': 'Буквоед'},
        ]

        customers = []
        for data in customers_data:
            customer = Customer.objects.create(
                name=data['name'],
                email=f"{data['name'].split()[0].lower()}@example.ru",
                phone=f'+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                address=f'г. Москва, ул. {random.choice(["Ленина", "Пушкина", "Гоголя"])}, д. {random.randint(1, 100)}',
                company_name=data['company']
            )
            customers.append(customer)

        return customers

    def create_orders(self, customers, books):
        """Создает заказы с позициями"""
        orders = []

        for i in range(10):
            customer = random.choice(customers)
            order = Order.objects.create(
                order_number=f'ORD-2024-{str(i + 1).zfill(5)}',
                customer=customer,
                status=random.choice(['PENDING', 'PROCESSING', 'COMPLETED', 'COMPLETED']),  # Больше завершенных
                total_amount=Decimal('0')  # Будет рассчитано ниже
            )

            # Добавляем 1-5 книг в заказ
            num_books = random.randint(1, 5)
            selected_books = random.sample(books, num_books)
            total = Decimal('0')

            for book in selected_books:
                quantity = random.randint(1, 10)
                unit_price = book.cover_price
                subtotal = unit_price * quantity

                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )

                total += subtotal

            order.total_amount = total
            order.save()
            orders.append(order)

        return orders
