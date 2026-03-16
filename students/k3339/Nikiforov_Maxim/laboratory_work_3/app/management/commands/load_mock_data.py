"""
Команда для загрузки моковых данных: читальные залы, читатели, книги, экземпляры, закрепления.
Запуск: python manage.py load_mock_data
Опционально: python manage.py load_mock_data --clear — очистить и загрузить заново.
"""
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import ReadingRoom, Reader, Book, BookCopy, BookAssignment


class Command(BaseCommand):
    help = 'Загружает моковые данные (залы, читатели, книги, экземпляры, закрепления)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            BookAssignment.objects.all().delete()
            BookCopy.objects.all().delete()
            Book.objects.all().delete()
            Reader.objects.all().delete()
            ReadingRoom.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Данные очищены.'))

        self.stdout.write('Загрузка моковых данных...')

        # Читальные залы
        rooms_data = [
            {'number': '101', 'name': 'Зал художественной литературы', 'capacity': 50},
            {'number': '102', 'name': 'Зал технической литературы', 'capacity': 40},
            {'number': '201', 'name': 'Зал периодики', 'capacity': 30},
        ]
        rooms = []
        for r in rooms_data:
            room, _ = ReadingRoom.objects.get_or_create(number=r['number'], defaults=r)
            rooms.append(room)
        self.stdout.write(f'  Залы: {len(rooms)}')

        # Книги
        books_data = [
            {'title': 'Война и мир', 'authors': 'Л. Н. Толстой', 'publisher': 'Эксмо', 'publication_year': 2020, 'section': 'Художественная литература', 'code': 'ХЛ-001'},
            {'title': 'Мастер и Маргарита', 'authors': 'М. А. Булгаков', 'publisher': 'АСТ', 'publication_year': 2019, 'section': 'Художественная литература', 'code': 'ХЛ-002'},
            {'title': 'Введение в алгоритмы', 'authors': 'Кормен, Лейзерсон, Ривест', 'publisher': 'Вильямс', 'publication_year': 2019, 'section': 'Информатика', 'code': 'ИНФ-001'},
            {'title': 'Чистый код', 'authors': 'Роберт Мартин', 'publisher': 'Питер', 'publication_year': 2018, 'section': 'Программирование', 'code': 'ПР-001'},
            {'title': 'Паттерны проектирования', 'authors': 'Банда четырёх', 'publisher': 'Диалектика', 'publication_year': 2021, 'section': 'Программирование', 'code': 'ПР-002'},
        ]
        books = []
        for b in books_data:
            book, _ = Book.objects.get_or_create(code=b['code'], defaults=b)
            books.append(book)
        self.stdout.write(f'  Книги: {len(books)}')

        # Экземпляры книг в залах (книга — зал — количество)
        today = timezone.now().date()
        copies_spec = [
            (0, 0, 5),   # Война и мир в зале 101 — 5
            (0, 1, 2),   # Война и мир в зале 102 — 2
            (1, 0, 3),   # Мастер и Маргарита в зале 101 — 3
            (2, 1, 4),   # Введение в алгоритмы в зале 102 — 4
            (2, 2, 2),   # Введение в алгоритмы в зале 201 — 2
            (3, 1, 6),   # Чистый код в зале 102 — 6
            (4, 1, 3),   # Паттерны в зале 102 — 3
        ]
        for book_idx, room_idx, qty in copies_spec:
            BookCopy.objects.update_or_create(
                book=books[book_idx],
                reading_room=rooms[room_idx],
                defaults={'quantity': qty}
            )
        self.stdout.write(f'  Экземпляры в залах: {len(copies_spec)} записей')

        # Читатели (привязка к залам, разные образования)
        readers_data = [
            {'ticket_number': 'Б-1001', 'full_name': 'Иванов Иван Иванович', 'passport_number': '4010 123456', 'birth_date': date(1995, 3, 15), 'address': 'ул. Пушкина, 10', 'phone_number': '+7 911 111-11-11', 'education': 'higher', 'has_degree': False, 'room_idx': 0},
            {'ticket_number': 'Б-1002', 'full_name': 'Петрова Мария Сергеевна', 'passport_number': '4010 234567', 'birth_date': date(1988, 7, 22), 'address': 'пр. Невский, 5', 'phone_number': '+7 911 222-22-22', 'education': 'degree', 'has_degree': True, 'room_idx': 0},
            {'ticket_number': 'Б-1003', 'full_name': 'Сидоров Алексей Петрович', 'passport_number': '4010 345678', 'birth_date': date(2000, 1, 8), 'address': 'ул. Ленина, 3', 'phone_number': '+7 911 333-33-33', 'education': 'secondary', 'has_degree': False, 'room_idx': 1},
            {'ticket_number': 'Б-1004', 'full_name': 'Козлова Анна Викторовна', 'passport_number': '4010 456789', 'birth_date': date(1992, 11, 30), 'address': 'ул. Мира, 7', 'phone_number': '+7 911 444-44-44', 'education': 'higher', 'has_degree': False, 'room_idx': 1},
            {'ticket_number': 'Б-1005', 'full_name': 'Новиков Дмитрий Олегович', 'passport_number': '4010 567890', 'birth_date': date(1985, 5, 12), 'address': 'пер. Университетский, 1', 'phone_number': '+7 911 555-55-55', 'education': 'higher', 'has_degree': True, 'room_idx': 2},
        ]
        readers = []
        for r in readers_data:
            room_idx = r.pop('room_idx')
            defaults = {**r, 'reading_room': rooms[room_idx]}
            reader, _ = Reader.objects.get_or_create(ticket_number=r['ticket_number'], defaults=defaults)
            readers.append(reader)
        self.stdout.write(f'  Читатели: {len(readers)}')

        # Закрепления книг за читателями (часть активных, часть возвращённых)
        assignments_spec = [
            (0, 0, True, today - timedelta(days=20), today - timedelta(days=35)),   # Иванов — Война и мир
            (1, 0, False, None, today - timedelta(days=7)),                            # Иванов — Мастер и Маргарита
            (2, 2, False, None, today - timedelta(days=3)),                            # Сидоров — Введение в алгоритмы
            (3, 3, True, today - timedelta(days=5), today - timedelta(days=14)),      # Козлова — Чистый код
            (4, 1, False, None, today - timedelta(days=1)),                            # Петрова — Паттерны
        ]
        for reader_idx, book_idx, is_returned, return_date, assignment_date in assignments_spec:
            book = books[book_idx]
            reader = readers[reader_idx]
            if not BookAssignment.objects.filter(book=book, reader=reader).exists():
                BookAssignment.objects.create(
                    book=book,
                    reader=reader,
                    assignment_date=assignment_date,
                    is_returned=is_returned,
                    return_date=return_date
                )
        self.stdout.write(f'  Закрепления: {len(assignments_spec)}')

        self.stdout.write(self.style.SUCCESS('Моковые данные загружены.'))
