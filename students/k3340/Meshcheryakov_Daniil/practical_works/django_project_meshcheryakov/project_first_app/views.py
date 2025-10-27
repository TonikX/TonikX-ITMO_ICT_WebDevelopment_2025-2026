from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Book, Reader, Borrowing, Review
from .forms import ReviewForm, BorrowingForm, RegisterForm

def book_list(request):
    query = request.GET.get("q", "")
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    paginator = Paginator(books, 5)  # 5 книг на странице
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "books/book_list.html", {"page_obj": page_obj, "query": query})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')
    
    # Проверяем, может ли пользователь оставить отзыв
    can_review = False
    if request.user.is_authenticated and hasattr(request.user, 'reader'):
        can_review = not reviews.filter(reader=request.user.reader).exists()
    
    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.reader = request.user.reader
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()
    
    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': form,
        'can_review': can_review
    })

def reader_detail(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    borrowings = Borrowing.objects.filter(reader=reader).order_by('-date_from')
    return render(request, 'reader_detail.html', {
        'reader': reader, 
        'borrowings': borrowings
    })

@login_required
def my_borrowings(request):
    if not hasattr(request.user, 'reader'):
        messages.error(request, 'У вас нет профиля читателя')
        return redirect('book_list')
    
    # Показываем ВСЕ бронирования (активные и прошлые)
    # Сначала активные (is_returned=False), потом прошлые, сортировка по дате
    borrowings = Borrowing.objects.filter(
        reader=request.user.reader
    ).order_by('is_returned', '-date_from')
    
    return render(request, 'borrowings/my_borrowings.html', {
        'borrowings': borrowings
    })

@login_required
def borrow_book(request, book_id):
    if not hasattr(request.user, 'reader'):
        messages.error(request, 'У вас нет профиля читателя')
        return redirect('book_list')
    
    book = get_object_or_404(Book, id=book_id)
    
    if not book.available:
        messages.error(request, 'Книга недоступна для бронирования')
        return redirect('book_detail', book_id=book.id)
    
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        if form.is_valid():
            borrowing = form.save(commit=False)
            borrowing.reader = request.user.reader
            borrowing.book = book
            borrowing.save()
            
            book.available = False
            book.save()
            
            messages.success(request, f'Книга "{book.title}" успешно забронирована!')
            return redirect('my_borrowings')
    else:
        form = BorrowingForm()
    
    return render(request, 'borrowings/borrow_book.html', {
        'form': form, 
        'book': book
    })

@login_required
def delete_borrowing(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)
    
    if not hasattr(request.user, 'reader') or borrowing.reader != request.user.reader:
        messages.error(request, 'У вас нет прав на удаление этого бронирования')
        return redirect('my_borrowings')
    
    if borrowing.is_returned:
        messages.error(request, 'Нельзя удалить уже возвращенную книгу')
        return redirect('my_borrowings')
    
    book = borrowing.book
    book.available = True
    book.save()
    
    borrowing.delete()
    messages.success(request, 'Бронирование удалено')
    return redirect('my_borrowings')

def active_readers(request):
    # Читатели, которые брали книги за последний месяц
    one_month_ago = timezone.now() - timedelta(days=30)
    recent_borrowings = Borrowing.objects.filter(
        date_from__gte=one_month_ago
    ).select_related('reader', 'book').order_by('-date_from')
    
    return render(request, 'active_readers.html', {
        'borrowings': recent_borrowings
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('book_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('book_list')
