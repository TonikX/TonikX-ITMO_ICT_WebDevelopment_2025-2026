from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Count, Q
from django.contrib.auth.models import User
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


# class OverdueLoansAPIView(APIView):
#     """2. Кто из читателей взял книгу более месяца тому назад?"""
#
#     def get(self, request):
#         month_ago = date.today() - timedelta(days=30)
#
#         overdue_loans = LoanRecord.objects.filter(
#             issued_at__lt=month_ago,
#             returned_at__isnull=True
#         )
#
#         readers = []
#         for loan in overdue_loans:
#             readers.append({
#                 'reader_id': loan.reader_id.reader_id,
#                 'reader_name': loan.reader_id.full_name,
#                 'book_title': loan.copy_book_id.book_id.title,
#                 'copy_book_id': loan.copy_book_id.copy_book_id,
#                 'issued_at': loan.issued_at,
#                 'days_overdue': (date.today() - loan.issued_at).days
#             })
#
#         return Response({'overdue_readers': readers})
class OverdueLoansAPIView(APIView):
    """2. Кто из читателей взял книгу более месяца тому назад?"""

    def get(self, request):
        today = date.today()

        overdue_loans = LoanRecord.objects.filter(
            returned_at__isnull=True,
            due_date__lt=today  # ПРОСРОЧКА: срок возврата меньше сегодняшней даты
        )

        readers = []
        for loan in overdue_loans:
            readers.append({
                'loan_id': loan.loan_id,
                'reader_id': loan.reader_id.reader_id,
                'reader_name': loan.reader_id.full_name,
                'reader_card': loan.reader_id.library_card_id,
                'book_title': loan.copy_book_id.book_id.title,
                'copy_book_id': loan.copy_book_id.copy_book_id,
                'issued_at': loan.issued_at,
                'due_date': loan.due_date,
                'days_overdue': (today - loan.due_date).days  # ДНИ ПРОСРОЧКИ ОТ ДАТЫ ВОЗВРАТА!
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


class AdminReaderListAPIView(generics.ListAPIView):
    """Список ВСЕХ читателей для администратора (включая неактивных)"""
    serializer_class = ReaderSerializer
    queryset = Reader.objects.all()  # БЕЗ фильтра!
    permission_classes = [IsAdminUser]  # Только для админов


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
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Дата год назад
        one_year_ago = date.today() - timedelta(days=365)

        # Ищем читателей, у которых last_registration_at ≤ one_year_ago
        inactive_readers = Reader.objects.filter(
            last_registration_at__lte=one_year_ago,  # ИЗМЕНИТЬ: __lt → __lte
            is_active_member=True
        )

        count = inactive_readers.count()
        names = [reader.full_name for reader in inactive_readers]

        # Обновляем статус
        inactive_readers.update(is_active_member=False)

        return Response({
            'message': f'Исключено {count} неактивных читателей',
            'removed_readers': names,
            'count': count
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


from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class LinkUserToReaderAPIView(APIView):
    """Связать текущего пользователя с читателем"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Проверяем, есть ли уже у пользователя профиль
        if hasattr(user, 'reader_profile'):
            return Response({
                'message': 'User already has a reader profile',
                'reader_id': user.reader_profile.reader_id
            })

        # Получаем данные из запроса
        card_number = request.data.get('card_number')
        passport = request.data.get('passport')

        if not card_number or not passport:
            return Response({'error': 'card_number and passport required'}, status=400)

        try:
            # Ищем читателя по номеру билета и паспорту
            reader = Reader.objects.get(
                library_card_id=card_number,
                passport=passport
            )

            # Если у читателя уже есть привязанный пользователь
            if reader.user:
                return Response({'error': 'Reader already linked to another user'}, status=400)

            # Связываем
            reader.user = user
            reader.save()

            return Response({
                'message': 'User successfully linked to reader',
                'reader': ReaderSerializer(reader).data
            })

        except Reader.DoesNotExist:
            return Response({'error': 'Reader not found'}, status=404)


class MyProfileAPIView(APIView):
    """Получить профиль текущего авторизованного читателя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'reader_profile'):
            return Response({'error': 'No reader profile linked'}, status=404)

        reader = user.reader_profile
        serializer = ReaderSerializer(reader)

        # Получаем активные выдачи
        active_loans = LoanRecord.objects.filter(
            reader_id=reader,
            returned_at__isnull=True
        )

        loans_data = []
        for loan in active_loans:
            loans_data.append({
                'loan_id': loan.loan_id,
                'book_title': loan.copy_book_id.book_id.title,
                'issued_at': loan.issued_at,
                'due_date': loan.due_date,
                'days_on_loan': (date.today() - loan.issued_at).days
            })

        return Response({
            'reader': serializer.data,
            'active_loans': loans_data
        })


class HallListAPIView(generics.ListAPIView):
    """Список читальных залов"""
    serializer_class = ReadingHallSerializer
    queryset = ReadingHall.objects.all()
    permission_classes = [IsAdminUser]


class AuthorListAPIView(generics.ListAPIView):
    """Список всех авторов"""
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]


class AuthorCreateAPIView(generics.CreateAPIView):
    """Создание нового автора"""
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]


class AuthorDetailAPIView(generics.RetrieveAPIView):
    """Получение одного автора"""
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class BookAuthorCreateAPIView(generics.CreateAPIView):
    """Создание связи книги и автора"""
    serializer_class = BookAuthorSerializer
    queryset = BookAuthor.objects.all()
    permission_classes = [IsAdminUser]


class CopyOfBookCreateAPIView(generics.CreateAPIView):
    """Создание нового экземпляра книги"""
    serializer_class = CopyOfBookSerializer
    queryset = CopyOfBook.objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(
            availability_status='available',
            received_date=date.today()
        )


class AuthorListAPIView(generics.ListAPIView):
    """Список всех авторов"""
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]


