# create_test_data_fixed.py
import os
import sys
import django
import random
from datetime import date, timedelta

# Настраиваем Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library_app.models import Author, Book, BookAuthor, ReadingHall, Reader, CopyOfBook, LoanRecord


def create_test_data():
    print("=" * 60)
    print("СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ДЛЯ БИБЛИОТЕКИ")
    print("=" * 60)

    # Очищаем старые данные
    print("\n🗑️  Очистка старых данных...")
    LoanRecord.objects.all().delete()
    CopyOfBook.objects.all().delete()
    BookAuthor.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    Reader.objects.all().delete()
    ReadingHall.objects.all().delete()

    # ============================================================================
    # 1. СОЗДАЕМ ЧИТАЛЬНЫЕ ЗАЛЫ
    # ============================================================================
    print("\n📚 Создание читальных залов...")

    halls = [
        ReadingHall(name="Главный зал", hall_number=1, capacity=50),
        ReadingHall(name="Научный зал", hall_number=2, capacity=30),
        ReadingHall(name="Детский зал", hall_number=3, capacity=40),
        ReadingHall(name="Художественный зал", hall_number=4, capacity=25),
    ]
    ReadingHall.objects.bulk_create(halls)
    hall1 = halls[0]
    hall2 = halls[1]
    hall3 = halls[2]
    hall4 = halls[3]
    print(f"✅ Создано залов: {len(halls)}")

    # ============================================================================
    # 2. СОЗДАЕМ АВТОРОВ
    # ============================================================================
    print("\n✍️  Создание авторов...")

    authors = [
        Author(full_name="Лев Толстой", birth_date=date(1828, 9, 9)),
        Author(full_name="Фёдор Достоевский", birth_date=date(1821, 11, 11)),
        Author(full_name="Антон Чехов", birth_date=date(1860, 1, 29)),
        Author(full_name="Александр Пушкин", birth_date=date(1799, 6, 6)),
        Author(full_name="Михаил Булгаков", birth_date=date(1891, 5, 15)),
        Author(full_name="Иван Тургенев", birth_date=date(1818, 11, 9)),
    ]
    Author.objects.bulk_create(authors)
    print(f"✅ Создано авторов: {len(authors)}")

    # ============================================================================
    # 3. СОЗДАЕМ КНИГИ
    # ============================================================================
    print("\n📖 Создание книг...")

    books = [
        Book(title="Война и мир", publisher="Русский вестник",
             publication_year=1869, section="Русская классика",
             inventory_code="RUS-001", is_in_catalog=True),
        Book(title="Преступление и наказание", publisher="Русский вестник",
             publication_year=1866, section="Русская классика",
             inventory_code="RUS-002", is_in_catalog=True),
        Book(title="Вишневый сад", publisher="Знание",
             publication_year=1904, section="Драматургия",
             inventory_code="RUS-003", is_in_catalog=True),
        Book(title="Евгений Онегин", publisher="Современник",
             publication_year=1833, section="Поэзия",
             inventory_code="RUS-004", is_in_catalog=True),
        Book(title="Анна Каренина", publisher="Русский вестник",
             publication_year=1878, section="Русская классика",
             inventory_code="RUS-005", is_in_catalog=True),
        Book(title="Мастер и Маргарита", publisher="Художественная литература",
             publication_year=1967, section="Русская классика",
             inventory_code="RUS-006", is_in_catalog=True),
        Book(title="Отцы и дети", publisher="Современник",
             publication_year=1862, section="Русская классика",
             inventory_code="RUS-007", is_in_catalog=True),
    ]
    Book.objects.bulk_create(books)
    book1 = books[0]
    book2 = books[1]
    book3 = books[2]
    book4 = books[3]
    book5 = books[4]
    book6 = books[5]
    book7 = books[6]
    print(f"✅ Создано книг: {len(books)}")

    # ============================================================================
    # 4. СОЗДАЕМ СВЯЗИ КНИГИ-АВТОРЫ
    # ============================================================================
    print("\n🔗 Связывание книг с авторами...")

    book_authors = [
        BookAuthor(book_id=book1, author_id=authors[0], author_order=1),
        BookAuthor(book_id=book2, author_id=authors[1], author_order=1),
        BookAuthor(book_id=book3, author_id=authors[2], author_order=1),
        BookAuthor(book_id=book4, author_id=authors[3], author_order=1),
        BookAuthor(book_id=book5, author_id=authors[0], author_order=1),
        BookAuthor(book_id=book6, author_id=authors[4], author_order=1),
        BookAuthor(book_id=book7, author_id=authors[5], author_order=1),
    ]
    BookAuthor.objects.bulk_create(book_authors)
    print(f"✅ Создано связей: {len(book_authors)}")

    # ============================================================================
    # 5. СОЗДАЕМ ЧИТАТЕЛЕЙ
    # ============================================================================
    print("\n👥 Создание читателей...")

    # Сохраняем каждого по отдельности для генерации номера билета
    reader1 = Reader(
        full_name="Иванов Иван Иванович",
        birth_date=date(2000, 5, 15),
        education_level="higher",
        passport="1234 567890",
        phone_number="+7 (123) 456-78-90",
        home_address="г. Москва, ул. Ленина, д. 1",
        hall_id=hall1,
        is_active_member=True,
        first_registered_at=date.today() - timedelta(days=730),
        last_registration_at=date.today() - timedelta(days=180),
    )
    reader1.save()

    reader2 = Reader(
        full_name="Петрова Анна Сергеевна",
        birth_date=date(1995, 8, 22),
        education_level="secondary",
        passport="2345 678901",
        phone_number="+7 (234) 567-89-01",
        home_address="г. Санкт-Петербург, ул. Пушкина, д. 10",
        hall_id=hall2,
        is_active_member=True,
        first_registered_at=date.today() - timedelta(days=550),
        last_registration_at=date.today() - timedelta(days=400),
    )
    reader2.save()

    reader3 = Reader(
        full_name="Сидоров Алексей Владимирович",
        birth_date=date(2010, 3, 8),  # Младше 20 лет
        education_level="primary",
        passport="3456 789012",
        phone_number="+7 (345) 678-90-12",
        home_address="г. Новосибирск, ул. Советская, д. 25",
        hall_id=hall3,
        is_active_member=True,
        first_registered_at=date.today() - timedelta(days=30),
        last_registration_at=date.today() - timedelta(days=30),
    )
    reader3.save()

    reader4 = Reader(
        full_name="Кузнецова Ольга Дмитриевна",
        birth_date=date(1988, 12, 5),
        education_level="degree",
        passport="4567 890123",
        phone_number="+7 (456) 789-01-23",
        home_address="г. Екатеринбург, ул. Мира, д. 15",
        hall_id=hall1,
        is_active_member=False,
        first_registered_at=date.today() - timedelta(days=800),
        last_registration_at=date.today() - timedelta(days=400),
    )
    reader4.save()

    reader5 = Reader(
        full_name="Савченко Анастасия Сергеевна",
        birth_date=date(2006, 1, 31),
        education_level="higher",
        passport="3333 506333",
        phone_number="79990333232",
        home_address="Санкт-Петербург, Варшавская улица, д. 125",
        hall_id=hall2,
        is_active_member=True,
        first_registered_at=date.today(),
        last_registration_at=date.today(),
    )
    reader5.save()

    reader6 = Reader(
        full_name="Смирнов Дмитрий Петрович",
        birth_date=date(1998, 7, 20),
        education_level="higher",
        passport="5678 901234",
        phone_number="+7 (567) 890-12-34",
        home_address="г. Казань, ул. Баумана, д. 5",
        hall_id=hall4,
        is_active_member=True,
        first_registered_at=date.today() - timedelta(days=100),
        last_registration_at=date.today() - timedelta(days=100),
    )
    reader6.save()

    print(f"✅ Создано читателей: 6")

    # ============================================================================
    # 6. СОЗДАЕМ ЭКЗЕМПЛЯРЫ КНИГ
    # ============================================================================
    print("\n📚 Создание экземпляров книг...")

    copies = []
    # Создаем разное количество экземпляров
    # book3 и book4 будут редкими (по 1 экземпляру)

    # book1 - 3 экземпляра
    for i in range(3):
        copies.append(CopyOfBook(
            book_id=book1,
            hall_id=hall1,
            availability_status='available',
            copy_condition='good',
            received_date=date.today() - timedelta(days=30)
        ))

    # book2 - 3 экземпляра
    for i in range(3):
        copies.append(CopyOfBook(
            book_id=book2,
            hall_id=hall2,
            availability_status='available',
            copy_condition='good',
            received_date=date.today() - timedelta(days=60)
        ))

    # book3 - 1 экземпляр (редкая книга)
    copies.append(CopyOfBook(
        book_id=book3,
        hall_id=hall3,
        availability_status='available',
        copy_condition='excellent',
        received_date=date.today() - timedelta(days=90)
    ))

    # book4 - 1 экземпляр (редкая книга)
    copies.append(CopyOfBook(
        book_id=book4,
        hall_id=hall4,
        availability_status='available',
        copy_condition='good',
        received_date=date.today() - timedelta(days=120)
    ))

    # book5 - 3 экземпляра
    for i in range(3):
        copies.append(CopyOfBook(
            book_id=book5,
            hall_id=hall1,
            availability_status='available',
            copy_condition='fair',
            received_date=date.today() - timedelta(days=150)
        ))

    # book6 - 2 экземпляра
    copies.append(CopyOfBook(
        book_id=book6,
        hall_id=hall2,
        availability_status='available',
        copy_condition='good',
        received_date=date.today() - timedelta(days=180)
    ))
    copies.append(CopyOfBook(
        book_id=book6,
        hall_id=hall3,
        availability_status='available',
        copy_condition='excellent',
        received_date=date.today() - timedelta(days=200)
    ))

    # book7 - 2 экземпляра
    copies.append(CopyOfBook(
        book_id=book7,
        hall_id=hall4,
        availability_status='available',
        copy_condition='good',
        received_date=date.today() - timedelta(days=210)
    ))
    copies.append(CopyOfBook(
        book_id=book7,
        hall_id=hall1,
        availability_status='available',
        copy_condition='fair',
        received_date=date.today() - timedelta(days=240)
    ))

    CopyOfBook.objects.bulk_create(copies)
    copy1 = copies[0]
    copy2 = copies[1]
    copy3 = copies[2]
    copy4 = copies[3]
    copy5 = copies[4]
    copy6 = copies[5]
    copy7 = copies[6]
    copy8 = copies[7]  # book3 (Вишневый сад) - редкая
    copy9 = copies[8]  # book4 (Евгений Онегин) - редкая
    print(f"✅ Создано экземпляров книг: {len(copies)}")

    # ============================================================================
    # 7. СОЗДАЕМ ЗАПИСИ О ВЫДАЧЕ
    # ============================================================================
    print("\n📅 Создание записей о выдаче книг...")

    loans = [
        # Просроченная выдача (>30 дней)
        LoanRecord(
            copy_book_id=copy1,
            reader_id=reader1,
            issued_at=date.today() - timedelta(days=40),
            due_date=date.today() - timedelta(days=10),
            returned_at=None  # Не возвращена
        ),
        LoanRecord(
            copy_book_id=copy2,
            reader_id=reader2,
            issued_at=date.today() - timedelta(days=35),
            due_date=date.today() - timedelta(days=5),
            returned_at=None  # Не возвращена
        ),
        # Активная выдача (не просрочена)
        LoanRecord(
            copy_book_id=copy3,
            reader_id=reader1,
            issued_at=date.today() - timedelta(days=20),
            due_date=date.today() + timedelta(days=10),
            returned_at=None
        ),
        # Возвращенная книга
        LoanRecord(
            copy_book_id=copy4,
            reader_id=reader3,
            issued_at=date.today() - timedelta(days=50),
            due_date=date.today() - timedelta(days=20),
            returned_at=date.today() - timedelta(days=25)
        ),
        # Читатель с редкой книгой (book3 - Вишневый сад)
        LoanRecord(
            copy_book_id=copy8,
            reader_id=reader5,
            issued_at=date.today() - timedelta(days=15),
            due_date=date.today() + timedelta(days=15),
            returned_at=None
        ),
        # Еще одна выдача редкой книги (book4 - Евгений Онегин)
        LoanRecord(
            copy_book_id=copy9,
            reader_id=reader6,
            issued_at=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=20),
            returned_at=None
        ),
    ]
    LoanRecord.objects.bulk_create(loans)
    print(f"✅ Создано выдач: {len(loans)}")

    # Обновляем статусы выданных книг
    for loan in loans:
        if loan.returned_at is None:
            loan.copy_book_id.availability_status = 'on_loan'
            loan.copy_book_id.save()

    # ============================================================================
    # 8. ВЫВОД СТАТИСТИКИ
    # ============================================================================
    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА СОЗДАННЫХ ДАННЫХ")
    print("=" * 60)

    print(f"📚 Авторов: {Author.objects.count()}")
    print(f"📖 Книг: {Book.objects.count()}")
    print(f"🏛️  Читальных залов: {ReadingHall.objects.count()}")
    print(f"👥 Читателей: {Reader.objects.count()}")
    print(f"   • Активных: {Reader.objects.filter(is_active_member=True).count()}")
    print(f"   • Неактивных: {Reader.objects.filter(is_active_member=False).count()}")

    twenty_years_ago = date.today() - timedelta(days=20 * 365)
    young_count = Reader.objects.filter(birth_date__gt=twenty_years_ago, is_active_member=True).count()
    print(f"   • Младше 20 лет: {young_count}")

    print(f"📚 Экземпляров книг: {CopyOfBook.objects.count()}")
    print(f"   • Доступных: {CopyOfBook.objects.filter(availability_status='available').count()}")
    print(f"   • Выданных: {CopyOfBook.objects.filter(availability_status='on_loan').count()}")

    print(f"📅 Выдач: {LoanRecord.objects.count()}")
    print(f"   • Активных: {LoanRecord.objects.filter(returned_at__isnull=True).count()}")

    month_ago = date.today() - timedelta(days=30)
    overdue_count = LoanRecord.objects.filter(returned_at__isnull=True, issued_at__lt=month_ago).count()
    print(f"   • Просроченных (>30 дней): {overdue_count}")

    print("\n🎯 ДЛЯ ТЕСТИРОВАНИЯ ЭНДПОЙНТОВ:")
    print("ID читателя Иванова И.И.:", reader1.reader_id)
    print("ID читателя Сидорова А.В. (младше 20 лет):", reader3.reader_id)
    print("ID читателя Савченко А.С. (с редкой книгой):", reader5.reader_id)
    print("ID редкой книги (Вишневый сад):", book3.book_id)

    print("\n✅ ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
    print("=" * 60)


if __name__ == "__main__":
    create_test_data()