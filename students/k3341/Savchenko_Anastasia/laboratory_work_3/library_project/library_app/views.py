from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Book, Reader, CopyOfBook, LoanRecord, Author, BookAuthor, ReadingHall
from .serializers import *


# ============================================================================
# 1. APIView классы (как в практической 3.2)
# ============================================================================
#  **`GET /api/reader/<int:pk>/books/`** (http://127.0.0.1:8000/api/reader/20/books/)

class ReaderBooksAPIView(APIView):
    """1. Какие книги закреплены за заданным читателем?"""

    def get(self, request, pk):
        try:
            reader = Reader.objects.get(pk=pk)
            loans = LoanRecord.objects.filter(reader_id=reader, returned_at__isnull=True)

            books = []
            for loan in loans:
                book = loan.copy_book_id.book_id
                books.append({
                    'title': book.title,
                    'author': book.bookauthor_set.first().author_id.full_name if book.bookauthor_set.exists() else "Автор неизвестен",
                    'issued_at': loan.issued_at,
                    'due_date': loan.due_date
                })

            serializer = ReaderSerializer(reader)
            return Response({
                'reader': serializer.data,  # выведет все о пользователе
                'books': books
            })
        except Reader.DoesNotExist:
            return Response({'error': 'Reader not found'})


class OverdueLoansAPIView(APIView):
    """2. Кто из читателей взял книгу более месяца тому назад?"""

    def get(self, request):
        month_ago = date.today() - timedelta(days=30)

        overdue_loans = LoanRecord.objects.filter(
            issued_at__lt=month_ago,
            returned_at__isnull=True
        )

        readers = []
        for loan in overdue_loans:
            readers.append({
                'reader_id': loan.reader_id.reader_id,
                'reader_name': loan.reader_id.full_name,
                'book_title': loan.copy_book_id.book_id.title,
                'copy_book_id': loan.copy_book_id.copy_book_id,
                'issued_at': loan.issued_at,
                'days_overdue': (date.today() - loan.issued_at).days
            })

        return Response({'overdue_readers': readers})


class RareBooksReadersAPIView(APIView):
    """3. За кем из читателей закреплены редкие книги (≤2 экз.)?"""

    def get(self, request):
        # Аннотируем книги количеством доступных экземпляров
        rare_books = Book.objects.annotate(
            available_copies=Count('copyofbook', filter=Q(
                copyofbook__availability_status__in=['available', 'on_loan']
            ))
        ).filter(available_copies__lte=2)

        readers = []
        for book in rare_books:
            # Получаем активные выдачи для этой книги
            loans = LoanRecord.objects.filter(
                copy_book_id__book_id=book,
                returned_at__isnull=True
            ).select_related('reader_id')

            for loan in loans:
                readers.append({
                    'reader_id': loan.reader_id.reader_id,
                    'reader_name': loan.reader_id.full_name,
                    'book_id': book.book_id,
                    'book_title': book.title,
                    'copy_count': book.available_copies  # аннотированное поле
                })

        return Response({'readers_with_rare_books': readers})


class YoungReadersAPIView(APIView):
    """4. Сколько в библиотеке читателей младше 20 лет?"""

    def get(self, request):
        twenty_years_ago = date.today() - timedelta(days=20 * 365)

        young_readers = Reader.objects.filter(
            birth_date__gt=twenty_years_ago,
            is_active_member=True
        )

        serializer = ReaderSerializer(young_readers, many=True)
        return Response({
            'count': young_readers.count(),
            'readers': serializer.data  # для сокращения кода
        })


class EducationStatsAPIView(APIView):
    """5. Процент читателей по образованию"""

    # последовательно проходит все уровни образования Reader, подсчитывая колво читателей каждого уровня и вычисляя их процент от общего числа. Результат возвращается в виде списка с названием уровня образования, количеством читателей и рассчитанным процентом для каждого уровня.
    def get(self, request):
        total = Reader.objects.filter(is_active_member=True).count()

        if total == 0:
            return Response({'error': 'No active readers'})

        stats = []
        for level_code, level_name in Reader.EDUCATION_CHOICES:
            count = Reader.objects.filter(
                education_level=level_code,
                is_active_member=True
            ).count()

            percentage = (count / total) * 100 if total > 0 else 0

            stats.append({
                'education': level_name,
                'count': count,
                'percentage': round(percentage, 2)
            })

        return Response({
            'total_readers': total,
            'stats': stats
        })


# ============================================================================
# 2. Generic классы (как в практической 3.2)
# ============================================================================

class BookListAPIView(generics.ListAPIView):
    """Список книг"""
    serializer_class = BookSerializer
    queryset = Book.objects.filter(is_in_catalog=True)


class ReaderListAPIView(generics.ListAPIView):
    """Список читателей"""
    serializer_class = ReaderSerializer
    queryset = Reader.objects.filter(is_active_member=True)


class CopyOfBookListAPIView(generics.ListAPIView):
    """Список доступных экземпляров книг"""
    serializer_class = CopyOfBookSerializer
    queryset = CopyOfBook.objects.filter(availability_status='available')


# ============================================================================
# 3. CreateAPIView (создание объектов)
# ============================================================================

class RegisterReaderAPIView(generics.CreateAPIView):
    """6. Зарегистрировать нового читателя"""
    serializer_class = ReaderSerializer

    def perform_create(self, serializer):
        # Номер билета сгенерируется автоматически в методе save() модели
        serializer.save()