class AuthorCreateAPIView(generics.CreateAPIView):
    """Создание нового автора"""
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]

# ЛАБА 4 /books/with-copies/ Поиск книги с количеством доступных экземпляров
class BookWithCopiesAPIView(generics.ListAPIView):
    """Список книг с количеством доступных экземпляров"""
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Доступно всем

    def get_queryset(self):
        return Book.objects.filter(is_in_catalog=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []

        for book in queryset:
            # Считаем доступные экземпляры (не выданные и не списанные)
            available_copies = CopyOfBook.objects.filter(
                book_id=book,
                availability_status='available'
            ).count()

            book_data = BookSerializer(book).data
            book_data['available_copies'] = available_copies
            data.append(book_data)

        return Response(data)


class ActiveLoansAPIView(APIView):
    """Все активные выдачи (невозвращенные)"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        active_loans = LoanRecord.objects.filter(
            returned_at__isnull=True
        ).select_related('reader_id', 'copy_book_id__book_id')

        result = []
        for loan in active_loans:
            result.append({
                'loan_id': loan.loan_id,
                'reader_name': loan.reader_id.full_name,
                'reader_card': loan.reader_id.library_card_id,
                'book_title': loan.copy_book_id.book_id.title,
                'issued_at': loan.issued_at,
                'due_date': loan.due_date,
                'days_on_loan': (date.today() - loan.issued_at).days,
                'days_overdue': max(0, (date.today() - loan.due_date).days) if loan.due_date < date.today() else 0
            })

        return Response(result)


class LoanCreateAPIView(generics.CreateAPIView):
    """Создание новой выдачи книги"""
    serializer_class = LoanRecordSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        # При выдаче меняем статус экземпляра на 'on_loan'
        copy = serializer.validated_data['copy_book_id']
        copy.availability_status = 'on_loan'
        copy.save()
        serializer.save()


class LoanCreateAPIView(generics.CreateAPIView):
    """Создание новой выдачи книги"""
    serializer_class = LoanRecordSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        copy_id = request.data.get('copy_book_id')
        reader_id = request.data.get('reader_id')

        # Проверяем, доступен ли экземпляр
        try:
            book_copy = CopyOfBook.objects.get(pk=copy_id)
            if book_copy.availability_status != 'available':
                return Response(
                    {'error': 'Этот экземпляр уже выдан или недоступен'},
                    status=400
                )
        except CopyOfBook.DoesNotExist:
            return Response(
                {'error': 'Экземпляр не найден'},
                status=404
            )

        # Создаем выдачу
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Обновляем статус экземпляра
        book_copy.availability_status = 'on_loan'
        book_copy.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class ReturnBookAPIView(APIView):
    """Возврат книги читателем"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        loan_id = request.data.get('loan_id')

        if not loan_id:
            return Response({'error': 'loan_id is required'}, status=400)

        try:
            # Получаем запись о выдаче
            loan = LoanRecord.objects.get(pk=loan_id)

            # Проверяем, что книга действительно у этого читателя
            if not hasattr(request.user, 'reader_profile') or loan.reader_id != request.user.reader_profile:
                return Response({'error': 'Это не ваша книга'}, status=403)

            # Проверяем, что книга еще не возвращена
            if loan.returned_at is not None:
                return Response({'error': 'Книга уже возвращена'}, status=400)

            # Обновляем запись о выдаче
            loan.returned_at = date.today()
            loan.save()

            # Обновляем статус экземпляра книги
            book_copy = loan.copy_book_id
            book_copy.availability_status = 'available'
            book_copy.save()

            return Response({
                'success': True,
                'message': 'Книга успешно возвращена',
                'loan_id': loan.loan_id,
                'book_title': book_copy.book_id.title,
                'returned_at': loan.returned_at
            })

        except LoanRecord.DoesNotExist:
            return Response({'error': 'Запись о выдаче не найдена'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ReaderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Разрешаем читателю редактировать только себя
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        # Для PATCH проверяем, что это его профиль
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        reader = self.get_object()
        # Проверяем, что читатель редактирует свой профиль
        if not request.user.is_staff and reader.user != request.user:
            return Response({'error': 'Нет прав'}, status=403)
        return super().update(request, *args, **kwargs)