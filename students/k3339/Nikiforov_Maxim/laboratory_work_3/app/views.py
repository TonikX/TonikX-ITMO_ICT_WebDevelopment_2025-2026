from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, F, Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from .models import ReadingRoom, Reader, Book, BookCopy, BookAssignment
from .serializers import (
    ReadingRoomSerializer, ReaderSerializer, BookSerializer,
    BookCopySerializer, BookAssignmentSerializer
)


class ReadingRoomViewSet(viewsets.ModelViewSet):
    """ViewSet для читальных залов"""
    queryset = ReadingRoom.objects.all()
    serializer_class = ReadingRoomSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['number', 'name']
    ordering_fields = ['number', 'name', 'capacity']


class ReaderViewSet(viewsets.ModelViewSet):
    """ViewSet для читателей"""
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['ticket_number', 'full_name', 'passport_number', 'phone_number']
    ordering_fields = ['ticket_number', 'full_name', 'registration_date']
    
    def get_queryset(self):
        queryset = Reader.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Получить список книг, закрепленных за читателем"""
        reader = self.get_object()
        assignments = reader.book_assignments.filter(is_returned=False)
        serializer = BookAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def old_assignments(self, request):
        """Читатели, взявшие книгу более месяца назад"""
        month_ago = timezone.now().date() - timedelta(days=30)
        assignments = BookAssignment.objects.filter(
            assignment_date__lt=month_ago,
            is_returned=False
        ).select_related('reader')
        readers = {assignment.reader for assignment in assignments}
        serializer = ReaderSerializer(readers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def with_rare_books(self, request):
        """Читатели с книгами, количество экземпляров которых <= 2"""
        # Находим книги с общим количеством <= 2
        books_with_few_copies = Book.objects.annotate(
            total_copies=Sum('copies__quantity')
        ).filter(total_copies__lte=2)
        
        # Находим читателей с такими книгами
        assignments = BookAssignment.objects.filter(
            book__in=books_with_few_copies,
            is_returned=False
        ).select_related('reader')
        readers = {assignment.reader for assignment in assignments}
        serializer = ReaderSerializer(readers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def young_readers(self, request):
        """Количество читателей младше 20 лет"""
        today = timezone.now().date()
        twenty_years_ago = today - timedelta(days=20*365)
        count = Reader.objects.filter(
            birth_date__gt=twenty_years_ago,
            is_active=True
        ).count()
        return Response({'count': count})
    
    @action(detail=False, methods=['get'])
    def education_stats(self, request):
        """Статистика по образованию читателей в процентах"""
        total = Reader.objects.filter(is_active=True).count()
        if total == 0:
            return Response({
                'primary': 0,
                'secondary': 0,
                'higher': 0,
                'degree': 0
            })
        
        stats = Reader.objects.filter(is_active=True).values('education', 'has_degree').annotate(
            count=Count('id')
        )
        
        result = {
            'primary': 0,
            'secondary': 0,
            'higher': 0,
            'degree': 0
        }
        
        for stat in stats:
            if stat['has_degree']:
                result['degree'] += stat['count']
            else:
                education = stat['education']
                if education in result:
                    result[education] += stat['count']
        
        # Конвертируем в проценты
        for key in result:
            result[key] = round((result[key] / total) * 100, 2)
        
        return Response(result)


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet для книг"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'authors', 'code', 'section']
    ordering_fields = ['title', 'code', 'publication_year']
    
    def get_queryset(self):
        queryset = Book.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset


class BookCopyViewSet(viewsets.ModelViewSet):
    """ViewSet для экземпляров книг в залах"""
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['book__title', 'reading_room__name']
    ordering_fields = ['book__title', 'reading_room__number', 'quantity']


class BookAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet для закреплений книг"""
    queryset = BookAssignment.objects.all()
    serializer_class = BookAssignmentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['book__title', 'reader__full_name', 'reader__ticket_number']
    ordering_fields = ['assignment_date', 'return_date']
    
    def get_queryset(self):
        queryset = BookAssignment.objects.all()
        is_returned = self.request.query_params.get('is_returned', None)
        if is_returned is not None:
            queryset = queryset.filter(is_returned=is_returned.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Вернуть книгу"""
        assignment = self.get_object()
        if assignment.is_returned:
            return Response(
                {'error': 'Книга уже возвращена'},
                status=status.HTTP_400_BAD_REQUEST
            )
        assignment.is_returned = True
        assignment.return_date = timezone.now().date()
        assignment.save()
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)


# Специальные views для операций библиотекаря
class LibrarianOperationsViewSet(viewsets.ViewSet):
    """ViewSet для операций библиотекаря"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def register_reader(self, request):
        """Записать нового читателя в библиотеку"""
        serializer = ReaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def unregister_old_readers(self, request):
        """Исключить читателей, записавшихся более года назад и не прошедших перерегистрацию"""
        year_ago = timezone.now().date() - timedelta(days=365)
        old_readers = Reader.objects.filter(
            registration_date__lt=year_ago,
            is_active=True,
            unregistration_date__isnull=True
        )
        count = old_readers.count()
        old_readers.update(
            is_active=False,
            unregistration_date=timezone.now().date()
        )
        return Response({
            'message': f'Исключено {count} читателей',
            'count': count
        })
    
    @action(detail=False, methods=['post'])
    def write_off_book(self, request):
        """Списать книгу"""
        book_id = request.data.get('book_id')
        if not book_id:
            return Response(
                {'error': 'Не указан ID книги'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            book = Book.objects.get(id=book_id)
            book.is_active = False
            book.save()
            # Удаляем все экземпляры книги
            BookCopy.objects.filter(book=book).delete()
            return Response({
                'message': f'Книга "{book.title}" списана',
                'book': BookSerializer(book).data
            })
        except Book.DoesNotExist:
            return Response(
                {'error': 'Книга не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def accept_book(self, request):
        """Принять книгу в фонд библиотеки"""
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            # Если указан зал и количество, создаем экземпляры
            reading_room_id = request.data.get('reading_room_id')
            quantity = request.data.get('quantity', 0)
            if reading_room_id and quantity:
                try:
                    reading_room = ReadingRoom.objects.get(id=reading_room_id)
                    BookCopy.objects.update_or_create(
                        book=book,
                        reading_room=reading_room,
                        defaults={'quantity': quantity}
                    )
                except ReadingRoom.DoesNotExist:
                    pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """Отчет о работе библиотеки за месяц"""
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)
        
        if not month or not year:
            # Используем текущий месяц
            now = timezone.now()
            month = now.month
            year = now.year
        
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {'error': 'Неверный формат месяца или года'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from datetime import date
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        # Статистика по дням
        daily_stats = []
        current_date = start_date
        
        while current_date < end_date:
            # Количество книг на этот день
            books_count = Book.objects.filter(
                created_at__date__lte=current_date,
                is_active=True
            ).count()
            
            # Количество читателей на этот день
            readers_count = Reader.objects.filter(
                registration_date__lte=current_date,
                is_active=True
            ).count()
            
            # Количество читателей, записавшихся в этот день
            new_readers_count = Reader.objects.filter(
                registration_date=current_date,
                is_active=True
            ).count()
            
            # Статистика по залам
            rooms_stats = []
            for room in ReadingRoom.objects.all():
                room_books = BookCopy.objects.filter(
                    reading_room=room,
                    created_at__date__lte=current_date
                ).aggregate(total=Sum('quantity'))['total'] or 0
                
                room_readers = Reader.objects.filter(
                    reading_room=room,
                    registration_date__lte=current_date,
                    is_active=True
                ).count()
                
                room_new_readers = Reader.objects.filter(
                    reading_room=room,
                    registration_date=current_date,
                    is_active=True
                ).count()
                
                rooms_stats.append({
                    'room_id': room.id,
                    'room_name': room.name,
                    'books_count': room_books,
                    'readers_count': room_readers,
                    'new_readers_count': room_new_readers
                })
            
            daily_stats.append({
                'date': current_date.isoformat(),
                'books_count': books_count,
                'readers_count': readers_count,
                'new_readers_count': new_readers_count,
                'rooms': rooms_stats
            })
            
            current_date += timedelta(days=1)
        
        # Общая статистика за месяц
        total_new_readers = Reader.objects.filter(
            registration_date__gte=start_date,
            registration_date__lt=end_date,
            is_active=True
        ).count()
        
        return Response({
            'month': month,
            'year': year,
            'daily_stats': daily_stats,
            'total_new_readers': total_new_readers
        })


# View для главной страницы
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from .forms import ReadingRoomForm, ReaderForm, BookForm, BookCopyForm, BookAssignmentForm


def index_view(request):
    """Главная страница"""
    stats = {
        'total_books': Book.objects.filter(is_active=True).count(),
        'total_readers': Reader.objects.filter(is_active=True).count(),
        'total_rooms': ReadingRoom.objects.count(),
        'active_assignments': BookAssignment.objects.filter(is_returned=False).count(),
    }
    return render(request, 'index.html', {'stats': stats})


# ========== Читальные залы ==========
@login_required
def reading_rooms_list(request):
    """Список читальных залов"""
    rooms = ReadingRoom.objects.annotate(
        readers_count=Count('readers', filter=Q(readers__is_active=True)),
        books_count=Sum('book_copies__quantity')
    )
    return render(request, 'reading_rooms/list.html', {'rooms': rooms})


@login_required
def reading_room_create(request):
    """Создать читальный зал"""
    if request.method == 'POST':
        form = ReadingRoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Читальный зал успешно создан!')
            return redirect('reading_rooms_list')
    else:
        form = ReadingRoomForm()
    return render(request, 'reading_rooms/form.html', {'form': form, 'title': 'Создать читальный зал'})


@login_required
def reading_room_detail(request, pk):
    """Детали читального зала"""
    room = get_object_or_404(ReadingRoom, pk=pk)
    readers = room.readers.filter(is_active=True)
    book_copies = room.book_copies.all()
    return render(request, 'reading_rooms/detail.html', {
        'room': room,
        'readers': readers,
        'book_copies': book_copies
    })


@login_required
def reading_room_edit(request, pk):
    """Редактировать читальный зал"""
    room = get_object_or_404(ReadingRoom, pk=pk)
    if request.method == 'POST':
        form = ReadingRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Читальный зал успешно обновлен!')
            return redirect('reading_room_detail', pk=pk)
    else:
        form = ReadingRoomForm(instance=room)
    return render(request, 'reading_rooms/form.html', {'form': form, 'title': 'Редактировать читальный зал', 'room': room})


# ========== Читатели ==========
@login_required
def readers_list(request):
    """Список читателей"""
    readers = Reader.objects.all()
    search = request.GET.get('search', '')
    if search:
        readers = readers.filter(
            Q(full_name__icontains=search) |
            Q(ticket_number__icontains=search) |
            Q(passport_number__icontains=search)
        )
    return render(request, 'readers/list.html', {'readers': readers, 'search': search})


@login_required
def reader_create(request):
    """Создать читателя"""
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Читатель успешно зарегистрирован!')
            return redirect('readers_list')
    else:
        form = ReaderForm()
    return render(request, 'readers/form.html', {'form': form, 'title': 'Зарегистрировать читателя'})


@login_required
def reader_detail(request, pk):
    """Детали читателя"""
    reader = get_object_or_404(Reader, pk=pk)
    assignments = reader.book_assignments.filter(is_returned=False)
    return render(request, 'readers/detail.html', {
        'reader': reader,
        'assignments': assignments
    })


@login_required
def reader_edit(request, pk):
    """Редактировать читателя"""
    reader = get_object_or_404(Reader, pk=pk)
    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные читателя успешно обновлены!')
            return redirect('reader_detail', pk=pk)
    else:
        form = ReaderForm(instance=reader)
    return render(request, 'readers/form.html', {'form': form, 'title': 'Редактировать читателя', 'reader': reader})


# ========== Книги ==========
@login_required
def books_list(request):
    """Список книг"""
    books = Book.objects.filter(is_active=True)
    search = request.GET.get('search', '')
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(authors__icontains=search) |
            Q(code__icontains=search)
        )
    return render(request, 'books/list.html', {'books': books, 'search': search})


@login_required
def book_create(request):
    """Создать книгу"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Книга успешно добавлена!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'books/form.html', {'form': form, 'title': 'Добавить книгу'})


@login_required
def book_detail(request, pk):
    """Детали книги"""
    book = get_object_or_404(Book, pk=pk)
    copies = book.copies.all()
    assignments = book.assignments.filter(is_returned=False)
    return render(request, 'books/detail.html', {
        'book': book,
        'copies': copies,
        'assignments': assignments
    })


@login_required
def book_edit(request, pk):
    """Редактировать книгу"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно обновлена!')
            return redirect('book_detail', pk=pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/form.html', {'form': form, 'title': 'Редактировать книгу', 'book': book})


@login_required
def book_delete(request, pk):
    """Списать книгу"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.is_active = False
        book.save()
        messages.success(request, f'Книга "{book.title}" списана!')
        return redirect('books_list')
    return render(request, 'books/delete.html', {'book': book})


# ========== Экземпляры книг ==========
@login_required
def book_copy_create(request, book_id=None):
    """Добавить экземпляры книги в зал"""
    if request.method == 'POST':
        form = BookCopyForm(request.POST)
        if form.is_valid():
            book_copy, created = BookCopy.objects.get_or_create(
                book=form.cleaned_data['book'],
                reading_room=form.cleaned_data['reading_room'],
                defaults={'quantity': form.cleaned_data['quantity']}
            )
            if not created:
                book_copy.quantity += form.cleaned_data['quantity']
                book_copy.save()
            messages.success(request, 'Экземпляры книги успешно добавлены!')
            return redirect('book_detail', pk=form.cleaned_data['book'].pk)
    else:
        form = BookCopyForm()
        if book_id:
            try:
                book = Book.objects.get(pk=book_id)
                form.fields['book'].initial = book.pk
            except Book.DoesNotExist:
                pass
    return render(request, 'book_copies/form.html', {
        'form': form,
        'title': 'Добавить экземпляры книги',
        'book_id': book_id
    })


# ========== Закрепления ==========
@login_required
def assignments_list(request):
    """Список закреплений"""
    assignments = BookAssignment.objects.all().order_by('-assignment_date')
    is_returned = request.GET.get('is_returned', '')
    if is_returned == 'false':
        assignments = assignments.filter(is_returned=False)
    elif is_returned == 'true':
        assignments = assignments.filter(is_returned=True)
    return render(request, 'assignments/list.html', {'assignments': assignments, 'is_returned': is_returned})


@login_required
def assignment_create(request):
    """Создать закрепление"""
    if request.method == 'POST':
        form = BookAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, 'Книга успешно закреплена за читателем!')
            return redirect('assignments_list')
    else:
        form = BookAssignmentForm()
        reader_id = request.GET.get('reader')
        if reader_id:
            try:
                reader = Reader.objects.get(pk=reader_id)
                form.fields['reader'].initial = reader.pk
            except Reader.DoesNotExist:
                pass
    return render(request, 'assignments/form.html', {'form': form, 'title': 'Закрепить книгу за читателем'})


@login_required
def assignment_return(request, pk):
    """Вернуть книгу"""
    assignment = get_object_or_404(BookAssignment, pk=pk)
    if request.method == 'POST':
        assignment.is_returned = True
        assignment.return_date = timezone.now().date()
        assignment.save()
        messages.success(request, 'Книга успешно возвращена!')
        return redirect('assignments_list')
    return render(request, 'assignments/return.html', {'assignment': assignment})


# ========== Операции библиотекаря ==========
@login_required
def librarian_operations(request):
    """Страница операций библиотекаря"""
    return render(request, 'librarian/operations.html')


@login_required
def librarian_old_readers(request):
    """Исключить старых читателей"""
    if request.method == 'POST':
        year_ago = timezone.now().date() - timedelta(days=365)
        old_readers = Reader.objects.filter(
            registration_date__lt=year_ago,
            is_active=True,
            unregistration_date__isnull=True
        )
        count = old_readers.count()
        old_readers.update(
            is_active=False,
            unregistration_date=timezone.now().date()
        )
        messages.success(request, f'Исключено {count} читателей')
        return redirect('librarian_operations')
    return render(request, 'librarian/unregister_old.html')


@login_required
def librarian_monthly_report(request):
    """Месячный отчет"""
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        month = timezone.now().month
        year = timezone.now().year
    
    from datetime import date
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Статистика по дням
    daily_stats = []
    current_date = start_date
    
    while current_date < end_date:
        books_count = Book.objects.filter(
            created_at__date__lte=current_date,
            is_active=True
        ).count()
        
        readers_count = Reader.objects.filter(
            registration_date__lte=current_date,
            is_active=True
        ).count()
        
        new_readers_count = Reader.objects.filter(
            registration_date=current_date,
            is_active=True
        ).count()
        
        rooms_stats = []
        for room in ReadingRoom.objects.all():
            room_books = BookCopy.objects.filter(
                reading_room=room,
                created_at__date__lte=current_date
            ).aggregate(total=Sum('quantity'))['total'] or 0
            
            room_readers = Reader.objects.filter(
                reading_room=room,
                registration_date__lte=current_date,
                is_active=True
            ).count()
            
            room_new_readers = Reader.objects.filter(
                reading_room=room,
                registration_date=current_date,
                is_active=True
            ).count()
            
            rooms_stats.append({
                'room': room,
                'books_count': room_books,
                'readers_count': room_readers,
                'new_readers_count': room_new_readers
            })
        
        daily_stats.append({
            'date': current_date,
            'books_count': books_count,
            'readers_count': readers_count,
            'new_readers_count': new_readers_count,
            'rooms_stats': rooms_stats
        })
        
        current_date += timedelta(days=1)
    
    total_new_readers = Reader.objects.filter(
        registration_date__gte=start_date,
        registration_date__lt=end_date,
        is_active=True
    ).count()
    
    return render(request, 'librarian/monthly_report.html', {
        'month': month,
        'year': year,
        'daily_stats': daily_stats,
        'total_new_readers': total_new_readers
    })


# ========== Специальные запросы ==========
@login_required
def query_reader_books(request, reader_id):
    """Книги закрепленные за читателем"""
    reader = get_object_or_404(Reader, pk=reader_id)
    assignments = reader.book_assignments.filter(is_returned=False)
    return render(request, 'queries/reader_books.html', {
        'reader': reader,
        'assignments': assignments
    })


@login_required
def query_old_assignments(request):
    """Читатели с книгами старше месяца"""
    month_ago = timezone.now().date() - timedelta(days=30)
    assignments = BookAssignment.objects.filter(
        assignment_date__lt=month_ago,
        is_returned=False
    ).select_related('reader')
    readers = {assignment.reader for assignment in assignments}
    return render(request, 'queries/old_assignments.html', {'readers': readers})


@login_required
def query_rare_books(request):
    """Читатели с редкими книгами"""
    books_with_few_copies = Book.objects.annotate(
        total_copies=Sum('copies__quantity')
    ).filter(total_copies__lte=2)
    
    assignments = BookAssignment.objects.filter(
        book__in=books_with_few_copies,
        is_returned=False
    ).select_related('reader')
    readers = {assignment.reader for assignment in assignments}
    return render(request, 'queries/rare_books.html', {'readers': readers})


@login_required
def query_young_readers(request):
    """Читатели младше 20 лет"""
    today = timezone.now().date()
    twenty_years_ago = today - timedelta(days=20*365)
    readers = Reader.objects.filter(
        birth_date__gt=twenty_years_ago,
        is_active=True
    )
    count = readers.count()
    return render(request, 'queries/young_readers.html', {'readers': readers, 'count': count})


@login_required
def query_education_stats(request):
    """Статистика по образованию"""
    total = Reader.objects.filter(is_active=True).count()
    stats = {
        'primary': Reader.objects.filter(is_active=True, education='primary', has_degree=False).count(),
        'secondary': Reader.objects.filter(is_active=True, education='secondary', has_degree=False).count(),
        'higher': Reader.objects.filter(is_active=True, education='higher', has_degree=False).count(),
        'degree': Reader.objects.filter(is_active=True, has_degree=True).count(),
        'total': total
    }
    
    if total > 0:
        stats['primary_percent'] = round((stats['primary'] / total) * 100, 2)
        stats['secondary_percent'] = round((stats['secondary'] / total) * 100, 2)
        stats['higher_percent'] = round((stats['higher'] / total) * 100, 2)
        stats['degree_percent'] = round((stats['degree'] / total) * 100, 2)
    else:
        stats['primary_percent'] = stats['secondary_percent'] = stats['higher_percent'] = stats['degree_percent'] = 0
    
    return render(request, 'queries/education_stats.html', {'stats': stats})
