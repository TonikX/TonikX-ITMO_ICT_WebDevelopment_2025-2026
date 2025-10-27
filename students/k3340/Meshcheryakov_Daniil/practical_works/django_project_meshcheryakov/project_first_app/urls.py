from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("reader/<int:reader_id>/", views.reader_detail, name="reader_detail"),
    path("my-borrowings/", views.my_borrowings, name="my_borrowings"),
    path("borrow/<int:book_id>/", views.borrow_book, name="borrow_book"),
    path("borrowing/delete/<int:borrowing_id>/", views.delete_borrowing, name="delete_borrowing"),
    path("active-readers/", views.active_readers, name="active_readers"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
