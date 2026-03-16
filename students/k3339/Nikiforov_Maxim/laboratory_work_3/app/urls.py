from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReadingRoomViewSet, ReaderViewSet, BookViewSet,
    BookCopyViewSet, BookAssignmentViewSet, LibrarianOperationsViewSet,
    # Web views
    index_view, reading_rooms_list, reading_room_create, reading_room_detail, reading_room_edit,
    readers_list, reader_create, reader_detail, reader_edit,
    books_list, book_create, book_detail, book_edit, book_delete,
    book_copy_create, assignments_list, assignment_create, assignment_return,
    librarian_operations, librarian_old_readers, librarian_monthly_report,
    query_reader_books, query_old_assignments, query_rare_books, query_young_readers, query_education_stats
)
from .views_auth import login_view, register_view, logout_view

router = DefaultRouter()
router.register(r'reading-rooms', ReadingRoomViewSet, basename='readingroom')
router.register(r'readers', ReaderViewSet, basename='reader')
router.register(r'books', BookViewSet, basename='book')
router.register(r'book-copies', BookCopyViewSet, basename='bookcopy')
router.register(r'book-assignments', BookAssignmentViewSet, basename='bookassignment')
router.register(r'librarian-operations', LibrarianOperationsViewSet, basename='librarian')

urlpatterns = [
    # Главная страница
    path('', index_view, name='index'),
    
    # Аутентификация (веб-интерфейс)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web interface
    # Читальные залы
    path('reading-rooms/', reading_rooms_list, name='reading_rooms_list'),
    path('reading-rooms/create/', reading_room_create, name='reading_room_create'),
    path('reading-rooms/<int:pk>/', reading_room_detail, name='reading_room_detail'),
    path('reading-rooms/<int:pk>/edit/', reading_room_edit, name='reading_room_edit'),
    
    # Читатели
    path('readers/', readers_list, name='readers_list'),
    path('readers/create/', reader_create, name='reader_create'),
    path('readers/<int:pk>/', reader_detail, name='reader_detail'),
    path('readers/<int:pk>/edit/', reader_edit, name='reader_edit'),
    
    # Книги
    path('books/', books_list, name='books_list'),
    path('books/create/', book_create, name='book_create'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', book_delete, name='book_delete'),
    
    # Экземпляры книг
    path('book-copies/create/', book_copy_create, name='book_copy_create'),
    path('book-copies/create/<int:book_id>/', book_copy_create, name='book_copy_create'),
    
    # Закрепления
    path('assignments/', assignments_list, name='assignments_list'),
    path('assignments/create/', assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/return/', assignment_return, name='assignment_return'),
    
    # Операции библиотекаря
    path('librarian/', librarian_operations, name='librarian_operations'),
    path('librarian/unregister-old/', librarian_old_readers, name='librarian_old_readers'),
    path('librarian/monthly-report/', librarian_monthly_report, name='librarian_monthly_report'),
    
    # Специальные запросы
    path('queries/reader/<int:reader_id>/books/', query_reader_books, name='query_reader_books'),
    path('queries/old-assignments/', query_old_assignments, name='query_old_assignments'),
    path('queries/rare-books/', query_rare_books, name='query_rare_books'),
    path('queries/young-readers/', query_young_readers, name='query_young_readers'),
    path('queries/education-stats/', query_education_stats, name='query_education_stats'),
]
