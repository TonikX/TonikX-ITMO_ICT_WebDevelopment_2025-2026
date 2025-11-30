"""
Django management command для генерации тестовых данных в БД.
Использует русские имена, названия и реальные названия известных книг.
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
import random

from library.models import (
    Author, Publisher, BookSection, Book,
    Hall, Reader, BookCopy, BookIssue, HallBookStock, Staff
)


class Command(BaseCommand):
    help = 'Генерирует тестовые данные для библиотеки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--authors',
            type=int,
            default=30,
            help='Количество авторов для генерации (по умолчанию: 30)'
        )
        parser.add_argument(
            '--publishers',
            type=int,
            default=15,
            help='Количество издательств для генерации (по умолчанию: 15)'
        )
        parser.add_argument(
            '--sections',
            type=int,
            default=10,
            help='Количество разделов для генерации (по умолчанию: 10)'
        )
        parser.add_argument(
            '--books',
            type=int,
            default=100,
            help='Количество книг для генерации (по умолчанию: 100)'
        )
        parser.add_argument(
            '--halls',
            type=int,
            default=5,
            help='Количество залов для генерации (по умолчанию: 5)'
        )
        parser.add_argument(
            '--readers',
            type=int,
            default=200,
            help='Количество читателей для генерации (по умолчанию: 200)'
        )
        parser.add_argument(
            '--copies',
            type=int,
            default=300,
            help='Количество экземпляров книг для генерации (по умолчанию: 300)'
        )
        parser.add_argument(
            '--issues',
            type=int,
            default=150,
            help='Количество выдач книг для генерации (по умолчанию: 150)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начало генерации данных...'))

        # Генерируем данные в правильном порядке зависимостей
        authors = self.generate_authors(options['authors'])
        publishers = self.generate_publishers(options['publishers'])
        sections = self.generate_sections(options['sections'])
        books = self.generate_books(options['books'], authors, publishers, sections)
        halls = self.generate_halls(options['halls'])
        readers = self.generate_readers(options['readers'], halls)
        copies = self.generate_copies(options['copies'], books, halls)
        self.generate_issues(options['issues'], readers, copies, halls)
        self.generate_staff()

        self.stdout.write(self.style.SUCCESS(f'\nГенерация завершена успешно!'))
        self.stdout.write(f'Создано:')
        self.stdout.write(f'  - Авторов: {len(authors)}')
        self.stdout.write(f'  - Издательств: {len(publishers)}')
        self.stdout.write(f'  - Разделов: {len(sections)}')
        self.stdout.write(f'  - Книг: {len(books)}')
        self.stdout.write(f'  - Залов: {len(halls)}')
        self.stdout.write(f'  - Читателей: {len(readers)}')
        self.stdout.write(f'  - Экземпляров: {len(copies)}')
        self.stdout.write(f'  - Выдач: {options["issues"]}')

    def generate_authors(self, count):
        """Генерация авторов."""
        self.stdout.write('Генерация авторов...')
        
        authors_list = [
            'Лев Толстой', 'Фёдор Достоевский', 'Александр Пушкин',
            'Антон Чехов', 'Иван Тургенев', 'Николай Гоголь',
            'Михаил Лермонтов', 'Александр Грибоедов', 'Иван Бунин',
            'Максим Горький', 'Александр Блок', 'Сергей Есенин',
            'Владимир Маяковский', 'Марина Цветаева', 'Анна Ахматова',
            'Борис Пастернак', 'Михаил Булгаков', 'Александр Солженицын',
            'Владимир Набоков', 'Иосиф Бродский', 'Чингиз Айтматов',
            'Василий Шукшин', 'Валентин Распутин', 'Юрий Трифонов',
            'Виктор Астафьев', 'Василий Белов', 'Фазиль Искандер',
            'Даниил Гранин', 'Юрий Бондарев', 'Константин Симонов'
        ]
        
        authors = []
        for i in range(count):
            if i < len(authors_list):
                full_name = authors_list[i]
            else:
                # Генерируем случайные имена
                first_names = ['Иван', 'Пётр', 'Александр', 'Дмитрий', 'Сергей', 'Андрей', 'Михаил', 'Николай']
                last_names = ['Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Соколов', 'Лебедев']
                full_name = f'{random.choice(first_names)} {random.choice(last_names)}'
            
            author = Author.objects.create(full_name=full_name)
            authors.append(author)
        
        return authors

    def generate_publishers(self, count):
        """Генерация издательств."""
        self.stdout.write('Генерация издательств...')
        
        publishers_list = [
            'Эксмо', 'АСТ', 'Азбука', 'Молодая гвардия', 'Художественная литература',
            'Детская литература', 'Просвещение', 'Наука', 'Росмэн', 'Махаон',
            'Самокат', 'Альпина', 'Манн, Иванов и Фербер', 'Альпина Паблишер', 'Питер'
        ]
        
        publishers = []
        for i in range(count):
            if i < len(publishers_list):
                name = publishers_list[i]
            else:
                name = f'Издательство {i + 1}'
            
            publisher = Publisher.objects.create(name=name)
            publishers.append(publisher)
        
        return publishers

    def generate_sections(self, count):
        """Генерация разделов книг."""
        self.stdout.write('Генерация разделов...')
        
        sections_list = [
            'Художественная литература', 'Детская литература', 'Научная литература',
            'История', 'Философия', 'Психология', 'Экономика', 'Техника',
            'Медицина', 'Спорт и здоровье'
        ]
        
        sections = []
        for i in range(count):
            if i < len(sections_list):
                name = sections_list[i]
            else:
                name = f'Раздел {i + 1}'
            
            section = BookSection.objects.create(name=name)
            sections.append(section)
        
        return sections

    def generate_books(self, count, authors, publishers, sections):
        """Генерация книг."""
        self.stdout.write('Генерация книг...')
        
        books_list = [
            ('Война и мир', 1869, 'Лев Толстой'),
            ('Преступление и наказание', 1866, 'Фёдор Достоевский'),
            ('Евгений Онегин', 1833, 'Александр Пушкин'),
            ('Мёртвые души', 1842, 'Николай Гоголь'),
            ('Герой нашего времени', 1840, 'Михаил Лермонтов'),
            ('Отцы и дети', 1862, 'Иван Тургенев'),
            ('Вишнёвый сад', 1904, 'Антон Чехов'),
            ('Мастер и Маргарита', 1940, 'Михаил Булгаков'),
            ('Тихий Дон', 1940, 'Михаил Шолохов'),
            ('Доктор Живаго', 1957, 'Борис Пастернак'),
            ('Один день Ивана Денисовича', 1962, 'Александр Солженицын'),
            ('Лолита', 1955, 'Владимир Набоков'),
            ('Анна Каренина', 1877, 'Лев Толстой'),
            ('Братья Карамазовы', 1880, 'Фёдор Достоевский'),
            ('Идиот', 1869, 'Фёдор Достоевский'),
            ('Бесы', 1872, 'Фёдор Достоевский'),
            ('Капитанская дочка', 1836, 'Александр Пушкин'),
            ('Пиковая дама', 1834, 'Александр Пушкин'),
            ('Ревизор', 1836, 'Николай Гоголь'),
            ('Тарас Бульба', 1835, 'Николай Гоголь'),
            ('Собачье сердце', 1925, 'Михаил Булгаков'),
            ('Белая гвардия', 1924, 'Михаил Булгаков'),
            ('Гроза', 1859, 'Александр Островский'),
            ('Обломов', 1859, 'Иван Гончаров'),
            ('Что делать?', 1863, 'Николай Чернышевский'),
            ('Отцы и дети', 1862, 'Иван Тургенев'),
            ('Рудин', 1856, 'Иван Тургенев'),
            ('Дворянское гнездо', 1859, 'Иван Тургенев'),
            ('Три сестры', 1901, 'Антон Чехов'),
            ('Чайка', 1896, 'Антон Чехов'),
        ]
        
        books = []
        for i in range(count):
            if i < len(books_list):
                title, year, author_name = books_list[i]
                # Ищем автора по имени
                author = next((a for a in authors if author_name in a.full_name), None)
                if not author:
                    author = random.choice(authors)
            else:
                title = f'Книга {i + 1}'
                year = random.randint(1900, 2023)
                author = random.choice(authors)
            
            publisher = random.choice(publishers) if publishers else None
            section = random.choice(sections) if sections else None
            cipher = f'BOOK_{i + 1:04d}'
            
            book = Book.objects.create(
                title=title,
                publisher=publisher,
                publish_year=year,
                section=section,
                cipher=cipher
            )
            
            # Добавляем авторов через raw SQL (так как в таблице нет поля id)
            author_ids_to_add = [author.author_id]
            # Иногда добавляем второго автора
            if random.random() < 0.2 and len(authors) > 1:
                second_author = random.choice([a for a in authors if a != author])
                author_ids_to_add.append(second_author.author_id)
            
            for author_id in author_ids_to_add:
                try:
                    with connection.cursor() as cursor:
                        # Проверяем существование связи
                        cursor.execute(
                            "SELECT COUNT(*) FROM book_author WHERE book_id = %s AND author_id = %s",
                            [book.book_id, author_id]
                        )
                        exists = cursor.fetchone()[0] > 0
                        
                        if not exists:
                            cursor.execute(
                                "INSERT INTO book_author (book_id, author_id, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())",
                                [book.book_id, author_id]
                            )
                except Exception:
                    pass
            
            books.append(book)
        
        return books

    def generate_halls(self, count):
        """Генерация читальных залов."""
        self.stdout.write('Генерация залов...')
        
        halls_list = [
            ('Читальный зал №1', 50),
            ('Читальный зал №2', 75),
            ('Читальный зал №3', 100),
            ('Детский читальный зал', 30),
            ('Зал периодики', 40),
            ('Зал редких книг', 20),
            ('Электронный читальный зал', 60),
            ('Зал научной литературы', 80)
        ]
        
        halls = []
        for i in range(count):
            if i < len(halls_list):
                name, capacity = halls_list[i]
            else:
                name = f'Читальный зал №{i + 1}'
                capacity = random.randint(30, 100)
            
            hall = Hall.objects.create(
                hall_number=i + 1,
                name=name,
                capacity=capacity
            )
            halls.append(hall)
        
        return halls

    def generate_readers(self, count, halls):
        """Генерация читателей."""
        self.stdout.write('Генерация читателей...')
        
        first_names = [
            'Иван', 'Пётр', 'Александр', 'Дмитрий', 'Сергей', 'Андрей', 'Михаил', 'Николай',
            'Алексей', 'Владимир', 'Евгений', 'Максим', 'Антон', 'Павел', 'Роман',
            'Мария', 'Анна', 'Елена', 'Ольга', 'Татьяна', 'Наталья', 'Ирина', 'Светлана',
            'Екатерина', 'Юлия', 'Анастасия', 'Дарья', 'Виктория', 'Полина', 'София'
        ]
        
        last_names = [
            'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Соколов', 'Лебедев',
            'Козлов', 'Новиков', 'Морозов', 'Петров', 'Волков', 'Соловьёв', 'Васильев',
            'Зайцев', 'Павлов', 'Семёнов', 'Голубев', 'Виноградов', 'Богданов', 'Воробьёв',
            'Фёдоров', 'Михайлов', 'Белов', 'Тарасов', 'Белов', 'Комаров', 'Орлов', 'Макаров'
        ]
        
        middle_names = [
            'Иванович', 'Петрович', 'Александрович', 'Дмитриевич', 'Сергеевич', 'Андреевич',
            'Михайлович', 'Николаевич', 'Алексеевич', 'Владимирович', 'Евгеньевич',
            'Ивановна', 'Петровна', 'Александровна', 'Дмитриевна', 'Сергеевна', 'Андреевна',
            'Михайловна', 'Николаевна', 'Алексеевна', 'Владимировна', 'Евгеньевна'
        ]
        
        education_levels = ['начальное', 'среднее', 'высшее', None]
        
        readers = []
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            middle_name = random.choice(middle_names)
            full_name = f'{last_name} {first_name} {middle_name}'
            
            # Генерируем дату рождения (от 18 до 80 лет)
            birth_year = random.randint(1944, 2006)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = date(birth_year, birth_month, birth_day)
            
            # Генерируем дату регистрации (от 1 года назад до сегодня)
            registration_date = timezone.now().date() - timedelta(days=random.randint(0, 365))
            
            education_level = random.choice(education_levels)
            has_academic_degree = random.random() < 0.15  # 15% имеют учёную степень
            
            hall = random.choice(halls) if halls else None
            
            # Генерируем уникальные номера
            card_number = f'R{i + 1:05d}'
            passport_number = f'{random.randint(1000, 9999)}{random.randint(100000, 999999)}'
            
            address = f'г. Москва, ул. {random.choice(["Ленина", "Пушкина", "Гагарина", "Мира", "Советская"])}, д. {random.randint(1, 100)}'
            phone = f'+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}'
            
            reader = Reader.objects.create(
                card_number=card_number,
                full_name=full_name,
                passport_number=passport_number,
                birth_date=birth_date,
                address=address,
                phone=phone,
                education_level=education_level,
                has_academic_degree=has_academic_degree,
                hall=hall,
                registration_date=registration_date,
                is_active=random.random() > 0.1  # 90% активны
            )
            readers.append(reader)
        
        return readers

    def generate_copies(self, count, books, halls):
        """Генерация экземпляров книг."""
        self.stdout.write('Генерация экземпляров книг...')
        
        # Находим максимальный существующий инвентарный номер
        existing_copies = BookCopy.objects.all()
        start_num = 1
        if existing_copies.exists():
            max_num = 0
            for copy in existing_copies:
                # Извлекаем числовую часть из инвентарного номера
                digits = ''.join(filter(str.isdigit, copy.inventory_number))
                if digits:
                    try:
                        num = int(digits)
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        pass
            start_num = max_num + 1
        
        copies = []
        for i in range(count):
            book = random.choice(books)
            hall = random.choice(halls) if halls else None
            
            inventory_number = f'INV{start_num + i:06d}'
            
            # Некоторые книги списаны
            is_written_off = random.random() < 0.1  # 10% списаны
            writeoff_date = None
            if is_written_off:
                writeoff_date = timezone.now().date() - timedelta(days=random.randint(1, 365))
            
            registration_date = timezone.now().date() - timedelta(days=random.randint(0, 1000))
            
            copy = BookCopy.objects.create(
                book=book,
                hall=hall,
                inventory_number=inventory_number,
                registration_date=registration_date,
                writeoff_date=writeoff_date,
                is_written_off=is_written_off
            )
            copies.append(copy)
            
            # Обновляем или создаём запись на складе через raw SQL
            try:
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
            except Exception:
                pass
        
        return copies

    def generate_issues(self, count, readers, copies, halls):
        """Генерация выдач книг."""
        self.stdout.write('Генерация выдач книг...')
        
        # Фильтруем только активных читателей и не списанные книги
        active_readers = [r for r in readers if r.is_active]
        available_copies = [c for c in copies if not c.is_written_off]
        
        if not active_readers or not available_copies:
            self.stdout.write(self.style.WARNING('Нет активных читателей или доступных экземпляров для выдачи'))
            return
        
        issues = []
        for i in range(count):
            reader = random.choice(active_readers)
            copy = random.choice(available_copies)
            hall = copy.hall or random.choice(halls) if halls else None
            
            # Дата выдачи (от 1 года назад до сегодня)
            issue_date = timezone.now().date() - timedelta(days=random.randint(0, 365))
            
            # 70% книг возвращены
            return_date = None
            if random.random() < 0.7:
                return_date = issue_date + timedelta(days=random.randint(1, 90))
            
            issue = BookIssue.objects.create(
                reader=reader,
                copy=copy,
                hall=hall,
                issue_date=issue_date,
                return_date=return_date
            )
            issues.append(issue)
        
        return issues

    def generate_staff(self):
        """Генерация сотрудников библиотеки."""
        self.stdout.write('Генерация сотрудников...')
        
        staff_list = [
            ('admin', 'admin@library.ru', 'admin123'),
            ('librarian1', 'librarian1@library.ru', 'lib123'),
            ('librarian2', 'librarian2@library.ru', 'lib123'),
        ]
        
        for login, email, password in staff_list:
            if not Staff.objects.filter(login=login).exists():
                Staff.objects.create(
                    login=login,
                    email=email,
                    password_hash=make_password(password)
                )