class AddBookAPIView(generics.CreateAPIView):
    """9. Добавить книгу в фонд"""
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(is_in_catalog=True)


# ============================================================================
# 4. Операции через APIView (POST методы)
# ============================================================================

class RemoveInactiveReadersAPIView(APIView):
    """7. Исключить неактивных читателей"""

    def post(self, request):
        one_year_ago = date.today() - timedelta(days=365)

        inactive_readers = Reader.objects.filter(
            last_registration_at__lt=one_year_ago,
            is_active_member=True
        )

        count = inactive_readers.count()
        names = [reader.full_name for reader in inactive_readers]

        # Обновляем статус
        inactive_readers.update(is_active_member=False)

        return Response({
            'message': f'Removed {count} inactive readers',
            'removed_readers': names
        })


class DecommissionBookAPIView(APIView):
    """8. Списать книгу"""

    def post(self, request):
        copy_id = request.data.get('copy_id')

        try:
            book_copy = CopyOfBook.objects.get(pk=copy_id)

            if book_copy.availability_status == 'on_loan':
                return Response({'error': 'Book is currently on loan'})

            book_copy.availability_status = 'decommissioned'
            book_copy.decommission_date = date.today()
            book_copy.save()

            return Response({
                'message': f'Book copy {copy_id} decommissioned',
                'book_title': book_copy.book_id.title
            })

        except CopyOfBook.DoesNotExist:
            return Response({'error': 'Book copy not found'})


# ============================================================================
# 5.  ЭНДПОИНТЫ
# ============================================================================
# Необходимо предусмотреть возможность выдачи отчета о работе библиотеки в течение месяца. Отчет должен включать в себя следующую информацию: количество книг и читателей на каждый день в каждом из залов и в библиотеке в целом, количество читателей, записавшихся в библиотеку в каждый зал и в библиотеку за отчетный месяц.
class MonthlyReportAPIView(APIView):
    """Отчет о работе библиотеки за месяц"""

    def get(self, request):
        # Параметры
        today = date.today()
        month = int(request.query_params.get('month', today.month))
        year = int(request.query_params.get('year', today.year))

        # Даты месяца
        start = date(year, month, 1)
        end = start + timedelta(days=32)
        end = date(end.year, end.month, 1) - timedelta(days=1)

        halls = ReadingHall.objects.all()
        result = {'daily': [], 'halls': [], 'total': {}}

        # По дням
        for day in range((end - start).days + 1):
            current = start + timedelta(days=day)
            day_data = {'date': str(current)}

            for hall in halls:
                # Книги
                books = CopyOfBook.objects.filter(
                    hall_id=hall,
                    received_date__lte=current
                ).exclude(
                    Q(decommission_date__lte=current) |
                    Q(availability_status='decommissioned')
                ).count()

                # Читатели
                readers = Reader.objects.filter(
                    hall_id=hall,
                    is_active_member=True,
                    first_registered_at__lte=current
                ).count()

                day_data[f'{hall.name}_books'] = books
                day_data[f'{hall.name}_readers'] = readers

            result['daily'].append(day_data)

        # По залам (новые читатели за месяц)
        for hall in halls:
            new = Reader.objects.filter(
                hall_id=hall,
                first_registered_at__range=[start, end]
            ).count()

            result['halls'].append({
                'name': hall.name,
                'new_readers': new
            })

        # Итоги
        last_day = result['daily'][-1]
        total_books = sum(v for k, v in last_day.items() if k.endswith('_books'))
        total_readers = sum(v for k, v in last_day.items() if k.endswith('_readers'))

        result['total'] = {
            'books': total_books,
            'readers': total_readers,
            'new_readers': sum(h['new_readers'] for h in result['halls'])
        }

        return Response(result)


class TransferCopyToHallAPIView(APIView):
    """Перемещение книги между залами"""

    def post(self, request):
        copy_id = request.data.get('copy_id')
        new_hall_id = request.data.get('hall_id')

        if not copy_id or not new_hall_id:
            return Response({'error': 'copy_id and hall_id are required'})

        try:
            book_copy = CopyOfBook.objects.get(pk=copy_id)
            new_hall = ReadingHall.objects.get(pk=new_hall_id)

            # Проверяем, не выдан ли экземпляр
            if book_copy.availability_status == 'on_loan':
                return Response({'error': 'Cannot transfer book that is on loan'})

            old_hall = book_copy.hall_id
            book_copy.hall_id = new_hall
            book_copy.save()

            return Response({
                'message': f'Book transferred from hall {old_hall.name} to hall {new_hall.name}',
                'book_title': book_copy.book_id.title,
                'old_hall': old_hall.name,
                'new_hall': new_hall.name
            })

        except CopyOfBook.DoesNotExist:
            return Response({'error': 'Book copy not found'})
        except ReadingHall.DoesNotExist:
            return Response({'error': 'Hall not found'})


class UpdateBookCodeAPIView(APIView):
    """Изменение шифра книги"""

    def post(self, request, pk):
        new_code = request.data.get('new_code')

        if not new_code:
            return Response({'error': 'new_code is required'})

        try:
            book = Book.objects.get(pk=pk)

            old_code = book.inventory_code
            book.inventory_code = new_code
            book.save()

            return Response({
                'message': f'Book code updated from {old_code} to {new_code}',
                'book_title': book.title,
                'old_code': old_code,
                'new_code': new_code
            })

        except Book.DoesNotExist:
            return Response({'error': 'Book not found'})
